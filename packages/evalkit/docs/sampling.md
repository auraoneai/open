# Model Output Sampling

Sampling strategies help select model outputs for follow-up human review under a fixed budget. Sampling is not a replacement for validation.

## Quickstart

```bash
evalkit sample examples/sampling/model_outputs.jsonl --strategy random --n 2 --seed 7
evalkit sample examples/sampling/model_outputs.jsonl --strategy failure-heavy --n 2 --seed 7
```

## Strategies

- random
- stratified
- diversity
- failure-heavy
- judge-disagreement-heavy
- uncertainty
- regression

When metadata is missing, use documented fallback behavior or choose a strategy that matches available fields.
