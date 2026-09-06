---
key: lgmt
title: 'LGMT: Logic-Grounded Metamorphic Testing for Evaluating the Reasoning Reliability
  of LLMs'
method: Derives metamorphic relations from first-order logical equivalences and tests
  output consistency across semantically invariant problem variants.
baselines:
- Static reasoning benchmark evaluation
- Few-shot chain-of-thought
- Oracle-free metamorphic relation
---

Source: https://arxiv.org/html/2605.23965 ; full framing, formal method, and experiments inspected on 2026-09-05.

Headline claim: logically equivalent transformations uncover reasoning inconsistencies missed by static accuracy evaluation.

Open gap: invariant-pair/metamorphic framing is established and must not be claimed as new. It targets models solving logical problems, not outcome verifiers judging serialized long-horizon agent evidence. Our novelty must come from the trajectory semantic-object contract and verifier-specific deployment estimands.
