# Eval Report Generator

The report generator turns local score output or a report input object into a
deterministic evidence artifact. Markdown, self-contained HTML, and normalized
JSON all use the `auraone.evalkit.report.v1` contract.

The HTML artifact uses the AuraOne Proofline visual system with OSS-safe system
fonts. It embeds its stylesheet, loads no scripts or remote assets, works
offline, responds down to narrow mobile viewports, exposes semantic tables and
stable anchors, honors reduced-motion and high-contrast preferences, and
prints in a light document layout.

## Quickstart

```bash
evalkit report --score examples/reports/tutorial_input.json --out /tmp/evalkit-report.md
evalkit report --input examples/reports/tutorial_input.json --out /tmp/evalkit-report.html
evalkit report --input examples/reports/tutorial_input.json --format json --out /tmp/evalkit-report.contract
```

The output suffix selects Markdown, HTML, or JSON. Use `--format` when the
destination has a nonstandard suffix. Use `--quiet` in scripts that do not want
the success message.

## Report Contract

Every normalized report contains:

- report schema, EvalKit version, source metadata, optional run ID, commit, and
  generation timestamp;
- an executive decision and summary metrics;
- explicit gate status with observed and threshold values;
- findings linked to evidence IDs;
- evidence records with optional links and checksums;
- a reproduction command, input paths, and environment metadata;
- legacy rubric coverage, score breakdown, unstable criteria, agreement,
  drift, leakage, and limitations sections;
- an explicit list of missing or omitted evidence;
- a deterministic SHA-256 of the normalized report input.

The generator never invents a timestamp. Supply `metadata.generated_at` as an
ISO 8601 value when a run owns that fact. If it is absent, the report records
the timestamp as omitted. `metadata.artifact_sha256` is rendered only when a
caller supplies a checksum for an external artifact; the embedded
`input_sha256` always covers the normalized evidence payload.

Minimal v1 input:

```json
{
  "title": "Release candidate evaluation",
  "source": {"name": "customer-owned-eval", "synthetic": false},
  "metadata": {
    "generated_at": "2026-07-12T19:30:00Z",
    "run_id": "eval-2026-07-12-001",
    "commit": "0123456789abcdef"
  },
  "decision": {
    "status": "review",
    "label": "Review required",
    "detail": "Agreement gate needs calibration."
  },
  "summary": {
    "headline": "The score gate passed and agreement remains below target.",
    "metrics": [
      {"id": "average-score", "label": "Average score", "value": 0.81}
    ]
  },
  "gates": [
    {
      "id": "agreement",
      "label": "Reviewer agreement",
      "status": "warning",
      "observed": 0.72,
      "threshold": 0.8,
      "detail": "Calibrate before release."
    }
  ],
  "findings": [
    {
      "id": "agreement-gap",
      "severity": "review",
      "title": "Agreement below target",
      "detail": "Two criteria account for most disagreements.",
      "evidence_refs": ["agreement-output"]
    }
  ],
  "evidence": [
    {
      "id": "agreement-output",
      "label": "Agreement output",
      "kind": "metric",
      "value": {"percent_agreement": 0.72}
    }
  ],
  "reproduce": {
    "command": "evalkit agreement labels.jsonl --out agreement.json",
    "inputs": {"labels": "labels.jsonl"},
    "environment": {"python": "3.11", "evalkit": "0.3.0"}
  },
  "limitations": ["The reviewer sample is small."]
}
```

Gate statuses are `passed`, `warning`, `failed`, or `not_run`. Finding
severities are `info`, `review`, `warning`, `danger`, or `blocked`. Unknown
values normalize to `not_run` or `info` rather than creating color-only,
unrecognized states.

Score payloads generated with `evalkit score --format report-json` remain
supported. EvalKit derives score, label coverage, and output pass-rate gates,
plus findings and evidence for failed outputs and missing labels.

## Determinism And Safety

- Dictionary keys and JSON output are sorted.
- No current time, random ID, network response, or browser script is injected.
- HTML values are escaped unconditionally.
- Evidence links accept only `http`, `https`, or same-document anchors.
- The report stylesheet and template ship inside the wheel and source
  distribution.
- The base artifact uses no JavaScript and no remote font, image, or CSS URL.
- Print output forces the light palette and avoids splitting core evidence
  records where practical.

## Data Status

Synthetic tutorial reports are not model leaderboards, safety certifications, or claims of expert validation.
