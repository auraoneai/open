# Leakage Audit

This is a compatibility mirror for the PRD 17 path `docs/leakage-audit.md`.
The canonical EvalKit documentation currently lives at [`leakage.md`](leakage.md)
and [`leakage/README.md`](leakage/README.md).

The leakage checker is a local audit aid for finding exact duplicates,
near-duplicate text, and n-gram overlap in synthetic/tutorial eval prompt
files or user-provided local corpora. It does not prove that an eval dataset
is uncontaminated, benchmark-grade, human-validated, or expert-authored.

## Quickstart

```bash
evalkit leakage-check examples/leakage/tutorial_prompts.jsonl
```

The tutorial prompt file is synthetic tutorial data with seeded duplicates for
deterministic smoke tests. The command runs fully offline and does not require
an AuraOne account, API key, hosted tenant, or customer data.

## Output

The checker emits item-level evidence snippets, similarity scores, duplicate
groups, and report-generator-compatible JSON so teams can review contamination
risk without sending data to an external service.

## Limitations

- The tool compares local inputs and optional local reference corpora only.
- Similarity findings are review signals, not proof of training contamination.
- The v0.1 implementation does not perform web search or private benchmark
  matching.
- Synthetic/tutorial examples are not validation data and should not be cited
  as an expert-authored benchmark.

See [`../../README.md`](../../README.md) and [`../../../opensource.md`](../../../opensource.md)
for the standalone EvalKit package context and the distinction from hosted
AuraOne SDKs.
