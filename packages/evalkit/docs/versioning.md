# Rubric Versioning

Rubric diffs help teams decide whether score comparisons remain valid across rubric releases.

## Quickstart

```bash
evalkit diff-rubric examples/versioning/rubric_v1.jsonl examples/versioning/rubric_v2.jsonl
```

## What To Review

- Added or removed criteria.
- Criteria with changed wording.
- Weight changes that can shift rankings.
- Severity changes that alter release gates.
- Missing version metadata.

## Limitations

Diffs identify comparability risk. They do not prove that a new rubric is valid or expert-reviewed.
