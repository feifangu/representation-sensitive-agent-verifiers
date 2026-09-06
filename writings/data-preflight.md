# Terminal-Bench 2.0 data preflight — 2026-09-05

This is verifier-blind substrate validation, not experiment evidence.

## Pinned inputs

- Trajectory dataset: `yoonholee/terminalbench-trajectories`, revision
  `04e8940f5b6736a7ce8d22224fe2f2af74163ed2`, Apache-2.0.
- 52,104 rows; two Parquet shards; advertised compressed size 220,993,900 bytes.
- Local shard SHA-256 values match the Hugging Face LFS object hashes:
  - `e95bc8dc9f3e1b2f3c6c383d0a060064205d87e93e9ac9541847d1c511effdfa`
  - `00d61614054bedcbadda9974cef30fe1e07d1701e7126edfa210f99840ae99b2`
- Task instructions: `jvpoulos/terminal-bench` revision
  `1a6ffa9674b571da0ed040c470cb40c4d85f9b9b`; 88 of the corpus's 89 task names match. The unmatched
  `headless-terminal` task is excluded from common support.

## Schema correction

The corpus uses `src`, `msg`, `tools`, and `obs` inside its JSON-encoded `steps` field. A separate
LLM-as-a-Verifier loader uses `source`, `message`, `tool_calls`, and `observation`; the project
adapter now supports the pinned corpus directly and preserves each raw step mapping without
renaming or dropping unknown fields. Rows with null/malformed steps are excluded with a reason.

## Frozen sample

- 120 trajectories across 66 tasks; task-disjoint split: 36 calibration, 84 evaluation.
- Each source contributes exactly 20 failures and 20 successes:
  - `terminus-2::moonshotai/Kimi-K2-Thinking@together_ai`
  - `openhands::Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8@together_ai`
  - `claude-code::claude-opus-4-5-20251101@anthropic`
- The three sources share 88 eligible tasks. Before sampling, valid failure/success supports were
  572/320, 644/226, and 204/232 respectively.
- Calibration support remains non-degenerate in every source: 5/9, 6/6, and 6/4 failures/successes.
- Evaluation support: 15/11, 14/14, and 14/16 failures/successes.

The manifest and validity ledger are in `experiments/e0-data-preflight/`. All 600 R0–R4 renderings
round-trip to the exact source event-graph digest.

## Length risk

Selected-rendering character counts range up to 288,564. P95 is approximately 154k–163k characters
depending on renderer. Tokenizer-specific counts are therefore a mandatory pre-model audit; no
character-to-token heuristic will be used to authorize the full run. A6000 suitability remains
conditional on the longest-tokenized examples fitting each pinned checkpoint at BF16.
