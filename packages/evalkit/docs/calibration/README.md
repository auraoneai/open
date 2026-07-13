# Rubric Weight Calibration

Weight calibration helps rubric authors and evaluation engineers see how
criterion-weight choices change aggregate model scores and rankings.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit weight-calibrate \
  examples/quality/calibration/rubric_weight_scenarios.json
```

The result identifies baseline rankings, changed-rank scenarios, and
high-leverage criteria. Use it before treating a weighted aggregate as a stable
release gate.

## Data And Decision Boundary

The bundled scenario is synthetic. Weight sensitivity explains dependence on
rubric design; it does not prove that a weight is correct, validate the rubric,
or certify a release decision.

[EvalKit docs index](../README.md) |
[Weight calibration guide](../weight-calibration.md) |
[Package README](../../README.md)
