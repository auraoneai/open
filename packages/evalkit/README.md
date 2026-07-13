# AuraOne EvalKit

A local-first Python CLI for AI and LLM evaluation teams that need to turn
evaluation rubrics, saved model outputs, and supplied human or judge labels
into inspectable scores, QA diagnostics, and evidence reports.

[![PyPI version](https://img.shields.io/pypi/v/auraone-evalkit.svg)](https://pypi.org/project/auraone-evalkit/)
[![Python versions](https://img.shields.io/pypi/pyversions/auraone-evalkit.svg)](https://pypi.org/project/auraone-evalkit/)
[![license](https://img.shields.io/pypi/l/auraone-evalkit.svg)](https://github.com/auraoneai/open/blob/main/LICENSE)
[![CI](https://github.com/auraoneai/open/actions/workflows/ci.yml/badge.svg)](https://github.com/auraoneai/open/actions/workflows/ci.yml)

[AuraOne Open](https://auraone.ai/open) |
[Documentation](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs) |
[Source](https://github.com/auraoneai/open/tree/main/packages/evalkit) |
[Robotics ReviewKit](https://github.com/auraoneai/open/tree/main/robotics-reviewkit)

EvalKit covers the judgment layer around an evaluation run: rubric contracts,
deterministic aggregation of labels you already own, reviewer and LLM-judge
quality signals, dataset leakage checks, sampling, rubric versioning, dataset
cards, and report generation. It does not run models, generate labels, manage a
review workforce, or require a hosted AuraOne account.

## Who It Is For

- Evaluation engineers building file-based AI or LLM evaluation pipelines.
- ML platform and model-quality teams adding rubric checks and score evidence
  to CI or release reviews.
- Human-evaluation and annotation leads measuring reviewer agreement,
  adjudication, drift, and calibration needs.
- Teams auditing saved LLM-judge outputs without calling a model provider
  during analysis.
- Researchers and developers who want versionable rubric, label, and report
  artifacts instead of a platform-only data model.

## What EvalKit Does

| Workflow | Command | Result |
| --- | --- | --- |
| Rubric schema validation | `evalkit validate-rubric` | Structured issues with paths, row numbers, and suggested fixes |
| Rubric quality linting | `evalkit lint-rubric` | Deterministic findings for vague, compound, duplicated, incomplete, or unscorable criteria |
| Label-based model scoring | `evalkit score` | Weighted per-output scores, pass/fail status, missing-label diagnostics, and run summary |
| Evidence reporting | `evalkit report` | Markdown, self-contained HTML, or normalized `auraone.evalkit.report.v1` JSON |
| Reviewer agreement | `evalkit agreement` | Percent agreement, Krippendorff alpha, applicable kappa metrics, adjudication rate, and breakdowns |
| Saved judge calibration | `evalkit judge-calibrate` | Pairwise agreement, criterion disagreement, judge variance, prompt sensitivity, and unstable criteria |
| Reviewer or criterion drift | `evalkit drift` | Batch-to-batch drift and instability findings |
| Local leakage checks | `evalkit leakage-check` | Exact and near-duplicate evidence over local inputs and optional local references |
| Review sampling | `evalkit sample` | Deterministic random, stratified, diversity, failure, disagreement, uncertainty, or regression samples |
| Rubric change review | `evalkit diff-rubric` | Cosmetic, added, removed, rename-candidate, and scoring-impact changes |
| Weight sensitivity | `evalkit weight-calibrate` | Scenario rankings and high-leverage rubric criteria |
| Dataset documentation | `evalkit card init` | Eval or robotics dataset-card Markdown with visible data-status disclosure |

## Why EvalKit

- **Rubrics remain reviewable contracts.** EvalKit accepts JSONL, JSON arrays,
  and canonical `rubric-spec` objects that can be diffed and versioned in git.
- **Scoring is explicit and deterministic.** The scorer aggregates labels you
  provide. It does not create hidden judge labels or contact hosted services.
- **QA signals share one local CLI.** Agreement, judge calibration, drift,
  leakage, sampling, versioning, and reports operate on files rather than a
  required tenant or database.
- **Evidence is portable.** Outputs include structured JSON/JSONL plus
  human-readable CSV, Markdown, and self-contained HTML where supported.
- **Boundaries are visible.** Synthetic fixtures, omitted evidence, missing
  labels, and limitations are surfaced instead of being converted into
  validation or benchmark claims.

## Install

EvalKit requires Python 3.10 or newer. Repository CI covers Python 3.10, 3.11,
and 3.12.

Install the latest published release from PyPI:

```bash
python -m pip install --upgrade auraone-evalkit
```

The repository can contain changes that have not been published yet. To run
the current checkout from the AuraOne Open repository root:

```bash
python -m pip install -e "./packages/evalkit"
```

For development and package verification:

```bash
python -m pip install -e "./packages/evalkit[dev]"
```

## Quickstart

The commands below assume an editable source install from the repository root.
They use synthetic tutorial files included in this checkout.

```bash
evalkit validate-rubric \
  packages/evalkit/examples/tutorial/rubric.jsonl

evalkit lint-rubric \
  packages/evalkit/examples/tutorial/rubric.jsonl

evalkit score \
  --rubric packages/evalkit/examples/tutorial/rubric.jsonl \
  --responses packages/evalkit/examples/tutorial/model_outputs.jsonl \
  --labels packages/evalkit/examples/tutorial/labels.jsonl \
  --format json \
  --out /tmp/evalkit-tutorial-scores.json

evalkit report \
  --input packages/evalkit/examples/reports/tutorial_input.json \
  --out /tmp/evalkit-tutorial-report.html
```

The scoring output contains per-output weighted scores, pass/fail status,
missing-label diagnostics, average score, and pass rate. The HTML report is a
single offline file with explicit decisions, gates, findings, evidence,
reproduction metadata, limitations, and omitted evidence.

## Core Command Details

### `evalkit validate-rubric`

Validates EvalKit JSONL or JSON-array rubric files and canonical `rubric-spec`
v1 JSON objects.

```bash
evalkit validate-rubric rubric.jsonl --format json
```

Output formats are `text`, `json`, and `jsonl`.

### `evalkit lint-rubric`

Runs deterministic rubric-authoring checks before labels or scores depend on a
criterion.

```bash
evalkit lint-rubric rubric.jsonl --format json --fail-on warning
```

Rules cover compound criteria, vague wording, missing examples, missing
weights, duplicate IDs or text, inconsistent severity, unscorable language,
unavailable context, unclear scoring boundaries, and weight totals. Rules can
be disabled explicitly with repeated `--disable-rule` arguments.

### `evalkit score`

Aggregates supplied per-criterion labels into normalized weighted scores.

```bash
evalkit score \
  --rubric rubric.jsonl \
  --responses outputs.jsonl \
  --labels labels.jsonl \
  --pass-threshold 0.75 \
  --format json \
  --out scores.json
```

Output formats are `json`, `jsonl`, `csv`, and `report-json`. In `--strict`
mode, any missing criterion label fails the command.

### `evalkit report`

Renders a score payload or report input as Markdown, self-contained HTML, or
the normalized `auraone.evalkit.report.v1` JSON contract.

```bash
evalkit report \
  --input report-input.json \
  --out report.html
```

The output suffix selects the format; `--format markdown|html|json` overrides
it. HTML reports contain embedded CSS, no JavaScript, and no remote assets.
They separate identity, summary, quality gates, findings, evidence,
reproduction metadata, limitations, and omitted evidence.

### QA And Dataset Workflows

From `packages/evalkit/` in a source checkout:

```bash
evalkit agreement examples/quality/agreement/tutorial_labels.jsonl
evalkit judge-calibrate examples/quality/judge/tutorial_judge_outputs.jsonl
evalkit drift examples/quality/drift/tutorial_batches.jsonl
evalkit leakage-check examples/quality/leakage/tutorial_prompts.jsonl
evalkit sample examples/quality/sampling/model_outputs.jsonl --strategy random --n 10
evalkit diff-rubric examples/quality/versioning/rubric_v1.jsonl examples/quality/versioning/rubric_v2.jsonl
evalkit weight-calibrate examples/quality/calibration/rubric_weight_scenarios.json
```

Agreement, judge calibration, drift, leakage, and weight calibration support
`--format text|json|jsonl`. Sampling supports `json` and `jsonl`. Use
`--no-color` anywhere in the command, or set the standard `NO_COLOR`
environment variable, to disable ANSI styling in human-readable output.

Run `evalkit --help` or `evalkit <command> --help` for the authoritative command
surface.

## Data Contracts

Rubric rows require:

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

See the
[rubric schema documentation](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/schema/rubric-schema.md)
for field definitions and examples.

Scoring labels require:

- `output_id`
- `criterion_id`
- `score`

Labels can also provide `applicable` and `rationale`. Scores are normalized by
scoring type, multiplied by criterion weight, and divided by applicable rubric
weight. Missing labels remain visible in each output record.

## Runtime And Data Boundary

- Core commands run in the local Python process over file paths supplied by the
  user.
- No AuraOne account, API key, tenant, database, or private reviewer pool is
  required.
- `score` aggregates existing labels; it does not run inference or create
  labels.
- `judge-calibrate` analyzes saved judge outputs; it does not call OpenAI,
  AuraOne, or another model provider.
- `leakage-check` compares local items and optional local reference corpora. It
  does not perform web search or prove the absence of contamination.
- HTML reports are generated locally and contain no remote runtime assets.
- Tutorial datasets and examples are synthetic. They are not expert-authored,
  human-validated, benchmark-grade, safety-certified, or suitable for model
  leaderboard claims.

## Scope And Limitations

EvalKit is not a replacement for:

- A model runner or public benchmark harness that executes standard tasks.
- A hosted annotation platform with workforce management and task assignment.
- Domain-expert validation of rubric meaning or release criteria.
- A statistical guarantee that a reviewer, judge, dataset, or model is safe or
  production-ready.
- A contamination search across the public web or private corpora that were not
  supplied as input.

Use EvalKit when the job is to make the judgment artifacts around an eval run
more inspectable, repeatable, and reviewable.

## Proof And Verification

The repository includes synthetic fixtures, command tests, package metadata
checks, deterministic report tests, and wheel/sdist content verification.

```bash
cd packages/evalkit
python -m pip install -e ".[dev]"
python -m pytest -p no:cacheprovider -q tests
python -m build
python scripts/verify_release.py dist
```

Package verification checks version alignment, required report templates and
schemas, the Jinja2 runtime dependency, expected wheel/sdist contents, and the
absence of private font files. Passing these checks validates the local build;
it does not prove that a registry publication has occurred.

## Documentation

- [Documentation index](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs)
- [Rubric schema](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/schema/rubric-schema.md)
- [Rubric linter](https://github.com/auraoneai/open/blob/main/packages/evalkit/docs/lint/rubric-linter.md)
- [Reviewer agreement](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/agreement)
- [Judge calibration](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/judge)
- [Reviewer drift](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/drift)
- [Leakage audit](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/leakage)
- [Sampling](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/sampling)
- [Rubric versioning](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/versioning)
- [Evidence reports](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/reports)
- [Dataset cards](https://github.com/auraoneai/open/tree/main/packages/evalkit/docs/cards)
- [Tutorial files](https://github.com/auraoneai/open/tree/main/packages/evalkit/examples/tutorial)

## Next Actions

1. Install the published package or the current source checkout.
2. Run `validate-rubric` and `lint-rubric` on one real rubric before scoring.
3. Score a saved output set with labels you already own.
4. Add agreement, drift, leakage, or judge-calibration evidence where the
   release decision depends on those signals.
5. Generate a self-contained report and store it with the evaluated inputs and
   source revision.

## Contributing

Issues and focused pull requests are welcome. See the repository
[contributing guide](https://github.com/auraoneai/open/blob/main/CONTRIBUTING.md),
[security policy](https://github.com/auraoneai/open/blob/main/SECURITY.md), and
[AuraOne Open changelog](https://github.com/auraoneai/open/blob/main/CHANGELOG.md).

## License

MIT. See the repository
[LICENSE](https://github.com/auraoneai/open/blob/main/LICENSE).
