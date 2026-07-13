# Rubric Versioning

Compare two JSONL rubric versions by `criterion_id` before treating scores
across versions as comparable.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit diff-rubric \
  examples/quality/versioning/rubric_v1.jsonl \
  examples/quality/versioning/rubric_v2.jsonl
```

The diff classifies added, removed, rename-candidate, cosmetic, and
scoring-impact changes. Weight, severity, scoring type, maximum score, and
threshold changes are treated as score-comparability risks.

## Release Guidance

Use high-risk diffs as release-review inputs. When scoring semantics change,
re-score a stable holdout before comparing old and new aggregates. A rubric
diff records change; it does not determine whether the new rubric is correct.

[EvalKit docs index](../README.md) |
[Versioning guide](../versioning.md) |
[Package README](../../README.md)
