from pathlib import Path

from auraone_evalkit.drift.detector import detect_drift, load_drift_records


ROOT = Path(__file__).resolve().parents[2]


def test_prd_drift_detector_finds_seeded_warning():
    report = detect_drift(load_drift_records(ROOT / "examples/drift/tutorial_batches.jsonl"))
    assert report.batch_warnings
