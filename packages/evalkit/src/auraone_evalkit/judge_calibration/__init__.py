"""Compatibility namespace for PRD 05 judge calibration paths.

The maintained implementation lives in :mod:`auraone_evalkit.judge`.
This wrapper preserves the initially documented module layout.
"""

from auraone_evalkit.judge.calibrate import calibrate_file, calibrate_judges, load_judge_outputs
from auraone_evalkit.judge.models import JudgeCalibrationResult, JudgeOutput

__all__ = [
    "JudgeCalibrationResult",
    "JudgeOutput",
    "calibrate_file",
    "calibrate_judges",
    "load_judge_outputs",
]
