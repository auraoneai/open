# Judge Calibration

Judge calibration reads saved judge outputs and computes local stability diagnostics without calling model providers.

Tutorial data in `examples/quality/judge/tutorial_judge_outputs.jsonl` is synthetic and not a benchmark.

## Output

The module reports:

- pairwise judge agreement
- per-criterion disagreement
- variance by judge
- prompt-version sensitivity
- unstable criteria

## CLI Hook

`auraone_evalkit.judge.cli.register(subparsers)` is ready for Worker 1 CLI integration as `evalkit judge-calibrate`.

Example:

```bash
evalkit judge-calibrate examples/quality/judge/tutorial_judge_outputs.jsonl
```

## Limitations

This audits judge behavior on saved data. It does not certify safety, replace human validation, or prove a judge is appropriate for production release gates.
