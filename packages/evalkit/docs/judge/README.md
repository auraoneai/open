# Judge Calibration

Judge calibration audits saved LLM-judge outputs for agreement, criterion
instability, judge variance, and prompt-version sensitivity.

The command is for evaluation teams that already have judge outputs and need a
local diagnostic pass. It does not call model providers or generate new
labels.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit judge-calibrate \
  examples/quality/judge/tutorial_judge_outputs.jsonl
```

The result includes pairwise judge agreement, per-criterion disagreement,
variance by judge, prompt-version sensitivity, and unstable criteria.

## Limitations

The tutorial data is synthetic and not a benchmark. Agreement on saved examples
does not prove production reliability, safety, or suitability for a release
gate. Escalate unstable criteria and consequential decisions to human review.

[EvalKit docs index](../README.md) |
[Judge calibration guide](../judge-calibration.md) |
[Package README](../../README.md)
