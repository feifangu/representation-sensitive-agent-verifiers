"""Versioned semantic trajectory object and canonical hashing."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping

SCHEMA_VERSION = "rsav-event-graph-v1"


def canonical_json(value: Any) -> str:
    """Return a deterministic, Unicode-preserving JSON encoding."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EventGraph:
    """Lossless experiment object.

    `trajectory` is the complete parsed source trajectory, not a selected projection.
    `task` contains verifier-visible task information. `provenance` is retained for
    auditing but renderers deliberately omit it so labels/source IDs cannot leak.
    """

    task: Mapping[str, Any]
    trajectory: Mapping[str, Any]
    provenance: Mapping[str, Any]
    schema_version: str = SCHEMA_VERSION

    def semantic_object(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "task": dict(self.task),
            "trajectory": dict(self.trajectory),
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.semantic_object())

    def to_record(self) -> dict[str, Any]:
        return {
            "semantic": self.semantic_object(),
            "provenance": dict(self.provenance),
            "semantic_digest": self.digest,
        }

    @classmethod
    def from_semantic_object(
        cls, semantic: Mapping[str, Any], provenance: Mapping[str, Any] | None = None
    ) -> "EventGraph":
        version = semantic.get("schema_version")
        if version != SCHEMA_VERSION:
            raise ValueError(f"unsupported schema version: {version!r}")
        task = semantic.get("task")
        trajectory = semantic.get("trajectory")
        if not isinstance(task, Mapping) or not isinstance(trajectory, Mapping):
            raise TypeError("semantic object requires mapping-valued task and trajectory")
        return cls(task=dict(task), trajectory=dict(trajectory), provenance=dict(provenance or {}))
