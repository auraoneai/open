# Leakage Audit

Use the leakage checker to find exact duplicates, near-duplicate text, n-gram
overlap, and duplicate clusters in local evaluation items.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit leakage-check \
  examples/quality/leakage/tutorial_prompts.jsonl
```

Pass `--reference path/to/reference.jsonl` to compare the primary items against
another local corpus you own.

## Output

The command emits item-level findings, similarity scores, evidence snippets,
and duplicate groups in deterministic structured output.

## Boundary

The checker runs offline over supplied files. It does not search the web,
access private benchmark corpora, or prove that an evaluation is free from
training contamination. Similarity findings are review signals.

The bundled prompts are synthetic and contain seeded overlap for deterministic
tests.

[EvalKit docs index](../README.md) |
[Leakage audit guide](../leakage-audit.md) |
[Package README](../../README.md)
