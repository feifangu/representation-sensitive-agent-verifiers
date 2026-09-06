---
key: mobilejudgebench
title: Benchmarking LLM Judges for Mobile Agent Evaluation
method: Crosses six judge methods with five model backends over human-labeled mobile
  trajectories; includes input-component and screenshot-budget ablations.
baselines:
- Simple direct judge
- AgentRewardBench judge
- SPA-Bench judge
- AndroidArena judge
- A3 judge modes
---

Source: https://arxiv.org/html/2608.11434v1 ; method and §§5.1–5.3 inspected on 2026-09-05.

Headline claim: judge method and backbone both matter; a simple baseline is competitive, and input components/resolution alter performance and downstream evaluation utility.

Open gap: its ablations add/remove evidence and alter visual resolution, so they do not identify sensitivity to lossless representation changes. It precludes broad claims that input-representation effects on agent judges are unstudied.
