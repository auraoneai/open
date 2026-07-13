# Changelog

All notable changes to `auraone-evalkit` are documented here.

## 0.3.0 - 2026-07-12

### Added

- Stable `auraone.evalkit.report.v1` JSON contract with summary metrics,
  quality gates, findings, evidence references, reproduction metadata, omitted
  evidence, and deterministic input checksums.
- Self-contained AuraOne Proofline HTML reports with responsive, print,
  reduced-motion, forced-colors, semantic-table, skip-link, and offline
  behavior.
- Explicit `markdown`, `html`, and `json` report format selection.
- JSONL output for rubric validation and linting.
- Text, JSON, and JSONL output selection for agreement, drift, leakage,
  judge-calibration, and weight-calibration commands.
- `--no-color` and `NO_COLOR` handling for human-readable terminal output.
- Package release verification for versions, metadata, private-font exclusion,
  and wheel/sdist template contents.

### Changed

- The canonical Jinja report template now owns the HTML structure and embedded
  OSS-safe design tokens.
- Score payload reports derive decision gates, failed-output findings, missing
  label findings, and scored-output evidence automatically.
- The PyPI release workflow runs the full EvalKit tests and artifact checks
  before trusted publishing.

### Compatibility

- Existing Markdown generation and report input fields remain supported.
- Existing score output formats and default JSON behavior remain unchanged.
- HTML values are now unconditionally escaped.

### Limitations

- EvalKit does not invent generation timestamps or external artifact
  checksums. Callers must supply evidence they own.
- Generated reports are evidence artifacts, not certifications, benchmark
  claims, or substitutes for domain review.
