# Local EvalKit And Hosted AuraOne SDKs

AuraOne EvalKit is a local open-source evaluation toolkit. It is intentionally
separate from SDKs and CLIs that call hosted AuraOne APIs.

## Local EvalKit

- Distribution project: `auraone-evalkit`
- Python import package: `auraone_evalkit`
- CLI: `evalkit`
- Inputs: local rubric, output, label, judge, batch, and report files
- Runtime: local Python process
- Authentication: none
- Core jobs: rubric validation and linting, deterministic scoring, reviewer
  agreement, saved judge calibration, drift, leakage checks, sampling, rubric
  diffs, weight calibration, dataset cards, and evidence reports

EvalKit exists so teams can inspect and run the judgment layer of an evaluation
without sending private eval material to AuraOne.

## Hosted AuraOne Integrations

Hosted SDKs or product clients are separate projects with separate
authentication and runtime contracts. They are not dependencies of EvalKit and
are not required for local rubric, scoring, QA, or report workflows.

The namespace boundary is deliberate:

- `evalkit validate-rubric` validates local rubric files.
- `evalkit score` aggregates local labels and outputs.
- `evalkit report` writes local evidence artifacts.
- Hosted product commands, when used, follow their own package documentation
  and credentials.

## Why The Boundary Matters

Private evaluation prompts, criteria, labels, and failure cases can encode
unreleased capabilities, customer workflows, policy, or domain expertise. A
local package lets teams adopt public schemas and deterministic checks without
making that data public or placing it behind a required service account.

The separation also keeps claims precise. EvalKit can prove what its local
inputs and algorithms produced. It cannot prove that a hosted run occurred,
that data was collected by AuraOne, or that a model, judge, reviewer, or
dataset is production-ready.

## Data Status

Bundled examples are synthetic fixtures for tutorials and tests. They are not
expert-authored benchmarks, customer data, human-validated datasets, or safety
certifications.

[EvalKit docs index](../README.md) |
[Package README](../../README.md)
