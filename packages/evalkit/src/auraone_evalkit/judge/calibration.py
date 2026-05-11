from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List


def calibrate_judge(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = 0
    exact = 0
    by_criterion: Dict[str, List[float]] = defaultdict(list)
    disagreements = []
    for row in rows:
        ref = row.get("reference_score")
        judge = row.get("judge_score")
        if not isinstance(ref, (int, float)) or not isinstance(judge, (int, float)):
            continue
        total += 1
        err = abs(float(ref) - float(judge))
        exact += int(err <= 1e-9)
        by_criterion[str(row.get("criterion_id"))].append(err)
        if err >= 0.5:
            disagreements.append({"response_id": row.get("response_id"), "criterion_id": row.get("criterion_id"), "reference_score": ref, "judge_score": judge, "absolute_error": err})
    return {"schema_version": "evalkit-judge-calibration-v0.1", "row_count": total, "exact_match_rate": exact / total if total else None, "mean_absolute_error_by_criterion": {k: sum(v)/len(v) for k, v in sorted(by_criterion.items())}, "large_disagreements": disagreements}
