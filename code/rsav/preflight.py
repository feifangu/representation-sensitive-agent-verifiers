"""Verifier-blind preparation of a pinned Terminal-Bench sample."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any, Iterable

from .dataset import binary_reward, load_task_catalog, terminalbench_row_to_graph
from .renderers import TIER_A, validate_roundtrip
from .sampling import select_balanced, stable_id, task_disjoint_split


def iter_parquet_rows(paths: Iterable[Path]):
    import pyarrow.parquet as pq

    columns = ["task_name", "agent", "model", "reward", "duration_seconds", "input_tokens",
               "output_tokens", "cache_tokens", "cost_cents", "trial_name", "trial_id",
               "started_at", "ended_at", "steps"]
    offset = 0
    for path in sorted(paths):
        table = pq.read_table(path, columns=columns)
        for index, row in enumerate(table.to_pylist(), offset):
            yield index, row
        offset += table.num_rows


def prepare_sample(
    parquet_paths: list[Path],
    task_root: Path,
    sources: list[str],
    output_dir: Path,
    per_source: int = 40,
    seed: int = 20260905,
) -> dict[str, Any]:
    catalog = load_task_catalog(task_root)
    graphs = []
    exclusions = Counter()
    source_support: Counter[tuple[str, int]] = Counter()
    source_tasks: dict[str, set[str]] = defaultdict(set)

    for row_index, row in iter_parquet_rows(parquet_paths):
        source = f"{row.get('agent')}::{row.get('model')}"
        if source not in sources:
            exclusions["source_not_selected"] += 1
            continue
        try:
            graph = terminalbench_row_to_graph(row, row_index, catalog)
            reward = binary_reward(graph)
        except (TypeError, ValueError, json.JSONDecodeError):
            exclusions["invalid_or_incomplete_row"] += 1
            continue
        graphs.append(graph)
        source_support[(source, reward)] += 1
        source_tasks[source].add(str(graph.task["task_name"]))

    common_tasks = set.intersection(*(source_tasks[source] for source in sources))
    eligible = [g for g in graphs if str(g.task["task_name"]) in common_tasks]
    exclusions["not_in_common_task_support"] += len(graphs) - len(eligible)
    selected, sample_exclusions = select_balanced(eligible, sources, per_source=per_source, seed=seed)
    exclusions.update(item["reason"] for item in sample_exclusions)
    split = task_disjoint_split(selected, seed=seed)

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.jsonl"
    validity_path = output_dir / "renderer-validity.jsonl"
    with manifest_path.open("w", encoding="utf-8") as manifest, validity_path.open(
        "w", encoding="utf-8"
    ) as validity:
        for graph in selected:
            record = graph.to_record()
            record["trajectory_id"] = stable_id(graph)
            record["reward"] = binary_reward(graph)
            record["source"] = graph.provenance["source"]
            record["task_name"] = graph.task["task_name"]
            record["partition"] = split[str(graph.task["task_name"])]
            manifest.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            for renderer_name in TIER_A:
                check = validate_roundtrip(graph, renderer_name)
                check["trajectory_id"] = stable_id(graph)
                check["task_name"] = graph.task["task_name"]
                validity.write(json.dumps(check, ensure_ascii=False, sort_keys=True) + "\n")

    selected_counts = Counter((g.provenance["source"], binary_reward(g)) for g in selected)
    partition_counts = Counter(split[str(g.task["task_name"])] for g in selected)
    summary = {
        "sampling_seed": seed,
        "sources": sources,
        "selected_trajectories": len(selected),
        "selected_tasks": len({g.task["task_name"] for g in selected}),
        "common_eligible_tasks": len(common_tasks),
        "selected_counts": {
            source: {str(label): selected_counts[(source, label)] for label in (0, 1)}
            for source in sources
        },
        "eligible_counts": {
            source: {str(label): source_support[(source, label)] for label in (0, 1)}
            for source in sources
        },
        "partition_counts": dict(sorted(partition_counts.items())),
        "exclusion_counts": dict(sorted(exclusions.items())),
        "task_catalog_entries": len(catalog),
        "all_tier_a_roundtrips_valid": True,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary
