from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from auraone_evalkit.schema.validate import load_rubric
from auraone_evalkit.scoring.engine import ScoringError, score_from_files, score_outputs
from auraone_evalkit.scoring.io import load_json_records


ROOT = Path(__file__).resolve().parents[2]
TUTORIAL = ROOT / "examples/tutorial"
CLI_ENV = {"PYTHONPATH": str(ROOT / "src")}


def test_tutorial_scores_match_expected_snapshot() -> None:
    result = score_from_files(
        rubric_path=TUTORIAL / "rubric.jsonl",
        responses_path=TUTORIAL / "model_outputs.jsonl",
        labels_path=TUTORIAL / "labels.jsonl",
    ).to_dict()
    expected = json.loads((TUTORIAL / "expected_scores.json").read_text(encoding="utf-8"))

    assert result["summary"] == expected["summary"]
    assert [
        {
            "output_id": output["output_id"],
            "score": output["score"],
            "passed": output["passed"],
            "applicable_weight": output["applicable_weight"],
            "weighted_points": output["weighted_points"],
            "missing_criteria": output["missing_criteria"],
        }
        for output in result["outputs"]
    ] == expected["outputs"]


def test_missing_criteria_are_reported_and_strict_fails() -> None:
    rubric = load_rubric(TUTORIAL / "rubric.jsonl")
    responses = load_json_records(TUTORIAL / "model_outputs.jsonl")[:1]
    labels = load_json_records(TUTORIAL / "labels.jsonl")[:3]

    result = score_outputs(rubric, responses, labels)
    assert result.summary["missing_label_count"] == 1
    assert result.outputs[0]["missing_criteria"] == ["code_review.tone"]

    with pytest.raises(ScoringError):
        score_outputs(rubric, responses, labels, strict=True)


def test_score_cli_writes_json_and_uses_default_labels(tmp_path: Path) -> None:
    out = tmp_path / "scores.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "auraone_evalkit.cli",
            "score",
            "--rubric",
            str(TUTORIAL / "rubric.jsonl"),
            "--responses",
            str(TUTORIAL / "model_outputs.jsonl"),
            "--out",
            str(out),
        ],
        check=True,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=CLI_ENV,
    )

    assert "Wrote json scores" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["summary"]["average_score"] == 0.645833


def test_score_cli_supports_csv(tmp_path: Path) -> None:
    out = tmp_path / "scores.csv"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "auraone_evalkit.cli",
            "score",
            "--rubric",
            str(TUTORIAL / "rubric.jsonl"),
            "--responses",
            str(TUTORIAL / "model_outputs.jsonl"),
            "--labels",
            str(TUTORIAL / "labels.jsonl"),
            "--format",
            "csv",
            "--out",
            str(out),
        ],
        check=True,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=CLI_ENV,
    )

    assert out.read_text(encoding="utf-8").splitlines()[0] == "output_id,score,passed,applicable_weight,weighted_points,missing_criteria"
