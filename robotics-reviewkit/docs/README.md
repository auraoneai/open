# AuraOne Robotics ReviewKit Documentation

Technical guides for local robotics teleoperation and VLA review: schemas,
event streams, failure and intervention taxonomies, sensor QA, rubric anchors,
the evidence viewer, and metadata-only export bridges.

ReviewKit is for robotics data, ML infrastructure, and review teams working
with review sidecars they own. It does not collect raw robot data, upload
episodes, or emit trainable LeRobot, RLDS, or OpenX datasets.

## Start By Job

| Job | Guide | First action |
| --- | --- | --- |
| Inspect a review record in the browser | [Failure viewer](failure-viewer.md) | Open the checked-in single-file viewer |
| Define teleoperation review metadata | [Teleop Review Schema](teleop-review-schema.md) | Validate the full synthetic fixture |
| Represent timestamped VLA review events | [Event-stream review](event-stream-review.md) | Inspect labels and monotonic timestamp rules |
| Apply task-specific scoring anchors | [VLA rubric anchors](vla-rubric-anchors.md) | Import the anchor libraries or inspect the v2 fixture |
| Classify robotics failures | [Failure taxonomy](failure-taxonomy.md) | Map review findings to stable failure IDs |
| Record human or system interventions | [Intervention ontology](intervention-ontology.md) | Preserve intervention type and timing |
| Review sensor quality | [Sensor-QA checklist](sensor-qa-checklist.md) | Record affected sensors and recommended action |
| Standardize teleoperation tasks | [Teleop task library](teleop-task-library.md) | Select or adapt a task definition |
| Anticipate dataset QA failures | [Robotics data failure modes](robotics-data-failure-modes.md) | Add relevant checks to the review plan |
| Document a robotics dataset | [Dataset card template](robotics-dataset-card-template.md) | Disclose data status and limitations |
| Map review metadata toward LeRobot | [LeRobot metadata bridge](lerobot-adapter.md) | Run the source exporter on the synthetic fixture |
| Map review metadata toward RLDS/OpenX | [RLDS/OpenX metadata bridge](rlds-openx-export.md) | Run the source exporter in `rlds`, `openx`, or `both` mode |

## Supported Run Paths

Open the generated viewer from the AuraOne Open repository root:

```bash
python -m http.server 8765 --directory robotics-reviewkit
```

Then open `http://127.0.0.1:8765/viewer/app/index.html`.

Validate a review fixture:

```bash
python robotics-reviewkit/tests/validate_reviewkit.py \
  robotics-reviewkit/examples/teleop_review_mock_episode.json
```

The viewer and Python helpers are source-run artifacts. The private viewer
workspace is not an npm package, and this directory does not publish a Python
package.

## Runtime And Data Boundary

- Browser parsing, filtering, inspection, and export happen locally.
- Python validators and exporters read and write local files.
- Bundled examples are synthetic metadata, not real robot clips or customer
  data.
- Metadata bridges omit observations, actions, tensors, media, and training
  shards.
- ReviewKit does not detect failures automatically, validate privacy, or make a
  dataset training-ready.

## Proof And Next Action

Run the repository tests, then load one record from your own review workflow:

```bash
cd robotics-reviewkit
python -m pytest -p no:cacheprovider -q tests
cd viewer/reviewkit-v2
npm ci --no-audit --no-fund
npm run check
```

See the [ReviewKit README](../README.md) for the complete scope, supported
commands, viewer capabilities, and release boundary.

## AuraOne Links

- [AuraOne Open product overview](https://auraone.ai/open)
- [AuraOne Open source](https://github.com/auraoneai/open)
- [AuraOne EvalKit](../../packages/evalkit/)
