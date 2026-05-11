from pathlib import Path

from auraone_evalkit.schema.validate import validate_rubric_file
from auraone_evalkit.scoring.engine import score_eval
from auraone_evalkit.linting.rules import lint_rubric
from auraone_evalkit.io import read_json_or_jsonl

ROOT = Path(__file__).resolve().parents[1]


def test_validate_tutorial_rubric():
    result = validate_rubric_file(ROOT / "examples/tutorial/rubric.jsonl")
    assert result["valid"] is True
    assert result["criteria"] == 4


def test_lint_tutorial_rubric_has_no_errors():
    rows = read_json_or_jsonl(ROOT / "examples/tutorial/rubric.jsonl")
    result = lint_rubric(rows)
    assert result["error_count"] == 0


def test_score_tutorial_expected_math():
    result = score_eval(str(ROOT / "examples/tutorial/rubric.jsonl"), str(ROOT / "examples/tutorial/model_outputs.jsonl"), str(ROOT / "examples/tutorial/labels.jsonl"))
    assert round(result["overall_score"], 4) == 0.6458
    assert result["missing_labels"] == []
