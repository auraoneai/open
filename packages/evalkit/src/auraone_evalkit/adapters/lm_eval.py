from __future__ import annotations

from typing import Any, Dict, List


def to_lm_eval_task(rubric_rows: List[Dict[str, Any]], response_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"task": "auraone_evalkit_tutorial", "disclosure": "Synthetic/tutorial conversion; not a leaderboard task.", "dataset_path": "local_json", "rubric_criteria": [r.get("criterion_id") for r in rubric_rows], "doc_to_text": "{{prompt}}", "doc_to_target": "{{expected}}", "samples": response_rows}
