# Initial novelty and collision audit — 2026-09-05

Verdict: retain after narrowing. The broad proposition that judge outputs depend on input
representation is already established. The potentially defensible contribution is a controlled,
paired invariance benchmark for frozen agent outcome verifiers in which a typed semantic event
graph is unchanged and each primary renderer is mechanically round-trippable.

| Neighbor | Collision | Narrow delta still to test |
|---|---|---|
| trajectory-judge (2609.00038) | Controlled paired fault injections on agent trajectories, including an appended unsupported claim | Their intervention changes process correctness/fault labels; ours would change serialization while preserving the complete semantic event graph |
| AgentRewardBench (2504.08942) | Direct input-representation ablations for web-agent judges | Their screenshot/A11Y conditions add or remove evidence; no paired lossless rendering test |
| MobileJudgeBench (2608.11434) | Input-component and resolution ablations across judge methods/backends | Evidence quantity/quality changes, rather than bijective serialization |
| LGMT (2605.23965) | Metamorphic consistency under logically equivalent inputs | Establishes the general testing frame, not trajectory-verifier evidence contracts or deployment errors |
| Harness-Induced Belief Divergence (2607.04528) | Canonical schema embeddings and controlled harness effects | Acting-model beliefs under behavior-changing harnesses, not frozen outcome judgments on one saved trajectory |
| Universal Verifier / CUAVerifierBench (2604.06240) | Full-trajectory evidence management, process/outcome labels, verifier design ablations | Optimizes evidence selection; does not isolate serialization invariance |
| LLM-as-a-Verifier (2607.05391) | Strong probabilistic trajectory-verification protocol and position-bias handling | No inspected paired wrapper/style/serialization invariance evaluation |

## Method lineage and bottleneck

AgentRewardBench and MobileJudgeBench show that evidence representation and judge design affect
aggregate accuracy. Universal Verifier makes evidence selection an explicit part of verifier
quality. LLM-as-a-Verifier improves scoring granularity and variance. LGMT supplies the mature
metamorphic-testing analogy. `trajectory-judge` is the strongest paired-intervention collision,
but it intentionally changes correctness-relevant process facts.

The subtractive bottleneck is therefore not “representation has never mattered.” It is that prior
agent-verifier evaluations generally conflate representation with evidence content, modality,
source agent, or process correctness. A lossless event-graph rendering family could remove those
confounds. The idea dies if realistic substrates cannot support useful bijective transformations or
if apparent effects are entirely explained by truncation/parser failures.

## Mandatory comparison families

- Direct discrete pointwise outcome judge.
- A probabilistic/fine-grained verifier protocol in the LLM-as-a-Verifier family if reproducible
  within budget.
- Original/native renderer versus each paired renderer, with identity/no-op and repeated-inference
  controls.
- Canonical rendering only as a mitigation after a material primary effect.
- Round-trip parser equality, event hashes, token lengths, truncation/error counts, and grader-label
  preservation as validity checks—not performance baselines.

Search was focused rather than systematic. Full methods were inspected for the seven stored notes;
the absence of an exact prior paired serialization benchmark is provisional and must not be phrased
as a first-ever claim.
