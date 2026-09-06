import json

import pytest

from rsav.dataset import binary_reward, terminalbench_row_to_graph
from rsav.sampling import select_balanced, stable_id, task_disjoint_split


def make_row(source, model, reward, task, trial):
    return {
        "agent": source,
        "model": model,
        "reward": reward,
        "task_name": task,
        "trial_name": trial,
        "steps": json.dumps([{"source": "user", "message": task}, {"source": "agent", "message": trial}]),
        "unknown_top_level": {"kept_in_raw_hash": True},
    }


def test_row_adapter_parses_steps_and_label():
    graph = terminalbench_row_to_graph(make_row("a", "m", 1, "t", "r"), 7)
    assert binary_reward(graph) == 1
    assert graph.trajectory["steps"][0]["message"] == "t"
    assert graph.provenance["row_index"] == 7


def test_balanced_selection_and_task_disjoint_split():
    rows = []
    for source in ("a", "b", "c"):
        for reward in (0, 1):
            for i in range(3):
                rows.append(make_row(source, "m", reward, f"task-{i}", f"{source}-{reward}-{i}"))
    graphs = [terminalbench_row_to_graph(row, i) for i, row in enumerate(rows)]
    selected, _ = select_balanced(graphs, ["a::m", "b::m", "c::m"], per_source=4)
    assert len(selected) == 12
    assert len({stable_id(g) for g in selected}) == 12
    split = task_disjoint_split(selected)
    assert set(split.values()) == {"calibration", "evaluation"}


def test_selection_fails_instead_of_silently_unbalancing():
    graph = terminalbench_row_to_graph(make_row("a", "m", 1, "t", "r"))
    with pytest.raises(ValueError, match="insufficient support"):
        select_balanced([graph], ["a::m"], per_source=2)


def test_public_src_msg_schema_uses_catalog_instruction():
    row = {
        "agent": "a", "model": "m", "reward": 0, "task_name": "task-x",
        "steps": json.dumps([
            {"src": "user", "msg": "Warmup", "tools": None, "obs": None},
            {"src": "user", "msg": "$32", "tools": None, "obs": None},
            {"src": "agent", "msg": "working", "tools": [{"fn": "shell"}], "obs": "output"},
        ]),
    }
    graph = terminalbench_row_to_graph(row, task_catalog={"task-x": "Official instruction"})
    assert graph.task["instruction"] == "Official instruction"
    assert graph.trajectory["steps"][2]["tools"] == [{"fn": "shell"}]


def test_missing_steps_are_rejected():
    row = {"agent": "a", "model": "m", "reward": 0, "task_name": "t", "steps": None}
    with pytest.raises(TypeError, match="list-valued steps"):
        terminalbench_row_to_graph(row, task_catalog={"t": "instruction"})
