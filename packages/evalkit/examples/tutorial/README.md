# EvalKit Tutorial Data

This directory contains synthetic tutorial data for exercising AuraOne EvalKit v0.1. It is not expert-authored, not human-validated, not benchmark-grade, and not suitable for publishing model comparisons.

The examples use a low-risk code-review-style task:

- `rubric.jsonl`: four valid rubric criteria.
- `model_outputs.jsonl`: three synthetic model outputs.
- `labels.jsonl`: synthetic per-criterion labels for the three outputs.
- `expected_scores.json`: deterministic expected scorer output.

Run from `opensource/evalkit`:

```bash
evalkit validate-rubric examples/tutorial/rubric.jsonl
evalkit lint-rubric examples/tutorial/rubric.jsonl
evalkit score --rubric examples/tutorial/rubric.jsonl --responses examples/tutorial/model_outputs.jsonl --labels examples/tutorial/labels.jsonl --out /tmp/evalkit-tutorial-scores.json
```

