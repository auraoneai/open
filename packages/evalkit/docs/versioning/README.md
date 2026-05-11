# Rubric Versioning

Rubric diffs compare JSONL rubric versions by `criterion_id`.

Example:

```bash
evalkit diff-rubric examples/quality/versioning/rubric_v1.jsonl examples/quality/versioning/rubric_v2.jsonl
```

The diff flags added, removed, renamed-candidate, cosmetic, and scoring-impact changes. Weight, severity, scoring type, max score, and threshold changes are treated as score-comparability risks.

## Release Guidance

Use high-risk rubric diffs as release-gate inputs. If weights or severities change, avoid comparing old and new aggregate scores without re-scoring a stable holdout.
