"""Analyze how rubric weights affect aggregate model rankings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


def load_weight_scenarios(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict):
        raise ValueError("Weight calibration scenario must be a JSON object")
    return data


def analyze_weight_scenarios(data: Mapping[str, Any]) -> dict[str, Any]:
    criteria = data.get("criteria", [])
    models = data.get("models", [])
    scenarios = data.get("scenarios", [])
    if not criteria or not models or not scenarios:
        raise ValueError("criteria, models, and scenarios are required")
    criterion_ids = [criterion["criterion_id"] for criterion in criteria]
    scenario_results = []
    rankings = []
    for scenario in scenarios:
        weights = {cid: float(scenario.get("weights", {}).get(cid, 0.0)) for cid in criterion_ids}
        total_weight = sum(weights.values()) or 1.0
        scores = {}
        for model in models:
            model_scores = model.get("scores", {})
            scores[model["model_id"]] = sum(float(model_scores.get(cid, 0.0)) * weights[cid] for cid in criterion_ids) / total_weight
        ranking = sorted(scores, key=lambda model_id: (-scores[model_id], model_id))
        rankings.append(ranking)
        scenario_results.append({"scenario_id": scenario["scenario_id"], "scores": scores, "ranking": ranking})
    baseline = rankings[0]
    changed = [result["scenario_id"] for result, ranking in zip(scenario_results, rankings) if ranking != baseline]
    return {
        "scenario_results": scenario_results,
        "baseline_ranking": baseline,
        "ranking_instability": bool(changed),
        "changed_ranking_scenarios": changed,
        "high_leverage_criteria": _criterion_leverage(criteria, models),
        "limitations": [
            "Weight sensitivity explains ranking dependence on rubric design; it does not validate the rubric.",
            "Tutorial scenarios are synthetic and not human-validated.",
        ],
    }


def calibrate_weights(rows: list[Mapping[str, Any]] | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(rows, Mapping):
        return analyze_weight_scenarios(rows)
    grouped: dict[str, list[float]] = {}
    for row in rows:
        cid = str(row.get("criterion_id", "__default__"))
        disagreement = row.get("disagreement_rate", row.get("error_rate"))
        if isinstance(disagreement, (int, float)):
            grouped.setdefault(cid, []).append(float(disagreement))
    suggestions = []
    for cid, values in sorted(grouped.items()):
        avg = sum(values) / len(values)
        suggestions.append({"criterion_id": cid, "observed_disagreement": avg, "suggestion": "lower weight or rewrite criterion" if avg >= 0.35 else "keep weight, monitor drift"})
    return {"schema_version": "evalkit-weight-calibration-v0.1", "suggestions": suggestions}


def _criterion_leverage(criteria: list[Mapping[str, Any]], models: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for criterion in criteria:
        cid = criterion["criterion_id"]
        values = [float(model.get("scores", {}).get(cid, 0.0)) for model in models]
        spread = max(values) - min(values) if values else 0.0
        output.append({"criterion_id": cid, "score_spread": round(spread, 6)})
    return sorted(output, key=lambda row: (-row["score_spread"], row["criterion_id"]))
