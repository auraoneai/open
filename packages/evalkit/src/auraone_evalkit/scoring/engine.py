"""Deterministic weighted scoring for EvalKit rubric labels."""
from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from auraone_evalkit.schema.models import RubricCriterion
from auraone_evalkit.schema.validate import load_rubric
from auraone_evalkit.scoring.io import load_json_records


class ScoringError(Exception):
    """Raised when scoring inputs cannot produce a deterministic result."""


@dataclass(frozen=True)
class ScoreResult:
    schema_version: str
    dataset_notice: str
    pass_threshold: float
    summary: dict[str, Any]
    outputs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "dataset_notice": self.dataset_notice,
            "pass_threshold": self.pass_threshold,
            "summary": self.summary,
            "outputs": self.outputs,
        }


def score_from_files(
    rubric_path: Path | str,
    responses_path: Path | str,
    labels_path: Path | str | None = None,
    pass_threshold: float = 0.75,
    strict: bool = False,
) -> ScoreResult:
    responses_path = Path(responses_path)
    if labels_path is None:
        labels_path = responses_path.with_name("labels.jsonl")
    labels_path = Path(labels_path)
    if not labels_path.exists():
        raise ScoringError(f"Labels file {labels_path} does not exist. Pass --labels or place labels.jsonl next to responses.")
    try:
        rubric = load_rubric(rubric_path)
        responses = load_json_records(responses_path)
        labels = load_json_records(labels_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise ScoringError(str(exc)) from exc
    return score_outputs(rubric, responses, labels, pass_threshold=pass_threshold, strict=strict)


def score_outputs(
    rubric: list[RubricCriterion],
    responses: list[dict[str, Any]],
    labels: list[dict[str, Any]],
    pass_threshold: float = 0.75,
    strict: bool = False,
) -> ScoreResult:
    if not rubric:
        raise ScoringError("Rubric must contain at least one criterion.")
    if not responses:
        raise ScoringError("Responses must contain at least one output.")
    if not labels:
        raise ScoringError("Labels must contain at least one row.")
    if pass_threshold < 0 or pass_threshold > 1:
        raise ScoringError("pass_threshold must be between 0 and 1.")

    rubric_by_id = {criterion.criterion_id: criterion for criterion in rubric}
    response_by_id = _index_responses(responses)
    labels_by_output: dict[str, dict[str, dict[str, Any]]] = {output_id: {} for output_id in response_by_id}
    for row_number, label in enumerate(labels, start=1):
        output_id = _label_output_id(label, row_number)
        criterion_id = _required_string(label, "criterion_id", f"label row {row_number}")
        if output_id not in response_by_id:
            raise ScoringError(f"label row {row_number} references unknown output_id {output_id!r}")
        if criterion_id not in rubric_by_id:
            raise ScoringError(f"label row {row_number} references unknown criterion_id {criterion_id!r}")
        labels_by_output[output_id][criterion_id] = label

    scored_outputs = []
    missing_total = 0
    for output_id in sorted(response_by_id):
        result = _score_one_output(output_id, rubric, labels_by_output[output_id], pass_threshold)
        missing_total += len(result["missing_criteria"])
        if strict and result["missing_criteria"]:
            missing = ", ".join(result["missing_criteria"])
            raise ScoringError(f"output_id {output_id!r} is missing labels for: {missing}")
        scored_outputs.append(result)

    average_score = round(sum(item["score"] for item in scored_outputs) / len(scored_outputs), 6)
    passed = sum(1 for item in scored_outputs if item["passed"])
    summary = {
        "scored_outputs": len(scored_outputs),
        "criterion_count": len(rubric),
        "average_score": average_score,
        "pass_rate": round(passed / len(scored_outputs), 6),
        "passed_outputs": passed,
        "missing_label_count": missing_total,
    }
    return ScoreResult(
        schema_version="auraone.evalkit.score.v0.1",
        dataset_notice="Synthetic/tutorial scoring output. Not expert-authored, human-validated, benchmark-grade, or produced by hosted AuraOne services.",
        pass_threshold=pass_threshold,
        summary=summary,
        outputs=scored_outputs,
    )


def score_eval(rubric_path: str, responses_path: str, labels_path: str | None = None) -> dict[str, Any]:
    result = score_from_files(rubric_path, responses_path, labels_path).to_dict()
    summary = result["summary"]
    result["overall_score"] = summary["average_score"]
    result["response_count"] = summary["scored_outputs"]
    result["criterion_count"] = summary["criterion_count"]
    result["missing_labels"] = [
        {"output_id": output["output_id"], "criterion_id": cid}
        for output in result["outputs"]
        for cid in output["missing_criteria"]
    ]
    result["responses"] = result["outputs"]
    result["criterion_summary"] = {}
    return result


def write_score_output(result: ScoreResult, out_path: Path | None, output_format: str) -> None:
    if output_format == "json":
        payload = json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
    elif output_format == "report-json":
        report = result.to_dict()
        report["report_input_type"] = "auraone.evalkit.report_input.v0.1"
        payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    elif output_format == "jsonl":
        payload = "".join(json.dumps(item, sort_keys=True) + "\n" for item in result.outputs)
    elif output_format == "csv":
        payload = _to_csv(result)
    else:
        raise ScoringError(f"Unsupported output format: {output_format}")
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


def _score_one_output(output_id: str, rubric: list[RubricCriterion], labels_by_criterion: dict[str, dict[str, Any]], pass_threshold: float) -> dict[str, Any]:
    criterion_scores = []
    weighted_points = 0.0
    applicable_weight = 0.0
    missing: list[str] = []
    for criterion in rubric:
        label = labels_by_criterion.get(criterion.criterion_id)
        if label is None:
            applicable_weight += criterion.weight
            missing.append(criterion.criterion_id)
            criterion_scores.append({"criterion_id": criterion.criterion_id, "status": "missing", "weight": criterion.weight, "normalized_score": None, "weighted_points": 0.0})
            continue
        applicable = bool(label.get("applicable", True))
        if not applicable:
            criterion_scores.append({"criterion_id": criterion.criterion_id, "status": "not_applicable", "weight": criterion.weight, "normalized_score": None, "weighted_points": 0.0, "rationale": label.get("rationale")})
            continue
        normalized = _normalize_score(label.get("score"), criterion)
        points = criterion.weight * normalized
        weighted_points += points
        applicable_weight += criterion.weight
        criterion_scores.append({"criterion_id": criterion.criterion_id, "status": "scored", "weight": criterion.weight, "raw_score": label.get("score"), "max_score": criterion.max_score, "normalized_score": round(normalized, 6), "weighted_points": round(points, 6), "rationale": label.get("rationale")})
    if applicable_weight <= 0:
        raise ScoringError(f"output_id {output_id!r} has no applicable criteria")
    score = round(weighted_points / applicable_weight, 6)
    return {"output_id": output_id, "score": score, "passed": score >= pass_threshold, "applicable_weight": round(applicable_weight, 6), "weighted_points": round(weighted_points, 6), "missing_criteria": missing, "criteria": criterion_scores}


def _normalize_score(value: Any, criterion: RubricCriterion) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ScoringError(f"label for {criterion.criterion_id!r} must contain numeric score")
    numeric = float(value)
    if numeric < 0 or numeric > criterion.max_score:
        raise ScoringError(f"score {numeric} for {criterion.criterion_id!r} outside allowed range 0..{criterion.max_score:g}")
    return numeric / criterion.max_score


def _index_responses(responses: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row_number, response in enumerate(responses, start=1):
        output_id = _response_output_id(response, row_number)
        if output_id in indexed:
            raise ScoringError(f"duplicate output_id {output_id!r}")
        indexed[output_id] = response
    return indexed


def _response_output_id(row: dict[str, Any], row_number: int) -> str:
    value = row.get("output_id", row.get("response_id", row.get("id")))
    if not isinstance(value, str) or not value.strip():
        raise ScoringError(f"response row {row_number} missing non-empty output_id")
    return value


def _label_output_id(row: dict[str, Any], row_number: int) -> str:
    value = row.get("output_id", row.get("response_id"))
    if not isinstance(value, str) or not value.strip():
        raise ScoringError(f"label row {row_number} missing non-empty output_id")
    return value


def _required_string(row: dict[str, Any], field_name: str, location: str) -> str:
    value = row.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ScoringError(f"{location} missing non-empty {field_name}")
    return value


def _to_csv(result: ScoreResult) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["output_id", "score", "passed", "applicable_weight", "weighted_points", "missing_criteria"])
    writer.writeheader()
    for output in result.outputs:
        writer.writerow({"output_id": output["output_id"], "score": output["score"], "passed": output["passed"], "applicable_weight": output["applicable_weight"], "weighted_points": output["weighted_points"], "missing_criteria": ",".join(output["missing_criteria"])})
    return buffer.getvalue()
