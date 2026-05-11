import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.drift.detector import detect_drift, load_drift_records


def test_drift_detector_flags_seeded_reviewer():
    records = load_drift_records(ROOT / "examples/quality/drift/tutorial_batches.jsonl")
    report = detect_drift(records, reviewer_threshold=0.35)
    result = report.to_dict()

    assert result["reviewer_drift"]["drifted-reviewer"]["status"] == "warning"
    assert result["reviewer_drift"]["stable-reviewer"]["status"] == "stable"
    assert any(warning["id"] == "drifted-reviewer" for warning in result["batch_warnings"])
