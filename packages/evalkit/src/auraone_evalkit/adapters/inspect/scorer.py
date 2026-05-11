"""Map EvalKit tutorial records to Inspect-like sample and score shapes."""

from __future__ import annotations

from typing import Any, Mapping


def to_inspect_sample(row: Mapping[str, Any]) -> dict[str, Any]:
    if "item_id" not in row or "prompt" not in row:
        raise ValueError("Inspect sample mapping requires item_id and prompt")
    return {
        "id": row["item_id"],
        "input": row["prompt"],
        "target": row.get("expected_output", row.get("target", "")),
        "metadata": {
            "criterion_id": row.get("criterion_id"),
            "synthetic": bool(row.get("synthetic", True)),
            "source": "evalkit-tutorial",
        },
    }


def inspect_score_record(row: Mapping[str, Any], score: float, explanation: str = "") -> dict[str, Any]:
    return {
        "sample_id": row.get("item_id"),
        "score": float(score),
        "answer": row.get("output", ""),
        "explanation": explanation,
        "metadata": {
            "criterion_id": row.get("criterion_id"),
            "adapter": "inspect",
        },
    }


def optional_dependency_available() -> bool:
    try:
        __import__("inspect_ai")
    except ImportError:
        return False
    return True
