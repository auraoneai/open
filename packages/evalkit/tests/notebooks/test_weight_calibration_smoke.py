import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_prd_weight_calibration_notebook_source_smoke_runs():
    result = runpy.run_path(str(ROOT / "notebooks/rubric_weight_calibration.py"))
    assert "main" in result

