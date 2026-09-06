# Decision record

2026-09-05: User requested a full RX pipeline for the supplied representation-sensitivity seed.
This authorizes project bootstrap and research/design work, not paid compute.

D1 — Create a project independent of `verifier-transport`. That project studies natural
generator/harness distribution shifts; this project holds the saved semantic trajectory fixed.

D2 — Narrow the clean primary intervention to mechanically bijective renderings of a typed event
graph. Wrapper, delimiter, whitespace, and lossless schema changes are candidates. Prose deletion,
chatter insertion, observation compression, and segment reordering require separate validity tiers.

D3 — Do not claim that paired/metamorphic invariance testing, verifier input-representation
effects, or canonicalization are new in general. The provisional delta is their combination for
frozen long-horizon agent outcome verifiers under an explicit evidence-preservation contract and
deployment-level paired error estimands.

D4 — Closest conceptual collision is `trajectory-judge` (controlled paired trajectory fault
injection). Closest agent-judge representation neighbor is AgentRewardBench. Neither inspected
study tests lossless paired serialization invariance, but priority remains provisional.

D5 — No model calls, dataset downloads, container runs, or paid compute are approved. The shared
KB hardware snapshot reports no usable GPU information. Bootstrap succeeded, although its optional
KB hardware refresh was denied by workspace permissions.

D6 — User targets workshop acceptance rather than a main-track claim. The study must remain
inference-only (no training or fine-tuning) and total GPU/inference spending must stay below a hard
USD 1,000 cap.

D7 — User approved: make mechanically bijective
Tier-A renderings the primary study; retain at most two Tier-B practical stress tests; omit Tier-C
paraphrase/reordering from the first paper. Target roughly 120 labeled trajectories, four Tier-A
families plus identity control, and three frozen verifier checkpoints across at least two families.

D8 — User approved Terminal-Bench 2.0 as the primary substrate: sample 120 existing full,
labeled trajectories across three generator/scaffold sources, approximately class-balanced within
source where support permits and with task overlap where feasible. Source is a stratification
variable; every representation comparison remains paired within the same saved trajectory. The
LLM-as-a-Verifier release is a candidate reproduction/sensitivity subset. Approval selects the
substrate but does not yet authorize download or inference before plan lock.

D9 — User approved executable task outcome as the sole ground-truth target. The verifier asks
whether the trajectory completed the task. Process quality, safety, efficiency, and style are out
of scope; no new human process annotations are planned.

D10 — User approved a forced-choice `SUCCESS`/`FAILURE` verifier protocol with continuous score
derived from normalized output log-likelihood. Primary invariance summaries are paired absolute
score change, decision flips at 0.5, and false-accept/false-reject changes. A task-disjoint threshold
calibrated only on native trajectories is frozen for deployment sensitivity. Identity rerenders and
identical repeated inference estimate non-transformation variance; AUROC/calibration are secondary.

D11 — User approved Lambda Cloud rental and is willing to use A10, A100, or GH200. Current public
prices checked 2026-09-05: A10 24 GB USD 1.29/GPU-hour, A100 40 GB USD 1.99,
A100 80 GB USD 2.79, and GH200 96 GB USD 2.29, before applicable tax. Recommend GH200 as the
primary final-run target because it has the largest listed memory among these choices at lower cost
than A100 80 GB; fall back to A100 80 GB if ARM/software compatibility fails. A10 may be used for
cheap preprocessing/smoke tests but not if it forces quantization absent from the locked protocol.

D12 — User proposed Lambda A6000 48 GB. Adopt it as the new default: current listed price is USD
1.09/hour, it is x86-compatible, and its extra 8 GB over A100 40 GB gives more BF16 KV-cache
headroom. Lower bandwidth is handled by the measured throughput/cost gate. GH200 remains the
capacity/throughput fallback and A100 80 GB the x86 fallback.

D13 — Public model metadata pinned before inference. Qwen3.5-9B revision `c2022362` is BF16;
Gemma 3 12B IT revision `96b6f1ec` is BF16 and manually gated; Ministral's default repository is
FP8 and was therefore replaced before scoring with the explicit BF16 repository at revision
`3cea74c1`. Qwen thinking output is disabled in the frozen chat-template arguments so the forced
answer likelihood is evaluated at the intended verdict position.

D14 — Verifier-blind data preflight selected three sources with complete raw traces and strong
binary support: Terminus-2/Kimi-K2-Thinking, OpenHands/Qwen3-Coder-480B, and Claude Code/Claude
Opus 4.5. The frozen 120-row manifest is exactly balanced within source and spans 66 tasks. Public
steps use `src/msg/tools/obs`; 17 selected-source rows with invalid/incomplete payloads were rejected
before sampling. All 600 Tier-A renderer validations pass.
