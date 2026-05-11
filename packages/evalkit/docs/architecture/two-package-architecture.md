# Two-Package Architecture

AuraOne EvalKit is intentionally separate from AuraOne's hosted SDKs.

## Local Open-Source EvalKit

- Distribution package: `auraone-evalkit`
- Import package: `auraone_evalkit`
- CLI binary: `evalkit`
- Runtime posture: local files only
- Auth posture: no AuraOne account, API key, hosted tenant, Prisma database, or production service
- v0.1 scope: rubric schema validation, rubric linting, deterministic scoring, and synthetic tutorial fixtures

EvalKit exists so teams can inspect and run evaluation workflow tools without sending private eval material to AuraOne or any hosted service.

## Hosted AuraOne SDKs

- Hosted Python SDK: `auraone-sdk`
- Hosted TypeScript SDK: `@auraone/sdk`
- Hosted API CLI: `aura`
- Runtime posture: hosted AuraOne APIs and account-specific workflows

These packages are for AuraOne platform integrations. They are not required for EvalKit quickstarts and should not be installed just to validate, lint, or score local rubric files.

## Why They Are Separate

Private evals often need public standards but not public data. The local package keeps schemas, checks, and deterministic aggregation inspectable. The hosted SDKs remain focused on authenticated AuraOne product workflows.

This separation also prevents namespace confusion:

- `evalkit validate-rubric` validates local rubric files.
- `evalkit lint-rubric` checks local authoring quality.
- `evalkit score` aggregates local labels and outputs.
- `aura` remains the hosted API CLI and is not used by EvalKit.

## Data Boundary

EvalKit v0.1 examples are synthetic tutorial data only. They are not expert-authored, not human-validated, not benchmark-grade, and not safety or quality certifications. The tutorial files exist to make commands runnable and tests deterministic.
