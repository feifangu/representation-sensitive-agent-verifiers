import json

from rsav.costing import project_from_score_logs


def test_cost_projection_uses_measured_wall_time(tmp_path):
    path = tmp_path / "scores.jsonl"
    path.write_text("\n".join([
        json.dumps({"elapsed_seconds": 10}),
        json.dumps({"elapsed_seconds": 20}),
    ]) + "\n")
    result = project_from_score_logs([path], total_examples=100, hourly_price_usd=2, overhead_fraction=0.2)
    assert result["projected_gpu_hours"] == 0.5
    assert result["projected_pre_tax_usd"] == 1.0
