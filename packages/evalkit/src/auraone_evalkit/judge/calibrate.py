"""Local judge calibration from saved tutorial outputs."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Iterable, Mapping

from .models import JudgeCalibrationResult, JudgeOutput


def load_judge_outputs(path: str | Path) -> list[JudgeOutput]:
    rows: list[JudgeOutput] = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if line.strip():
            rows.append(JudgeOutput.from_mapping(json.loads(line), line_no=line_no))
    return rows


def calibrate_judges(
    outputs: Iterable[JudgeOutput | Mapping],
    *,
    agreement_tolerance: float = 0.0,
    unstable_threshold: float = 0.5,
) -> JudgeCalibrationResult:
    rows = [row if isinstance(row, JudgeOutput) else JudgeOutput.from_mapping(row) for row in outputs]
    if not rows:
        raise ValueError("At least one saved judge output is required")
    judges = sorted({row.judge_id for row in rows})
    if len(judges) < 2:
        raise ValueError("At least two judges are required for calibration")

    by_key: dict[tuple[str, str, str], float] = {}
    for row in rows:
        by_key[(row.judge_id, row.criterion_id, row.item_id)] = row.score

    pairwise: dict[str, float] = {}
    for index, left in enumerate(judges):
        for right in judges[index + 1 :]:
            common = sorted(
                {(criterion, item) for judge, criterion, item in by_key if judge == left}
                & {(criterion, item) for judge, criterion, item in by_key if judge == right}
            )
            if not common:
                pairwise[f"{left}::{right}"] = 0.0
                continue
            matches = sum(
                1
                for criterion, item in common
                if abs(by_key[(left, criterion, item)] - by_key[(right, criterion, item)]) <= agreement_tolerance
            )
            pairwise[f"{left}::{right}"] = matches / len(common)

    criterion_scores: dict[str, dict[tuple[str, str], list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        criterion_scores[row.criterion_id][(row.item_id, row.prompt_version)].append(row.score)
    per_criterion = {
        criterion: round(mean(pstdev(scores) for scores in grouped.values() if len(scores) > 1), 6)
        if any(len(scores) > 1 for scores in grouped.values())
        else 0.0
        for criterion, grouped in criterion_scores.items()
    }

    variance_by_judge: dict[str, float] = {}
    for judge in judges:
        values = [row.score for row in rows if row.judge_id == judge]
        variance_by_judge[judge] = round(pstdev(values), 6) if len(values) > 1 else 0.0

    sensitivity: dict[str, float] = {}
    by_prompt: dict[str, dict[tuple[str, str], list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        by_prompt[row.criterion_id][(row.item_id, row.prompt_version)].append(row.score)
    for criterion, grouped in by_prompt.items():
        by_item: dict[str, list[float]] = defaultdict(list)
        for (item_id, _prompt), scores in grouped.items():
            by_item[item_id].append(mean(scores))
        deltas = [max(values) - min(values) for values in by_item.values() if len(values) > 1]
        sensitivity[criterion] = round(mean(deltas), 6) if deltas else 0.0

    unstable = sorted(
        criterion
        for criterion in per_criterion
        if per_criterion[criterion] >= unstable_threshold or sensitivity.get(criterion, 0.0) >= unstable_threshold
    )
    return JudgeCalibrationResult(
        pairwise_agreement=pairwise,
        per_criterion_disagreement=per_criterion,
        variance_by_judge=variance_by_judge,
        prompt_sensitivity=sensitivity,
        unstable_criteria=unstable,
        item_count=len({row.item_id for row in rows}),
        judge_count=len(judges),
    )


def calibrate_file(path: str | Path) -> dict:
    return calibrate_judges(load_judge_outputs(path)).to_dict()
