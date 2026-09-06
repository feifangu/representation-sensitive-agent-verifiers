"""Apply the locked native-threshold and paired task-cluster analysis."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

from .analysis import conservative_balanced_threshold, task_cluster_bootstrap


def load_rows(paths: list[Path]) -> list[dict]:
    rows = []
    seen = set()
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            key = (row["model_id"], row["trajectory_id"], row["renderer"])
            if key in seen:
                raise ValueError(f"duplicate score row: {key}")
            seen.add(key)
            rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scores", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260905)
    args = parser.parse_args()
    rows = load_rows(args.scores)
    by_model: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_model[row["model_id"]].append(row)
    result = {"analysis_seed": args.seed, "bootstrap_replicates": args.replicates, "models": {}}
    for model_id, model_rows in sorted(by_model.items()):
        calibration = [
            row for row in model_rows
            if row["partition"] == "calibration" and row["renderer"] == "R0_native"
        ]
        threshold = conservative_balanced_threshold(
            [int(row["reward"]) for row in calibration],
            [float(row["success_score"]) for row in calibration],
        )
        renderers = sorted({row["renderer"] for row in model_rows if row["renderer"] != "R0_native"})
        cells = {}
        for renderer in renderers:
            evaluation = [
                row for row in model_rows
                if row["partition"] == "evaluation" and row["renderer"] in {"R0_native", renderer}
            ]
            cells[renderer] = task_cluster_bootstrap(
                evaluation, threshold, replicates=args.replicates, seed=args.seed
            )
        result["models"][model_id] = {
            "native_calibration_threshold": threshold,
            "calibration_n": len(calibration),
            "cells": cells,
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
