---
key: harness-belief-divergence
title: Measuring Harness-Induced Belief Divergence in Multi-Step LLM Agents
method: Formalizes harness components, maps observations/actions into canonical schema
  spaces, and measures belief trajectories under controlled harness interventions.
baselines:
- Raw reference harness
- Canonical schema embedding
- Belief instrumentation and verification masks
---

Source: https://arxiv.org/html/2607.04528v1 ; full formal setup and canonical-embedding mechanism inspected on 2026-09-05.

Headline claim: execution harnesses are first-order variables affecting multi-step agent beliefs; canonical schema embedding removes syntactic non-identifiability for cross-harness comparisons.

Open gap: canonical embeddings and harness-normalization motivation are prior art. The paper studies the acting model’s elicited beliefs under behavior-changing harnesses, not a frozen outcome verifier on paired renderings of an unchanged saved trajectory. Q3 cannot claim canonicalization itself as novel.
