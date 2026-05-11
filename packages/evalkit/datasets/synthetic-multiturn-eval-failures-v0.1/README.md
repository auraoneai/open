# Synthetic Multi-Turn Eval Failures v0.1 Dataset Card

This dataset is synthetic tutorial data for exercising EvalKit multi-turn workflows. It is not expert-authored, not human-validated, not benchmark-grade, and not a safety certification.

## Intended Use

Use this package to test loading, scoring, report rendering, judge calibration examples, and multi-turn template adaptation with safe tutorial conversations.

## Out Of Scope Use

Do not use this dataset as a safety benchmark, refusal benchmark, public leaderboard, customer validation set, or substitute for domain-expert review.

## Coverage

The synthetic conversations cover eight benign failure categories:

- instruction_drift
- clarification_miss
- hallucinated_tool_result
- conflicting_constraints
- context_loss
- inconsistent_claim
- recovery_after_correction
- ambiguity_exploitation

## Files

- `conversations.jsonl`: eight synthetic multi-turn conversations.
- `rubric.jsonl`: tutorial rubric for scoring the conversations.
- `labels.jsonl`: synthetic tutorial labels for deterministic scoring.
- `LICENSE`: MIT-compatible fixture license.

## Synthetic Generation Process

Examples were hand-written as low-risk assistant-quality scenarios. They avoid operationally harmful instructions, customer data, reviewer identity data, and claims of expert validation.

## Limitations

- Small sample count intended for tests and tutorials.
- Public fixture data should not be reused as a hidden eval.
- Categories are illustrative and require adaptation for private production evals.

## Citation

Cite AuraOne EvalKit documentation when adapting this dataset structure.
