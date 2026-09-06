"""Local, non-paid preprocessing commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataset import terminalbench_row_to_graph
from .preflight import prepare_sample
from .renderers import TIER_A, validate_roundtrip


def _iter_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                yield line_number, json.loads(line)


def audit_jsonl(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as out:
        for line_number, row in _iter_jsonl(input_path):
            graph = terminalbench_row_to_graph(row, row_index=line_number - 1)
            record = graph.to_record()
            record["trajectory_id"] = graph.digest[:20]
            record["renderers"] = [validate_roundtrip(graph, name) for name in TIER_A]
            out.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(prog="rsav")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit-jsonl", help="parse rows and validate all Tier-A renderers")
    audit.add_argument("input", type=Path)
    audit.add_argument("output", type=Path)
    prepare = sub.add_parser("prepare-sample", help="freeze a verifier-blind Parquet sample")
    prepare.add_argument("--parquet", type=Path, nargs="+", required=True)
    prepare.add_argument("--task-root", type=Path, required=True)
    prepare.add_argument("--source", action="append", required=True)
    prepare.add_argument("--per-source", type=int, default=40)
    prepare.add_argument("--seed", type=int, default=20260905)
    prepare.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "audit-jsonl":
        audit_jsonl(args.input, args.output)
    elif args.command == "prepare-sample":
        summary = prepare_sample(
            args.parquet,
            args.task_root,
            args.source,
            args.output_dir,
            per_source=args.per_source,
            seed=args.seed,
        )
        print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
