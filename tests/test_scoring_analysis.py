import math

import pytest

from rsav.analysis import (
    conservative_balanced_threshold,
    paired_outcome_metrics,
    paired_renderer_metrics,
    task_cluster_bootstrap,
)
from rsav.scoring import normalized_success_score, verifier_messages


def test_normalized_score():
    assert normalized_success_score(0.0, 0.0) == pytest.approx(0.5)
    assert normalized_success_score(math.log(3), 0.0) == pytest.approx(0.75)


def test_prompt_prohibits_style_shortcut():
    messages = verifier_messages("task", "trace")
    assert "style" in messages[0]["content"]
    assert "SUCCESS or FAILURE" in messages[0]["content"]


def test_conservative_threshold_prefers_higher_tie():
    threshold = conservative_balanced_threshold([0, 0, 1, 1], [0.1, 0.4, 0.6, 0.9])
    assert threshold == pytest.approx(0.6)


def test_paired_metrics():
    rows = [
        {"trajectory_id": "a", "renderer": "R0_native", "success_score": 0.6},
        {"trajectory_id": "a", "renderer": "R1_tagged", "success_score": 0.4},
        {"trajectory_id": "b", "renderer": "R0_native", "success_score": 0.2},
        {"trajectory_id": "b", "renderer": "R1_tagged", "success_score": 0.3},
    ]
    result = paired_renderer_metrics(rows, threshold=0.5)
    assert result["decision_flip_rate"] == pytest.approx(0.5)
    assert result["mean_abs_score_delta"] == pytest.approx(0.15)


def test_outcome_metrics_and_cluster_bootstrap():
    rows = []
    for task, reward, native, other in [
        ("t1", 0, 0.2, 0.8),
        ("t2", 1, 0.8, 0.4),
        ("t3", 0, 0.3, 0.4),
        ("t4", 1, 0.9, 0.7),
    ]:
        for renderer, score in [("R0_native", native), ("R1_tagged", other)]:
            rows.append({
                "trajectory_id": task,
                "task_name": task,
                "renderer": renderer,
                "reward": reward,
                "success_score": score,
            })
    point = paired_outcome_metrics(rows, 0.5)
    assert point["decision_flip_rate"] == pytest.approx(0.5)
    assert point["fpr_change"] == pytest.approx(0.5)
    assert point["fnr_change"] == pytest.approx(0.5)
    boot = task_cluster_bootstrap(rows, 0.5, replicates=100, seed=1)
    assert boot["decision_flip_rate"]["estimate"] == pytest.approx(0.5)
    assert boot["decision_flip_rate"]["valid_replicates"] > 0
