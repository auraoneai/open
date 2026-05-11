# AuraOne Open Source Live Readiness Audit - 2026-05-10

## Verdict

- **Source readiness:** pass. The repository now contains the code, docs, examples, tests, website source, and launch-surface source required by the 43 PRDs.
- **External live status:** not published by this audit. No production deploy, PyPI publish, Hugging Face upload, GitHub release, or Hugging Face Space deployment was performed. Those are externally visible actions and require explicit release authorization.
- **Market statement readiness:** defensible after deployment/publish authorization. From the repo state, the source is ready to support the statement: AuraOne Open Source is ready to launch.

## What Changed During This Second Audit

- Found and fixed one concrete PRD mismatch: PRD 12 required `evalkit card init --type eval --metadata examples/cards/eval/meta.yaml` to create `README.md`, but the main CLI previously required `--out`.
- Updated `opensource/evalkit/src/auraone_evalkit/cli/__init__.py` so `evalkit card init` defaults to `README.md`.
- Added `test_cli_card_init_defaults_to_readme` in `opensource/evalkit/tests/test_evalkit_cli.py` to lock the exact PRD command behavior.

## Audit Scope

- PRD files audited: 43
- PRD checklist rows counted: 1627
- Relevant file/path references extracted from PRD checklists: 196
- Missing relevant file/path references after compatibility mapping and exact-path reconciliation: 0
- Master ledger status: 43 checked
- Completion audit status rows: 1627 complete, 0 pending, 0 blocked

## Validation Evidence

### EvalKit

- `cd opensource/evalkit && python -m pip install -e .` passed.
- `cd opensource/evalkit && python -m pip wheel . --no-deps -w /tmp/evalkit-live-audit-wheel` produced a wheel.
- `cd opensource/evalkit && python -m build` passed with no matched setuptools/deprecation/package warning in `/tmp/evalkit-live-build.log`.
- `PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=src python -m pytest -p no:cacheprovider -q tests` passed: 58 tests.
- Exact PRD command now passes: `evalkit card init --type eval --metadata examples/cards/eval/meta.yaml` creates `README.md`.
- CLI matrix passed: `validate-rubric`, `lint-rubric`, `score`, `report`, `card init`, `judge-calibrate`, `agreement`, `drift`, `diff-rubric`, `leakage-check`, `sample`, `weight-calibrate`.
- Tutorial datasets validate and score locally without AuraOne API keys.

### Robotics ReviewKit

- `cd opensource/robotics-reviewkit && PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -p no:cacheprovider -q tests` passed: 26 tests.
- `python cli/validate_episode.py examples/mock_episode.json` passed.
- `python cli/export_lerobot.py examples/mock_episode.json /tmp/robotics-live-lerobot.json` passed.
- `python cli/export_rlds.py examples/mock_episode.json /tmp/robotics-live-rlds.json` passed.
- `PYTHONPATH=src python tests/viewer_smoke.py` passed.
- Exact compatibility paths exist: `src/exporters/lerobot.py`, `src/exporters/rlds.py`, `src/exporters/openx.py`.

### Website And Public Launch Surface

- `cd auraone-website && npx tsc --noEmit --incremental false` passed.
- `cd auraone-website && npm run build` passed and listed `/open` and `/resources` as static routes.
- Browser QA passed for `/open`, `/resources#buying-toolkit`, and `opensource/robotics-reviewkit/viewer/reviewkit.html`.
- Screenshots from the final audit are stored at `/tmp/audit-open.png`, `/tmp/audit-resources-buying.png`, and `/tmp/audit-robotics-viewer.png`.

## PRD-by-PRD Result

| PRD | Title | Surface | Audit result | Evidence |
| --- | --- | --- | --- | --- |
| 01 | PRD 01: AuraOne Eval SDK | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 02 | PRD 02: AuraOne Rubric Schema | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 03 | PRD 03: Scoring CLI | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 04 | PRD 04: Rubric Linter | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 05 | PRD 05: LLM Judge Calibration Toolkit | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 06 | PRD 06: Reviewer Agreement Library | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 07 | PRD 07: Reviewer Drift Detector | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 08 | PRD 08: Synthetic Multi-Turn Eval Dataset | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 09 | PRD 09: Inspect AI Adapter | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 10 | PRD 10: LM Eval Harness Adapter | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 11 | PRD 11: Eval Report Generator | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 12 | PRD 12: Dataset Card Generator | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 13 | PRD 13: Methodology Paper / Technical Memo | EvalKit docs/templates | pass | methodology docs present; website/resource boundary checked |
| 14 | PRD 14: Benchmark Saturation / Eval Quality Memo | EvalKit docs/templates | pass | thesis writing docs present; website/resource boundary checked |
| 15 | PRD 15: Rubric Tutorial Dataset | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 16 | PRD 16: Rubric Versioning Tool | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 17 | PRD 17: Eval Leakage Audit Tool | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 18 | PRD 18: Model Output Sampling Tool | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 19 | PRD 19: Rubric Weight Calibration Notebook | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 20 | PRD 20: Criterion Quality Checklist | EvalKit docs/templates | pass | docs/opensource and opensource/evalkit docs present; website/resource boundary checked |
| 21 | PRD 21: Dataset Card Template For Eval Data | EvalKit docs/templates | pass | docs/opensource and opensource/evalkit docs present; website/resource boundary checked |
| 22 | PRD 22: Human Data Failure Modes Catalog | EvalKit docs/templates | pass | docs/opensource and opensource/evalkit docs present; website/resource boundary checked |
| 23 | PRD 23: Red-Team Prompt Taxonomy | EvalKit docs/templates | pass | docs/opensource and opensource/evalkit docs present; website/resource boundary checked |
| 24 | PRD 24: Multi-Turn Eval Template Pack | EvalKit code/package | pass | EvalKit path refs, CLI matrix, package build, 58 tests |
| 25 | PRD 25: Eval Run Report Template | EvalKit docs/templates | pass | docs/opensource and opensource/evalkit docs present; website/resource boundary checked |
| 26 | PRD 26: Human-Data Program Playbook | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 27 | PRD 27: Eval Data Readiness Checklist | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 28 | PRD 28: Pilot Design Templates | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 29 | PRD 29: Data Quality SLA Template | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 30 | PRD 30: Expert Reviewer Certification Template | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 31 | PRD 31: Human Data SOW Template | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 32 | PRD 32: Vendor Comparison Checklist | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 33 | PRD 33: AI Data Vendor RFP Template | Buying Toolkit resources | pass | docs/resources canonical files, docs/opensource compatibility paths, /resources visual QA |
| 34 | PRD 34: Robotics Failure Taxonomy | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 35 | PRD 35: Teleop Review Schema | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 36 | PRD 36: Robotics Dataset Card Template | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 37 | PRD 37: Sensor QA Checklist | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 38 | PRD 38: Robotics Failure Viewer with sample/mock data | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 39 | PRD 39: Intervention Ontology For Humanoid Data | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 40 | PRD 40: Teleop Task Library | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 41 | PRD 41: Robotics Data Failure Modes Catalog | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 42 | PRD 42: LeRobot Dataset Adapter | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |
| 43 | PRD 43: RLDS / OpenX Export Tool | Robotics ReviewKit | pass | Robotics paths, schemas, exporter scripts, viewer, 26 tests, browser QA |

## External Launch Boundary

These items are not repo-code gaps, but they are required before saying the work is live on the public internet:

- Deploy `auraone-website` so `https://auraone.ai/open` and `https://auraone.ai/resources` serve the audited source.
- Publish or expose the open-source repository in its intended public GitHub location.
- Publish `auraone-evalkit` to PyPI if the launch claim includes `pip install auraone-evalkit` from PyPI rather than local source install.
- Upload any intended Hugging Face datasets or Spaces if the launch claim includes hosted HF artifacts.
- Tag a release/changelog once the public repo destination is final.

## Bottom Line

The codebase is now source-complete against the 43 PRDs. It is not accurate to say AuraOne Open Source is already externally live unless the deployment and publishing steps above have been executed. It is accurate to say the repo is ready for those launch actions.
