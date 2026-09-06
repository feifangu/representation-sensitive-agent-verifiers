---
key: trajectory-judge
title: 'trajectory-judge: What Outcome-Only LLM Judges Miss on Agent Trajectories'
method: Deterministic tool environment, scripted oracle trajectories, and single-fault
  injection with known fault type, step, and outcome-survival labels.
baselines:
- Outcome-only judge
- Step-rubric judge
- Programmatic rule engine
- Self-consistency ensemble
---

Source: https://arxiv.org/html/2609.00038 ; full method, metrics, and reported results inspected on 2026-09-05.

Headline claim: controlled fault injection exposes silent process faults that outcome-only judges miss; appended unsupported claims evade all tested trajectory judges frequently.

Open gap: this is the strongest conceptual collision for controlled paired trajectory interventions. However, its transformations deliberately change process correctness/fault labels, even when customer-visible outcome survives; they are not representation-only invariances preserving all decision-relevant evidence. Our defensible delta is the immutable-event/evidence contract, not merely paired perturbation.
