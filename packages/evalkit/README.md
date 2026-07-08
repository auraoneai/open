# AuraOne EvalKit

A local Python CLI for turning AI evaluation rubrics, model outputs, and reviewer labels into validated, scored, auditable eval results.

[![PyPI version](https://img.shields.io/pypi/v/auraone-evalkit.svg)](https://pypi.org/project/auraone-evalkit/)
[![Python versions](https://img.shields.io/pypi/pyversions/auraone-evalkit.svg)](https://pypi.org/project/auraone-evalkit/)
[![license](https://img.shields.io/pypi/l/auraone-evalkit.svg)](https://github.com/auraoneai/open/blob/main/LICENSE)
[![CI](https://github.com/auraoneai/open/actions/workflows/ci.yml/badge.svg)](https://github.com/auraoneai/open/actions/workflows/ci.yml)

- Validate rubric files before they become production eval contracts.
- Lint criteria for vague wording, compound checks, missing examples, and weight problems.
- Score model outputs from local labels with deterministic JSON, JSONL, CSV, or report-ready output.
- Audit reviewer agreement, judge calibration, drift, leakage risk, sampling, and rubric diffs without an API key.

## Install

```bash
pip install auraone-evalkit
```

Requires Python 3.10 or newer.

## Quickstart

Create one rubric, two model outputs, two labels, then score them locally:

```bash
mkdir -p /tmp/evalkit-demo

cat > /tmp/evalkit-demo/rubric.jsonl <<'JSONL'
{"criterion_id":"helpfulness","domain":"support","task_type":"answer_quality","criterion":"Answer resolves the user's request with a concrete next step.","weight":1.0,"severity":"warning","scoring_type":"scale_0_1","examples":[{"positive":"Names the fix and the next command to run.","negative":"Gives a vague reassurance."}],"edge_cases":["partial answers"],"disagreement_risk":{"level":"low","notes":"The expected next step is visible in the answer."}}
JSONL

cat > /tmp/evalkit-demo/responses.jsonl <<'JSONL'
{"output_id":"answer-1","output":"Restart the worker, then run the health check to confirm jobs drain."}
{"output_id":"answer-2","output":"Looks fine to me."}
JSONL

cat > /tmp/evalkit-demo/labels.jsonl <<'JSONL'
{"output_id":"answer-1","criterion_id":"helpfulness","score":1.0}
{"output_id":"answer-2","criterion_id":"helpfulness","score":0.25}
JSONL

evalkit validate-rubric /tmp/evalkit-demo/rubric.jsonl
evalkit score \
  --rubric /tmp/evalkit-demo/rubric.jsonl \
  --responses /tmp/evalkit-demo/responses.jsonl \
  --labels /tmp/evalkit-demo/labels.jsonl \
  --format json
```

The score output includes per-output scores, pass/fail status, missing-label diagnostics, and a summary with average score and pass rate.

## What You Can Build

- CI checks that reject malformed or low-quality rubric changes before an eval run starts.
- Offline eval scoring jobs for saved model outputs and human-supplied labels.
- Reviewer agreement reports for annotation QA and calibration review.
- Rubric diffs that separate wording edits from scoring-impact changes.
- Leakage, drift, sampling, judge-calibration, and dataset-card workflows for eval operations.

## Why AuraOne EvalKit?

- **Rubric files stay inspectable.** EvalKit works with JSONL or JSON-array rubrics that can be reviewed, diffed, and versioned in git.
- **Scoring is deterministic.** The `score` command aggregates labels you provide; it does not call hosted services or generate hidden judge labels.
- **Authoring feedback is immediate.** `validate-rubric` catches schema issues, while `lint-rubric` catches common criterion-quality problems before reviewers see the rubric.
- **QA workflows share one CLI.** Agreement, drift, leakage, sampling, reports, dataset cards, and rubric diffs use the same local `evalkit` entry point.

## Compared To Adjacent Tools

EvalKit is not a replacement for experiment trackers, hosted annotation platforms, or full benchmark harnesses. It focuses on the local judgment layer around rubrics, labels, and review QA.

| Need | AuraOne EvalKit | Adjacent tools |
| --- | --- | --- |
| Validate and lint rubric contracts | Built-in CLI commands for rubric structure and criterion quality | Often handled with custom scripts or platform-specific schemas |
| Score saved outputs from reviewer labels | Deterministic local scoring with JSON, JSONL, CSV, and report JSON output | Evaluation harnesses often focus on model execution and benchmark tasks |
| Analyze reviewer quality signals | Agreement, drift, leakage, judge calibration, and sampling commands live in one package | Annotation platforms may provide dashboards but are not usually local-first |
| Run without a hosted account | No AuraOne API key, tenant, database, or network call is required for core commands | Hosted platforms usually require service credentials |

Use a benchmark harness instead if you need to run standard public benchmark tasks end to end. Use an annotation platform instead if you need workforce management, task assignment, or hosted review UI.

## Commands

### `evalkit validate-rubric`

Validates EvalKit JSONL or JSON-array rubric files, and accepts canonical `rubric-spec` v1 JSON objects as input.

```bash
evalkit validate-rubric examples/tutorial/rubric.jsonl --format json
```

Validation errors include row number, field, message, and a suggested fix.

### `evalkit lint-rubric`

Runs deterministic rubric quality checks that catch common authoring problems before scoring.

```bash
evalkit lint-rubric examples/tutorial/rubric.jsonl --format json
```

The linter includes rules for compound criteria, vague wording, missing examples, missing weight, duplicate IDs, duplicate text, inconsistent severity, unscorable language, unavailable context, unclear scoring boundaries, and weight totals.

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

### More CLI Workflows

From a source checkout, try the bundled examples:

```bash
evalkit agreement examples/quality/agreement/tutorial_labels.jsonl
evalkit drift examples/quality/drift/tutorial_batches.jsonl
evalkit leakage-check examples/quality/leakage/tutorial_prompts.jsonl
evalkit sample examples/quality/sampling/model_outputs.jsonl --strategy random --count 10
evalkit diff-rubric examples/quality/versioning/rubric_v1.jsonl examples/quality/versioning/rubric_v2.jsonl
```

Run `evalkit --help` or `evalkit <command> --help` for the full command reference.

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

See the [rubric schema docs](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/schema/rubric-schema.md) for the full schema and examples.

Scoring labels use:

- `output_id`
- `criterion_id`
- `score`
- optional `applicable`
- optional `rationale`

Scores are normalized by scoring type, multiplied by criterion weight, and divided by the applicable rubric weight. Missing labels are reported in every output record. In `--strict` mode, missing labels fail the command.

## Examples And Docs

- Tutorial data: [`examples/tutorial/`](https://github.com/auraoneai/open/tree/main/packages/evalkit/examples/tutorial)
- Rubric schema docs: [`docs/schema/rubric-schema.md`](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/schema/rubric-schema.md)
- Agreement docs: [`docs/agreement/README.md`](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/agreement/README.md)
- Drift docs: [`docs/drift/README.md`](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/drift/README.md)
- Leakage audit docs: [`docs/leakage-audit.md`](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/leakage-audit.md)
- Reports docs: [`docs/reports.md`](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/reports.md)
- Dataset card docs: [`docs/cards/README.md`](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/cards/README.md)

## Compatibility And Limitations

- Requires Python 3.10 or newer.
- EvalKit runs locally and does not require an AuraOne account, API key, hosted tenant, database, or private reviewer pool.
- Tutorial data and bundled examples are synthetic. They are not expert-authored benchmarks and should not be used to publish model-quality claims.
- The scorer aggregates labels supplied by the user. It does not generate labels, call LLM judges, or contact AuraOne hosted services.
- The linter is a deterministic authoring aid, not a replacement for domain review.
- `auraone-evalkit` is the local open-source package. Use [`auraone-sdk`](https://pypi.org/project/auraone-sdk/) or [`@auraone/sdk`](https://www.npmjs.com/package/@auraone/sdk) only when you intend to call hosted AuraOne APIs.

## Related AuraOne OSS Projects

EvalKit is part of the broader AuraOne open-source evaluation stack:

| Project | Purpose |
| --- | --- |
| [`rubric-spec`](https://github.com/auraoneai/rubric-spec) | Portable rubric schema, validator, linter, diff, and framework adapters. |
| [`iaa-kit`](https://github.com/auraoneai/iaa-kit) | Inter-annotator agreement metrics with bootstrap intervals and skew-aware statistics. |
| [`judge-bench`](https://github.com/auraoneai/judge-bench) | Diagnostic probes for judge-model bias, calibration, and stability. |
| [`eval-adapter`](https://github.com/auraoneai/eval-adapter) | Shared run config and result normalization across evaluation frameworks. |
| [`judge-card`](https://github.com/auraoneai/judge-card) | Disclosure card schema, generator, renderer, and validator for judge models. |
| [`datasheet-ci`](https://github.com/auraoneai/datasheet-ci) | GitHub Action and Python validator for dataset/model/data-card documentation. |
| [`contamination-audit`](https://github.com/auraoneai/contamination-audit) | Synthetic-safe contamination detectors and reproducible audit reports. |
| [`evalkit-action`](https://github.com/auraoneai/evalkit-action) | EvalKit scoring and reporting in pull-request CI. |
| [`robotics-reviewkit`](https://github.com/auraoneai/open/tree/main/robotics-reviewkit) | VLA review anchors, event streams, analyzers, exporters, and React viewer. |

## Development

```bash
cd packages/evalkit
python -m pip install -e ".[dev]"
python -m pytest -q tests
python -m build
```

## Contributing

Issues and focused pull requests are welcome. See the repository-level [contributing guide](https://github.com/auraoneai/open/blob/main/CONTRIBUTING.md), [security policy](https://github.com/auraoneai/open/blob/main/SECURITY.md), and [changelog](https://github.com/auraoneai/open/blob/main/CHANGELOG.md).

## License

MIT. See the repository [LICENSE](https://github.com/auraoneai/open/blob/main/LICENSE).
