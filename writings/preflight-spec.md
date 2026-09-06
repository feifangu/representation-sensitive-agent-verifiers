# Preflight specification — no run authorized yet

This document defines what must be prepared before paid verifier inference. It is not a plan lock
or compute authorization.

## Data checks

1. Record dataset revision, license, row count, source combinations, task IDs, rewards, and schema.
2. Verify that task text, raw ordered steps, tool calls, typed arguments, observations, errors, and
   final response are available without using hidden grader output as verifier input.
3. Report duplicate trajectories, missing labels, infrastructure statuses, malformed steps, and
   label support by source/task.
4. Measure native token lengths under all three tokenizers before sampling; do not select examples
   based on verifier outputs.

## Renderer checks

1. Parse raw data into a versioned typed event graph while retaining unknown fields and raw source
   hashes.
2. For every R0–R4 rendering, assert `parse(render(graph)) == graph` and identical canonical digest.
3. Property-test empty payloads, multiline output, Unicode, binary/escaped strings, nested
   arguments, missing observations, tool errors, repeated IDs, and very long fields.
4. Keep invalid transforms and reasons in the audit; never drop them silently from denominators.

## Model and hardware smoke gate

1. Start with Lambda A6000 48 GB and a current x86 CUDA image.
2. Load each exact checkpoint one at a time in BF16; no quantization or CPU offload.
3. Score the longest eligible input plus all R0–R4 variants using complete-sequence conditional
   log-likelihood for `SUCCESS` and `FAILURE`.
4. Record peak VRAM, prefill latency, throughput, output-token scores, and parsing failures.
5. Move to GH200 if A6000 cannot preserve the locked context/precision or measured throughput fails
   the cost gate; use A100 80 GB if GH200 ARM64 compatibility fails.
6. Project full-matrix cost from measured tokens and wall time. Stop if projected pre-tax total
   exceeds USD 700 or smoke spend reaches USD 50.

## Artifacts required before full inference

- Frozen sample manifest and calibration/evaluation task split.
- Canonical graph schema and digest version.
- Renderer validity report with 100% Tier-A round-trip success among included pairs.
- Exact verifier prompt, tokenizer revisions, answer-sequence scoring implementation, and tests.
- Cost projection and explicit user approval for the bounded paid run.
