import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.adapters.inspect import inspect_score_record, to_inspect_sample


def test_inspect_adapter_maps_without_optional_dependency():
    row = {
        "item_id": "task-001",
        "prompt": "Summarize the release notes.",
        "expected_output": "A concise summary.",
        "criterion_id": "clarity",
        "synthetic": True,
    }

    sample = to_inspect_sample(row)
    score = inspect_score_record(row, 1.0, "matches rubric")

    assert sample["id"] == "task-001"
    assert sample["metadata"]["synthetic"] is True
    assert score["metadata"]["adapter"] == "inspect"
