# Judge Calibration

Judge calibration audits saved local judge outputs for agreement, criterion instability, judge variance, and prompt-version sensitivity. It does not call model providers and does not certify that model judges replace human validation.

## Quickstart

```bash
evalkit judge-calibrate examples/judge_calibration/tutorial_judge_outputs.jsonl
```

## Input Contract

Each JSONL row should include:

- `judge_id`
- `item_id`
- `criterion_id`
- `score`
- optional `prompt_version`

The tutorial fixture is synthetic and intentionally includes an unstable `evidence` criterion so reports have a deterministic warning.

## Escalation Guidance

Escalate to human calibration when pairwise agreement is low, a criterion is repeatedly unstable, prompt-version sensitivity changes outcomes, or the eval will affect launch, compensation, safety, compliance, or customer-facing claims.

## Limitations

- Saved judge outputs audit behavior; they do not create labels.
- Tutorial fixtures are not expert-authored or benchmark-grade.
- Agreement on synthetic examples does not prove production reliability.
