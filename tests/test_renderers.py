import pytest

from rsav.renderers import TIER_A, tier_b_chatter_inserted, tier_b_reasoning_removed, validate_roundtrip
from rsav.schema import EventGraph


@pytest.fixture
def graph():
    return EventGraph(
        task={"task_name": "unicode-task", "instruction": "Write café output."},
        trajectory={
            "steps": [
                {"source": "user", "message": "Do it"},
                {
                    "source": "agent",
                    "step_id": 1,
                    "message": "I will run it.",
                    "tool_calls": [{"name": "terminal", "arguments": {"keystrokes": "printf 'café\\n'"}}],
                    "observation": {"results": [{"content": "café\n", "status": 0}]},
                    "unknown": {"nested": [1, True, None, "line\nline"]},
                },
                {"source": "agent", "step_id": 2, "message": "Completed."},
            ]
        },
        provenance={"reward": 1, "source": "fixture"},
    )


@pytest.mark.parametrize("renderer_name", list(TIER_A))
def test_tier_a_exact_roundtrip(graph, renderer_name):
    result = validate_roundtrip(graph, renderer_name)
    assert result["valid"]
    assert result["source_digest"] == result["recovered_digest"]


def test_reasoning_removal_preserves_actions_observations_and_final(graph):
    changed = tier_b_reasoning_removed(graph)
    before = graph.trajectory["steps"]
    after = changed.trajectory["steps"]
    assert after[1]["message"] == ""
    assert after[1]["tool_calls"] == before[1]["tool_calls"]
    assert after[1]["observation"] == before[1]["observation"]
    assert after[-1] == before[-1]
    assert changed.digest != graph.digest


def test_chatter_is_tier_b_and_does_not_mutate_source(graph):
    changed = tier_b_chatter_inserted(graph)
    assert len(changed.trajectory["steps"]) == len(graph.trajectory["steps"]) + 1
    assert len(graph.trajectory["steps"]) == 3
    assert changed.digest != graph.digest
