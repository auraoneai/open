# Dataset Cards

Generate reviewable Markdown documentation for eval or robotics datasets with
visible data-status, intended-use, validation, leakage-risk, and limitation
fields.

## Quickstart

From `packages/evalkit/`:

```bash
evalkit card init \
  --type eval \
  --metadata examples/quality/cards/eval/meta.yaml \
  --out /tmp/eval-dataset-card.md

evalkit card init \
  --type robotics \
  --metadata examples/quality/cards/robotics/meta.yaml \
  --out /tmp/robotics-dataset-card.md
```

Generated cards place synthetic and not-human-validated disclosures near the
top when those values are present. They also cover intended use, out-of-scope
use, generation or collection method, validation, leakage risk, limitations,
license, and citation.

## Boundary

This command is a documentation generator. It does not inspect raw data,
validate factual metadata, grant permission to use a dataset, or create a
quality or safety certification.

[EvalKit docs index](../README.md) |
[Dataset card guide](../dataset-cards.md) |
[Package README](../../README.md)
