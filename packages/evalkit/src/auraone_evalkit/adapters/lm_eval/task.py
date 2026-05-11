"""Map EvalKit tutorial rows to lm-eval-style task configuration."""

from __future__ import annotations

from typing import Any, Iterable, Mapping


def build_task_config(
    rows: Iterable[Mapping[str, Any]],
    *,
    task_name: str = "evalkit_tutorial",
    dataset_path: str = "examples/quality/synthetic_multiturn/conversations.jsonl",
) -> dict[str, Any]:
    rows = list(rows)
    if not rows:
        raise ValueError("At least one tutorial row is required")
    return {
        "task": task_name,
        "dataset_path": dataset_path,
        "output_type": "generate_until",
        "doc_to_text": "{{prompt}}",
        "doc_to_target": "{{expected_output}}",
        "metadata": {
            "synthetic": True,
            "not_benchmark": True,
            "criteria": sorted({str(row.get("criterion_id", "__default__")) for row in rows}),
        },
    }


def normalize_result(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "item_id": result.get("doc_id", result.get("item_id")),
        "score": float(result.get("score", result.get("acc", 0.0))),
        "adapter": "lm_eval",
        "raw": dict(result),
    }


def optional_dependency_available() -> bool:
    try:
        __import__("lm_eval")
    except ImportError:
        return False
    return True
