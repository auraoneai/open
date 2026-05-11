# LM Eval Harness Adapter

The lm-eval adapter builds simple task config dictionaries and normalizes result rows. Importing `auraone_evalkit.adapters.lm_eval` does not require `lm_eval`.

Tutorial config: `examples/quality/adapters/lm_eval/auraone_tutorial.yaml`.

## Limitations

EvalKit rubric workflows are not the same as classic exact-match or multiple-choice lm-eval tasks. Use the adapter to compare workflow outputs, not to claim a new public benchmark.
