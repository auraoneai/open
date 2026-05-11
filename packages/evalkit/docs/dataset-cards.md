# Dataset Cards

Dataset cards document eval and robotics datasets with visible data-status disclosure. The generator is a documentation helper, not a validation stamp.

## Quickstart

```bash
evalkit dataset-card --dataset-name "EvalKit Synthetic Tutorial Dataset" --license MIT --out /tmp/eval-card.md
```

The Python generator module also supports YAML or JSON metadata through `auraone_evalkit.cards.generator.load_metadata` and `generate_card`.

## Required Metadata

- Synthetic or human/expert status.
- Intended use and out-of-scope use.
- Task domain and rubric design.
- Scoring and validation method.
- Leakage risk and limitations.
- License and citation.

Robotics cards should also include embodiment, sensors, task, environment, failure modes, and privacy.

## Publication Checklist

- Confirm the top paragraph states whether data is synthetic/tutorial.
- Confirm no benchmark, safety, legal, medical, or customer claim appears without evidence.
- Confirm license and citation are explicit.
- Confirm private reviewer identities and customer data are absent.
