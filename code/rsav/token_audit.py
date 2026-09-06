"""Tokenizer-only context audit for all frozen renderings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .renderers import TIER_A
from .schema import EventGraph
from .scoring import verifier_messages


def main() -> None:
    from transformers import AutoProcessor

    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    processor = AutoProcessor.from_pretrained(args.model, revision=args.revision, trust_remote_code=False)
    tokenizer = getattr(processor, "tokenizer", processor)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open(encoding="utf-8") as inp, args.output.open("w", encoding="utf-8") as out:
        for line in inp:
            record = json.loads(line)
            graph = EventGraph.from_semantic_object(record["semantic"], record["provenance"])
            for name, (render, _) in TIER_A.items():
                messages = verifier_messages(str(graph.task["instruction"]), render(graph))
                ids = tokenizer.apply_chat_template(
                    messages,
                    add_generation_prompt=True,
                    tokenize=True,
                    **{"enable_thinking": False},
                )
                out.write(json.dumps({
                    "trajectory_id": record["trajectory_id"],
                    "task_name": record["task_name"],
                    "renderer": name,
                    "model_id": args.model,
                    "model_revision": args.revision,
                    "prompt_tokens": len(ids),
                }, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
