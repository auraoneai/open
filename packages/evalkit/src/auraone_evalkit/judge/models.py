"""Models for local judge calibration inputs and outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class JudgeOutput:
    judge_id: str
    item_id: str
    criterion_id: str
    score: float
    prompt_version: str = "default"

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any], *, line_no: int | None = None) -> "JudgeOutput":
        missing = [name for name in ("judge_id", "item_id", "criterion_id", "score") if row.get(name) is None]
        if missing:
            prefix = f"Line {line_no}: " if line_no is not None else ""
            raise ValueError(f"{prefix}missing required judge output field(s): {', '.join(missing)}")
        return cls(
            judge_id=str(row["judge_id"]),
            item_id=str(row["item_id"]),
            criterion_id=str(row["criterion_id"]),
            score=float(row["score"]),
            prompt_version=str(row.get("prompt_version", "default")),
        )


@dataclass(frozen=True)
class JudgeCalibrationResult:
    pairwise_agreement: dict[str, float]
    per_criterion_disagreement: dict[str, float]
    variance_by_judge: dict[str, float]
    prompt_sensitivity: dict[str, float]
    unstable_criteria: list[str]
    item_count: int
    judge_count: int

    def to_dict(self) -> dict:
        return {
            "pairwise_agreement": self.pairwise_agreement,
            "per_criterion_disagreement": self.per_criterion_disagreement,
            "variance_by_judge": self.variance_by_judge,
            "prompt_sensitivity": self.prompt_sensitivity,
            "unstable_criteria": self.unstable_criteria,
            "item_count": self.item_count,
            "judge_count": self.judge_count,
            "limitations": [
                "Saved judge outputs audit stability; they do not certify safety or replace human calibration.",
                "Tutorial fixtures are synthetic and not expert-authored.",
            ],
        }
