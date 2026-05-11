from pathlib import Path

from auraone_evalkit.judge.calibrate import calibrate_file


ROOT = Path(__file__).resolve().parents[2]


def test_prd_judge_calibration_fixture_reports_unstable_criteria():
    report = calibrate_file(ROOT / "examples/judge_calibration/tutorial_judge_outputs.jsonl")
    assert "unstable_criteria" in report

