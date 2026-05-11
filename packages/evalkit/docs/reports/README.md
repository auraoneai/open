# Eval Reports

The report generator turns local EvalKit outputs into Markdown, HTML, or JSON. It is intentionally static and works without a web app.

Tutorial input lives at `examples/quality/reports/tutorial_input.json` and is synthetic.

Example:

```bash
evalkit report --input examples/quality/reports/tutorial_input.json --out report.md
evalkit report --input examples/quality/reports/tutorial_input.json --out report.html
```

Reports include executive summary, rubric coverage, score breakdown, unstable criteria, agreement, drift, limitations, and explicit synthetic/tutorial disclosure when present.

## Limitations

Generated reports communicate evidence and gaps. They do not create validation status, safety certification, or expert-authored benchmark claims.
