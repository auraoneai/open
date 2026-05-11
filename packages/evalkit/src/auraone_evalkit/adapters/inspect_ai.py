from __future__ import annotations

from typing import Any, Dict, List


def to_inspect_dataset(rubric_rows: List[Dict[str, Any]], response_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"adapter": "inspect-ai", "disclosure": "Synthetic/tutorial conversion; not a benchmark.", "samples": [{"id": r.get("response_id") or r.get("id"), "input": r.get("prompt"), "target": r.get("expected"), "metadata": {"rubric_criteria": [c.get("criterion_id") for c in rubric_rows]}} for r in response_rows]}
