---
primary_question_id: Q1
novelty_gap: Existing agent-judge representation ablations change evidence modality
  or content, natural generator/harness studies change the trajectory, and controlled
  fault injection changes process correctness. The open measurement gap is a paired
  test of a frozen outcome verifier across mechanically bijective serializations of
  one immutable typed agent-event graph.
metric_intent: On task-disjoint evaluation trajectories, measure paired absolute and
  directional verifier-score changes, 0.5-boundary and frozen native-calibrated decision
  flips, and separate FPR/FNR changes. Use task-cluster uncertainty; treat AUROC and
  calibration as secondary.
baselines:
- native renderer
- byte-identical repeat
- parse-to-native no-op rerender
- direct forced-choice pointwise verifier
- LLM-as-a-Verifier-style probabilistic scoring if reproducible within budget
- identity and inference-nondeterminism controls
falsifiers:
- All Tier-A renderer-by-model primary flip-rate and error-drift intervals lie below
  the locked five-point equivalence margin with adequate precision.
- The approved Terminal-Bench substrate cannot support nontrivial exact round-trip
  renderer transformations.
- Observed instability is explained by truncation, parser failure, changed payloads,
  or ordinary inference nondeterminism.
- Canonicalization fails its joint robustness-improvement and accuracy-retention criteria.
scope_cuts:
- No training, fine-tuning, adapters, or new trajectory generation.
- Outcome success only; no process, safety, efficiency, or style labels.
- Tier C paraphrase and segment reordering excluded.
- Tier B reasoning removal and irrelevant chatter are secondary stress tests, not
  evidence-preserving primary interventions.
- No model-size scaling claim, no first-ever generic metamorphic-testing claim, and
  no generalization beyond tested models/renderers/substrate.
machine_time_budget: Single Lambda GPU, A100 40 GB default; GH200 96 GB memory fallback
  and A100 80 GB x86 fallback. USD 50 smoke cap, stop if measured full-run projection
  exceeds USD 700 pre-tax, hard all-in cap below USD 1,000. Models run one at a time
  in BF16 without quantization, truncation, or CPU offload.
open_risks:
- Terminal-Bench dataset revision/license/raw schema and executable-label provenance
  require preflight.
- Class balance and common-task support across three sources may be insufficient.
- Four lossless renderers may tokenize to materially different lengths; context overflow
  must be excluded from the clean estimand and reported.
- Qwen3.5-9B, Gemma 3 12B IT, or Ministral 3 14B Instruct may fail access, tokenizer,
  full-sequence score, BF16 memory, or serving compatibility gates.
- Five-point equivalence may be imprecise with 120 trajectories, especially within
  FPR/FNR strata.
- Irrelevant-chatter insertion can change semantic/process evidence and must remain
  Tier B.
diff_framing: Paired representation invariance of a frozen outcome verifier under
  fixed complete trajectory evidence, rather than accuracy on heterogeneous natural
  trajectories or injected faults.
diff_mechanism: A versioned typed event graph, exact round-trip renderers, canonical
  digests, and validity ledger isolate serialization from evidence content; this differs
  from evidence ablation and fault injection.
diff_insight: Determine whether operational verifier decisions depend on serialization
  after subtracting parser, truncation, length, and nondeterminism explanations; characterize
  success/failure and source heterogeneity.
diff_domain: Long-horizon terminal-agent outcome verification with executable labels.
  Domain novelty is low and is not claimed.
collision_threats:
- 'trajectory-judge (2609.00038): paired controlled faults but changes process correctness'
- 'AgentRewardBench (2504.08942): closest agent-judge input-representation ablation'
- 'MobileJudgeBench (2608.11434): input component/resolution ablations'
- 'LGMT (2605.23965): general invariant-pair metamorphic testing'
- 'Harness-Induced Belief Divergence (2607.04528): canonical schemas across harnesses'
- 'Universal Verifier/CUAVerifierBench (2604.06240): strong evidence-management verifier'
- 'LLM-as-a-Verifier (2607.05391): strong probabilistic trajectory-verification protocol'
evidence_expectations:
- Renderer validity ledger with raw hashes, canonical graph digests, round-trip equality,
  token lengths, context status, and rejected transformations.
- Trajectory-by-renderer paired score heatmap and renderer-by-verifier table of absolute/directional
  changes, flips, FPR/FNR deltas, support, and task-cluster intervals.
- Identity/no-op/repeated-inference control table separating transformation effects
  from backend variance.
- Native-versus-canonical mitigation table jointly reporting robustness, discrimination,
  calibration, thresholds, and token/truncation costs.
failure_mode_checks:
- Novel-but-empty avoided only by releasing the semantic schema, validator suite,
  paired corpus, and frozen evaluation harness.
- "Sum-of-parts risk addressed by making the lossless equivalence contract\u2014not\
  \ miscellaneous formatting changes\u2014the constructive core."
- Strongest neighbors remain explicit and mandatory comparisons are not hidden.
- No positive claim from score movement alone; deployment flips/error drift and validity
  controls are required.
- No equivalence claim from nonsignificance or wide intervals.
- No silent exclusions, changed precision, outcome-label leakage, or post-result model/renderer
  replacement.
---

Human confirmed this design on 2026-09-05 by saying “lock it.”

Use 120 existing Terminal-Bench 2.0 trajectories, 40 from each of three generator/scaffold sources, targeting balanced labels and overlapping tasks where support permits. Ground truth is executable outcome pass/fail. Parse each raw trajectory into one immutable typed event graph and generate R0 native, R1 neutral tagged plaintext, R2 compact canonical JSON, R3 alternate pretty JSON, and R4 role/message JSON. All Tier-A renderers must round-trip to the identical graph digest. B1 reasoning/prose removal and B2 irrelevant chatter insertion are separately labeled Tier-B stress tests.

Score frozen Qwen3.5-9B, Gemma 3 12B IT, and Ministral 3 14B Instruct checkpoints, subject to predeclared access and smoke gates, using normalized full-answer likelihood for SUCCESS versus FAILURE. Pin revisions, prompt, BF16 precision, context policy, and serving stack. Split by task into native calibration and evaluation sets; calibrate one conservative tied threshold per verifier by balanced accuracy. Use shared task-cluster bootstrap intervals and Holm-corrected cell claims. The five-percentage-point margin defines material deployment instability/equivalence.

Run no paid inference until data/schema validation, renderer property tests, longest-context model smoke tests, cost projection, plan lock, and explicit bounded-run approval are complete.
