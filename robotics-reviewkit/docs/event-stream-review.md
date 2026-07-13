# Event-Stream Review

ReviewKit v2 represents timestamped robotics review evidence for success,
contact, safety, drift, recovery, and intervention events.

Use the event stream when a robotics or VLA review needs per-step evidence that
can be filtered, summarized, viewed on a timeline, and preserved in
metadata-only exports.

## Contract

Each event includes:

- a non-negative `timestamp_s`
- one supported `label`
- optional `severity`
- optional reviewer `notes`

Events must be monotonically increasing. The validator rejects unsorted or
unsupported events so downstream viewers and streaming exporters do not need
to silently reorder the evidence.

The authoritative JSON shape is
[`../schema/event_stream_schema.json`](../schema/event_stream_schema.json).

## Python Helpers

Run from a source checkout with `robotics-reviewkit/src` on `PYTHONPATH`:

```python
from robotics_reviewkit.analyzers import intervention_density, summarize_events

summary = summarize_events(episode["event_stream"])
density = intervention_density(
    episode["event_stream"],
    episode["duration_seconds"],
)
```

`summarize_events()` returns counts for every supported label, observed
duration, and synthetic disclosure. `intervention_density()` reports
interventions, recoveries, and safety events per minute.

## Viewer And Export Behavior

The canonical viewer renders the same records through a filtered timeline,
ordered event table, selected-event inspector, rubric anchors, and
intervention-density summary.

LeRobot v2 and streaming RLDS outputs preserve event metadata. They remain
metadata-only and do not add real observations, actions, tensors, or media.

## Next Action

Inspect the bundled
[`vla_synthetic_episode_v2.json`](../examples/vla_synthetic_episode_v2.json),
then validate a record with the focused v2 tests:

```bash
cd robotics-reviewkit
python -m pytest -p no:cacheprovider -q tests/test_v2_reviewkit.py
```

[ReviewKit docs index](README.md) |
[Failure viewer](failure-viewer.md) |
[VLA rubric anchors](vla-rubric-anchors.md)
