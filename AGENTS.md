# Representation-sensitive verifier project

Follow `/Users/feifangu/research/AGENTS.md`. Before substantive work, read `PROJECT.md`,
`STATUS.md`, `DECISIONS.md`, `.rx/state.json`, and the current grill/design artifacts.

- Keep representation-only transformations distinct from evidence ablations, process faults,
  generator shift, and behavior-changing harness interventions.
- The primary invariance claim requires round-trip equality of a typed semantic event graph.
- Do not treat unchanged executable outcome alone as proof that decision-relevant evidence was
  preserved.
- Do not run experiments or paid inference before human-confirmed shared understanding, a locked
  plan, an explicit compute budget, and user approval.
- Literature notes are not experiment evidence; keep `.rx/evidence/` and claims empty until runs
  warrant them.
