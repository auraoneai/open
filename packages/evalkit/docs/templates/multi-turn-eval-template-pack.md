# Multi-Turn Eval Template Pack

These templates are synthetic/tutorial scaffolds for teams building private multi-turn evals. They are not safety benchmarks and are not expert-authored validation assets.

## Templates

- Generic assistant quality.
- Code-review dialogue.
- Tool-use consistency.

## Turn-Level Vs Trajectory-Level Scoring

Turn-level scoring evaluates one assistant turn against visible constraints. Trajectory-level scoring evaluates the whole conversation: context retention, recovery after correction, and consistency across turns.

## Adapting A Template

1. Choose the template closest to the workflow.
2. Replace tutorial criteria with user-owned rubric criteria.
3. Add private examples and scoring levels.
4. Validate the rubric with `evalkit validate-rubric`.
5. Score synthetic or user-owned labels with `evalkit score`.

## Local Paths

- `src/auraone_evalkit/templates/multiturn/`
- `examples/multiturn/templates/`
- `datasets/synthetic-multiturn-eval-failures-v0.1/`

## Limitations

Public tutorial examples should not be reused as hidden eval items.
