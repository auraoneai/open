"""Deterministic sampling strategies for model outputs."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import random
from typing import Any, Iterable, Mapping


def load_outputs(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if "item_id" not in row:
            raise ValueError(f"Line {line_no}: missing item_id")
        rows.append(row)
    return rows


def sample_outputs(
    rows: Iterable[Mapping[str, Any]],
    *,
    strategy: str,
    k: int,
    seed: int = 13,
    strata_field: str = "criterion_id",
) -> dict[str, Any]:
    items = [dict(row) for row in rows]
    if not items:
        raise ValueError("At least one output row is required")
    if k <= 0:
        raise ValueError("k must be positive")
    rng = random.Random(seed)
    if strategy == "random":
        selected = rng.sample(items, min(k, len(items)))
        rationale = "deterministic random sample"
    elif strategy == "stratified":
        selected = _stratified(items, k, rng, strata_field)
        rationale = f"balanced across {strata_field}"
    elif strategy == "diversity":
        selected = sorted(items, key=lambda row: (-len(set(str(row.get("output", "")).split())), str(row["item_id"])))[:k]
        rationale = "highest lexical diversity proxy"
    elif strategy == "failure-heavy":
        selected = sorted(items, key=lambda row: (-float(row.get("failure_score", row.get("error_score", 0))), str(row["item_id"])))[:k]
        rationale = "highest failure score"
    elif strategy == "judge-disagreement-heavy":
        selected = sorted(items, key=lambda row: (-float(row.get("judge_disagreement", 0)), str(row["item_id"])))[:k]
        rationale = "highest judge disagreement"
    elif strategy == "uncertainty":
        selected = sorted(items, key=lambda row: (-_uncertainty(row), str(row["item_id"])))[:k]
        rationale = "highest uncertainty"
    elif strategy == "regression":
        selected = sorted(items, key=lambda row: (-float(row.get("regression_delta", 0)), str(row["item_id"])))[:k]
        rationale = "largest regression delta"
    else:
        raise ValueError(f"Unknown sampling strategy: {strategy}")
    return {
        "strategy": strategy,
        "seed": seed,
        "selected": [
            {
                "item_id": row["item_id"],
                "rationale": _item_rationale(row, strategy),
            }
            for row in selected
        ],
        "warnings": _warnings(items, strategy, strata_field),
        "limitations": ["Sampling prioritizes review candidates; it is not a substitute for full validation."],
        "summary": rationale,
    }


def _stratified(items: list[dict[str, Any]], k: int, rng: random.Random, field: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[str(item.get(field, "__missing__"))].append(item)
    selected = []
    for key in sorted(grouped):
        bucket = grouped[key][:]
        rng.shuffle(bucket)
        if bucket:
            selected.append(bucket[0])
            if len(selected) == k:
                return selected
    remaining = [item for item in items if item not in selected]
    rng.shuffle(remaining)
    return selected + remaining[: max(0, k - len(selected))]


def _uncertainty(row: Mapping[str, Any]) -> float:
    if "uncertainty" in row:
        return float(row["uncertainty"])
    if "confidence" in row:
        return 1.0 - float(row["confidence"])
    return 0.0


def _item_rationale(row: Mapping[str, Any], strategy: str) -> str:
    if strategy == "uncertainty":
        return f"uncertainty={_uncertainty(row):.3f}"
    for field in ("failure_score", "judge_disagreement", "regression_delta"):
        if field in row:
            return f"{field}={float(row[field]):.3f}"
    return "selected by strategy"


def _warnings(items: list[dict[str, Any]], strategy: str, strata_field: str) -> list[str]:
    required = {
        "stratified": strata_field,
        "failure-heavy": "failure_score",
        "judge-disagreement-heavy": "judge_disagreement",
        "regression": "regression_delta",
    }.get(strategy)
    if required and any(required not in item for item in items):
        return [f"Some rows are missing {required}; defaults may affect selection."]
    if strategy == "uncertainty" and any("uncertainty" not in item and "confidence" not in item for item in items):
        return ["Some rows are missing uncertainty/confidence; default uncertainty=0 was used."]
    return []
