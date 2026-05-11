# Rubric Schema

AuraOne EvalKit rubric files are JSONL rows or a JSON array of row objects. The canonical machine-readable schema is `src/auraone_evalkit/schema/rubric.schema.json`.

The schema is local and does not require hosted AuraOne services. Tutorial examples using the schema are synthetic and not expert-authored, human-validated, benchmark-grade, or safety-certified.

## Required Fields

| Field | Type | Description |
| --- | --- | --- |
| `criterion_id` | string | Stable lowercase identifier such as `code_review.correctness`. |
| `domain` | string | Domain or tutorial namespace, such as `code_review_tutorial`. |
| `task_type` | string | Task family the criterion applies to. |
| `criterion` | string | One observable scoring criterion. |
| `weight` | number | Criterion weight, greater than `0` and less than or equal to `1`. |
| `severity` | string | One of `info`, `warning`, or `error`. |
| `scoring_type` | string | One of `binary`, `scale_0_1`, `scale_0_2`, `scale_0_3`, `scale_0_5`. |
| `examples` | array | At least one object with `positive` and `negative` examples. |
| `edge_cases` | array | Boundary cases that clarify how to apply the criterion. |
| `disagreement_risk` | object | Includes `level` (`low`, `medium`, `high`) and `notes`. |

## Optional Fields

| Field | Type | Description |
| --- | --- | --- |
| `tags` | array | Strings such as `synthetic` and `tutorial`. |
| `version` | string | Rubric or row version. |
| `parent_criterion_id` | string | Parent criterion for future hierarchy or diffs. |
| `policy_source` | string | Source policy or public standard, if applicable. |
| `data_source` | string | Data source disclosure. Tutorial rows should say they are synthetic. |
| `notes` | string | Human-readable implementation notes. |
| `score_levels` | object | Score boundary descriptions for scale criteria. |

## Valid JSONL Row

```json
{"criterion_id":"code_review.actionability","domain":"code_review_tutorial","task_type":"code_review_response","criterion":"Provide a concrete next step such as a test case, code change, or validation check that follows from the concern.","weight":0.2,"severity":"warning","scoring_type":"scale_0_2","examples":[{"positive":"Suggests adding a regression test for an empty input list before merging.","negative":"Says fix this without describing the test or change needed."}],"edge_cases":["A next step may be concise when the correctness concern is already specific."],"disagreement_risk":{"level":"low","notes":"Actionability is present when a concrete test, code change, or check is named."},"tags":["synthetic","tutorial"],"version":"0.1.0","data_source":"synthetic tutorial fixture","score_levels":{"0":"No concrete next step.","1":"Partial or generic next step.","2":"Concrete test, code change, or validation check."}}
```

## Invalid Example

```json
{"criterion_id":"Correctness","criterion":"Good answer","weight":"high"}
```

This row fails because:

- `criterion_id` is not lowercase schema-compatible.
- Required fields such as `domain`, `task_type`, `severity`, `scoring_type`, `examples`, `edge_cases`, and `disagreement_risk` are missing.
- `criterion` is too vague and too short.
- `weight` is not numeric.

## Validation Output

`evalkit validate-rubric` reports row-level issues:

```bash
evalkit validate-rubric examples/tutorial/rubric.jsonl --format json
```

Each issue includes:

- `path`
- `row_number`
- `field`
- `error`
- `suggested_fix`

## Scoring Semantics

For every output and criterion:

1. The raw label score is normalized by `scoring_type`.
2. The normalized score is multiplied by `weight`.
3. Applicable weighted points are divided by the applicable rubric weight.
4. Missing labels are reported as `missing_criteria`. In strict mode, missing labels fail scoring.
5. Non-applicable labels are excluded from the denominator.

This is deterministic local aggregation. EvalKit does not create labels, call LLM judges, or call hosted AuraOne APIs.
