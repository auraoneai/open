# Rubric Weight Calibration

Weight calibration shows how criterion weights can change aggregate scores and model rankings.

Tutorial scenario: `examples/quality/calibration/rubric_weight_scenarios.json`.

Example:

```bash
evalkit calibrate-weights examples/quality/calibration/rubric_weight_scenarios.json
```

The result includes scenario scores, baseline ranking, changed-rank scenarios, and high-leverage criteria.

## Limitations

Weight sensitivity explains dependence on rubric design. It does not validate the rubric or certify release decisions.
