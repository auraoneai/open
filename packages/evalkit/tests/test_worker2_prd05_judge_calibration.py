import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.judge.calibrate import calibrate_file


def test_judge_calibration_detects_seeded_unstable_criterion():
    result = calibrate_file(ROOT / "examples/quality/judge/tutorial_judge_outputs.jsonl")

    assert result["judge_count"] == 2
    assert "evidence" in result["unstable_criteria"]
    assert result["pairwise_agreement"]["judge-a::judge-b"] < 1
    json.dumps(result)
