# Rubric Linter

AuraOne EvalKit's rubric linter runs locally on user-owned or synthetic tutorial rubric files. It requires no AuraOne account, API key, hosted tenant, database, or private reviewer pool.

## Quickstart

```bash
evalkit lint-rubric examples/bad_rubrics/compound.jsonl --format json
evalkit lint-rubric examples/tutorial/rubric.jsonl
```

## Rule Catalog

| Rule | Purpose |
| --- | --- |
| `R001_COMPOUND_CRITERIA` | Flags criteria that combine multiple judgments. |
| `R002_VAGUE_WORDING` | Flags subjective wording such as "good" or "clear" without boundaries. |
| `R003_MISSING_EXAMPLES` | Requires examples that make scoring boundaries inspectable. |
| `R004_MISSING_WEIGHT` | Requires numeric weights for deterministic scoring. |
| `R005_DUPLICATE_ID` | Flags duplicate criterion IDs. |
| `R006_DUPLICATE_TEXT` | Flags duplicate or near-duplicate criterion wording. |
| `R007_INCONSISTENT_SEVERITY` | Flags reused text with inconsistent severity. |
| `R008_UNSCORABLE_LANGUAGE` | Flags language that cannot be scored from visible evidence. |
| `R009_UNAVAILABLE_CONTEXT` | Flags criteria that require private or unavailable context. |
| `R010_UNCLEAR_SCORING_BOUNDARY` | Flags scale criteria without score-level boundaries. |
| `R011_WEIGHT_TOTAL` | Flags rubric weights that do not sum to 1.0. |

## Data Status

Examples under `examples/bad_rubrics/` are synthetic tutorial fixtures. They are not expert-authored, not human-validated, and not benchmark-grade.

## Related Docs

- `docs/architecture/two-package-architecture.md`
- `docs/schema/rubric-schema.md`
