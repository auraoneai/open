# Leakage Audit

The leakage checker runs offline duplicate and near-duplicate detection over local prompts or eval items.

Example:

```bash
evalkit leakage-check examples/quality/leakage/tutorial_prompts.jsonl
```

The output includes item-level findings, similarity scores, evidence snippets, and duplicate clusters.

## Limitations

This is an audit aid. It can catch obvious overlap, but it is not proof that no benchmark contamination exists. v0.1 does not perform web search or compare against private reference corpora unless the user supplies local reference data.
