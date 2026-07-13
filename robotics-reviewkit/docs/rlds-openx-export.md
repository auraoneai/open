# RLDS And OpenX Metadata Bridge

Map Teleop Review Schema records into RLDS-like episode JSON or an OpenX-like
manifest while preserving review metadata and explicit missing-asset
disclosures.

This source exporter helps robotics data infrastructure teams inspect how
review sidecars could accompany downstream dataset organization. It does not
produce a trainable RLDS or Open X-Embodiment dataset.

## RLDS-Like Output

The writer creates:

- `manifest.json`: complete metadata bridge payload
- `dataset_info.json`: dataset-level metadata
- `episodes/<episode_id>.json`: per-episode metadata with placeholder steps

Placeholder steps include `is_first`, `is_last`, `is_terminal`,
`observation.placeholder`, and `action.placeholder`. Reviewed segment metadata
remains inspectable.

## OpenX-Like Output

The writer creates:

- `manifest.json`
- `openx_manifest.json`
- `episodes/<episode_id>.openx.json`

The manifest preserves task, embodiment, sensor, review, split, and
training-readiness metadata with explicit `null` asset references.

## Supported Source Commands

From the AuraOne Open repository root:

```bash
python robotics-reviewkit/cli/export_rlds.py \
  --format rlds \
  robotics-reviewkit/examples/rlds_export/mock_teleop_episode.json \
  /tmp/auraone-rlds-metadata

python robotics-reviewkit/cli/export_rlds.py \
  --format openx \
  robotics-reviewkit/examples/rlds_export/mock_teleop_episode.json \
  /tmp/auraone-openx-metadata

python robotics-reviewkit/cli/export_rlds.py \
  --format both \
  robotics-reviewkit/examples/rlds_export/mock_teleop_episode.json \
  /tmp/auraone-rlds-openx-metadata
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

The bridge intentionally stops at review metadata. Production RLDS or OpenX
generation still requires real observations, actions, timestamps, synchronized
sensor payloads, reward and discount semantics where applicable, media
storage, and format-specific dataset builders.

The bundled fixture is synthetic and not human-validated, benchmark-grade, or
training data.

[ReviewKit docs index](README.md) |
[Teleop Review Schema](teleop-review-schema.md) |
[LeRobot metadata bridge](lerobot-adapter.md)
