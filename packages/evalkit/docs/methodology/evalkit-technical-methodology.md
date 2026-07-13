# EvalKit Technical Methodology

EvalKit treats the human and LLM-judge layer of AI evaluation as versioned
release infrastructure: rubric contracts, supplied labels, quality
diagnostics, and evidence artifacts should be inspectable before an aggregate
score is trusted.

## Method

1. **Define the judgment contract.** Store rubric criteria in JSONL, a JSON
   array, or a canonical `rubric-spec` object with stable IDs, scoring types,
   weights, examples, edge cases, and disagreement risk.
2. **Validate structure.** Run `evalkit validate-rubric` before collecting or
   scoring labels so malformed fields fail early.
3. **Lint meaning.** Run `evalkit lint-rubric` to find deterministic authoring
   risks such as compound criteria, vague wording, unavailable context, and
   unclear score boundaries.
4. **Score supplied labels.** `evalkit score` normalizes each applicable label,
   applies criterion weights, reports missing labels, and computes per-output
   and aggregate results.
5. **Audit the judgment process.** Add reviewer agreement, saved judge
   calibration, drift, leakage, sampling, rubric diffs, or weight sensitivity
   when those signals affect interpretation.
6. **Generate evidence.** Produce JSON/JSONL for machines and Markdown or
   self-contained HTML for review. Preserve the command, input paths, source
   revision, and caller-owned metadata needed to reproduce the result.

## Determinism

EvalKit commands avoid hidden service state. Structured outputs use stable
field shapes and sorted serialization where implemented. Report generation
does not inject the current time, random IDs, network responses, or external
assets. A caller must provide timestamps or external checksums it wants to
claim.

Determinism means the same supported inputs and options can be inspected and
re-run. It does not mean that the rubric, labels, sample, or release decision
is correct.

## Interpretation

- A valid rubric is structurally acceptable, not automatically domain-valid.
- A lint-clean criterion still requires domain review.
- A score summarizes supplied labels; it does not create ground truth.
- Agreement and calibration metrics are sensitive to overlap, task mix, label
  balance, thresholds, and sample size.
- Leakage findings identify similarity in supplied corpora; absence of a
  finding is not proof of no contamination.
- A report communicates evidence and omissions; it is not a certification.

## Runtime And Data Boundary

Core workflows run in the local Python process and require no AuraOne account,
API key, tenant, or database. Judge calibration reads saved outputs and leakage
checks use local corpora. EvalKit does not run model inference, call judge
providers, assign reviewers, or upload evaluation data.

## Proof

The repository includes synthetic fixtures, unit and CLI tests, package builds,
and artifact-content verification. Run:

```bash
cd packages/evalkit
python -m pytest -p no:cacheprovider -q tests
python -m build
python scripts/verify_release.py dist
```

Passing those commands verifies the checked-out implementation and build
contents, not package publication or model quality.

[EvalKit docs index](../README.md) |
[Rubric schema](../schema/rubric-schema.md) |
[Reports](../reports/README.md)

