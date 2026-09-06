"""Bounded, resumable GPU inference for a single frozen verifier checkpoint."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time
from typing import Any

from .renderers import TIER_A
from .schema import EventGraph
from .scoring import score_messages, verifier_messages


def _git_commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def _load_model(model_id: str, revision: str):
    import torch
    from transformers import AutoModelForImageTextToText, AutoProcessor

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the locked GPU scoring run")
    processor = AutoProcessor.from_pretrained(model_id, revision=revision, trust_remote_code=False)
    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        revision=revision,
        torch_dtype=torch.bfloat16,
        device_map="cuda",
        trust_remote_code=False,
    ).eval()
    tokenizer = getattr(processor, "tokenizer", processor)
    return model, tokenizer


def _completed_keys(path: Path) -> set[tuple[str, str]]:
    completed = set()
    if not path.exists():
        return completed
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            completed.add((row["trajectory_id"], row["renderer"]))
    return completed


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def run(args: argparse.Namespace) -> None:
    import torch

    model, tokenizer = _load_model(args.model, args.revision)
    completed = _completed_keys(args.output)
    max_positions = int(getattr(model.config, "max_position_embeddings", 0) or 0)
    started = time.monotonic()
    with args.manifest.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            graph = EventGraph.from_semantic_object(record["semantic"], record["provenance"])
            for renderer_name in args.renderer:
                key = (record["trajectory_id"], renderer_name)
                if key in completed:
                    continue
                rendered = TIER_A[renderer_name][0](graph)
                messages = verifier_messages(str(graph.task["instruction"]), rendered)
                torch.cuda.reset_peak_memory_stats()
                t0 = time.monotonic()
                score = score_messages(
                    model,
                    tokenizer,
                    messages,
                    chat_template_kwargs={"enable_thinking": False},
                    max_context_tokens=max_positions,
                )
                elapsed = time.monotonic() - t0
                _append_jsonl(args.output, {
                    "schema_version": "rsav-score-v1",
                    "trajectory_id": record["trajectory_id"],
                    "task_name": record["task_name"],
                    "source": record["source"],
                    "partition": record["partition"],
                    "reward": record["reward"],
                    "renderer": renderer_name,
                    "model_id": args.model,
                    "model_revision": args.revision,
                    "dtype": "bfloat16",
                    "chat_template_kwargs": {"enable_thinking": False},
                    "git_commit": _git_commit(),
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "elapsed_seconds": elapsed,
                    "peak_cuda_bytes": int(torch.cuda.max_memory_allocated()),
                    "max_position_embeddings": max_positions,
                    **score,
                })
                if args.max_examples and len(_completed_keys(args.output)) >= args.max_examples:
                    print(f"bounded stop after {args.max_examples} scored renderer examples")
                    return
                if args.max_wall_seconds and time.monotonic() - started >= args.max_wall_seconds:
                    print(f"bounded stop after {args.max_wall_seconds} wall seconds")
                    return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--renderer", action="append", choices=sorted(TIER_A), required=True)
    parser.add_argument("--max-examples", type=int, default=0)
    parser.add_argument("--max-wall-seconds", type=float, default=0)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
