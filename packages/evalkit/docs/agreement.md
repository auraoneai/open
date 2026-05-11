# Reviewer Agreement

The agreement library summarizes local reviewer labels without requiring hosted services. Use it to inspect label consistency before scaling review volume or feeding labels into report generation.

## Quickstart

```bash
evalkit agreement examples/agreement/tutorial_labels.jsonl
```

## Metrics

- Percent agreement is easiest to explain but can be misleading when labels are imbalanced.
- Cohen kappa and Fleiss kappa are useful when label distributions are stable enough to support chance correction.
- Krippendorff alpha is useful for sparse or mixed-reviewer settings, but low sample counts remain fragile.
- Adjudication rate indicates how often reviewer disagreement required a tie-break.

## Data Status

The bundled labels are synthetic tutorial data only. They are not expert-authored, human-validated, or suitable for benchmark claims.
