# Leakage Audit

EvalKit's leakage checker is a local audit aid for finding exact duplicates,
near-duplicate text, n-gram overlap, and duplicate groups in evaluation prompts
or items.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit leakage-check \
  examples/quality/leakage/tutorial_prompts.jsonl
```

Compare against another local corpus with:

```bash
evalkit leakage-check \
  eval-items.jsonl \
  --reference local-reference.jsonl \
  --format json \
  --out /tmp/leakage-audit.json
```

## Output

The command emits item-level findings, similarity scores, evidence snippets,
and duplicate groups. Structured output can be preserved directly or included
as evidence in an EvalKit report.

## Runtime And Evidence Boundary

- Inputs and optional references are local files supplied by the caller.
- The command does not require an AuraOne account, API key, tenant, or
  database.
- It does not search the web or access benchmark corpora that were not supplied
  as input.
- Similarity is a review signal, not proof of training contamination.
- A clean result is not proof that no contamination exists.
- The bundled tutorial prompts are synthetic and contain seeded overlap for
  deterministic tests.

[EvalKit docs index](README.md) |
[Focused leakage guide](leakage/README.md) |
[Package README](../README.md)
