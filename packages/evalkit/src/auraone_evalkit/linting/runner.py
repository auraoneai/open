"""Rubric lint runner."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from auraone_evalkit.linting.rules import RULES, RuleContext
from auraone_evalkit.schema.validate import validate_rubric_rows
from auraone_evalkit.scoring.io import load_json_records


@dataclass(frozen=True)
class LintFinding:
    rule_id: str
    severity: str
    criterion_id: str | None
    row_number: int | None
    message: str
    rationale: str
    suggested_fix: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "criterion_id": self.criterion_id,
            "row_number": self.row_number,
            "message": self.message,
            "rationale": self.rationale,
            "suggested_fix": self.suggested_fix,
        }


def lint_rubric(path: Path | str, disabled_rules: set[str] | None = None) -> list[LintFinding]:
    disabled = disabled_rules or set()
    try:
        rows = load_json_records(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [
            LintFinding(
                rule_id="R000_PARSE",
                severity="error",
                criterion_id=None,
                row_number=None,
                message=f"Could not parse rubric: {exc}",
                rationale="The linter needs JSONL rows or a JSON array before it can inspect criteria.",
                suggested_fix="Fix the file path or JSON syntax.",
            )
        ]

    findings: list[LintFinding] = []
    if "R000_SCHEMA" not in disabled:
        for issue in validate_rubric_rows(rows, str(path)):
            findings.append(
                LintFinding(
                    rule_id="R000_SCHEMA",
                    severity="error",
                    criterion_id=_criterion_id(rows, issue.row_number),
                    row_number=issue.row_number,
                    message=issue.error,
                    rationale="Rubric rows must satisfy the v0.1 schema before they can be scored reliably.",
                    suggested_fix=issue.suggested_fix,
                )
            )
    for index, row in enumerate(rows, start=1):
        context = RuleContext(row=row, row_number=index, all_rows=rows)
        for rule_id, rule in RULES.items():
            if rule_id in disabled:
                continue
            for raw in rule(context):
                findings.append(
                    LintFinding(
                        rule_id=rule_id,
                        severity=raw["severity"],
                        criterion_id=row.get("criterion_id") if isinstance(row.get("criterion_id"), str) else None,
                        row_number=index,
                        message=raw["message"],
                        rationale=_rationale(rule_id),
                        suggested_fix=raw["suggested_fix"],
                    )
                )
    return sorted(findings, key=lambda item: (item.row_number or 0, item.rule_id, item.message))


def _criterion_id(rows: list[dict[str, Any]], row_number: int | None) -> str | None:
    if row_number is None or row_number < 1 or row_number > len(rows):
        return None
    value = rows[row_number - 1].get("criterion_id")
    return value if isinstance(value, str) else None


def _rationale(rule_id: str) -> str:
    rationales = {
        "R001_COMPOUND_CRITERIA": "Compound criteria hide which judgment drove the score.",
        "R002_VAGUE_WORDING": "Vague words create reviewer disagreement and weak reproducibility.",
        "R003_MISSING_EXAMPLES": "Examples make rubric boundaries easier to audit.",
        "R004_MISSING_WEIGHT": "Scoring requires explicit criterion weights.",
        "R005_DUPLICATE_ID": "Duplicate IDs make labels ambiguous.",
        "R006_DUPLICATE_TEXT": "Duplicate text can overweight the same judgment.",
        "R007_INCONSISTENT_SEVERITY": "Severity should be stable for the same judgment.",
        "R008_UNSCORABLE_LANGUAGE": "Subjective language cannot be scored consistently from local evidence.",
        "R009_UNAVAILABLE_CONTEXT": "Criteria must only require context available to the evaluator.",
        "R010_UNCLEAR_SCORING_BOUNDARY": "Scale scores need boundaries for deterministic interpretation.",
        "R011_WEIGHT_TOTAL": "A total weight of 1.0 keeps aggregate scores interpretable.",
    }
    return rationales.get(rule_id, "Rubric quality rule.")

