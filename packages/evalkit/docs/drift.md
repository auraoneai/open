# Reviewer Drift

The drift detector compares reviewer or criterion behavior across synthetic or user-owned batches. It is a local QA aid, not a reviewer performance certification.

## Quickstart

```bash
evalkit drift examples/drift/tutorial_batches.jsonl
```

## Interpretation

Treat drift warnings as prompts for review: inspect changed guidelines, reviewer assignment, task mix, and adjudication notes before changing production processes.

## Limitations

Small batches can create unstable signals. The tutorial fixture is synthetic and intentionally seeded with one drift pattern.
