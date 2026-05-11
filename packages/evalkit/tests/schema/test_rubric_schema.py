from __future__ import annotations

import json
from pathlib import Path

from auraone_evalkit.schema.validate import load_rubric, validate_rubric_file


ROOT = Path(__file__).resolve().parents[2]


def test_tutorial_rubric_validates() -> None:
    path = ROOT / "examples/tutorial/rubric.jsonl"
    assert validate_rubric_file(path) == []
    rubric = load_rubric(path)
    assert [criterion.criterion_id for criterion in rubric] == [
        "code_review.correctness",
        "code_review.specificity",
        "code_review.actionability",
        "code_review.tone",
    ]


def test_invalid_rubric_reports_row_level_errors(tmp_path: Path) -> None:
    path = tmp_path / "invalid.jsonl"
    path.write_text(json.dumps({"criterion_id": "Bad ID", "criterion": "Good", "weight": "high"}) + "\n", encoding="utf-8")

    issues = validate_rubric_file(path)

    fields = {issue.field for issue in issues}
    assert "criterion_id" in fields
    assert "weight" in fields
    assert "domain" in fields
    assert all(issue.row_number == 1 for issue in issues if issue.row_number is not None)
    assert any(issue.suggested_fix for issue in issues)


def test_empty_rubric_fails(tmp_path: Path) -> None:
    path = tmp_path / "empty.jsonl"
    path.write_text("", encoding="utf-8")

    issues = validate_rubric_file(path)

    assert len(issues) == 1
    assert issues[0].error == "File is empty."


def test_json_array_rubric_is_supported(tmp_path: Path) -> None:
    source = ROOT / "examples/tutorial/rubric.jsonl"
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
    path = tmp_path / "rubric.json"
    path.write_text(json.dumps(rows), encoding="utf-8")

    assert validate_rubric_file(path) == []
    assert len(load_rubric(path)) == 4

