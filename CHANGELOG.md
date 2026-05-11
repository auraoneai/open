# Changelog

All notable changes to AuraOne Open are documented here. This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-05-11

### Fixed

- Packaging: include `auraone_evalkit/reports/` subpackage in the wheel. The 0.1.0 wheel shipped without it because a stray `reports/` entry in `.gitignore` (intended for local eval output) also matched the source subpackage and excluded it from the repo, so `evalkit report` and any import of `auraone_evalkit.reports` failed on a fresh install.
- Packaging: include `reports/templates/*.j2` as package data so the report renderer can find its Jinja templates.

## [0.1.0] - 2026-05-11

Initial public release.

### EvalKit (`auraone-evalkit`)

- `auraone-evalkit` Python package with the `evalkit` CLI.
- Rubric authoring: schema, `validate-rubric`, `lint-rubric`, `diff-rubric`.
- Scoring: deterministic local `score` against a rubric and a JSONL of model responses.
- Reporting: `report` to produce an eval run report in Markdown.
- Judge calibration: `judge-calibrate` against reference labels.
- Reviewer agreement: `agreement` for pairwise and pool-level agreement.
- Drift: `drift` to detect shifts in reviewer pools across windows.
- Leakage audit: `leakage-check` for n-gram overlap between eval data and reference corpora.
- Sampling: `sample` for reproducible model output sampling.
- Weight calibration: `weight-calibrate` from per-criterion outcomes.
- Dataset cards: `card init` scaffolds a `README.md` from a metadata file.
- Synthetic multi-turn tutorial dataset, rubric tutorial dataset.
- Adapter notes for Inspect AI and the EleutherAI LM Eval Harness.
- 58 unit tests covering CLI, schema, scoring, agreement, drift, and leakage.

### Robotics ReviewKit

- Teleop review schema, intervention ontology, and failure-mode taxonomy.
- Episode validator (`cli/validate_episode.py`).
- LeRobot exporter (`cli/export_lerobot.py`).
- RLDS / OpenX exporter (`cli/export_rlds.py`).
- Static reviewer viewer (`viewer/reviewkit.html`).
- Mock example episode and dataset card (clearly marked synthetic).
- Sensor QA checklist, teleop task library, robotics dataset card template.
- 26 unit tests covering schema, exporters, and viewer smoke.

### Buying Toolkit

- Human-data SOW, SLA, RFP, and pilot design templates.
- Vendor comparison checklist, expert reviewer certification template.
- Eval data readiness checklist.
- Human data program playbook.

### Writing

- "Measuring the Human Judgment Layer" thesis post.
- "Frontier Models Are Becoming Eval-Quality-Limited" landing excerpt.

### Documentation

- 43-PRD source-to-v0.1.0 audit trail in `docs/PRD/`.

### Notes

- No real customer data, no real reviewer data, no real robotics teleop data.
- Tutorial datasets are synthetic and disclosed as such in their dataset cards.
- This is a methodology and tooling release, not a benchmark.
