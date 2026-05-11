# Model Output Sampling

Sampling selects model outputs for deeper review using deterministic strategies.

Example:

```bash
evalkit sample examples/quality/sampling/model_outputs.jsonl --strategy uncertainty -k 3 --seed 13
```

Supported strategies:

- `random`
- `stratified`
- `diversity`
- `failure-heavy`
- `judge-disagreement-heavy`
- `uncertainty`
- `regression`

The output includes selected item IDs and a rationale for each selection.

## Limitations

Sampling helps focus human review budgets. It is not a substitute for full validation or coverage analysis.
