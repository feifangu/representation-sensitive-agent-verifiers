---
metric: Task-clustered frozen-native-threshold decision-flip rate across valid Tier-A
  trajectory renderings
higher_is_better: false
comparison_family:
- R1 neutral tagged plaintext vs R0 native
- R2 canonical compact JSON vs R0 native
- R3 alternate-key-order pretty JSON vs R0 native
- R4 role/message JSON vs R0 native
- renderer-by-verifier cell family across three frozen verifier models
seed_policy: 2
baselines:
- byte-identical repeated inference
- parse-to-native no-op rerender
- R0 native renderer
- forced-choice discrete 0.5 decision
- frozen native-calibrated threshold
- LLM-as-a-Verifier-style score protocol if reproduced within budget
---

Blocker-first lock confirmed from the human-approved RX grill on 2026-09-05.

## Population and split

- Select 120 eligible Terminal-Bench 2.0 trajectories from three frozen generator/scaffold
  sources, 40 per source, targeting 20 pass/20 fail and common tasks where support permits.
- Freeze selection without verifier outputs. Preserve an exclusion ledger and report achieved
  support instead of silently replacing unavailable cells.
- Split by task, approximately one-third calibration and two-thirds evaluation. No task may cross
  the partition.

## Semantic and rendering contract

- Parse each raw trajectory into a versioned, typed event graph retaining all fields and raw hashes.
- R0–R4 are valid only when their inverse parsers recover exactly the same canonical graph digest.
- Context overflow, parser failure, missing evidence, or changed payload makes a pair invalid for
  the Tier-A primary estimand and must remain in the audit ledger.
- B1 reasoning removal and B2 chatter insertion are secondary Tier-B stress tests.

## Scoring and threshold

- For each pinned verifier, compute normalized full-sequence conditional likelihood for the exact
  answers `SUCCESS` and `FAILURE`; free-form numeric confidence is not used.
- Fit one threshold per verifier on R0 calibration tasks by maximizing balanced accuracy. If tied,
  select the highest threshold. Freeze before transformed evaluation scoring.
- Primary metric is the evaluation-task probability that R0 and a valid Tier-A renderer fall on
  opposite sides of that frozen threshold. Lower means more invariant.
- Report 0.5-boundary flips, absolute/directional score deltas, and separate FPR/FNR changes as
  required supporting outcomes. AUROC and calibration are secondary.

## Inference and uncertainty

- Qwen3.5-9B, Gemma 3 12B IT, and Ministral 3 14B Instruct; exact revisions frozen before scoring.
- BF16, one model at a time, identical prompt logic and context policy, no quantization/offload.
- Deterministic inference. On a fixed 20-trajectory subset, run byte-identical inputs three times.
- Shared 10,000-replicate task-cluster bootstrap. Reproduce intervals with two analysis seeds:
  20260905 and 20260906. Holm-correct renderer-by-verifier positive claims.
- Material sensitivity: corrected 95% lower bound above 5 percentage points for a flip-rate cell or
  directional FPR/FNR deterioration. Tier-A equivalence: every primary cell upper bound below 5
  points. Wide/mixed intervals are inconclusive.

## Compute contract

- Lambda A6000 48 GB default; GH200 96 GB for memory/throughput, A100 80 GB for x86 fallback.
- USD 50 smoke ceiling. Do not launch the full matrix if measured projection exceeds USD 700
  pre-tax. Hard all-in ceiling below USD 1,000 including tax/storage.
- No training, fine-tuning, adapters, trajectory generation, or post-result substitution.
- Paid full inference still requires a separate explicit user approval after smoke results and cost
  projection. This lock authorizes local implementation and non-paid validation only.
