# AuraOne Open

Open tools for the human-judgment layer of AI evaluation. Rubric authoring, scoring, judge calibration, reviewer agreement, drift detection, leakage audits, dataset documentation, and robotics review data — local, inspectable, and runnable without an AuraOne account.

The thesis behind this release: the best evals will stay private, but the standards for building trustworthy evals should not. Read it in full at [resources/writing/measuring-human-judgment-layer.md](resources/writing/measuring-human-judgment-layer.md).

## What's in this repository

| Component | What it is |
| --- | --- |
| [`packages/evalkit/`](packages/evalkit/) | `auraone-evalkit` Python package + `evalkit` CLI for rubric validation, scoring, judge calibration, reviewer agreement, drift, leakage audits, sampling, and versioning. |
| [`robotics-reviewkit/`](robotics-reviewkit/) | Schemas, exporters, taxonomy, and a static viewer for teleop review and failure data. Includes LeRobot and RLDS/OpenX export bridges. |
| [`resources/buying-toolkit/`](resources/buying-toolkit/) | Templates and checklists for teams buying human-data work: SOWs, RFPs, SLAs, vendor comparison, pilot design, reviewer certification, and program playbook. |
| [`resources/writing/`](resources/writing/) | The thesis posts behind this release. |
| [`docs/PRD/`](docs/PRD/) | The audit trail from source to v0.1.0. |

## Quick start

```bash
pip install auraone-evalkit

evalkit validate-rubric path/to/rubric.jsonl
evalkit lint-rubric path/to/rubric.jsonl
evalkit score --rubric rubric.jsonl --responses outputs.jsonl --out scores.json
```

Full CLI reference: [`packages/evalkit/README.md`](packages/evalkit/README.md).

## What this release is not

- Not an expert-authored benchmark. The tutorial datasets included here are synthetic and exist to make the tooling runnable.
- Not real robotics data. The example episodes in `robotics-reviewkit/examples/` are mock metadata.
- Not a hosted AuraOne service. EvalKit runs locally with no API key, no tenant, no database.

These limits are intentional. The release ships the standards, not the dataset.

## Related links

- AuraOne Open landing page: https://auraone.ai/open
- Resource hub: https://auraone.ai/resources
- Hosted AuraOne: https://auraone.ai

## License

MIT — see [LICENSE](LICENSE).
