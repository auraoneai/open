# Leakage Audit

The leakage checker finds duplicate or near-duplicate tutorial prompts in local files. It does not prove a dataset is uncontaminated.

## Quickstart

```bash
evalkit leakage-check examples/leakage/tutorial_prompts.jsonl
```

## Data Status

The tutorial prompt file is synthetic and contains an intentional duplicate for deterministic smoke tests.
