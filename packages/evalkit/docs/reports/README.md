# Eval Reports

Turn local EvalKit score output or a report input object into a portable
evidence artifact for model-quality reviews, CI records, or release
discussions.

The generator emits deterministic Markdown, self-contained Proofline HTML, or
normalized `auraone.evalkit.report.v1` JSON without a web app or network
dependency.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit report \
  --input examples/reports/tutorial_input.json \
  --out /tmp/evalkit-report.md

evalkit report \
  --input examples/reports/tutorial_input.json \
  --out /tmp/evalkit-report.html

evalkit report \
  --input examples/reports/tutorial_input.json \
  --format json \
  --out /tmp/evalkit-report.contract
```

Reports can include identity, source and generation metadata, an executive
decision, summary metrics, quality gates, findings, evidence, rubric coverage,
score breakdown, unstable criteria, agreement, drift, leakage, limitations,
omitted evidence, a reproduction command, EvalKit version, and caller-supplied
checksums.

See the [v1 report contract](../reports.md) for supported status values,
deterministic rendering guarantees, input normalization, and a complete
example.

## Boundary

The HTML file contains embedded CSS, no JavaScript, and no remote assets. The
generator does not invent timestamps, external checksums, validation status,
or certification. The tutorial report is synthetic.

[EvalKit docs index](../README.md) |
[Package README](../../README.md)
