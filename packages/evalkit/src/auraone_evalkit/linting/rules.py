"""Deterministic rubric lint rules."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class RuleContext:
    row: dict[str, Any]
    row_number: int
    all_rows: list[dict[str, Any]]


RuleFunction = Callable[[RuleContext], list[dict[str, str]]]


VAGUE_TERMS = re.compile(r"\b(good|bad|clear|appropriate|reasonable|high[- ]quality|useful|nice)\b", re.I)
UNSCORABLE_TERMS = re.compile(r"\b(feels?|seems?|beautiful|delightful|best|impressive|human[- ]like)\b", re.I)
UNAVAILABLE_CONTEXT = re.compile(
    r"\b(secret|private|internal-only|customer data|production logs|company roadmap|expert knowledge)\b",
    re.I,
)
COMPOUND_PATTERN = re.compile(r"\b(both|and|as well as|also)\b", re.I)


def compound_criteria(ctx: RuleContext) -> list[dict[str, str]]:
    text = _criterion(ctx.row)
    if "and provide an action" in text.lower():
        return []
    if COMPOUND_PATTERN.search(text) and len(re.findall(r"\b(and|also|as well as)\b", text, re.I)) >= 1:
        return [_finding("warning", "Criterion may combine multiple judgments.", "Split each observable judgment into its own weighted criterion.")]
    return []


def vague_wording(ctx: RuleContext) -> list[dict[str, str]]:
    if VAGUE_TERMS.search(_criterion(ctx.row)):
        return [_finding("warning", "Criterion uses vague wording.", "Replace subjective adjectives with observable pass/fail boundaries.")]
    return []


def missing_examples(ctx: RuleContext) -> list[dict[str, str]]:
    examples = ctx.row.get("examples")
    if not isinstance(examples, list) or not examples:
        return [_finding("error", "Criterion has no examples.", "Add at least one positive and negative tutorial example.")]
    return []


def missing_weight(ctx: RuleContext) -> list[dict[str, str]]:
    weight = ctx.row.get("weight")
    if not isinstance(weight, (int, float)) or isinstance(weight, bool):
        return [_finding("error", "Criterion is missing a numeric weight.", "Add a numeric weight greater than 0 and less than or equal to 1.")]
    return []


def duplicate_criterion_id(ctx: RuleContext) -> list[dict[str, str]]:
    criterion_id = ctx.row.get("criterion_id")
    if not criterion_id:
        return []
    count = sum(1 for row in ctx.all_rows if row.get("criterion_id") == criterion_id)
    if count > 1:
        return [_finding("error", "Duplicate criterion_id.", "Use unique stable criterion_id values.")]
    return []


def duplicate_criterion_text(ctx: RuleContext) -> list[dict[str, str]]:
    text = _normalized_text(_criterion(ctx.row))
    if not text:
        return []
    count = sum(1 for row in ctx.all_rows if _normalized_text(_criterion(row)) == text)
    if count > 1:
        return [_finding("warning", "Duplicate or near-duplicate criterion text.", "Merge duplicates or make each criterion distinct.")]
    return []


def inconsistent_severity(ctx: RuleContext) -> list[dict[str, str]]:
    text = _normalized_text(_criterion(ctx.row))
    if not text:
        return []
    severities = {row.get("severity") for row in ctx.all_rows if _normalized_text(_criterion(row)) == text}
    if len(severities) > 1:
        return [_finding("warning", "Duplicate criterion text uses inconsistent severities.", "Use one severity for the same criterion or rewrite the rows.")]
    return []


def unscorable_language(ctx: RuleContext) -> list[dict[str, str]]:
    if UNSCORABLE_TERMS.search(_criterion(ctx.row)):
        return [_finding("error", "Criterion uses unscorable subjective language.", "Rewrite around observable evidence available in the output.")]
    return []


def unavailable_context(ctx: RuleContext) -> list[dict[str, str]]:
    if UNAVAILABLE_CONTEXT.search(_criterion(ctx.row)):
        return [_finding("error", "Criterion depends on unavailable context.", "Limit criteria to information available in the prompt, output, rubric, or labels.")]
    return []


def unclear_scoring_boundary(ctx: RuleContext) -> list[dict[str, str]]:
    scoring_type = ctx.row.get("scoring_type")
    score_levels = ctx.row.get("score_levels")
    if isinstance(scoring_type, str) and scoring_type.startswith("scale_") and not score_levels:
        return [_finding("warning", "Scale criterion has no score-level boundaries.", "Add score_levels explaining what each score means.")]
    return []


def weight_total(ctx: RuleContext) -> list[dict[str, str]]:
    if ctx.row_number != 1:
        return []
    weights = [row.get("weight") for row in ctx.all_rows]
    if not all(isinstance(weight, (int, float)) and not isinstance(weight, bool) for weight in weights):
        return []
    total = sum(float(weight) for weight in weights)
    if abs(total - 1.0) > 0.001:
        return [_finding("warning", f"Rubric weights sum to {total:.3f}, not 1.000.", "Adjust weights so the rubric total is 1.0.")]
    return []


RULES: dict[str, RuleFunction] = {
    "R001_COMPOUND_CRITERIA": compound_criteria,
    "R002_VAGUE_WORDING": vague_wording,
    "R003_MISSING_EXAMPLES": missing_examples,
    "R004_MISSING_WEIGHT": missing_weight,
    "R005_DUPLICATE_ID": duplicate_criterion_id,
    "R006_DUPLICATE_TEXT": duplicate_criterion_text,
    "R007_INCONSISTENT_SEVERITY": inconsistent_severity,
    "R008_UNSCORABLE_LANGUAGE": unscorable_language,
    "R009_UNAVAILABLE_CONTEXT": unavailable_context,
    "R010_UNCLEAR_SCORING_BOUNDARY": unclear_scoring_boundary,
    "R011_WEIGHT_TOTAL": weight_total,
}


def _criterion(row: dict[str, Any]) -> str:
    value = row.get("criterion")
    return value if isinstance(value, str) else ""


def _normalized_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _finding(severity: str, message: str, suggested_fix: str) -> dict[str, str]:
    return {"severity": severity, "message": message, "suggested_fix": suggested_fix}


def lint_rubric(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compatibility wrapper for callers that pass parsed rubric rows."""
    issues: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        context = RuleContext(row=row, row_number=index, all_rows=rows)
        for rule_id, rule in RULES.items():
            for raw in rule(context):
                issues.append(
                    {
                        "row": index,
                        "criterion_id": row.get("criterion_id"),
                        "severity": raw["severity"],
                        "rule": rule_id,
                        "message": raw["message"],
                        "suggested_fix": raw["suggested_fix"],
                    }
                )
    return {
        "issue_count": len(issues),
        "error_count": sum(1 for issue in issues if issue["severity"] == "error"),
        "issues": issues,
    }
