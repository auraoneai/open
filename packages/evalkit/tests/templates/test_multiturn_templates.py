from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_prd_multiturn_templates_are_machine_readable():
    paths = sorted((ROOT / "examples/multiturn/templates").glob("*.yaml"))
    assert len(paths) >= 3
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["template_id"]
        assert data["expected_inputs"]
