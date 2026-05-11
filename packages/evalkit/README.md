# AuraOne EvalKit

AuraOne EvalKit is a standalone local Python package for rubric validation, rubric linting, and deterministic scoring. It installs as `auraone-evalkit`, imports as `auraone_evalkit`, and exposes the `evalkit` CLI.

EvalKit does not require an AuraOne account, API key, hosted tenant, database, or private reviewer pool. The files in `examples/tutorial/` are synthetic tutorial data only. They are not expert-authored, human-validated, benchmark-grade, safety certifications, or claims about model quality.

## Package Distinction

AuraOne has separate hosted SDKs:

| Tool | Package or binary | Purpose |
| --- | --- | --- |
| EvalKit | `auraone-evalkit`, `auraone_evalkit`, `evalkit` | Local open-source rubric tools. No API key. |
| Hosted Python SDK | `auraone-sdk` | Hosted AuraOne API client. Uses hosted services. |
| Hosted TypeScript SDK | `@auraone/sdk` | Hosted AuraOne API client for Node/TypeScript. Uses hosted services. |
| Hosted API CLI | `aura` | Hosted AuraOne command line workflows. Separate from `evalkit`. |

Use `evalkit` for local files and tutorial workflows. Use `auraone-sdk`, `@auraone/sdk`, or `aura` only when you intend to call hosted AuraOne services.

## Install

From this repository:

```bash
cd opensource/evalkit
python -m pip install -e .
```

After install:

```bash
evalkit --help
evalkit --version
```

## Five-Minute Quickstart

Validate the synthetic tutorial rubric:

```bash
evalkit validate-rubric examples/tutorial/rubric.jsonl
```

Lint the same rubric:

```bash
evalkit lint-rubric examples/tutorial/rubric.jsonl
```

Score the synthetic tutorial model outputs. If `--labels` is omitted, EvalKit looks for `labels.jsonl` next to the responses file.

```bash
evalkit score \
  --rubric examples/tutorial/rubric.jsonl \
  --responses examples/tutorial/model_outputs.jsonl \
  --out /tmp/evalkit-tutorial-scores.json
```

Expected summary for the bundled tutorial data:

```json
{
  "average_score": 0.645833,
  "pass_rate": 0.666667,
  "scored_outputs": 3
}
```

The full deterministic expected output is stored in `examples/tutorial/expected_scores.json`.

## Commands

### `evalkit validate-rubric`

Validates JSONL or JSON-array rubric files against the AuraOne EvalKit rubric contract.

```bash
evalkit validate-rubric examples/tutorial/rubric.jsonl --format json
```

Validation errors include row number, field, message, and a suggested fix.

### `evalkit lint-rubric`

Runs rubric quality checks that catch common authoring problems before scoring.

```bash
evalkit lint-rubric examples/tutorial/rubric.jsonl --format json
```

The v0.1 linter includes rules for compound criteria, vague wording, missing examples, missing weight, duplicate IDs, duplicate text, inconsistent severity, unscorable language, unavailable context, unclear scoring boundaries, and weight totals.

### `evalkit score`

Aggregates per-criterion labels into deterministic weighted scores.

```bash
evalkit score \
  --rubric examples/tutorial/rubric.jsonl \
  --responses examples/tutorial/model_outputs.jsonl \
  --labels examples/tutorial/labels.jsonl \
  --format json \
  --out /tmp/evalkit-tutorial-scores.json
```

Supported output formats are `json`, `jsonl`, `csv`, and `report-json`.

## Data Contracts

Rubric rows are JSON objects with required fields:

- `criterion_id`
- `domain`
- `task_type`
- `criterion`
- `weight`
- `severity`
- `scoring_type`
- `examples`
- `edge_cases`
- `disagreement_risk`

See `docs/schema/rubric-schema.md` for the full schema and examples.

Scoring labels use:

- `output_id`
- `criterion_id`
- `score`
- optional `applicable`
- optional `rationale`

Scores are normalized by scoring type, multiplied by criterion weight, and divided by the applicable rubric weight. Missing labels are reported in every output record. In `--strict` mode, missing labels fail the command.

## Documentation

- `docs/architecture/two-package-architecture.md`
- `docs/schema/rubric-schema.md`
- Repository roadmap context: `../../opensource.md`
- Public AuraOne open resources: `https://auraone.ai/open`

## Limitations

- v0.1 ships local tooling and synthetic tutorial fixtures only.
- The tutorial data is not a benchmark and should not be used to compare vendors or publish model claims.
- The linter is a deterministic authoring aid, not a replacement for domain review.
- The scorer aggregates labels supplied by the user. It does not generate labels, call LLM judges, or contact AuraOne hosted services.

## Development

Run focused checks from `opensource/evalkit`:

```bash
python -m pytest tests/test_package_imports.py tests/schema/test_rubric_schema.py tests/scoring/test_score_cli.py tests/linting/test_rules.py tests/examples/test_tutorial_dataset.py
python -m pip wheel . --no-deps -w /tmp/evalkit-wheel
```
