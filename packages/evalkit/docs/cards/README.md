# Dataset Cards

Dataset cards document eval and robotics datasets with visible data-status disclosure.

Tutorial metadata lives under:

- `examples/quality/cards/eval/meta.yaml`
- `examples/quality/cards/robotics/meta.yaml`

Example:

```bash
evalkit card init --type eval --metadata examples/quality/cards/eval/meta.yaml --out README.md
evalkit card init --type robotics --metadata examples/quality/cards/robotics/meta.yaml --out README.md
```

The generated card places synthetic/not-validated status near the top and includes intended use, out-of-scope use, generation or collection method, validation, leakage risk, limitations, license, and citation.

## Limitations

This is a documentation generator. It is not a validation stamp and does not certify the data.
