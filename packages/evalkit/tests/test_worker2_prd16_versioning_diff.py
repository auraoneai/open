import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.versioning.diff import diff_files, render_markdown


def test_versioning_diff_reports_seeded_scoring_changes():
    diff = diff_files(
        ROOT / "examples/quality/versioning/rubric_v1.jsonl",
        ROOT / "examples/quality/versioning/rubric_v2.jsonl",
    )

    assert diff["added"] == ["format"]
    assert diff["comparability_risk"] == "high"
    assert any(change["criterion_id"] == "grounding" for change in diff["scoring_impact_changes"])
    assert "Rubric Diff" in render_markdown(diff)
