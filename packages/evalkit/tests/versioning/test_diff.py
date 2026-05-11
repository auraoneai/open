from pathlib import Path

from auraone_evalkit.versioning.diff import diff_files


ROOT = Path(__file__).resolve().parents[2]


def test_prd_rubric_diff_reports_comparability_risk():
    diff = diff_files(ROOT / "examples/versioning/rubric_v1.jsonl", ROOT / "examples/versioning/rubric_v2.jsonl")
    assert diff["comparability_risk"] in {"low", "medium", "high"}

