import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.calibration.weights import analyze_weight_scenarios, load_weight_scenarios


def test_weight_calibration_detects_ranking_instability():
    data = load_weight_scenarios(ROOT / "examples/quality/calibration/rubric_weight_scenarios.json")
    result = analyze_weight_scenarios(data)

    assert result["ranking_instability"] is True
    assert "grounding-heavy" in result["changed_ranking_scenarios"]
    assert result["high_leverage_criteria"][0]["criterion_id"] == "grounding"
