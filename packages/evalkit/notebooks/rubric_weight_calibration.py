"""Synthetic tutorial rubric weight calibration walkthrough.

Run from ``opensource/evalkit``:

    python notebooks/rubric_weight_calibration.py

The fixture is synthetic tutorial data only. It is not expert-authored,
human-validated, benchmark-grade, or a recommendation for production weights.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "examples" / "weight_calibration" / "rubric_weight_scenarios.json"


def score_item(criterion_scores: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("weights must sum to a positive value")
    return round(sum(criterion_scores[name] * weight for name, weight in weights.items()) / total_weight, 6)


def main() -> None:
    payload = json.loads(SCENARIOS.read_text())
    items = payload["items"]
    for scenario in payload["scenarios"]:
        scores = [
            {
                "item_id": item["item_id"],
                "score": score_item(item["criterion_scores"], scenario["weights"]),
            }
            for item in items
        ]
        ranking = sorted(scores, key=lambda row: (-row["score"], row["item_id"]))
        print(json.dumps({"scenario_id": scenario["scenario_id"], "ranking": ranking}, sort_keys=True))


if __name__ == "__main__":
    main()
