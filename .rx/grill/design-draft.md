# RX grill design draft — NOT CONFIRMED OR LOCKED

## Proposed bottleneck and contribution

Retrieved agent-judge studies show that evidence modality, amount, and judge architecture matter,
while metamorphic testing establishes consistency tests over semantically equivalent inputs.
However, inspected agent-verifier work does not isolate a frozen verifier's response to multiple
lossless serializations of the same complete trajectory. Existing ablations typically add/remove
screenshots, accessibility trees, reasoning, or context; generator/harness studies alter the
trajectory itself; controlled fault injection changes correctness-relevant process facts.

Proposed primary move: construct an immutable typed trajectory event graph plus several bijective
renderers, then measure paired verifier instability and decision flips. Proposed supporting move:
if sensitivity is material, test whether one neutral canonical renderer reduces instability and
source-conditioned error gaps while retaining native accuracy.

## First dependency — resolved and user-approved

Recommended: restrict the primary causal claim to **Tier A**, where parse(render(graph)) equals the
same graph exactly (including ordered calls, typed arguments, observations, errors, timestamps only
when exposed, final response, and provenance). Treat the following separately:

- Tier A: wrapper/header/delimiter/whitespace changes and semantically equivalent lossless
  structured encodings with exact round-trip equality.
- Tier B: outcome-preserving but evidence-salience-changing transforms, such as removing reasoning,
  summaries, or duplicated text; mechanically check the executable outcome, but do not call these
  evidence-preserving.
- Tier C: chatter insertion/deletion, paraphrase, and commuting-segment reorderings validated by
  humans or an external grader; report as semantic stress tests, not the clean invariance estimate.

Alternative: include Tier B/C in the primary estimand under a broader external-validation rule.
That is closer to the original seed but makes the core claim vulnerable because unchanged outcome
does not prove unchanged decision-relevant evidence or process correctness.

User constraints recorded 2026-09-05: target a credible workshop paper rather than a main-track
claim; inference only, with no training or fine-tuning; hard total GPU/inference budget below
USD 1,000. Recommended resolution: Tier A supplies the primary novelty/validity claim, while a
small, explicitly secondary Tier B suite supplies practical breadth. Exclude Tier C paraphrase and
reordering from the first paper because validation cost and semantic ambiguity consume budget
without strengthening the clean claim.

User confirmed this resolution on 2026-09-05.

## Proposed semantic and verifier contract

- Target label: pinned executable grader success/failure for terminal tasks. Infrastructure errors
  remain a separate status, not silently mapped to failure.
- Verifier target: outcome success only, user-approved on 2026-09-05. Process quality, safety,
  efficiency, and style require separate labels and are out of scope.
- Verifier input: task instruction plus the rendered complete trajectory; never include the hidden
  grader result or post-run grader logs. Legitimate in-trajectory test output remains evidence.
- Semantic graph: chronological typed events with role, action/tool name, typed arguments,
  observation payload, error status, and final response. Raw bytes and a canonical digest are
  retained. Unknown fields are preserved, not discarded.
- A renderer pair is valid only if both parse to the identical graph and neither hits the verifier's
  context limit. Truncated pairs are a separate operational stress test.

## Candidate Tier-A transformation families

1. Harness-neutral headers and assistant/tool delimiters.
2. Equivalent JSON object key order and whitespace/pretty versus compact rendering where object
   order is semantically irrelevant.
3. JSON versus an explicitly specified tagged/text encoding with exact typed round trip.
4. Stable synthetic event identifiers replacing source-specific non-semantic IDs through a
   reversible mapping supplied outside the verifier input.
5. Escaping/quoting conventions that decode to identical string payloads.

Identity/no-op rerenders and repeated inference are mandatory controls. Renaming tool functions,
changing argument order for positional APIs, normalizing paths, deleting timestamps, or sorting
events are not presumed safe.

### Proposed locked renderer set

- R0 native display renderer reconstructed from the source graph.
- R1 neutral tagged plaintext with generic `EVENT`, `ACTION`, and `OBSERVATION` delimiters.
- R2 canonical compact JSON event array with fixed schema and key order.
- R3 pretty JSON with a second deterministic, schema-valid object-key order.
- R4 OpenAI-style role/message JSON with typed tool calls and tool-result linkage.

Every R0–R4 output must round-trip to the same canonical graph digest. A byte-identical input repeat
and parse-to-native no-op are controls, not transformation families. The two Tier-B diagnostics are
B1 removal of agent reasoning/prose fields and B2 insertion of clearly delimited irrelevant chatter;
neither is included in the primary evidence-preserving estimand.

## Proposed estimands and diagnostics

For verifier `v`, trajectory `i`, renderer `r`, retain the native score and define paired score
change. Primary summaries:

- median and mean absolute score difference, plus upper quantiles;
- native-to-renderer decision-flip rate at a threshold calibrated only on native calibration data;
- change in false-accept and false-reject rates, reported separately;
- renderer-direction mean shift to detect systematic leniency/harshness;
- within-item variance attributable to renderer after subtracting the repeated-inference/no-op
  control variance.

AUROC/calibration before and after rendering are secondary because unpaired aggregate metrics can
hide item-level instability. Cluster uncertainty at the underlying task (and source trajectory if
multiple renderings). Freeze threshold, prompt, model revision, decoding, score extraction, and
context budget. Decide an equivalence/materiality margin before evaluation; `5 pp` flip-rate and a
score-scale-normalized margin are discussion defaults, not locked values.

### Score interface — resolved and user-approved

Use a forced `SUCCESS` versus `FAILURE` completion and compute the normalized conditional
log-likelihood assigned to the two fixed answers. Report the 0.5-boundary flip analysis as the
model-level invariance test. Separately fit an operational threshold on task-disjoint native
calibration trajectories, freeze it, and apply it to native/transformed evaluation pairs. Check each
checkpoint's tokenization and score the complete fixed answer sequences when either label is
multi-token. Free-form numeric probability elicitation is not the primary score.

### Proposed sampling, thresholds, and inference lock

- Select 120 eligible trajectories before verifier scoring: 40 from each of three source
  generator/scaffold combinations, targeting 20 pass/20 fail per source where support permits.
- Use task-disjoint calibration/evaluation partitions with approximately one third of tasks for
  calibration and two thirds for evaluation. Freeze one threshold per verifier by maximizing
  balanced accuracy on native calibration trajectories; deterministic tie rule chooses the more
  conservative (higher) threshold.
- Primary estimands on evaluation tasks: mean and median absolute score delta, renderer-direction
  mean shift, 0.5-boundary flip rate, frozen-threshold flip rate, and separate FPR/FNR changes.
- Use a shared 10,000-replicate task-cluster bootstrap for intervals. Treat renderer-by-model cells
  as the transparent analysis family; use Holm correction for cell-level positive claims. A pooled
  average is descriptive and cannot hide opposite directions.
- Material sensitivity requires a cell's corrected 95% lower confidence bound for flip rate to
  exceed 5 percentage points, or a corrected directional FPR/FNR deterioration exceeding 5 points.
  Tier-A equivalence requires every primary cell's 95% upper bound below 5 points. Otherwise the
  result is mixed/inconclusive; score changes alone do not establish deployment harm.
- Run deterministic inference. Repeat byte-identical inference three times on a fixed 20-trajectory
  audit subset to measure backend nondeterminism; any nonzero variance is reported and subtracted
  only in a declared sensitivity model, never silently.

### Proposed verifier checkpoints

Use Qwen3.5-9B, Gemma 3 12B IT, and Ministral 3 14B Instruct as three distinct frozen families,
subject to license/access, full-sequence `SUCCESS`/`FAILURE` scoring, context-length, and BF16
serving smoke tests. Pin exact repository revisions. If one fails before any scored evaluation,
replace it with a predeclared <=14B open-weight fallback from a different family; do not choose a
replacement after seeing sensitivity results. This is not a scaling-law comparison.

### Hard budget and stop rules

- No training, fine-tuning, adapters, or trajectory generation.
- Hard all-in compute/inference cap: USD 1,000 including tax and persistent storage.
- Smoke/preflight cap: USD 50. Stop before the full matrix if measured throughput projects total
  spend above USD 700 pre-tax, preserving contingency under the hard cap.
- Log instance type, region, listed and actual hourly price, launch/termination times, GPU-hours,
  framework/container revisions, model revisions, precision, context cap, and failed calls.
- Terminate the instance after each bounded run; persistent Lambda filesystems are not created
  unless separately justified because billing continues while they exist.

## Proposed workshop-scale pilot scope

- Prefer roughly 120 already-labeled terminal trajectories with executable grader provenance and
  both classes represented; use a larger available pool only if preprocessing and inference
  preflight remain comfortably inside the cap.
- Start with four Tier-A renderer families plus identity/no-op. Add at most two Tier-B diagnostics:
  reasoning/prose removal and irrelevant-chatter insertion, clearly labeled as evidence-salience
  stress tests rather than lossless invariance.
- Use three frozen open-weight verifier checkpoints spanning at least two model families, all at or
  below 14B. This is an inference-only comparison, not a model-size scaling law.
- Use deterministic decoding where score extraction allows it, plus a small repeated-inference
  control to estimate backend nondeterminism. Seeds govern stochastic scoring/repeats; renderers
  themselves must be deterministic and versioned.
- No trajectory generation or parameter updates are allowed. Dataset acquisition, long-context
  lengths, licenses, grader replay, model serving, and GPU/token cost require preflight before plan
  lock. The locked plan must include a small smoke-test gate and projected worst-case spend; no run
  may proceed if the full matrix projects to USD 1,000 or more.

Suggested budget envelope (to refine after token-length preflight): reserve at most 10% for
data/render validation and smoke tests, 70% for the frozen primary inference matrix, and 20% for
repeats, failed calls, and analysis contingencies. Unspent contingency is not permission to expand
scope.

### Compute recommendation

Use a Lambda A6000 48 GB as the default candidate because it is x86-compatible, has 8 GB more VRAM
than A100 40 GB, and is currently listed at USD 1.09/hour. It should fit 9B–14B checkpoints one at a
time in BF16 with more KV-cache headroom, although its lower memory bandwidth may reduce throughput.
Promote GH200 96 GB (currently USD 2.29/hour) if measured A6000 throughput projects above the cost
gate or any locked model/context requires quantization, truncation, CPU offload, or impractically
small batching. A100 80 GB remains the x86 fallback if GH200 ARM64 compatibility fails. Hardware
must not change precision or input coverage across models.

### Compute provider — resolved

Use a single Lambda Cloud instance. The user subsequently proposed A6000 48 GB, which Lambda lists
at USD 1.09/hour before tax. Prefer A6000 for smoke and the final matrix if measured throughput and
context coverage pass. Use GH200 96 GB at USD 2.29/hour for capacity/throughput, and A100 80 GB as
the x86 fallback. Query the live Lambda instance API and record actual price/region before launch.

### Substrate — resolved and user-approved

Use the public Terminal-Bench 2.0 full-trajectory corpus as the primary substrate. Select 120
existing trajectories across three generator/scaffold sources, aiming for 40 per source,
approximately balanced success/failure support within source, and overlapping tasks where feasible.
Do not rejection-sample silently: report exclusions, achieved label support, and the target
population induced by selection. Source supports heterogeneity analysis but is not the treatment;
all invariance contrasts remain paired renderings of one immutable saved trajectory. Use released
LLM-as-a-Verifier terminal trajectories only as a candidate reproduction/sensitivity subset.

## Baselines and strongest collisions

Mandatory comparisons: direct discrete pointwise judge; a probabilistic/fine-grained verifier in
the LLM-as-a-Verifier family if reproducible within budget; native renderer; identity/no-op
rerender; repeated scoring; and a length/token-count diagnostic. A canonicalizer is a mitigation,
not a baseline proving novelty.

- Strongest controlled-intervention collision: `trajectory-judge` (2609.00038).
- Strongest agent-judge representation collision: AgentRewardBench (2504.08942), followed by
  MobileJudgeBench (2608.11434).
- General framing collision: LGMT/metamorphic testing.
- Canonicalization collision: Harness-Induced Belief Divergence (2607.04528).
- Strong verifier systems/baselines: Universal Verifier and LLM-as-a-Verifier.

Four-axis delta versus `trajectory-judge`: framing—representation invariance rather than fault
detection; mechanism—bijective event-graph rendering rather than injected process faults;
insight—presentation dependence under fixed evidence rather than visibility of silent faults;
domain—both tool-agent trajectories, so no domain delta is claimed.

## Evidence expectations and falsifiers

Q1 is inspectable if a paired heatmap and renderer-by-verifier table show score deltas, flips,
FPR/FNR changes, validity counts, and task-clustered intervals. It is falsified on tested support if
all locked primary Tier-A effects lie inside equivalence margins with adequate precision. Broad
intervals are inconclusive.

Q2 is inspectable if a transformation ledger proves round-trip equality, preserved raw payloads,
token/length changes, grader provenance, invalid-pair rates, and rejected examples. It fails if the
substrate cannot support enough nontrivial bijective renderers or if parser/truncation failures
explain the effect.

Q3 is inspectable if native/canonical paired results jointly show reduced instability and retained
accuracy/calibration under locked criteria. It fails if canonicalization drops evidence, mainly
changes context length, or violates the accuracy non-inferiority margin.

## Failure-mode audit

- Novel-but-empty: avoided only if the event schema, renderer validity suite, and paired deployment
  estimands are concrete and released.
- Sum of parts: a generic collection of formatting perturbations plus ordinary judge accuracy is
  insufficient; the typed lossless contract is the constructive core.
- Hidden neighbor: AgentRewardBench, MobileJudgeBench, `trajectory-judge`, LGMT, Universal
  Verifier, and LLM-as-a-Verifier remain explicit.
- Vague audit: predeclare equivalence margins, frozen threshold, invalid-pair policy, and a decisive
  table before scoring.
- Shortcut result: token length, truncation, parser failure, and model nondeterminism must be
  separated from semantic sensitivity.
- Overclaiming: do not generalize beyond tested renderers, substrates, or verifier models; a null
  on Tier A says nothing about paraphrases/evidence ablations.

## Provisional workshop novelty assessment

Overall: moderate and plausibly workshop-worthy, but execution-dependent. The current scope is not
novel because it discovers that formatting affects LLMs; it is novel only if it constructs and
validates a useful equivalence class over real agent trajectories and connects violations to frozen
deployment decisions.

- Problem framing — moderate: paired verifier invariance under fixed trajectory evidence is
  cleaner than natural cross-agent/harness evaluation, but metamorphic testing already supplies the
  general invariance frame.
- Core mechanism — moderate: typed event graph, lossless renderers, and round-trip validity can be
  a real benchmark construction. It collapses to low novelty if transformations are merely regex
  edits or prompt-template variants.
- Key insight — unknown until measured: strongest if sensitivity concentrates in meaningful
  renderer families, differs between success/failure, or survives no-op/nondeterminism and
  truncation controls. A loose collection of score changes is weak.
- Domain — low: agent trajectory verification is already populated by AgentRewardBench,
  MobileJudgeBench, Universal Verifier, and LLM-as-a-Verifier. No first agent-verifier benchmark
  claim is available.

Workshop acceptance case: release the semantic schema, validity suite, paired transformed corpus,
and frozen evaluation harness; predeclare deployment-level flip/error estimands; demonstrate either
a clear sensitivity result or tight equivalence bounds for a defined renderer class. Workshop risk:
if the study only shows that XML versus JSON changes scores, reviewers can classify it as ordinary
prompt-format sensitivity. The constructive validity artifact and paired causal control are what
raise it above that category.

## Remaining grill branches

1. Resolved: Tier A is the only primary evidence-preserving family; limited Tier B is secondary.
2. Confirm outcome-only target versus joint process/outcome verification.
3. Resolved in principle: Terminal-Bench 2.0, 120 trajectories across three existing sources.
   Raw-schema, license, and label-provenance preflight remains required before lock.
4. Lock exact renderer families after inspecting sample trajectories.
5. Select score interface, threshold-calibration split, equivalence margins, uncertainty method,
   and handling of stochastic outputs.
6. Select verifier checkpoints and confirm the <=14B constraint.
7. Specify available hardware/provider, maximum GPU-hours/token spend, and hard monetary cap.
8. Decide whether Q3 is confirmatory/conditional or only exploratory.
9. Human-confirm the final shared-understanding summary before advancing to plan.
