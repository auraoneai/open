"""Input and output structures for reviewer drift detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class DriftRecord:
    reviewer_id: str
    item_id: str
    criterion_id: str
    batch_id: str
    score: float
    gold_score: float | None = None

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any], *, line_no: int | None = None) -> "DriftRecord":
        score = row.get("score", row.get("value"))
        missing = [
            name
            for name, candidate in (
                ("reviewer_id", row.get("reviewer_id", row.get("annotator_id"))),
                ("item_id", row.get("item_id")),
                ("criterion_id", row.get("criterion_id")),
                ("batch_id", row.get("batch_id", row.get("timestamp"))),
                ("score", score),
            )
            if candidate is None
        ]
        if missing:
            prefix = f"Line {line_no}: " if line_no is not None else ""
            raise ValueError(f"{prefix}missing drift field(s): {', '.join(missing)}")
        gold = row.get("gold_score", row.get("gold_label", row.get("consensus_score")))
        return cls(
            reviewer_id=str(row.get("reviewer_id", row.get("annotator_id"))),
            item_id=str(row["item_id"]),
            criterion_id=str(row["criterion_id"]),
            batch_id=str(row.get("batch_id", row.get("timestamp"))),
            score=float(score),
            gold_score=float(gold) if gold is not None else None,
        )


@dataclass(frozen=True)
class DriftReport:
    reviewer_drift: dict[str, dict]
    criterion_instability: dict[str, dict]
    batch_warnings: list[dict]

    def to_dict(self) -> dict:
        return {
            "reviewer_drift": self.reviewer_drift,
            "criterion_instability": self.criterion_instability,
            "batch_warnings": self.batch_warnings,
            "limitations": [
                "Drift warnings are QA triage signals, not reviewer discipline decisions.",
                "Synthetic tutorial drift does not prove real reviewer quality.",
            ],
        }
