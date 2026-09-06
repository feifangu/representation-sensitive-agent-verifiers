---
key: agentrewardbench
title: 'AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories'
method: Expert-labeled, multi-agent web trajectories evaluated with 12 judge variants;
  compares judge representation functions and ablates screenshots versus accessibility
  trees.
baselines:
- AER trajectory judge
- NNetNav summary judge
- Simplified direct trajectory judge
- Human expert labels
---

Source: https://arxiv.org/html/2504.08942v2 ; full method §§3–4 and input-representation ablation inspected on 2026-09-05.

Headline claim: across 1,302 trajectories from four agent LLMs and five web benchmarks, no judge exceeds 70% precision; different evidence representations materially affect precision/recall.

Open gap: its representation ablation changes the evidence modality/content supplied to the judge (screenshots and/or accessibility trees) and compares aggregate accuracy, rather than applying paired lossless renderings to each trajectory. It is the closest published agent-judge representation study and a mandatory collision/baseline.
