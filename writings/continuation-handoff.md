# Continuation handoff — 2026-09-06

The project is paused at RX stage `experiment`, before any paid inference or verifier output.
Shared understanding and the evaluation contract are locked. No evidence or claims exist yet.

## Resume order

1. Read `PROJECT.md`, `AGENTS.md`, `STATUS.md`, `DECISIONS.md`, `.rx/state.json`,
   `.rx/grill/shared-understanding.md`, and `.rx/plan/lock.md`.
2. Provision one Lambda A6000 48 GB instance only after explicit user approval for the bounded
   smoke run. The smoke cap is USD 50; the hard all-in project cap is USD 1,000.
3. Follow `writings/lambda-gpu-runbook.md`. Authenticate to Hugging Face using the browser/device
   flow; never put a token in this repository or chat.
4. Reconstruct the full manifest by running the pinned preflight against the locally downloaded
   dataset. Verify that it matches `experiments/e0-data-preflight/sample-index.jsonl`,
   `summary.json`, and the 600-row renderer-validity ledger.
5. Run tokenizer and BF16 memory smoke checks for all three pinned verifiers. Do not truncate,
   quantize, offload, substitute models, or begin the full matrix.
6. Copy smoke artifacts back, terminate billing, and obtain fresh approval after reporting the
   measured full-run projection. Stop if projected pre-tax cost exceeds USD 700.

## Frozen study

- Dataset revision: `yoonholee/terminalbench-trajectories@04e8940f5b6736a7ce8d22224fe2f2af74163ed2`.
- Sample: 120 trajectories, exactly 20 pass and 20 fail from each of three frozen sources, spanning
  66 tasks with a task-disjoint 36/84 calibration/evaluation split.
- Primary interventions: R1–R4 mechanically bijective representations versus native R0.
- Secondary diagnostics: B1 reasoning/prose removal and B2 irrelevant-chatter insertion.
- Verifiers: pinned Qwen3.5-9B, Gemma-3-12B-IT, and Ministral-3-14B-Instruct BF16 revisions in
  `config/experiment.yaml`.
- Primary endpoint: task-clustered decision-flip rate at a threshold fitted on native calibration
  trajectories; paired score shifts, 0.5 flips, and FPR/FNR changes are also reported.

## Data and security note

The generated full manifest is intentionally ignored because public benchmark trajectories contain
credential-shaped strings inside archived task text. Git tracks only a provenance-only sample index.
Raw dataset/model caches are also ignored. Regenerated full trajectories must remain local and must
not be committed without a fresh security and redistribution review.
