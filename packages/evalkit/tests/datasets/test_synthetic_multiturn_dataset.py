from pathlib import Path

from auraone_evalkit.scoring.engine import score_from_files
from auraone_evalkit.schema.validate import validate_rubric_file


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "datasets/synthetic-multiturn-eval-failures-v0.1"


def test_prd_synthetic_multiturn_dataset_validates_and_scores():
    assert not validate_rubric_file(DATASET / "rubric.jsonl")
    result = score_from_files(
        rubric_path=DATASET / "rubric.jsonl",
        responses_path=DATASET / "conversations.jsonl",
        labels_path=DATASET / "labels.jsonl",
    ).to_dict()
    assert result["summary"]["scored_outputs"] > 0
    assert result["summary"]["average_score"] >= 0
