"""Measured wall-time cost projection; no token-price assumptions."""

from __future__ import annotations

import json
import math
from pathlib import Path


def project_from_score_logs(
    paths: list[Path],
    total_examples: int,
    hourly_price_usd: float,
    overhead_fraction: float = 0.25,
) -> dict[str, float]:
    elapsed = []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                elapsed.append(float(json.loads(line)["elapsed_seconds"]))
    if not elapsed:
        raise ValueError("at least one measured scoring record is required")
    conservative_seconds = sum(elapsed) / len(elapsed) * total_examples * (1 + overhead_fraction)
    hours = conservative_seconds / 3600
    return {
        "measured_examples": float(len(elapsed)),
        "mean_seconds_per_example": sum(elapsed) / len(elapsed),
        "projected_examples": float(total_examples),
        "overhead_fraction": overhead_fraction,
        "projected_gpu_hours": hours,
        "hourly_price_usd": hourly_price_usd,
        "projected_pre_tax_usd": math.ceil(hours * hourly_price_usd * 100) / 100,
    }
