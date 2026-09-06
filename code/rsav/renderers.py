"""Tier-A bijective renderers and explicitly non-bijective Tier-B transforms."""

from __future__ import annotations

import copy
import json
import re
from typing import Any, Callable, Mapping

from .schema import EventGraph, canonical_json

Renderer = Callable[[EventGraph], str]
Parser = Callable[[str], EventGraph]


def _semantic(graph: EventGraph) -> dict[str, Any]:
    return graph.semantic_object()


def render_r0_native(graph: EventGraph) -> str:
    return "TASK_AND_TRAJECTORY\n" + json.dumps(_semantic(graph), ensure_ascii=False)


def parse_r0_native(text: str) -> EventGraph:
    prefix = "TASK_AND_TRAJECTORY\n"
    if not text.startswith(prefix):
        raise ValueError("invalid R0 prefix")
    return EventGraph.from_semantic_object(json.loads(text[len(prefix):]))


def render_r1_tagged(graph: EventGraph) -> str:
    semantic = _semantic(graph)
    return "\n".join([
        "<<<TASK>>>", canonical_json(semantic["task"]), "<<<END_TASK>>>",
        "<<<TRAJECTORY>>>", canonical_json(semantic["trajectory"]), "<<<END_TRAJECTORY>>>",
        f"<<<SCHEMA>>>{semantic['schema_version']}<<<END_SCHEMA>>>",
    ])


_R1 = re.compile(
    r"^<<<TASK>>>\n(?P<task>.*)\n<<<END_TASK>>>\n"
    r"<<<TRAJECTORY>>>\n(?P<traj>.*)\n<<<END_TRAJECTORY>>>\n"
    r"<<<SCHEMA>>>(?P<schema>.*)<<<END_SCHEMA>>>$",
    re.DOTALL,
)


def parse_r1_tagged(text: str) -> EventGraph:
    match = _R1.fullmatch(text)
    if not match:
        raise ValueError("invalid R1 tagged rendering")
    return EventGraph.from_semantic_object({
        "schema_version": match.group("schema"),
        "task": json.loads(match.group("task")),
        "trajectory": json.loads(match.group("traj")),
    })


def render_r2_compact_json(graph: EventGraph) -> str:
    return canonical_json(_semantic(graph))


def parse_r2_compact_json(text: str) -> EventGraph:
    return EventGraph.from_semantic_object(json.loads(text))


def _ordered_semantic(graph: EventGraph) -> dict[str, Any]:
    semantic = _semantic(graph)
    return {
        "trajectory": semantic["trajectory"],
        "schema_version": semantic["schema_version"],
        "task": semantic["task"],
    }


def render_r3_pretty_json(graph: EventGraph) -> str:
    return json.dumps(_ordered_semantic(graph), ensure_ascii=False, indent=2, sort_keys=False)


def parse_r3_pretty_json(text: str) -> EventGraph:
    return EventGraph.from_semantic_object(json.loads(text))


def render_r4_messages(graph: EventGraph) -> str:
    semantic = _semantic(graph)
    envelope = {
        "schema_version": semantic["schema_version"],
        "messages": [
            {"role": "user", "name": "task", "content": canonical_json(semantic["task"])},
            {"role": "assistant", "name": "trajectory", "content": canonical_json(semantic["trajectory"])},
        ],
    }
    return json.dumps(envelope, ensure_ascii=False, indent=2)


def parse_r4_messages(text: str) -> EventGraph:
    envelope = json.loads(text)
    messages = envelope.get("messages")
    if not isinstance(messages, list) or len(messages) != 2:
        raise ValueError("R4 requires exactly task and trajectory messages")
    by_name = {m.get("name"): m for m in messages if isinstance(m, Mapping)}
    if set(by_name) != {"task", "trajectory"}:
        raise ValueError("invalid R4 message names")
    return EventGraph.from_semantic_object({
        "schema_version": envelope.get("schema_version"),
        "task": json.loads(by_name["task"]["content"]),
        "trajectory": json.loads(by_name["trajectory"]["content"]),
    })


TIER_A: dict[str, tuple[Renderer, Parser]] = {
    "R0_native": (render_r0_native, parse_r0_native),
    "R1_tagged": (render_r1_tagged, parse_r1_tagged),
    "R2_compact_json": (render_r2_compact_json, parse_r2_compact_json),
    "R3_pretty_json": (render_r3_pretty_json, parse_r3_pretty_json),
    "R4_messages": (render_r4_messages, parse_r4_messages),
}


def validate_roundtrip(graph: EventGraph, renderer_name: str) -> dict[str, Any]:
    render, parse = TIER_A[renderer_name]
    text = render(graph)
    recovered = parse(text)
    return {
        "renderer": renderer_name,
        "source_digest": graph.digest,
        "recovered_digest": recovered.digest,
        "valid": recovered.semantic_object() == graph.semantic_object(),
        "utf8_bytes": len(text.encode("utf-8")),
        "characters": len(text),
    }


def tier_b_reasoning_removed(graph: EventGraph) -> EventGraph:
    """Remove agent prose only on steps that contain explicit tool calls.

    This is deliberately Tier B: even when actions/observations/final response are
    retained, agent prose can affect an outcome verifier's evidence interpretation.
    """
    trajectory = copy.deepcopy(dict(graph.trajectory))
    for step in trajectory.get("steps", []):
        if not isinstance(step, dict):
            continue
        source = step.get("source", step.get("src"))
        tools = step.get("tool_calls", step.get("tools"))
        if source in {"agent", "assistant"} and tools:
            for key in ("message", "msg", "reasoning", "thought", "analysis"):
                if key in step:
                    step[key] = ""
    return EventGraph(graph.task, trajectory, {**graph.provenance, "tier_b": "reasoning_removed"})


def tier_b_chatter_inserted(graph: EventGraph) -> EventGraph:
    """Insert a fixed, explicitly irrelevant prose event before the final step."""
    trajectory = copy.deepcopy(dict(graph.trajectory))
    steps = trajectory.get("steps")
    if not isinstance(steps, list):
        raise TypeError("trajectory steps must be a list for chatter insertion")
    chatter = {
        "src": "agent",
        "msg": "Status note: I will continue using the observed tool evidence.",
        "tools": None,
        "obs": None,
        "rsav_intervention": "fixed_irrelevant_chatter_v1",
    }
    insert_at = max(0, len(steps) - 1)
    steps.insert(insert_at, chatter)
    return EventGraph(graph.task, trajectory, {**graph.provenance, "tier_b": "chatter_inserted"})
