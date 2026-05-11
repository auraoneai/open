"""Typed models for AuraOne EvalKit rubric rows."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SEVERITIES = {"info", "warning", "error", "low", "medium", "high", "critical"}
SCORING_TYPES = {"binary", "graded", "ordinal", "scale_0_1", "scale_0_2", "scale_0_3", "scale_0_5"}
DISAGREEMENT_LEVELS = {"low", "medium", "high"}


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    row_number: int | None
    field: str | None
    error: str
    suggested_fix: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "row_number": self.row_number,
            "field": self.field,
            "error": self.error,
            "suggested_fix": self.suggested_fix,
        }


@dataclass(frozen=True)
class RubricCriterion:
    criterion_id: str
    domain: str
    task_type: str
    criterion: str
    weight: float
    severity: str
    scoring_type: str
    examples: Any
    edge_cases: list[str] = field(default_factory=list)
    disagreement_risk: Any = field(default_factory=lambda: {"level": "medium", "notes": "not specified"})
    tags: list[str] = field(default_factory=list)
    version: str | None = None
    parent_criterion_id: str | None = None
    policy_source: str | None = None
    data_source: str | None = None
    notes: str | None = None
    score_levels: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, row: dict[str, Any]) -> "RubricCriterion":
        return cls(
            criterion_id=str(row["criterion_id"]),
            domain=str(row["domain"]),
            task_type=str(row["task_type"]),
            criterion=str(row["criterion"]),
            weight=float(row["weight"]),
            severity=str(row["severity"]),
            scoring_type=str(row["scoring_type"]),
            examples=row["examples"],
            edge_cases=list(row.get("edge_cases", [])),
            disagreement_risk=row.get("disagreement_risk", {"level": "medium", "notes": "not specified"}),
            tags=list(row.get("tags", [])),
            version=row.get("version"),
            parent_criterion_id=row.get("parent_criterion_id"),
            policy_source=row.get("policy_source"),
            data_source=row.get("data_source"),
            notes=row.get("notes"),
            score_levels=dict(row.get("score_levels", {})),
        )

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "RubricCriterion":
        return cls.from_mapping(row)

    @property
    def max_score(self) -> float:
        if self.scoring_type in {"binary", "graded", "ordinal", "scale_0_1"}:
            return 1.0
        return float(str(self.scoring_type).rsplit("_", 1)[1])

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
