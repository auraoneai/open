import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "examples/quality/synthetic_multiturn"


def _load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_synthetic_multiturn_dataset_has_disclosure_and_categories():
    readme = (DATASET / "README.md").read_text()
    conversations = _load_jsonl(DATASET / "conversations.jsonl")
    rubric = _load_jsonl(DATASET / "rubric.jsonl")
    labels = _load_jsonl(DATASET / "labels.jsonl")

    assert "not expert-authored, not human-validated, and not a benchmark" in readme
    assert len({row["category"] for row in conversations}) >= 8
    assert all(row["synthetic"] for row in conversations + rubric + labels)
    assert {row["criterion_id"] for row in rubric} >= {"follow_instructions", "use_context", "format"}
