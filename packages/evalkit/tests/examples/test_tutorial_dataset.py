from __future__ import annotations

import json
from pathlib import Path

from auraone_evalkit.schema.validate import load_rubric
from auraone_evalkit.scoring.engine import score_from_files


ROOT = Path(__file__).resolve().parents[2]
TUTORIAL = ROOT / "examples/tutorial"


def test_tutorial_dataset_declares_synthetic_status() -> None:
    readme = (TUTORIAL / "README.md").read_text(encoding="utf-8").lower()
    assert "synthetic tutorial data" in readme
    assert "not expert-authored" in readme
    assert "not benchmark-grade" in readme

    for row in (json.loads(line) for line in (TUTORIAL / "model_outputs.jsonl").read_text(encoding="utf-8").splitlines()):
        assert row["metadata"]["dataset"] == "synthetic tutorial"
        assert row["metadata"]["benchmark"] is False


def test_tutorial_files_stay_in_sync() -> None:
    rubric = load_rubric(TUTORIAL / "rubric.jsonl")
    result = score_from_files(
        rubric_path=TUTORIAL / "rubric.jsonl",
        responses_path=TUTORIAL / "model_outputs.jsonl",
        labels_path=TUTORIAL / "labels.jsonl",
    )

    assert len(rubric) == 4
    assert result.summary["scored_outputs"] == 3
    assert result.summary["missing_label_count"] == 0

