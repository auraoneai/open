# Reviewer Agreement

EvalKit agreement metrics run locally on JSONL labels and do not require an AuraOne account, hosted database, or API key.

Tutorial data in `examples/quality/agreement/tutorial_labels.jsonl` is synthetic. It is not expert-authored, not human-validated, and not a benchmark.

## Input

Each row should include:

- `item_id`
- `criterion_id`
- `reviewer_id` or `annotator_id`
- `value` or `score`
- optional `adjudicated`

## Metrics

The Python Krippendorff alpha behavior covers the standard cases: numeric values use interval disagreement; categorical values use pairwise coincidence; strings and booleans use exact-match distance; lists use Jaccard distance.

Additional v0.1 metrics include percent agreement, Cohen kappa for two reviewers, Fleiss kappa for equal-rater nominal overlaps, per-criterion agreement, per-reviewer agreement, and adjudication rate.

## CLI Hook

Worker 2 exposes `auraone_evalkit.agreement.cli.register(subparsers)` for the shared `evalkit agreement` command integration.

Example:

```bash
evalkit agreement examples/quality/agreement/tutorial_labels.jsonl
```

## Limitations

Agreement metrics are unstable for low overlap, imbalanced labels, sparse reviewer assignment, and unclear rubric boundaries. Treat low agreement as a triage signal for rubric review or human calibration, not as a standalone quality verdict.
