from __future__ import annotations

import hashlib
from typing import Any, Dict, List


def _fingerprint(text: str) -> str:
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def audit_leakage(train_rows: List[Dict[str, Any]], eval_rows: List[Dict[str, Any]], text_field: str = "prompt") -> Dict[str, Any]:
    train = {_fingerprint(str(r.get(text_field, ""))): r for r in train_rows}
    duplicates = []
    for row in eval_rows:
        fp = _fingerprint(str(row.get(text_field, "")))
        if fp in train:
            duplicates.append({"eval_id": row.get("id") or row.get("response_id"), "train_id": train[fp].get("id") or train[fp].get("response_id"), "fingerprint": fp})
    return {"schema_version": "evalkit-leakage-audit-v0.1", "text_field": text_field, "duplicate_count": len(duplicates), "duplicates": duplicates}
