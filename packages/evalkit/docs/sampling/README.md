# Model Output Sampling

Select saved model outputs for deeper human review with deterministic
strategies and an explicit rationale for each selected item.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit sample \
  examples/quality/sampling/model_outputs.jsonl \
  --strategy uncertainty \
  --n 3 \
  --seed 13
```

Supported strategies are `random`, `stratified`, `diversity`,
`failure-heavy`, `judge-disagreement-heavy`, `uncertainty`, and `regression`.
Output can be JSON or JSONL.

## Boundary

Sampling prioritizes a subset of supplied records. It does not create coverage,
validate the model, or replace full review where the decision requires it.
Strategy quality depends on the fields present in the input.

[EvalKit docs index](../README.md) |
[Sampling guide](../sampling.md) |
[Package README](../../README.md)
