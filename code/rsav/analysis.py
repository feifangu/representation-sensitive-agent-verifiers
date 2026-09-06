"""Locked threshold and paired metric utilities."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Mapping

import numpy as np


def balanced_accuracy(labels: np.ndarray, decisions: np.ndarray) -> float:
    pos = labels == 1
    neg = labels == 0
    if not pos.any() or not neg.any():
        raise ValueError("balanced accuracy requires both labels")
    return float(((decisions[pos] == 1).mean() + (decisions[neg] == 0).mean()) / 2)


def conservative_balanced_threshold(labels: Iterable[int], scores: Iterable[float]) -> float:
    y = np.asarray(list(labels), dtype=int)
    s = np.asarray(list(scores), dtype=float)
    if y.shape != s.shape or y.size == 0 or not np.isfinite(s).all():
        raise ValueError("labels/scores must be same-sized, non-empty, and finite")
    candidates = np.unique(np.concatenate(([0.0], s, [1.0, np.nextafter(1.0, 2.0)])))
    values = [(balanced_accuracy(y, s >= threshold), float(threshold)) for threshold in candidates]
    best = max(value for value, _ in values)
    return max(threshold for value, threshold in values if value == best)


def paired_renderer_metrics(rows: Iterable[Mapping[str, object]], threshold: float) -> dict[str, float]:
    by_id: dict[str, dict[str, Mapping[str, object]]] = defaultdict(dict)
    for row in rows:
        by_id[str(row["trajectory_id"])][str(row["renderer"])] = row
    deltas: list[float] = []
    flips: list[bool] = []
    directional: list[float] = []
    for renderings in by_id.values():
        if "R0_native" not in renderings or len(renderings) != 2:
            raise ValueError("each metric pair requires R0_native and exactly one comparator")
        native = float(renderings["R0_native"]["success_score"])
        other = next(float(r["success_score"]) for k, r in renderings.items() if k != "R0_native")
        directional.append(other - native)
        deltas.append(abs(other - native))
        flips.append((native >= threshold) != (other >= threshold))
    if not deltas:
        raise ValueError("no valid pairs")
    return {
        "n_pairs": float(len(deltas)),
        "mean_abs_score_delta": float(np.mean(deltas)),
        "median_abs_score_delta": float(np.median(deltas)),
        "mean_directional_score_delta": float(np.mean(directional)),
        "decision_flip_rate": float(np.mean(flips)),
    }


def paired_outcome_metrics(rows: Iterable[Mapping[str, object]], threshold: float) -> dict[str, float]:
    """Compute locked paired metrics, including directional error-rate changes."""
    by_id: dict[str, dict[str, Mapping[str, object]]] = defaultdict(dict)
    for row in rows:
        by_id[str(row["trajectory_id"])][str(row["renderer"])] = row
    abs_delta = []
    direction = []
    flips = []
    fpr_delta = []
    fnr_delta = []
    for renderings in by_id.values():
        if "R0_native" not in renderings or len(renderings) != 2:
            raise ValueError("each pair requires R0_native and one comparator")
        native = renderings["R0_native"]
        other = next(row for name, row in renderings.items() if name != "R0_native")
        if int(native["reward"]) != int(other["reward"]):
            raise ValueError("paired rows disagree on outcome label")
        y = int(native["reward"])
        s0, s1 = float(native["success_score"]), float(other["success_score"])
        d0, d1 = int(s0 >= threshold), int(s1 >= threshold)
        abs_delta.append(abs(s1 - s0))
        direction.append(s1 - s0)
        flips.append(d0 != d1)
        if y == 0:
            fpr_delta.append(d1 - d0)
        else:
            fnr_delta.append((1 - d1) - (1 - d0))
    if not abs_delta or not fpr_delta or not fnr_delta:
        raise ValueError("paired outcome metrics require pairs and both outcome classes")
    return {
        "n_pairs": float(len(abs_delta)),
        "n_failures": float(len(fpr_delta)),
        "n_successes": float(len(fnr_delta)),
        "mean_abs_score_delta": float(np.mean(abs_delta)),
        "median_abs_score_delta": float(np.median(abs_delta)),
        "mean_directional_score_delta": float(np.mean(direction)),
        "decision_flip_rate": float(np.mean(flips)),
        "fpr_change": float(np.mean(fpr_delta)),
        "fnr_change": float(np.mean(fnr_delta)),
    }


def task_cluster_bootstrap(
    rows: list[Mapping[str, object]],
    threshold: float,
    replicates: int = 10_000,
    seed: int = 20260905,
) -> dict[str, dict[str, float]]:
    """Percentile intervals from resampling whole task clusters."""
    tasks = sorted({str(row["task_name"]) for row in rows})
    if len(tasks) < 2:
        raise ValueError("cluster bootstrap requires at least two tasks")
    grouped = {task: [row for row in rows if str(row["task_name"]) == task] for task in tasks}
    rng = np.random.default_rng(seed)
    draws: dict[str, list[float]] = defaultdict(list)
    for _ in range(replicates):
        sampled = rng.choice(tasks, size=len(tasks), replace=True)
        expanded = []
        for occurrence, task in enumerate(sampled):
            for row in grouped[str(task)]:
                copied = dict(row)
                copied["trajectory_id"] = f"{occurrence}:{copied['trajectory_id']}"
                expanded.append(copied)
        try:
            metrics = paired_outcome_metrics(expanded, threshold)
        except ValueError:
            continue
        for key, value in metrics.items():
            draws[key].append(value)
    point = paired_outcome_metrics(rows, threshold)
    output = {}
    for key, value in point.items():
        values = np.asarray(draws.get(key, []), dtype=float)
        output[key] = {
            "estimate": value,
            "lower_95": float(np.quantile(values, 0.025)) if values.size else float("nan"),
            "upper_95": float(np.quantile(values, 0.975)) if values.size else float("nan"),
            "valid_replicates": float(values.size),
        }
    return output
