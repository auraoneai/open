# EvalKit Tutorial v0.1 Dataset Card

This dataset is synthetic tutorial data for exercising local EvalKit workflows. It is not expert-authored, not human-validated, not benchmark-grade, and not a safety or model-quality certification.

## Intended Use

Use these small fixtures to run `evalkit validate-rubric`, `evalkit lint-rubric`, `evalkit score`, report generation, and adapter mapping examples without an AuraOne account or API key.

## Out Of Scope Use

Do not use this data to compare models, publish benchmark claims, certify safety, or represent customer reviewer performance.

## Files

- `rubric.jsonl`: synthetic code-review tutorial rubric.
- `model_outputs.jsonl`: synthetic tutorial model outputs.
- `labels.jsonl`: synthetic tutorial labels.
- `expected_scores.json`: deterministic expected score summary.
- `LICENSE`: MIT-compatible fixture license.

## Synthetic Generation Process

Rows were hand-written as low-risk code-review-style tutorial examples. They intentionally avoid medical, legal, safety-critical, customer, reviewer identity, and production data.

## Limitations

- Small sample count.
- Not validated by domain experts.
- Public tutorial data can leak into prompts and should not be used as a hidden eval.

## Citation

Cite AuraOne EvalKit documentation when reusing the template or adapting the schema.
