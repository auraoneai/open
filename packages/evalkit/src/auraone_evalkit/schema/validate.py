"""Validation helpers for rubric JSONL and JSON-array files."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from auraone_evalkit.schema.models import (
    DISAGREEMENT_LEVELS,
    SCORING_TYPES,
    SEVERITIES,
    RubricCriterion,
    ValidationIssue,
)

REQUIRED_FIELDS = {
    "criterion_id": "Add a stable snake_case or dotted identifier, for example code_review.correctness.",
    "domain": "Add a short domain name, for example code_review_tutorial.",
    "task_type": "Add the task type this criterion applies to.",
    "criterion": "Add one observable criterion sentence.",
    "weight": "Add a numeric weight greater than 0 and less than or equal to 1.",
    "severity": "Use one of: info, warning, error.",
    "scoring_type": "Use one of: binary, scale_0_1, scale_0_2, scale_0_3, scale_0_5.",
    "examples": "Add at least one object with positive and negative examples.",
    "edge_cases": "Add at least one edge case that clarifies boundary behavior.",
    "disagreement_risk": "Add an object with level and notes fields.",
}
OPTIONAL_FIELDS = {
    "tags",
    "version",
    "parent_criterion_id",
    "policy_source",
    "data_source",
    "notes",
    "score_levels",
}
ID_RE = re.compile(r"^[a-z][a-z0-9_.-]*$")


class ValidationResult(list[ValidationIssue]):
    """List-like validation issues with dict-style summary compatibility."""

    def __init__(self, issues: list[ValidationIssue], criteria_count: int) -> None:
        super().__init__(issues)
        self.criteria_count = criteria_count

    def __getitem__(self, key: int | slice | str) -> Any:
        if isinstance(key, str):
            if key == "valid":
                return len(self) == 0
            if key == "criteria":
                return self.criteria_count if len(self) == 0 else 0
            if key == "issues":
                return [issue.to_dict() for issue in self]
            raise KeyError(key)
        return super().__getitem__(key)


def validate_rubric_file(path: Path | str) -> ValidationResult:
    rows, issues = _load_rows(Path(path))
    return ValidationResult(issues, len(rows))


def load_rubric(path: Path | str) -> list[RubricCriterion]:
    rows, issues = _load_rows(Path(path))
    if issues:
        formatted = format_issues_text(issues)
        raise ValueError(f"Invalid rubric:\n{formatted}")
    return [RubricCriterion.from_mapping(row) for row in rows]


def validate_rubric_rows(rows: list[dict[str, Any]], path: str = "<memory>") -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen_ids: dict[str, int] = {}
    for index, row in enumerate(rows, start=1):
        issues.extend(_validate_row(row, index, path))
        criterion_id = row.get("criterion_id")
        if isinstance(criterion_id, str):
            if criterion_id in seen_ids:
                issues.append(
                    ValidationIssue(
                        path=path,
                        row_number=index,
                        field="criterion_id",
                        error=f"Duplicate criterion_id also appears on row {seen_ids[criterion_id]}.",
                        suggested_fix="Use stable unique criterion_id values.",
                    )
                )
            else:
                seen_ids[criterion_id] = index
    if not rows:
        issues.append(
            ValidationIssue(
                path=path,
                row_number=None,
                field=None,
                error="Rubric is empty.",
                suggested_fix="Add at least one rubric criterion row.",
            )
        )
    return issues


def format_issues_text(issues: list[ValidationIssue]) -> str:
    lines = []
    for issue in issues:
        row = f"row {issue.row_number}" if issue.row_number is not None else "file"
        field = f" field {issue.field}" if issue.field else ""
        lines.append(f"{issue.path}: {row}{field}: {issue.error} Fix: {issue.suggested_fix}")
    return "\n".join(lines)


def _load_rows(path: Path) -> tuple[list[dict[str, Any]], list[ValidationIssue]]:
    if not path.exists():
        return [], [
            ValidationIssue(
                path=str(path),
                row_number=None,
                field=None,
                error="File does not exist.",
                suggested_fix="Check the path and rerun the command.",
            )
        ]
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [], [
            ValidationIssue(
                path=str(path),
                row_number=None,
                field=None,
                error="File is empty.",
                suggested_fix="Add JSONL rubric rows or a JSON array of rows.",
            )
        ]
    rows: list[dict[str, Any]] = []
    if text.lstrip().startswith("["):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            return [], [_json_issue(path, None, exc)]
        if not isinstance(parsed, list):
            return [], [
                ValidationIssue(str(path), None, None, "Top-level JSON value must be an array.", "Use JSONL rows or a JSON array.")
            ]
        for index, item in enumerate(parsed, start=1):
            if isinstance(item, dict):
                rows.append(item)
            else:
                return [], [
                    ValidationIssue(str(path), index, None, "Each rubric row must be an object.", "Replace the row with a JSON object.")
                ]
    else:
        for index, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                return [], [_json_issue(path, index, exc)]
            if not isinstance(item, dict):
                return [], [
                    ValidationIssue(str(path), index, None, "Each JSONL line must be an object.", "Replace the line with a JSON object.")
                ]
            rows.append(item)
    return rows, validate_rubric_rows(rows, str(path))


def _json_issue(path: Path, row_number: int | None, exc: json.JSONDecodeError) -> ValidationIssue:
    return ValidationIssue(
        path=str(path),
        row_number=row_number,
        field=None,
        error=f"Malformed JSON: {exc.msg}.",
        suggested_fix="Fix JSON syntax and ensure each JSONL row is complete.",
    )


def _validate_row(row: dict[str, Any], row_number: int, path: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    allowed_fields = set(REQUIRED_FIELDS) | OPTIONAL_FIELDS
    for field_name, fix in REQUIRED_FIELDS.items():
        if field_name not in row:
            issues.append(ValidationIssue(path, row_number, field_name, "Missing required field.", fix))
    for field_name in row:
        if field_name not in allowed_fields:
            issues.append(
                ValidationIssue(
                    path,
                    row_number,
                    field_name,
                    "Unknown field.",
                    "Remove the field or add it to a future schema version before relying on it.",
                )
            )
    if "criterion_id" in row and (not isinstance(row["criterion_id"], str) or not ID_RE.match(row["criterion_id"])):
        issues.append(
            ValidationIssue(
                path,
                row_number,
                "criterion_id",
                "criterion_id must be a lowercase stable identifier using letters, numbers, underscores, dots, or hyphens.",
                "Use an ID like code_review.correctness.",
            )
        )
    for field_name in ("domain", "task_type", "criterion"):
        if field_name in row and (not isinstance(row[field_name], str) or not row[field_name].strip()):
            issues.append(ValidationIssue(path, row_number, field_name, "Field must be a non-empty string.", "Add a non-empty string."))
    if "criterion" in row and isinstance(row["criterion"], str) and len(row["criterion"].strip()) < 20:
        issues.append(
            ValidationIssue(path, row_number, "criterion", "Criterion is too short to be actionable.", "Write an observable criterion sentence.")
        )
    if "weight" in row:
        if not isinstance(row["weight"], (int, float)) or isinstance(row["weight"], bool):
            issues.append(ValidationIssue(path, row_number, "weight", "Weight must be numeric.", "Use a number greater than 0 and <= 1."))
        elif row["weight"] <= 0 or row["weight"] > 1:
            issues.append(ValidationIssue(path, row_number, "weight", "Weight must be > 0 and <= 1.", "Choose a fractional rubric weight."))
    if "severity" in row and row["severity"] not in SEVERITIES:
        issues.append(ValidationIssue(path, row_number, "severity", "Invalid severity.", "Use one of: info, warning, error."))
    if "scoring_type" in row and row["scoring_type"] not in SCORING_TYPES:
        issues.append(ValidationIssue(path, row_number, "scoring_type", "Invalid scoring_type.", "Use binary or a supported scale_0_N value."))
    _validate_examples(row, row_number, path, issues)
    _validate_edge_cases(row, row_number, path, issues)
    _validate_disagreement_risk(row, row_number, path, issues)
    if "tags" in row and (not isinstance(row["tags"], list) or not all(isinstance(tag, str) for tag in row["tags"])):
        issues.append(ValidationIssue(path, row_number, "tags", "Tags must be a list of strings.", "Use tags like [\"synthetic\", \"tutorial\"]."))
    if "score_levels" in row and not isinstance(row["score_levels"], dict):
        issues.append(ValidationIssue(path, row_number, "score_levels", "score_levels must be an object.", "Map score values to boundary descriptions."))
    return issues


def _validate_examples(row: dict[str, Any], row_number: int, path: str, issues: list[ValidationIssue]) -> None:
    if "examples" not in row:
        return
    examples = row["examples"]
    if not isinstance(examples, list) or not examples:
        issues.append(ValidationIssue(path, row_number, "examples", "Examples must be a non-empty list.", "Add positive and negative example objects."))
        return
    for item in examples:
        if not isinstance(item, dict) or not isinstance(item.get("positive"), str) or not isinstance(item.get("negative"), str):
            issues.append(
                ValidationIssue(
                    path,
                    row_number,
                    "examples",
                    "Each example must include positive and negative string fields.",
                    "Use {\"positive\": \"...\", \"negative\": \"...\"}.",
                )
            )
            return


def _validate_edge_cases(row: dict[str, Any], row_number: int, path: str, issues: list[ValidationIssue]) -> None:
    if "edge_cases" not in row:
        return
    edge_cases = row["edge_cases"]
    if not isinstance(edge_cases, list) or not edge_cases or not all(isinstance(item, str) and item.strip() for item in edge_cases):
        issues.append(ValidationIssue(path, row_number, "edge_cases", "edge_cases must be a non-empty list of strings.", "Add boundary cases."))


def _validate_disagreement_risk(row: dict[str, Any], row_number: int, path: str, issues: list[ValidationIssue]) -> None:
    if "disagreement_risk" not in row:
        return
    risk = row["disagreement_risk"]
    if not isinstance(risk, dict):
        issues.append(ValidationIssue(path, row_number, "disagreement_risk", "disagreement_risk must be an object.", "Add level and notes."))
        return
    if risk.get("level") not in DISAGREEMENT_LEVELS:
        issues.append(ValidationIssue(path, row_number, "disagreement_risk.level", "Invalid disagreement risk level.", "Use low, medium, or high."))
    if not isinstance(risk.get("notes"), str) or not risk.get("notes", "").strip():
        issues.append(ValidationIssue(path, row_number, "disagreement_risk.notes", "Risk notes are required.", "Explain likely reviewer disagreement."))
