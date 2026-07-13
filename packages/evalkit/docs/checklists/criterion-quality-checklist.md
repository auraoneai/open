# Criterion Quality Checklist

Use this checklist before collecting labels or treating a rubric as a scoring
contract.

## Identity And Scope

- [ ] The criterion has a stable, unique `criterion_id`.
- [ ] It evaluates one judgment rather than several combined checks.
- [ ] The task, domain, and intended decision are explicit.
- [ ] The reviewer can observe every fact needed to score it.

## Scoring

- [ ] The scoring type and allowed values are defined.
- [ ] Positive and negative anchors describe observable evidence.
- [ ] Intermediate scale values have clear boundaries when applicable.
- [ ] Edge cases explain how to handle partial, missing, or conflicting
  evidence.
- [ ] `applicable: false` has a documented meaning if non-applicable labels are
  allowed.

## Weight And Severity

- [ ] The weight reflects the intended aggregate contribution.
- [ ] Severity is distinct from weight and maps to a documented response.
- [ ] Threshold or gate behavior is explicit outside the criterion prose.
- [ ] Weight sensitivity has been reviewed for high-impact rubrics.

## Reviewer Reliability

- [ ] Examples cover likely disagreement cases.
- [ ] The criterion can be applied without private or assumed context.
- [ ] Reviewer overlap is planned if agreement will be reported.
- [ ] Adjudication rules are documented for consequential disagreements.
- [ ] Saved LLM-judge outputs will be calibrated before automated labels are
  trusted.

## Version And Evidence

- [ ] The rubric version is pinned with the evaluated inputs.
- [ ] Changes are reviewed with `evalkit diff-rubric`.
- [ ] Missing labels remain visible in scoring output.
- [ ] Reports state unavailable or omitted QA evidence.
- [ ] Synthetic examples are disclosed and are not presented as benchmark
  validation.

Run the deterministic checks after the human review:

```bash
evalkit validate-rubric rubric.jsonl
evalkit lint-rubric rubric.jsonl --fail-on warning
```

Passing the checklist and linter does not replace domain expertise. It makes
the judgment contract easier to inspect and challenge.

[EvalKit docs index](../README.md) |
[Rubric linter](../lint/rubric-linter.md) |
[Rubric schema](../schema/rubric-schema.md)

