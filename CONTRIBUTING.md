# Contributing to AuraOne Open

Thanks for your interest in contributing. This repository hosts AuraOne's open tools for the human-judgment layer of AI evaluation: EvalKit (Python package + CLI), the Robotics ReviewKit (schemas, exporters, viewer), and the Buying Toolkit (documents).

This is the public, open-source half of AuraOne. It is intentionally narrow in scope. The hosted AuraOne platform, SDKs, and infrastructure live in a separate, private repository and are not in scope here.

## What we welcome

- Bug reports with a minimal reproduction.
- Documentation fixes — typos, broken links, clearer examples.
- Additional rubric examples, dataset card examples, or report templates.
- New EvalKit checks that fit the existing CLI surface (`validate-rubric`, `lint-rubric`, `score`, `agreement`, `drift`, `judge-calibrate`, `leakage-check`, `sample`, `weight-calibrate`, `report`, `card init`, `diff-rubric`).
- New Robotics ReviewKit taxonomy entries, schema validators, or exporter coverage for LeRobot / RLDS / OpenX.
- Improved tutorial datasets — clearly marked as synthetic.

## What is out of scope

- Hosted AuraOne platform features, billing, multi-tenant code, or APIs.
- Real customer data, real reviewer data, or real robotics teleop data.
- New benchmarks claimed as expert-authored or human-validated. This release is methodology and tooling, not a benchmark.
- Changes that require an AuraOne account or network access to run.

If your change is a good fit for the hosted platform rather than open tooling, open an issue describing it and we'll point you at the right surface.

## Project layout

```
packages/evalkit/          # auraone-evalkit Python package + `evalkit` CLI
robotics-reviewkit/        # Schemas, exporters, taxonomy, static viewer
resources/buying-toolkit/  # Markdown templates and checklists
resources/writing/         # Thesis posts
docs/PRD/                  # Source-to-v0.1.0 audit trail
```

## Development setup

EvalKit (Python ≥ 3.10):

```bash
cd packages/evalkit
python -m venv .venv && source .venv/bin/activate
pip install -e .
PYTHONPATH=src python -m pytest -q tests
```

Robotics ReviewKit:

```bash
cd robotics-reviewkit
PYTHONPATH=src python -m pytest -q tests
python cli/validate_episode.py examples/mock_episode.json
```

There is no monorepo build step, no Node/pnpm tooling, and no database in this repository.

## Pull request expectations

- Keep changes focused. One concern per PR.
- Run the relevant test suite locally before opening a PR. CI runs the same suites.
- Add or update tests when you change behavior.
- If you add a new CLI flag or command, document it in `packages/evalkit/README.md` (or the relevant component README).
- Do not commit large binary data. Robotics examples are intentionally mock metadata, not real episodes.

## Commit messages

Use short, descriptive commit messages. Conventional prefixes (`feat:`, `fix:`, `docs:`, `test:`, `chore:`) are appreciated but not required.

## Issue triage

When opening an issue:

- Include the component (`evalkit`, `robotics-reviewkit`, `buying-toolkit`, `docs`).
- For EvalKit bugs, include the CLI command, input file (or a minimal redacted version), and the unexpected output.
- For schema or exporter issues, link to the failing example.

## Code of conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Contributions are made under the [MIT License](LICENSE). By submitting a contribution, you agree your work may be distributed under that license.

## Reporting a security issue

Do not file public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md) for how to report.
