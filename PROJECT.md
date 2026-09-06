# Same Outcome, Different Trajectory

Research project bootstrapped by rx.

- Knowledge base: `/Users/feifangu/.rx-kb` (system/GPU, pitfalls, learnings, secrets-by-reference)
- Traceability state: `.rx/state.json`
- Topic: `llm-agents`
- Status: plan locked and implementation prepared; paused before the bounded A6000 smoke run
- Layout: `code/`, `writings/`, `experiments/`, `publication/<venue>/`
- Publication folders: `publication/arxiv/` (preprint) and `publication/anon/` (double-blind)

## Research question

When the task outcome and decision-relevant trajectory evidence are held fixed, do frozen
agent verifiers change their score or acceptance decision solely because that evidence is
serialized differently?

The primary study is limited to mechanically bijective renderings of an immutable typed event
graph. Evidence-removing normalization, chatter edits, and non-causal reordering are secondary
stress tests unless their preservation claim can be independently validated. A canonicalization
mitigation is conditional on first observing material sensitivity.

- Questions: `.rx/questions/Q1.md` through `Q3.md`
- Survey: `writings/survey-neighborhood.md`
- Current handoff: `STATUS.md`; decisions: `DECISIONS.md`
- Continuation checklist: `writings/continuation-handoff.md`
