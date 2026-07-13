# EvalKit Synthetic Tutorial Report

**Decision:** Review required
**Disclosure:** Synthetic tutorial data; not expert-authored, not human-validated, and not a benchmark.

## Summary

This report demonstrates EvalKit report rendering on synthetic tutorial data.

- **Criteria:** 4
- **Items:** 3

## Quality Gates

- **Model A score threshold:** Passed - Tutorial model A exceeds the configured threshold.
- **Reviewer agreement:** Warning - Agreement remains below the tutorial target.

## Findings

- **Review - Specificity criterion is unstable:** Reviewer labels diverged on evidence specificity.

## Evidence

- **Reviewer agreement output:** `{"krippendorff_alpha": 0.0, "percent_agreement": 0.5}`

## Executive Summary

This report demonstrates EvalKit report rendering on synthetic tutorial data.

## Rubric Coverage

- **criteria:** 4
- **items:** 3

## Score Breakdown

- **tutorial-model-a:** 0.78
- **tutorial-model-b:** 0.42

## Unstable Criteria

- code_review.specificity

## Agreement

- **percent_agreement:** 0.5
- **krippendorff_alpha:** 0.0

## Drift Warnings

- **warnings:** 1
- **affected_reviewer:** reviewer-a

## Leakage Warnings

- **status:** not_run
- **detail:** No reference corpus was supplied.

## Limitations

- Synthetic tutorial data only.
- Not expert-authored, not human-validated, and not a benchmark.

## Reproduce

```bash
evalkit report --input examples/reports/tutorial_input.json --out tutorial_report.html
```

- **report_input:** `examples/reports/tutorial_input.json`

## Missing Or Omitted Evidence

No required report evidence is marked as omitted.

## Artifact Metadata

- **Report schema:** `auraone.evalkit.report.v1`
- **EvalKit version:** `0.3.0`
- **Input SHA-256:** `d7f5650017043480127dc50c02ee8db397c7251886ce44e6de2cc1e4b907c61c`
- **Generated at:** `2026-07-12T19:30:00Z`
- **Run ID:** `tutorial-run-001`
