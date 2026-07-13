# AuraOne Robotics ReviewKit

A local robotics data review and evidence toolkit for teleoperation and
vision-language-action (VLA) teams that need to inspect failures,
interventions, sensor-QA flags, rubric anchors, and training-readiness metadata
without uploading robot data.

Viewer source version: `0.2.0`. The viewer workspace is private and exists to
build the checked-in artifact; Robotics ReviewKit is not published from this
directory as an npm or Python package.

[AuraOne Open](https://auraone.ai/open) |
[Documentation](docs/) |
[Source](https://github.com/auraoneai/open/tree/main/robotics-reviewkit) |
[EvalKit](../packages/evalkit/)

All bundled episodes and exports are synthetic or mock metadata. They are not
real robot clips, reviewed customer datasets, expert-authored benchmarks,
training data, or proof of collection volume.

## Who It Is For

- Robotics data and ML infrastructure engineers defining post-collection QA
  contracts.
- Teleoperation and VLA review teams inspecting task segments, interventions,
  failures, recoveries, contact, safety, drift, and success events.
- Dataset and release owners deciding whether an episode needs review,
  exclusion, or additional evidence.
- Tooling teams mapping review metadata toward LeRobot, RLDS, or OpenX
  organization without claiming to emit trainable datasets.

## What ReviewKit Does

| Surface | Job | Proof in this repository |
| --- | --- | --- |
| Teleop Review Schema | Defines review and QA metadata layered around a teleoperation episode | JSON Schema, full synthetic fixture, and cross-reference validators |
| ReviewKit v2 event stream | Represents timestamped review events and VLA rubric anchors | Event schema, analyzers, synthetic v2 episode, and tests |
| Failure and intervention taxonomies | Gives failures, interventions, tasks, and sensor-QA flags stable IDs | YAML/JSON taxonomies and reference examples |
| Local evidence viewer | Inspects teleop and v2 records in a responsive browser UI | React source plus a checked-in self-contained HTML build |
| Metadata exporters | Preserves review metadata in LeRobot-, RLDS-, and OpenX-like layouts | Deterministic Python writers, expected outputs, and tests |

## Why ReviewKit

- **Review is modeled separately from collection.** Raw observations, actions,
  and media can stay in the collection stack while review decisions remain a
  versioned sidecar.
- **Failures remain evidence-linked.** Segments, interventions, taxonomy IDs,
  reviewer notes, sensor-QA flags, and readiness decisions are not flattened
  into one success label.
- **The viewer works locally.** Parsing, filtering, inspection, editing, and
  export happen in the browser with no required account or service call.
- **Export limits are explicit.** LeRobot and RLDS/OpenX outputs preserve
  metadata structure but do not pretend that placeholders are trainable
  observations or actions.

## Supported Run Paths

### Open The Checked-In Viewer

From the AuraOne Open repository root:

```bash
python -m http.server 8765 --directory robotics-reviewkit
```

Open `http://127.0.0.1:8765/viewer/app/index.html`.

The generated artifact is a self-contained HTML file and can also be opened
directly from the local filesystem. Compatibility routes at
`viewer/index.html` and `viewer/reviewkit.html` redirect to the same artifact.

### Rebuild The Viewer

The source build requires Node `^20.19.0` or `>=22.12.0`.

```bash
cd robotics-reviewkit/viewer/reviewkit-v2
npm ci --no-audit --no-fund
npm run check
```

`npm run check` type-checks the React source and rebuilds the single-file
viewer. This is a private build workspace, not an installable ReviewKit npm
package.

### Run Validators And Exporters From Source

The Python helpers are also source-run tools rather than a separately published
package:

```bash
python robotics-reviewkit/cli/validate_episode.py \
  robotics-reviewkit/examples/mock_episode.json

python robotics-reviewkit/cli/export_lerobot.py \
  robotics-reviewkit/examples/lerobot_export/mock_teleop_episode.json \
  /tmp/auraone-lerobot-metadata

python robotics-reviewkit/cli/export_rlds.py \
  --format both \
  robotics-reviewkit/examples/rlds_export/mock_teleop_episode.json \
  /tmp/auraone-rlds-openx-metadata
```

Validate the full Teleop Review Schema fixture with:

```bash
python robotics-reviewkit/tests/validate_reviewkit.py \
  robotics-reviewkit/examples/teleop_review_mock_episode.json
```

## Runtime And Data Boundary

- The viewer reads bundled synthetic records or JSON files selected by the
  user. It does not upload files or call external services.
- The Python validators and exporters read local files and write local JSON or
  JSONL metadata artifacts.
- No AuraOne account, API key, tenant, database, robot, private reviewer pool,
  or real robot clip is required.
- The viewer does not play robot video, detect failures, collect labels,
  validate privacy, or create raw observations and actions.
- Review JSON, event CSV, LeRobot metadata, and RLDS/OpenX metadata exports do
  not contain sensor payloads, tensors, media, or training shards.

## Review Versus Collection

Data collection records observations, actions, timestamps, environment state,
and media. ReviewKit focuses on the judgment metadata layered after or
alongside collection:

- action and task segment boundaries
- operator interventions and recovery events
- failure taxonomy annotations
- sensor-QA findings
- reviewer notes and rubric-anchor decisions
- privacy-review state
- training-readiness or exclusion decisions

An episode can be collected successfully and still fail review because it
lacks reset evidence, hides final object state, has unlabeled interventions,
contains sensor-quality issues, or does not preserve action boundaries.

## What Ships

- Teleop schema: `schema/teleop_episode.schema.json`
- V2 episode schema: `schema/vla_episode_review_schema_v2.json`
- Event-stream schema: `schema/event_stream_schema.json`
- Failure taxonomy: `schema/taxonomy/failure_modes.yaml`
- Intervention ontology: `schema/taxonomy/intervention_ontology.yaml`
- Sensor-QA flags: `schema/taxonomy/sensor_qa_flags.yaml`
- Teleop task library: `schema/tasks/teleop_tasks.yaml`
- Full synthetic teleop fixture:
  `examples/teleop_review_mock_episode.json`
- Synthetic v2 fixture: `examples/vla_synthetic_episode_v2.json`
- Canonical React source: `viewer/reviewkit-v2/`
- Generated single-file viewer: `viewer/app/index.html`
- Source validators and exporters: `src/`, `cli/`, and `tests/`

Compatibility aliases under `taxonomy/` and `tasks/` remain available for
earlier PRD paths.

## Viewer Capabilities

The canonical viewer accepts Teleop Review Schema and ReviewKit v2 event-stream
records. It provides:

- a session rail for bundled and locally loaded episodes
- editable source JSON with path-specific issues and suggested fixes
- search and evidence filters
- a keyboard-navigable timeline and ordered event table
- a selected-record evidence inspector
- rubric anchors and intervention-density summaries
- sensor-QA and release-readiness context
- deterministic review JSON, event CSV, LeRobot metadata, and RLDS/OpenX
  metadata downloads

## Proof And Verification

Run the focused Python and viewer checks:

```bash
cd robotics-reviewkit
python -m pytest -p no:cacheprovider -q tests
python tests/validate_reviewkit.py examples/teleop_review_mock_episode.json
python tests/viewer_smoke.py
```

```bash
cd robotics-reviewkit/viewer/reviewkit-v2
npm ci --no-audit --no-fund
npm run check
```

These checks verify schemas, taxonomies, fixtures, exporters, compatibility
paths, generated viewer assets, TypeScript, and the local build. They do not
prove that real robotics data was reviewed or that a hosted deployment exists.

## Documentation

- [Documentation index](docs/)
- [Failure viewer](docs/failure-viewer.md)
- [Teleop Review Schema](docs/teleop-review-schema.md)
- [Event-stream review](docs/event-stream-review.md)
- [VLA rubric anchors](docs/vla-rubric-anchors.md)
- [Failure taxonomy](docs/failure-taxonomy.md)
- [Intervention ontology](docs/intervention-ontology.md)
- [Sensor-QA checklist](docs/sensor-qa-checklist.md)
- [Teleop task library](docs/teleop-task-library.md)
- [Robotics data failure modes](docs/robotics-data-failure-modes.md)
- [Robotics dataset card template](docs/robotics-dataset-card-template.md)
- [LeRobot metadata bridge](docs/lerobot-adapter.md)
- [RLDS/OpenX metadata bridge](docs/rlds-openx-export.md)

## Next Actions

1. Open the checked-in viewer and inspect both bundled synthetic episodes.
2. Load one local review JSON file and resolve any path-specific issues.
3. Validate the same record from the command line.
4. Export metadata only when the downstream workflow understands that
   observations, actions, and media are not included.
5. Adapt the schema or taxonomy in version control before reviewing real data.

## License

MIT. See the repository [LICENSE](../LICENSE).
