# Human Data Failure Modes

Common failure patterns in rubric-based AI evaluation and annotation programs.
Use this catalog to decide which EvalKit checks or human review steps belong in
an evaluation plan.

| Failure mode | Observable signal | Consequence | Response |
| --- | --- | --- | --- |
| Compound criterion | One criterion asks for several independent judgments | Reviewers can agree on one part and disagree on another while producing one score | Split the criterion and re-run rubric linting |
| Vague scoring boundary | Terms such as "good," "clear," or "safe" lack observable anchors | Labels become reviewer-dependent | Add positive, negative, and edge-case examples |
| Missing context | A criterion depends on information not present in the review task | Reviewers guess or use inconsistent outside knowledge | Supply the evidence or remove the criterion |
| Silent rubric change | Wording, weight, severity, or threshold changes without a versioned diff | Scores across runs look comparable when they are not | Run `evalkit diff-rubric` and re-score a stable holdout |
| Sparse reviewer overlap | Too few items are labeled by multiple reviewers | Agreement estimates become unstable or impossible | Increase overlap before interpreting the metric |
| Reviewer drift | Score distributions or error relative to reference labels change across batches | Release movement can be confused with reviewer movement | Run drift analysis and inspect task mix and guidance changes |
| Uncalibrated LLM judge | Judge agreement or prompt sensitivity is unknown | Automated scores appear precise without stability evidence | Audit saved judge outputs and escalate unstable criteria |
| Missing labels hidden by aggregation | Some criteria have no label but an aggregate is still reported | Scores overstate evidence coverage | Inspect missing-label diagnostics or use strict scoring |
| Evaluation leakage | Duplicate or near-duplicate items appear across eval and reference corpora | Results can overstate generalization | Run local leakage checks and review matched evidence |
| Weight-dominated score | A small number of criteria control ranking | Aggregate movement reflects rubric design more than broad quality | Run weight calibration and report criterion-level scores |
| Unrepresentative sample | Review selection over- or under-samples important failures | Human conclusions do not match the full output set | Document sampling strategy and preserve selected-item rationale |
| Missing limitations | Reports omit unavailable agreement, drift, leakage, or provenance | Readers treat absence of evidence as a pass | List omitted evidence and block unsupported claims |

These are operational review patterns, not customer disclosures, benchmark
results, or proof that a specific dataset or reviewer pool has a problem.

[EvalKit docs index](../README.md) |
[Criterion quality checklist](../checklists/criterion-quality-checklist.md) |
[Technical methodology](../methodology/evalkit-technical-methodology.md)

