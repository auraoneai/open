# Reviewer Drift

The drift detector compares reviewer behavior across local batches or time windows.

Tutorial data in `examples/quality/drift/tutorial_batches.jsonl` is synthetic and includes a seeded drifted reviewer.

## Input

Rows include `reviewer_id`, `item_id`, `criterion_id`, `batch_id`, `score`, and optional `gold_score` or `consensus_score`.

## Output

The detector returns per-reviewer drift, per-criterion instability, batch warnings, and recommended follow-up.

Example:

```bash
evalkit drift examples/quality/drift/tutorial_batches.jsonl --reviewer-threshold 0.35
```

## Limitations

Drift warnings are QA triage signals. They are not reviewer discipline decisions, employment recommendations, or proof that a real review pool has changed.
