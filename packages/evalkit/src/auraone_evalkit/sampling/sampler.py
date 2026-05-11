from __future__ import annotations

import random
from typing import Any, Dict, List


def sample_outputs(rows: List[Dict[str, Any]], n: int, seed: int = 13, stratify_field: str | None = None) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    if not stratify_field:
        rows_copy = list(rows)
        rng.shuffle(rows_copy)
        return rows_copy[:n]
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row.get(stratify_field, "__missing__")), []).append(row)
    result: List[Dict[str, Any]] = []
    for key in sorted(groups):
        group = groups[key]
        rng.shuffle(group)
        take = max(1, round(n * len(group) / max(1, len(rows))))
        result.extend(group[:take])
    rng.shuffle(result)
    return result[:n]
