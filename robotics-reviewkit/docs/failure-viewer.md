# Robotics Failure And Evidence Viewer

The canonical AuraOne Robotics ReviewKit viewer lets robotics data and review
teams inspect Teleop Review Schema and ReviewKit v2 event-stream records in a
local browser.

All bundled records are synthetic metadata. The viewer supports review and QA;
it is not a robotics data-collection, labeling-delivery, privacy-validation, or
training pipeline.

## Run Locally

From the AuraOne Open repository root:

```bash
python -m http.server 8765 --directory robotics-reviewkit
```

Open `http://127.0.0.1:8765/viewer/app/index.html`.

The single-file build is checked in at `viewer/app/index.html` and can also be
opened directly. Compatibility routes at `viewer/index.html` and
`viewer/reviewkit.html` redirect to the same canonical artifact.

## Load Data

The viewer bundles one synthetic teleop episode and one synthetic v2 episode.
Load or drag another local JSON file to inspect it. Parsing, filtering, source
editing, and export happen in the browser; the file is not uploaded and the
viewer does not call external services.

## What It Shows

- session rail for bundled and locally loaded episodes
- source JSON editor with path-specific issues and suggested fixes
- zoomable, keyboard-navigable event timeline
- ordered event table as the accessible evidence source
- filters for failure, intervention, segment, recovery, contact, drift, safety,
  and success records
- selected-event evidence inspector
- rubric anchors and intervention-density summaries
- sensor-QA count and release-readiness context
- persistent synthetic/permissioned and local-processing disclosures
- review JSON, event CSV, LeRobot metadata, and RLDS/OpenX metadata exports

## Rebuild And Verify

The source workspace requires Node `^20.19.0` or `>=22.12.0`.

```bash
cd robotics-reviewkit/viewer/reviewkit-v2
npm ci --no-audit --no-fund
npm run check
```

The build produces one HTML file with embedded application code and styles.
The workspace is private and is not an installable npm package.

## Limitations

The viewer does not play robot video, detect failures, assign reviewers,
validate privacy, or export training data. LeRobot and RLDS/OpenX downloads are
metadata bridges only and contain no observations, actions, sensor payloads,
tensors, media, or training shards.

Broken JSON and malformed episode fields produce visible, path-specific issues
instead of silently rendering a partial record.

[ReviewKit docs index](README.md) |
[ReviewKit README](../README.md) |
[Event-stream review](event-stream-review.md)
