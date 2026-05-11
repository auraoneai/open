# Eval Report Generator

The report generator renders deterministic Markdown from local EvalKit outputs through the v0.1 CLI. The Python generator can also render HTML or JSON. Reports include limitations and omitted-section notes so missing optional data does not look like a validation stamp.

## Quickstart

```bash
evalkit report --score examples/reports/tutorial_input.json --out /tmp/evalkit-report.md
```

## Sections

- Executive summary
- Rubric coverage
- Score breakdown
- Unstable criteria
- Reviewer agreement
- Drift warnings
- Limitations

## Data Status

Synthetic tutorial reports are not model leaderboards, safety certifications, or claims of expert validation.
