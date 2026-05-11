"""Reviewer drift detector for local JSONL batches."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Iterable, Mapping

from .models import DriftRecord, DriftReport


def load_drift_records(path: str | Path) -> list[DriftRecord]:
    records: list[DriftRecord] = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if line.strip():
            records.append(DriftRecord.from_mapping(json.loads(line), line_no=line_no))
    return records


def detect_drift(
    records: Iterable[DriftRecord | Mapping],
    *,
    reviewer_threshold: float = 0.35,
    criterion_threshold: float = 0.4,
) -> DriftReport:
    rows = [row if isinstance(row, DriftRecord) else DriftRecord.from_mapping(row) for row in records]
    if not rows:
        raise ValueError("At least one drift record is required")
    batches = sorted({row.batch_id for row in rows})
    if len(batches) < 2:
        raise ValueError("At least two batches or time windows are required")
    first, last = batches[0], batches[-1]

    reviewer_drift = {}
    for reviewer in sorted({row.reviewer_id for row in rows}):
        reviewer_rows = [row for row in rows if row.reviewer_id == reviewer]
        first_scores = [row.score for row in reviewer_rows if row.batch_id == first]
        last_scores = [row.score for row in reviewer_rows if row.batch_id == last]
        if not first_scores or not last_scores:
            continue
        mean_delta = mean(last_scores) - mean(first_scores)
        gold_delta = _gold_error_delta(reviewer_rows, first, last)
        drift_score = abs(mean_delta) + max(0.0, gold_delta)
        reviewer_drift[reviewer] = {
            "from_batch": first,
            "to_batch": last,
            "mean_score_delta": round(mean_delta, 6),
            "gold_error_delta": round(gold_delta, 6),
            "drift_score": round(drift_score, 6),
            "status": "warning" if drift_score >= reviewer_threshold else "stable",
            "recommendation": "review calibration examples" if drift_score >= reviewer_threshold else "continue monitoring",
        }

    criterion_instability = {}
    for criterion in sorted({row.criterion_id for row in rows}):
        criterion_rows = [row for row in rows if row.criterion_id == criterion]
        first_values = [row.score for row in criterion_rows if row.batch_id == first]
        last_values = [row.score for row in criterion_rows if row.batch_id == last]
        if not first_values or not last_values:
            continue
        spread_delta = _spread(last_values) - _spread(first_values)
        mean_delta = mean(last_values) - mean(first_values)
        instability = abs(mean_delta) + max(0.0, spread_delta)
        criterion_instability[criterion] = {
            "mean_score_delta": round(mean_delta, 6),
            "spread_delta": round(spread_delta, 6),
            "instability_score": round(instability, 6),
            "status": "warning" if instability >= criterion_threshold else "stable",
        }

    warnings = [
        {"type": "reviewer_drift", "id": reviewer, **details}
        for reviewer, details in reviewer_drift.items()
        if details["status"] == "warning"
    ]
    warnings.extend(
        {"type": "criterion_instability", "id": criterion, **details}
        for criterion, details in criterion_instability.items()
        if details["status"] == "warning"
    )
    return DriftReport(reviewer_drift, criterion_instability, warnings)


def population_stability_index(expected: list[float], actual: list[float], buckets: int = 10) -> float:
    if not expected or not actual:
        return 0.0
    low = min(expected + actual)
    high = max(expected + actual)
    if high == low:
        return 0.0
    step = (high - low) / buckets
    score = 0.0
    for index in range(buckets):
        start = low + index * step
        end = high if index == buckets - 1 else start + step
        exp = max(sum(start <= value <= end for value in expected) / len(expected), 0.0001)
        act = max(sum(start <= value <= end for value in actual) / len(actual), 0.0001)
        score += (act - exp) * __import__("math").log(act / exp)
    return score


def drift_report(rows: Iterable[Mapping], baseline_window: str = "baseline", current_window: str = "current") -> dict:
    mapped = []
    for row in rows:
        if "batch_id" in row or "timestamp" in row:
            mapped.append(row)
        else:
            window = row.get("window", current_window)
            mapped.append({**row, "batch_id": window, "criterion_id": row.get("criterion_id", "__default__"), "item_id": row.get("item_id", row.get("id", window))})
    try:
        report = detect_drift(mapped).to_dict()
        if "reviewers" not in report and "reviewer_drift" in report:
            report["reviewers"] = [
                {"reviewer_id": reviewer_id, **details}
                for reviewer_id, details in sorted(report["reviewer_drift"].items())
            ]
        return report
    except ValueError:
        by_reviewer: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
        for row in rows:
            score = row.get("score")
            if isinstance(score, (int, float)):
                by_reviewer[str(row.get("reviewer_id"))][str(row.get("window"))].append(float(score))
        reviewers = []
        for reviewer, windows in sorted(by_reviewer.items()):
            baseline = windows.get(baseline_window, [])
            current = windows.get(current_window, [])
            psi = population_stability_index(baseline, current)
            reviewers.append({"reviewer_id": reviewer, "baseline_count": len(baseline), "current_count": len(current), "psi": psi, "flag": psi >= 0.2})
        return {"schema_version": "evalkit-drift-v0.1", "reviewers": reviewers}


def _gold_error_delta(rows: list[DriftRecord], first: str, last: str) -> float:
    def errors(batch: str) -> list[float]:
        return [abs(row.score - row.gold_score) for row in rows if row.batch_id == batch and row.gold_score is not None]

    first_errors = errors(first)
    last_errors = errors(last)
    if not first_errors or not last_errors:
        return 0.0
    return mean(last_errors) - mean(first_errors)


def _spread(values: list[float]) -> float:
    return pstdev(values) if len(values) > 1 else 0.0
