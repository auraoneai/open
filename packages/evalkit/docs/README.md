# AuraOne EvalKit Documentation

Technical guides for building local AI and LLM evaluation workflows around
rubric quality, supplied labels, reviewer QA, saved judge outputs, dataset
integrity, and evidence reports.

These docs are for evaluation engineers, ML platform teams, annotation leads,
and researchers working with files they own. EvalKit runs locally and does not
require an AuraOne account, API key, hosted tenant, or database.

## Start By Job

| Job | Guide | Command |
| --- | --- | --- |
| Define and validate an evaluation rubric | [Rubric schema](schema/rubric-schema.md) | `evalkit validate-rubric` |
| Improve criterion quality before review | [Rubric linter](lint/rubric-linter.md) and [criterion checklist](checklists/criterion-quality-checklist.md) | `evalkit lint-rubric` |
| Score saved outputs from supplied labels | [EvalKit scoring guide](../README.md#evalkit-score) | `evalkit score` |
| Produce an offline evidence artifact | [Reports overview](reports/README.md) and [v1 report contract](reports.md) | `evalkit report` |
| Measure reviewer consistency | [Reviewer agreement](agreement/README.md) | `evalkit agreement` |
| Audit saved LLM-judge outputs | [Judge calibration](judge/README.md) | `evalkit judge-calibrate` |
| Detect reviewer or criterion changes | [Reviewer drift](drift/README.md) | `evalkit drift` |
| Test score sensitivity to rubric weights | [Weight calibration](calibration/README.md) | `evalkit weight-calibrate` |
| Find duplicate or near-duplicate eval items | [Leakage audit](leakage/README.md) | `evalkit leakage-check` |
| Select outputs for deeper human review | [Sampling](sampling/README.md) | `evalkit sample` |
| Review rubric changes across versions | [Rubric versioning](versioning/README.md) | `evalkit diff-rubric` |
| Document eval or robotics data | [Dataset cards](cards/README.md) | `evalkit card init` |
| Map data toward evaluation frameworks | [Adapters](adapters/README.md) | Adapter-specific Python APIs |

## Architecture And Methodology

- [Two-package architecture](architecture/two-package-architecture.md)
- [EvalKit technical methodology](methodology/evalkit-technical-methodology.md)
- [Human-data failure modes](catalogs/human-data-failure-modes.md)
- [Multi-turn evaluation template pack](templates/multi-turn-eval-template-pack.md)
- [Evaluation run report template](templates/eval-run-report-template.md)
- [Evaluation dataset card template](templates/eval-dataset-card-template.md)

## Runtime And Data Boundary

- Commands operate on local JSON, JSONL, CSV, YAML, or Markdown inputs as
  documented by each workflow.
- Scoring uses labels supplied by the caller; it does not run model inference
  or create labels.
- Judge calibration reads saved judge outputs and does not call a model
  provider.
- Leakage checks compare local inputs and optional local references only.
- Generated HTML reports are self-contained and load no remote runtime assets.
- Bundled examples are synthetic fixtures, not benchmarks or customer data.

## Proof And Next Action

Run the synthetic tutorial first, then replace one input at a time with files
from your own evaluation:

```bash
cd packages/evalkit
python -m pip install -e ".[dev]"
evalkit validate-rubric examples/tutorial/rubric.jsonl
evalkit score \
  --rubric examples/tutorial/rubric.jsonl \
  --responses examples/tutorial/model_outputs.jsonl \
  --labels examples/tutorial/labels.jsonl \
  --out /tmp/evalkit-scores.json
python -m pytest -p no:cacheprovider -q tests
```

See the [package README](../README.md) for installation, the full command map,
scope boundaries, and release artifact verification.

## AuraOne Links

- [AuraOne Open product overview](https://auraone.ai/open)
- [AuraOne Open source](https://github.com/auraoneai/open)
- [Robotics ReviewKit](../../../robotics-reviewkit/)
