# AuraOne Open

Local-first AI evaluation and robotics review tools for teams that need
inspectable judgment workflows without sending private rubrics, labels, model
outputs, or review metadata to AuraOne.

[AuraOne Open](https://auraone.ai/open) |
[EvalKit](packages/evalkit/) |
[Robotics ReviewKit](robotics-reviewkit/) |
[Documentation](packages/evalkit/docs/) |
[Source](https://github.com/auraoneai/open)

AuraOne Open focuses on the human-judgment layer around AI and LLM evaluation:
evaluation rubrics, deterministic scoring, reviewer agreement, judge
calibration, drift, leakage checks, evidence reports, and robotics
teleoperation/VLA review metadata. It does not run models, collect robot sensor
streams, or provide a hosted annotation service.

## Who This Is For

- AI evaluation and ML platform engineers building private eval pipelines.
- Annotation and human-evaluation leads improving rubric quality and reviewer
  consistency.
- Model quality teams auditing saved human or LLM-judge labels before release
  decisions.
- Robotics data and review teams inspecting teleoperation, intervention,
  failure, sensor-QA, and training-readiness metadata.
- Technical program owners who need reusable human-data buying and QA
  templates.

## Choose A Starting Point

| Need | Start here | Job | First action |
| --- | --- | --- | --- |
| AI or LLM evaluation rubrics, scoring, agreement, drift, leakage, or reports | [`packages/evalkit/`](packages/evalkit/) | Run a local Python CLI over files you own | Install EvalKit and validate the tutorial rubric |
| Robotics teleoperation or VLA review, failure analysis, and metadata export | [`robotics-reviewkit/`](robotics-reviewkit/) | Inspect review evidence in a local browser and validate review sidecars | Open the checked-in single-file viewer |
| Human-data vendor selection, pilot design, SOWs, RFPs, and SLAs | [`resources/buying-toolkit/`](resources/buying-toolkit/) | Adapt practical procurement and program templates | Start with the playbook or pilot checklist |
| Evaluation methodology and release thesis | [`resources/writing/`](resources/writing/) | Understand the design principles behind the tools | Read [The Human-Judgment Layer](resources/writing/measuring-human-judgment-layer.md) |

## Why AuraOne Open

- **Private data, public contracts.** Rubrics, labels, model outputs, and
  robotics review records remain local while schemas, checks, and report
  formats stay inspectable.
- **Evidence instead of hidden state.** Core workflows emit deterministic
  JSON, JSONL, CSV, Markdown, or self-contained HTML that can be reviewed,
  diffed, and stored with a release.
- **Judgment-layer focus.** EvalKit complements model runners, benchmark
  harnesses, and annotation systems by concentrating on rubric quality,
  supplied labels, reviewer QA, and decision evidence.
- **Review is separate from collection.** Robotics ReviewKit preserves
  interventions, failures, sensor-QA flags, and readiness decisions without
  claiming to produce raw or trainable robotics datasets.

## Install And Run

### AuraOne EvalKit

Install the latest published PyPI release:

```bash
python -m pip install --upgrade auraone-evalkit
```

Repository changes can precede package publication. To evaluate the current
checkout instead, install it from the repository root:

```bash
python -m pip install -e "./packages/evalkit"
```

After the editable source install, run the current checkout's complete local
tutorial:

```bash
evalkit validate-rubric packages/evalkit/examples/tutorial/rubric.jsonl
evalkit lint-rubric packages/evalkit/examples/tutorial/rubric.jsonl
evalkit score \
  --rubric packages/evalkit/examples/tutorial/rubric.jsonl \
  --responses packages/evalkit/examples/tutorial/model_outputs.jsonl \
  --labels packages/evalkit/examples/tutorial/labels.jsonl \
  --out /tmp/evalkit-scores.json
evalkit report \
  --input packages/evalkit/examples/reports/tutorial_input.json \
  --out /tmp/evalkit-report.html
```

See the [EvalKit README](packages/evalkit/README.md) for command contracts,
limitations, and development setup.

### AuraOne Robotics ReviewKit

The generated viewer is checked in and does not require an npm package
installation:

```bash
python -m http.server 8765 --directory robotics-reviewkit
```

Open `http://127.0.0.1:8765/viewer/app/index.html`.

To rebuild and verify the viewer from source:

```bash
cd robotics-reviewkit/viewer/reviewkit-v2
npm ci --no-audit --no-fund
npm run check
```

See the [Robotics ReviewKit README](robotics-reviewkit/README.md) for schema,
exporter, runtime, and data-boundary details.

## What Ships

| Component | Included surface |
| --- | --- |
| [`packages/evalkit/`](packages/evalkit/) | `auraone-evalkit` Python project and `evalkit` CLI for rubric validation and linting, deterministic scoring, reviewer agreement, judge calibration, drift, leakage checks, sampling, rubric diffs, dataset cards, and evidence reports |
| [`robotics-reviewkit/`](robotics-reviewkit/) | Review schemas, failure and intervention taxonomies, synthetic fixtures, Python validators and metadata exporters, and a self-contained React viewer |
| [`resources/buying-toolkit/`](resources/buying-toolkit/) | Editable SOW, RFP, SLA, vendor comparison, reviewer certification, pilot, and program-management templates |
| [`resources/writing/`](resources/writing/) | Public methodology and release writing |
| [`docs/PRD/`](docs/PRD/) | Historical product requirements and implementation audit trail |

## Runtime And Data Boundary

- EvalKit core commands read local files and run in the local Python process.
  They do not require an AuraOne account, API key, tenant, or database.
- EvalKit scoring aggregates labels supplied by the user. It does not create
  human labels, call LLM judges, or run model inference.
- Judge calibration analyzes saved judge outputs. Leakage checks compare local
  inputs and optional local reference files; they do not search the web.
- The Robotics ReviewKit viewer parses, filters, and exports records in the
  browser. The checked-in single-file build has no remote runtime assets.
- LeRobot and RLDS/OpenX outputs are explicit metadata bridges. They do not
  contain observations, actions, tensors, video, or training shards.
- Bundled eval and robotics examples are synthetic fixtures for runnable tests
  and tutorials. They are not expert-authored benchmarks, customer data,
  human-validated datasets, or evidence of model quality.

## Proof You Can Inspect

The repository provides schemas, deterministic fixtures, package builds,
focused tests, and a fail-closed release preflight. Run the local discovery and
package checks with:

```bash
npm run docs:verify
```

```bash
cd packages/evalkit
python -m pytest -p no:cacheprovider -q tests
python -m build
python scripts/verify_release.py dist
```

```bash
cd robotics-reviewkit
python -m pytest -p no:cacheprovider -q tests
cd viewer/reviewkit-v2
npm run check
```

Passing local checks verifies the checked-out source. It does not authorize a
registry publication, hosted deployment, signed artifact, or release claim.

## What This Repository Is Not

- Not a public benchmark suite or a source of model leaderboard claims.
- Not a model execution harness, LLM-judge provider, or hosted eval dashboard.
- Not a workforce-management or annotation-delivery platform.
- Not a robotics data-collection stack or trainable LeRobot/RLDS/OpenX dataset
  generator.
- Not proof that a package, viewer, release asset, or hosted route has been
  published. Publication remains separately gated.

## Coordinated Release Preflight

The Proofline UI/UX release is coordinated across this repository, the AuraOne
SDKs, the GitHub App, and the Open Studio products. Review the plan without
running builds:

```bash
npm run release:oss:preflight -- \
  --release-plan release/release-plan.json
```

Run the complete local command matrix after every target worktree is reviewed
and clean:

```bash
npm run release:oss:preflight:execute -- \
  --release-plan release/release-plan.json
```

The orchestrator records exact source commits, package/channel ownership,
public-asset findings, commands, failures, and whether publication is allowed.
It never publishes, tags, pushes, or deploys. Live publication remains an
explicit maintainer action through protected registry and GitHub environments.
The current per-channel decision, blocker, and next-action record is
`release/evidence/publication-decision.json`; a local green build cannot
override that publication gate.

## Next Actions

- For AI evaluation, install [AuraOne EvalKit](packages/evalkit/) and run the
  bundled rubric, scoring, and report tutorial.
- For robotics review, open [Robotics ReviewKit](robotics-reviewkit/) and load
  a local Teleop Review Schema or v2 event-stream JSON file.
- For technical discovery, browse the
  [EvalKit documentation index](packages/evalkit/docs/) or the
  [Robotics ReviewKit documentation index](robotics-reviewkit/docs/).

## AuraOne Links

- Product overview: [AuraOne Open](https://auraone.ai/open)
- Public source: [github.com/auraoneai/open](https://github.com/auraoneai/open)
- Issues: [AuraOne Open issue tracker](https://github.com/auraoneai/open/issues)
- Resource hub: [AuraOne Resources](https://auraone.ai/resources)

## License

MIT. See [LICENSE](LICENSE).
