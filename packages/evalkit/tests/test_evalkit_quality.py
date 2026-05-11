from pathlib import Path

from auraone_evalkit.agreement.metrics import agreement_report
from auraone_evalkit.drift.detector import drift_report
from auraone_evalkit.judge.calibration import calibrate_judge
from auraone_evalkit.io import read_json_or_jsonl
from auraone_evalkit.leakage.audit import audit_leakage
from auraone_evalkit.sampling.sampler import sample_outputs

ROOT = Path(__file__).resolve().parents[1]


def test_agreement_report():
    rows = read_json_or_jsonl(ROOT / "examples/quality/reviewer_labels.jsonl")
    assert agreement_report(rows)["percent_agreement"]["agreement"] == 1.0


def test_drift_report_flags_reviewer():
    rows = read_json_or_jsonl(ROOT / "examples/quality/drift_scores.jsonl")
    report = drift_report(rows)
    assert any(r["reviewer_id"] == "rev-a" for r in report["reviewers"])


def test_judge_calibration_reports_disagreement():
    rows = read_json_or_jsonl(ROOT / "examples/quality/judge_calibration.jsonl")
    report = calibrate_judge(rows)
    assert report["row_count"] == 2
    assert report["large_disagreements"]


def test_sampling_seed_is_deterministic():
    rows = read_json_or_jsonl(ROOT / "examples/tutorial/model_outputs.jsonl")
    assert sample_outputs(rows, 1, seed=7) == sample_outputs(rows, 1, seed=7)


def test_leakage_detects_duplicate_prompt():
    train = [{"id":"t1","prompt":"Same prompt"}]
    eval_rows = [{"id":"e1","prompt":"same   prompt"}]
    assert audit_leakage(train, eval_rows)["duplicate_count"] == 1
