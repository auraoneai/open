# Reviewer Agreement

Use reviewer agreement to inspect how consistently two or more reviewers apply
the same evaluation criteria before their labels become release evidence,
training data, or aggregate model scores.

EvalKit reads local JSONL labels and does not require an AuraOne account,
hosted database, or API key.

## Input

Each row includes:

- `item_id`
- `criterion_id`
- `reviewer_id` or `annotator_id`
- `value` or `score`
- optional `adjudicated`

## Metrics

The command reports percent agreement, Krippendorff alpha, Cohen kappa when
exactly two reviewers overlap, Fleiss kappa when equal-rater overlap is
available, adjudication rate, and per-criterion and per-reviewer breakdowns.

Numeric values use interval behavior for alpha; categorical values use nominal
behavior. Metric availability depends on reviewer count and overlapping label
shape, so inspect `null` or omitted metrics rather than treating every statistic
as universally applicable.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit agreement examples/quality/agreement/tutorial_labels.jsonl
```

The tutorial data is synthetic and intentionally limited. Replace it with
reviewer labels you own, then inspect low-overlap criteria before interpreting
the aggregate metric.

## Limitations

Agreement estimates are unstable with low overlap, imbalanced labels, sparse
reviewer assignment, or unclear rubric boundaries. A low result is a triage
signal for rubric review and human calibration, not an employment decision or
standalone quality verdict.

[EvalKit docs index](../README.md) |
[Agreement methodology](../agreement.md) |
[Package README](../../README.md)
