"""Adapters for public Terminal-Bench trajectory rows."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml

from .schema import EventGraph, canonical_digest


def _maybe_json(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if not stripped or stripped[0] not in "[{":
        return value
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return value


def _first(row: Mapping[str, Any], names: Iterable[str], default: Any = None) -> Any:
    for name in names:
        if name in row and row[name] is not None:
            return row[name]
    return default


def load_task_catalog(root: Path) -> dict[str, str]:
    """Load official task instructions from Terminal-Bench `task.yaml` files."""
    catalog: dict[str, str] = {}
    for path in root.rglob("task.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        instruction = data.get("instruction")
        if isinstance(instruction, str) and instruction.strip():
            catalog[path.parent.name] = instruction.strip()
    return catalog


def terminalbench_row_to_graph(
    row: Mapping[str, Any],
    row_index: int | None = None,
    task_catalog: Mapping[str, str] | None = None,
) -> EventGraph:
    """Convert a dataset row without dropping unknown trajectory fields.

    The adapter accepts both the public flat `steps` schema and nested
    `trajectory={steps: ...}` records used by verifier releases.
    """
    nested = _maybe_json(row.get("trajectory"))
    if isinstance(nested, Mapping):
        trajectory = dict(nested)
    else:
        steps = _maybe_json(row.get("steps", []))
        if not isinstance(steps, list) or not steps:
            raise TypeError("row must contain list-valued steps or a trajectory mapping")
        trajectory = {"steps": steps}

    task_name = _first(row, ("task_name", "task_id", "instance_id"), "")
    instruction = _first(row, ("instruction", "problem", "task", "prompt"), "")
    if not instruction and task_catalog is not None:
        instruction = task_catalog.get(str(task_name), "")
    if not instruction:
        # Last-resort recovery is explicit and conservative. Dataset `$<id>` references,
        # warmups, and harness greetings are not treated as task instructions.
        for step in trajectory.get("steps", []):
            if not isinstance(step, Mapping):
                continue
            source = step.get("source", step.get("src"))
            message = step.get("message", step.get("msg"))
            if source in {"user", "human"} and isinstance(message, str):
                candidate = message.strip()
                if candidate and candidate.lower() != "warmup" and not candidate.startswith("$"):
                    instruction = candidate
                    break
    if not instruction:
        raise ValueError(f"missing task instruction for {task_name!r}")
    task = {"task_name": task_name, "instruction": instruction}

    reward = _first(row, ("reward", "score", "success", "passed"))
    source_agent = _first(row, ("agent", "scaffold", "harness"), "unknown")
    source_model = _first(row, ("model", "model_name", "generator"), "unknown")
    source_id = f"{source_agent}::{source_model}"
    raw_digest = canonical_digest(dict(row))
    provenance = {
        "row_index": row_index,
        "source": source_id,
        "agent": source_agent,
        "model": source_model,
        "reward": reward,
        "trial_name": _first(row, ("trial_name", "run_id", "id"), ""),
        "raw_row_digest": raw_digest,
    }
    return EventGraph(task=task, trajectory=trajectory, provenance=provenance)


def binary_reward(graph: EventGraph) -> int:
    value = graph.provenance.get("reward")
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)) and value in (0, 1):
        return int(value)
    if isinstance(value, str) and value.strip().lower() in {
        "0", "1", "false", "true", "fail", "failed", "pass", "passed", "success"
    }:
        return int(value.strip().lower() in {"1", "true", "pass", "passed", "success"})
    raise ValueError(f"not a binary executable reward: {value!r}")
