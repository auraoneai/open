# LeRobot Metadata Bridge

Map Teleop Review Schema records into a LeRobot-like JSON directory while
preserving reviewed task, embodiment, segment, intervention, failure,
sensor-QA, reviewer, and training-readiness metadata.

This source exporter is for robotics data infrastructure teams evaluating how
review sidecars could accompany a downstream LeRobot dataset. It does not
write a trainable LeRobot dataset.

## Output Files

The writer creates:

- `manifest.json`: complete metadata bridge payload
- `meta/info.json`: dataset-level metadata
- `meta/tasks.jsonl`: task index rows
- `episodes/<episode_id>.json`: per-episode reviewed metadata

Fields named `observations` and `actions` are explicit placeholders. The
exporter does not write parquet shards, tensors, camera frames, video,
proprioception arrays, or action arrays.

## Supported Source Command

From the AuraOne Open repository root:

```bash
python robotics-reviewkit/cli/export_lerobot.py \
  robotics-reviewkit/examples/lerobot_export/mock_teleop_episode.json \
  /tmp/auraone-lerobot-metadata
```

Robotics ReviewKit does not currently expose an `evalkit robotics` command and
is not published as a standalone Python package. Run the checked-in script from
source.

## Supported Input Subset

Required fields:

- `episode_id` or `id`
- `task` as a string or an object with an ID and optional name

Optional fields include embodiment, training readiness, duration, sensors,
segments, interventions, failure modes, sensor QA, review metadata, and schema
version. Segment time ranges are validated when start and end fields are
present.

## Compatibility Boundary

The directory names mirror common LeRobot concepts such as `meta`, `tasks`, and
`episodes`, but the contents remain JSON review metadata. A production LeRobot
dataset still requires synchronized observations, actions, media, and
format-specific dataset writing.

The bundled fixture is synthetic and not human-validated, benchmark-grade, or
training data.

[ReviewKit docs index](README.md) |
[Teleop Review Schema](teleop-review-schema.md) |
[RLDS/OpenX metadata bridge](rlds-openx-export.md)
