"""Reviewer agreement metrics aligned with AuraOne platform IAA semantics."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
import math
from typing import Any, Iterable, Mapping


class InsufficientAgreementData(ValueError):
    """Raised when agreement cannot be estimated from the supplied rows."""


@dataclass(frozen=True)
class Annotation:
    reviewer_id: str
    item_id: str
    criterion_id: str
    value: Any
    adjudicated: bool = False

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any], *, line_no: int | None = None) -> "Annotation":
        reviewer_id = row.get("reviewer_id", row.get("annotator_id", row.get("rater_id")))
        item_id = row.get("item_id", row.get("response_id", row.get("id")))
        criterion_id = row.get("criterion_id", "__default__")
        value = row.get("value", row.get("score", row.get("label")))
        missing = [
            name
            for name, candidate in (("reviewer_id", reviewer_id), ("item_id", item_id), ("value", value))
            if candidate is None
        ]
        if missing:
            prefix = f"Line {line_no}: " if line_no is not None else ""
            raise ValueError(f"{prefix}missing required annotation field(s): {', '.join(missing)}")
        if isinstance(value, float) and not math.isfinite(value):
            prefix = f"Line {line_no}: " if line_no is not None else ""
            raise ValueError(f"{prefix}annotation value must be finite")
        return cls(str(reviewer_id), str(item_id), str(criterion_id), value, bool(row.get("adjudicated", False)))


@dataclass(frozen=True)
class AgreementSummary:
    item_count: int
    reviewer_count: int
    annotation_count: int
    percent_agreement: float
    krippendorff_alpha: float
    cohen_kappa: float | None
    fleiss_kappa: float | None
    adjudication_rate: float
    per_criterion: dict[str, dict[str, float]]
    per_reviewer: dict[str, dict[str, float]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_count": self.item_count,
            "reviewer_count": self.reviewer_count,
            "annotation_count": self.annotation_count,
            "percent_agreement": self.percent_agreement,
            "krippendorff_alpha": self.krippendorff_alpha,
            "cohen_kappa": self.cohen_kappa,
            "fleiss_kappa": self.fleiss_kappa,
            "adjudication_rate": self.adjudication_rate,
            "per_criterion": self.per_criterion,
            "per_reviewer": self.per_reviewer,
            "limitations": [
                "Agreement estimates are unstable for low overlap counts.",
                "Tutorial data is synthetic and not human-validated.",
            ],
        }


def _rows(annotations: Iterable[Annotation | Mapping[str, Any]]) -> list[Annotation]:
    rows = [row if isinstance(row, Annotation) else Annotation.from_mapping(row) for row in annotations]
    if not rows:
        raise InsufficientAgreementData("At least two reviewers and one overlapping item are required")
    if len({row.reviewer_id for row in rows}) < 2:
        raise InsufficientAgreementData("At least two reviewers are required")
    return rows


def _groups(rows: Iterable[Annotation]) -> dict[tuple[str, str], list[Annotation]]:
    grouped: dict[tuple[str, str], list[Annotation]] = defaultdict(list)
    for row in rows:
        grouped[(row.criterion_id, row.item_id)].append(row)
    return grouped


def _distance(left: Any, right: Any) -> float:
    if isinstance(left, bool) and isinstance(right, bool):
        return 0.0 if left == right else 1.0
    if isinstance(left, (int, float)) and not isinstance(left, bool) and isinstance(right, (int, float)) and not isinstance(right, bool):
        return abs(float(left) - float(right))
    if isinstance(left, str) and isinstance(right, str):
        return 0.0 if left == right else 1.0
    if isinstance(left, list) and isinstance(right, list):
        union = set(left) | set(right)
        return 0.0 if not union else 1.0 - (len(set(left) & set(right)) / len(union))
    return 0.0 if left == right else 1.0


def _hashable(value: Any) -> Any:
    return ("__list__", tuple(value)) if isinstance(value, list) else value


def _unhash(value: Any) -> Any:
    return list(value[1]) if isinstance(value, tuple) and value and value[0] == "__list__" else value


def _ensure_overlap(rows: list[Annotation]) -> None:
    if not any(len(group) >= 2 for group in _groups(rows).values()):
        raise InsufficientAgreementData("At least one item must have labels from two reviewers")


def krippendorffs_alpha(annotations: Iterable[Annotation | Mapping[str, Any]]) -> float:
    rows = _rows(annotations)
    _ensure_overlap(rows)
    if all(isinstance(row.value, (int, float)) and not isinstance(row.value, bool) for row in rows):
        return _interval_alpha(rows)
    return _categorical_alpha(rows)


def _interval_alpha(rows: list[Annotation]) -> float:
    observed_numerator = 0.0
    observed_pairs = 0
    for group in _groups(rows).values():
        n = len(group)
        if n < 2:
            continue
        values = [float(row.value) for row in group]
        observed_numerator += n * sum(value * value for value in values) - sum(values) ** 2
        observed_pairs += n * (n - 1)
    if observed_pairs == 0:
        raise InsufficientAgreementData("At least one overlapping item is required")
    observed = observed_numerator / observed_pairs
    values = [float(row.value) for row in rows]
    expected_pairs = len(values) * (len(values) - 1)
    expected = (len(values) * sum(value * value for value in values) - sum(values) ** 2) / expected_pairs
    return 1.0 if expected == 0 else 1.0 - observed / expected


def _categorical_alpha(rows: list[Annotation]) -> float:
    matrix: dict[Any, Counter] = defaultdict(Counter)
    for group in _groups(rows).values():
        n = len(group)
        if n < 2:
            continue
        weight = 2.0 / (n * (n - 1))
        for left, right in combinations([row.value for row in group], 2):
            left_key = _hashable(left)
            right_key = _hashable(right)
            matrix[left_key][right_key] += weight
            matrix[right_key][left_key] += weight
    if not matrix:
        raise InsufficientAgreementData("At least one overlapping item is required")
    observed_disagreement = 0.0
    observed_total = 0.0
    for left, row in matrix.items():
        for right, count in row.items():
            if left != right:
                observed_disagreement += _distance(_unhash(left), _unhash(right)) ** 2 * count
            observed_total += count
    observed = observed_disagreement / observed_total if observed_total else 0.0
    marginals: Counter = Counter()
    total = 0.0
    for left, row in matrix.items():
        for count in row.values():
            marginals[left] += count
            total += count
    expected = 0.0
    for left, left_count in marginals.items():
        for right, right_count in marginals.items():
            if left != right:
                expected += _distance(_unhash(left), _unhash(right)) ** 2 * (left_count / total) * (right_count / total)
    return 1.0 if expected == 0 else 1.0 - observed / expected


def percent_agreement(annotations: Iterable[Annotation | Mapping[str, Any]], *, threshold: float = 0.1) -> float:
    rows = _rows(annotations)
    matches = 0
    total = 0
    for group in _groups(rows).values():
        for left, right in combinations(group, 2):
            total += 1
            matches += int(_distance(left.value, right.value) <= threshold)
    if total == 0:
        raise InsufficientAgreementData("At least one reviewer pair is required")
    return matches / total


def cohen_kappa(annotations: Iterable[Annotation | Mapping[str, Any]]) -> float | None:
    rows = _rows(annotations)
    reviewers = sorted({row.reviewer_id for row in rows})
    if len(reviewers) != 2:
        return None
    by_reviewer = {reviewer: {} for reviewer in reviewers}
    for row in rows:
        by_reviewer[row.reviewer_id][(row.criterion_id, row.item_id)] = _hashable(row.value)
    common = sorted(set(by_reviewer[reviewers[0]]) & set(by_reviewer[reviewers[1]]))
    if not common:
        raise InsufficientAgreementData("Cohen kappa requires overlapping labels")
    observed = sum(by_reviewer[reviewers[0]][key] == by_reviewer[reviewers[1]][key] for key in common) / len(common)
    labels = set(by_reviewer[reviewers[0]][key] for key in common) | set(by_reviewer[reviewers[1]][key] for key in common)
    expected = sum(
        (sum(by_reviewer[reviewers[0]][key] == label for key in common) / len(common))
        * (sum(by_reviewer[reviewers[1]][key] == label for key in common) / len(common))
        for label in labels
    )
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def fleiss_kappa(annotations: Iterable[Annotation | Mapping[str, Any]]) -> float | None:
    rows = _rows(annotations)
    complete = [group for group in _groups(rows).values() if len(group) >= 2]
    if not complete:
        raise InsufficientAgreementData("Fleiss kappa requires overlapping labels")
    rater_counts = {len(group) for group in complete}
    if len(rater_counts) != 1:
        return None
    n = next(iter(rater_counts))
    label_counts = Counter()
    p_i = []
    for group in complete:
        counts = Counter(_hashable(row.value) for row in group)
        label_counts.update(counts)
        p_i.append((sum(count * count for count in counts.values()) - n) / (n * (n - 1)))
    p_bar = sum(p_i) / len(p_i)
    total = len(complete) * n
    p_e = sum((count / total) ** 2 for count in label_counts.values())
    return 1.0 if p_e == 1 else (p_bar - p_e) / (1 - p_e)


def per_criterion_agreement(annotations: Iterable[Annotation | Mapping[str, Any]]) -> dict[str, dict[str, float]]:
    rows = _rows(annotations)
    grouped: dict[str, list[Annotation]] = defaultdict(list)
    for row in rows:
        grouped[row.criterion_id].append(row)
    output = {}
    for criterion_id, criterion_rows in grouped.items():
        try:
            output[criterion_id] = {
                "percent_agreement": percent_agreement(criterion_rows),
                "krippendorff_alpha": krippendorffs_alpha(criterion_rows),
                "annotation_count": float(len(criterion_rows)),
            }
        except InsufficientAgreementData:
            output[criterion_id] = {"percent_agreement": 0.0, "krippendorff_alpha": 0.0, "annotation_count": float(len(criterion_rows))}
    return output


def per_reviewer_agreement(annotations: Iterable[Annotation | Mapping[str, Any]]) -> dict[str, dict[str, float]]:
    rows = _rows(annotations)
    output = {}
    for reviewer in sorted({row.reviewer_id for row in rows}):
        matches = 0
        total = 0
        for group in _groups(rows).values():
            own = [row for row in group if row.reviewer_id == reviewer]
            others = [row for row in group if row.reviewer_id != reviewer]
            for own_row in own:
                for other_row in others:
                    total += 1
                    matches += int(_distance(own_row.value, other_row.value) <= 0.1)
        output[reviewer] = {
            "agreement_rate": matches / total if total else 0.0,
            "total_annotations": float(sum(row.reviewer_id == reviewer for row in rows)),
            "consistency": 1.0,
        }
    return output


def adjudication_rate(annotations: Iterable[Annotation | Mapping[str, Any]]) -> float:
    rows = _rows(annotations)
    items = {row.item_id for row in rows}
    adjudicated = {row.item_id for row in rows if row.adjudicated}
    return len(adjudicated) / len(items) if items else 0.0


def analyze_agreement(annotations: Iterable[Annotation | Mapping[str, Any]]) -> AgreementSummary:
    rows = _rows(annotations)
    return AgreementSummary(
        item_count=len({row.item_id for row in rows}),
        reviewer_count=len({row.reviewer_id for row in rows}),
        annotation_count=len(rows),
        percent_agreement=percent_agreement(rows),
        krippendorff_alpha=krippendorffs_alpha(rows),
        cohen_kappa=cohen_kappa(rows),
        fleiss_kappa=fleiss_kappa(rows),
        adjudication_rate=adjudication_rate(rows),
        per_criterion=per_criterion_agreement(rows),
        per_reviewer=per_reviewer_agreement(rows),
    )


def agreement_report(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    report = analyze_agreement(rows).to_dict()
    report["percent_agreement_value"] = report["percent_agreement"]
    report["percent_agreement"] = {
        "agreement": report["percent_agreement_value"],
        "pairs": None,
    }
    return report
