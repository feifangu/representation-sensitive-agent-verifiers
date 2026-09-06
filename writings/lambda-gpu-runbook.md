# Lambda A6000 48 GB preparation runbook

No command in this document authorizes paid compute. Launch only after the bounded smoke run is
explicitly approved.

## Before launch

- Confirm the frozen dataset sources and model revisions in `config/experiment.yaml`. Leave
  `quantization: null` unchanged (it explicitly means no quantization). Resolve
  `max_context_tokens: null` only from the tokenizer-length audit, record the per-model value, and
  do not begin scoring until every selected input fits without truncation.
- Commit the exact code/config and record the commit hash.
- Gemma license terms were accepted by the user on 2026-09-05. Confirm live access to pinned
  revision `96b6f1eccf38110c56df3a15bffe176da04bfd80` and authenticate through the configured
  Hugging Face credential store; never copy tokens into this repository.
- Confirm the Lambda console's live price and available region. Do not create a persistent
  filesystem by default.

## Instance setup

Use a current Lambda x86 PyTorch image on a single A6000 48 GB. Transfer the committed repository,
create an isolated environment, and install `.[data,gpu,test]`. Record:

```text
nvidia-smi
python --version
python -m pip freeze
git rev-parse HEAD
```

Run local tests before downloading models. Download one pinned checkpoint at a time into instance
storage, verify repository revision, and remove neither logs nor manifests when switching models.

## Smoke sequence

1. Run the dataset/schema audit and freeze the candidate manifest.
2. Measure tokenizer lengths for every R0–R4 rendering before model inference.
3. Select the longest eligible trajectory and one median trajectory without looking at verifier
   results.
4. Load each model in BF16 with no quantization or CPU offload.
5. Score both examples and all Tier-A renderings; record peak VRAM and wall time.
6. Exercise both answer sequences and verify finite log-likelihoods and a score in `[0,1]`.
7. Repeat one identical input three times and check determinism.
8. Project the complete matrix using measured prefill time plus a conservative 25% overhead.

Stop and terminate the instance if spend reaches USD 50, any Tier-A pair fails round trip, any input
would be truncated, a model cannot fit at BF16, outputs are non-finite, or projected pre-tax spend
  exceeds USD 700. Lower A6000 throughput is acceptable if the measured cost projection passes. Do
not improvise quantization or replace a model during the run.

## Handoff after smoke

Copy back the manifest, audit ledger, environment lock, hardware report, timings, projected cost,
and logs. Terminate the instance and verify in Lambda that it is no longer billed. Present the
measured projection for explicit approval before a full inference launch.
