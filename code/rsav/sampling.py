"""Frozen, verifier-blind sampling for the 3-source/120-trajectory design."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import random
from typing import Iterable

from .dataset import binary_reward
from .schema import EventGraph


def stable_id(graph: EventGraph) -> str:
    source = str(graph.provenance.get("source", "unknown"))
    trial = str(graph.provenance.get("trial_name", ""))
    raw = str(graph.provenance.get("raw_row_digest", graph.digest))
    return hashlib.sha256(f"{source}\0{trial}\0{raw}".encode()).hexdigest()[:20]


def select_balanced(
    graphs: Iterable[EventGraph],
    sources: list[str],
    per_source: int = 40,
    seed: int = 20260905,
) -> tuple[list[EventGraph], list[dict[str, str]]]:
    """Select without verifier outputs; return selections and exclusion ledger."""
    if per_source % 2:
        raise ValueError("per_source must be even for a balanced target")
    wanted = set(sources)
    cells: dict[tuple[str, int], list[EventGraph]] = defaultdict(list)
    exclusions: list[dict[str, str]] = []
    seen: set[str] = set()
    for graph in graphs:
        sid = stable_id(graph)
        source = str(graph.provenance.get("source", "unknown"))
        if sid in seen:
            exclusions.append({"trajectory_id": sid, "reason": "duplicate"})
            continue
        seen.add(sid)
        if source not in wanted:
            exclusions.append({"trajectory_id": sid, "reason": "source_not_selected"})
            continue
        try:
            reward = binary_reward(graph)
        except ValueError:
            exclusions.append({"trajectory_id": sid, "reason": "invalid_binary_reward"})
            continue
        cells[(source, reward)].append(graph)

    rng = random.Random(seed)
    selected: list[EventGraph] = []
    target = per_source // 2
    for source in sources:
        for reward in (0, 1):
            candidates = sorted(cells[(source, reward)], key=stable_id)
            rng.shuffle(candidates)
            chosen = candidates[:target]
            if len(chosen) < target:
                raise ValueError(
                    f"insufficient support for source={source!r}, reward={reward}: "
                    f"need {target}, found {len(chosen)}"
                )
            selected.extend(chosen)
            exclusions.extend(
                {"trajectory_id": stable_id(g), "reason": "not_sampled"}
                for g in candidates[target:]
            )
    return sorted(selected, key=stable_id), exclusions


def task_disjoint_split(
    graphs: Iterable[EventGraph], calibration_fraction: float = 1 / 3, seed: int = 20260905
) -> dict[str, str]:
    tasks = sorted({str(g.task.get("task_name", "")) for g in graphs})
    if len(tasks) < 2:
        raise ValueError("need at least two distinct tasks for a disjoint split")
    rng = random.Random(seed)
    rng.shuffle(tasks)
    n_cal = max(1, min(len(tasks) - 1, round(len(tasks) * calibration_fraction)))
    calibration = set(tasks[:n_cal])
    return {task: ("calibration" if task in calibration else "evaluation") for task in tasks}
