---
key: universal-verifier
title: The Art of Building Verifiers for Computer Use Agents
method: Rubric generation plus criterion-specific screenshot relevance selection,
  process/outcome separation, side-effect detection, and structured failure diagnosis.
baselines:
- WebJudge
- WebVoyager evaluator
- AgentRewardBench judge
- Human annotator agreement
---

Source: https://arxiv.org/html/2604.06240 ; full method §§3–5 inspected on 2026-09-05.

Headline claim: a cumulative verifier design reaches approximately human-human agreement and reduces false positives relative to WebJudge/WebVoyager on CUA trajectories.

Open gap: it optimizes evidence selection and rubric design and evaluates natural trajectories; it does not test whether one frozen verifier is invariant across semantically identical serializations. Its emphasis that omitted/transient screenshots change correctness makes evidence preservation a stricter requirement for our transformations.
