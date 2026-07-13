# Reviewer Drift

Use the drift detector to compare reviewer behavior and criterion stability
across local batches or time windows.

## Input And Output

Rows include `reviewer_id`, `item_id`, `criterion_id`, `batch_id`, `score`, and
optional `gold_score` or `consensus_score`.

The command returns per-reviewer drift, per-criterion instability, warnings,
and recommended follow-up.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit drift \
  examples/quality/drift/tutorial_batches.jsonl \
  --reviewer-threshold 0.35
```

The tutorial fixture is synthetic and contains a seeded drift pattern so the
warning path is deterministic.

## Limitations

Small or compositionally different batches can create unstable signals.
Inspect guideline changes, task mix, reviewer overlap, and adjudication context
before acting. Drift output is a QA triage aid, not a reviewer discipline,
employment, or certification decision.

[EvalKit docs index](../README.md) |
[Drift methodology](../drift.md) |
[Package README](../../README.md)
