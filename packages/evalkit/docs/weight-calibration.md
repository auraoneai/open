# Rubric Weight Calibration

Weight calibration shows how aggregate scores change when rubric weights change. It is a rubric engineering aid, not proof that weights are correct.

## Quickstart

```bash
python notebooks/rubric_weight_calibration.py
```

The script reads `examples/weight_calibration/rubric_weight_scenarios.json` and prints deterministic scenario rankings.

## Interpretation

Use the output to spot high-leverage criteria, unstable rankings, and scenarios that require reviewer or stakeholder calibration.

## Data Status

The example scenarios are synthetic tutorial data only.
