# Status — 2026-09-06

RX stage: **experiment implementation**. Ideation, survey, human-confirmed shared understanding,
and the blocker-first plan lock are recorded. No paid inference, evidence record, or empirical claim
exists yet.

Completed:

- Bootstrapped the independent `llm-agents/representation-sensitive-agent-verifiers` project.
- Wrote three coordinated research questions: paired invariance, transformation validity, and a
  conditional canonicalization mitigation.
- Inspected seven close papers and stored structured notes plus a candidate baseline set.
- Narrowed the novelty claim around an immutable event graph and mechanically checked lossless
  renderers.

Current gate:

- Implement and locally validate the data audit, event schema, renderers, sampling, scoring,
  analysis, and Lambda runbook against the locked contract.
- First question posed: whether only mechanically bijective Tier-A renderings support the primary
  evidence-preserving claim, with chatter/removal/reordering relegated to secondary stress tests.
- User clarified the target: workshop-level novelty, inference only, and under USD 1,000 total
  GPU/inference cost. User approved Tier A as primary, a small Tier B diagnostic suite, and no Tier
  C in the first paper.
- User approved Terminal-Bench 2.0 as the primary substrate, using 120 existing trajectories across
  three generator/scaffold sources; the pinned corpus and task metadata are available locally.
- User approved executable grader pass/fail as the sole outcome target; process/safety labels are
  outside scope.
- User approved forced-choice log-likelihood scoring, 0.5 decision flips, and a separate frozen
  native-calibrated deployment threshold analysis.
- User approved Lambda Cloud rental and proposed A6000 48 GB. It is now the default if all locked
  BF16 models/contexts fit and measured throughput passes; GH200 96 GB is the capacity/throughput
  fallback and A100 80 GB the x86 fallback. No instance has been launched.
- Remaining choices have been consolidated into a proposed full design lock: R0–R4 lossless
  renderers, B1–B2 stress tests, three verifier families, task-disjoint calibration, task-cluster
  inference, 5-point materiality/equivalence margin, and bounded preflight/full-run stop rules.
- Shared understanding and the plan are locked. The pinned public corpus was downloaded and
  verifier-blind sampling produced a balanced 120-trajectory manifest over 66 tasks; all 600 Tier-A
  round trips pass. No verifier output or paid compute has been produced.
- The user accepted the Hugging Face terms for `google/gemma-3-12b-it`; live credentialed checkpoint
  access must still be verified on the rented instance without storing a token in this repository.
- Before paid inference: complete the longest-input smoke test under USD 50, produce a measured
  full-matrix cost projection below USD 700 pre-tax, and obtain explicit user approval.
- Work is intentionally paused before provisioning the Lambda A6000. The repository is packaged
  for private GitHub backup; full trajectory text remains local/ignored, while a 120-row
  provenance-only sample index is tracked.

Resume with `writings/continuation-handoff.md` after reading the required project records.
