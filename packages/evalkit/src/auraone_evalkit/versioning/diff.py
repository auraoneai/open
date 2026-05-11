from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping


SCORING_FIELDS = {"weight", "severity", "scoring_type", "max_score", "threshold"}


def diff_rubrics(old_rows: List[Dict[str, Any]], new_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    old = _by_id(old_rows, "old")
    new = _by_id(new_rows, "new")
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    scoring_impact_changes = []
    cosmetic_changes = []
    for cid in sorted(set(old) & set(new)):
        fields = {}
        for field in sorted(k for k in set(old[cid]) | set(new[cid]) if old[cid].get(k) != new[cid].get(k)):
            fields[field] = {
                "old": old[cid].get(field),
                "new": new[cid].get(field),
                "impact": "scoring" if field in SCORING_FIELDS else "cosmetic",
            }
        if fields:
            target = scoring_impact_changes if any(change["impact"] == "scoring" for change in fields.values()) else cosmetic_changes
            target.append({"criterion_id": cid, "fields": fields})
    return {
        "schema_version": "evalkit-rubric-diff-v0.1",
        "added": added,
        "removed": removed,
        "changed": scoring_impact_changes + cosmetic_changes,
        "scoring_impact_changes": scoring_impact_changes,
        "cosmetic_changes": cosmetic_changes,
        "renamed_candidates": _detect_renames(old, new, removed, added),
        "breaking_change": bool(added or removed or scoring_impact_changes),
        "comparability_risk": "high" if scoring_impact_changes or removed else "medium" if added else "low",
        "warnings": sorted(
            {
                f"{row.get('criterion_id')}: missing rubric_version metadata"
                for row in list(old_rows) + list(new_rows)
                if not row.get("rubric_version")
            }
        ),
    }


def load_rubric(path: str | Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if "criterion_id" not in row:
            raise ValueError(f"Line {line_no}: missing criterion_id")
        rows.append(row)
    return rows


def diff_files(old_path: str | Path, new_path: str | Path) -> Dict[str, Any]:
    return diff_rubrics(load_rubric(old_path), load_rubric(new_path))


def render_markdown(diff: Mapping[str, Any]) -> str:
    lines = [
        "# Rubric Diff",
        "",
        f"- Breaking change: {diff.get('breaking_change')}",
        f"- Comparability risk: {diff.get('comparability_risk')}",
        f"- Added: {', '.join(diff.get('added', [])) or 'none'}",
        f"- Removed: {', '.join(diff.get('removed', [])) or 'none'}",
        "",
        "## Scoring Impact Changes",
        "",
    ]
    changes = diff.get("scoring_impact_changes", [])
    lines.extend(f"- {change['criterion_id']}: {', '.join(change['fields'])}" for change in changes)
    if not changes:
        lines.append("No scoring-impact changes.")
    return "\n".join(lines) + "\n"


def _by_id(rows: List[Dict[str, Any]], label: str) -> dict[str, Dict[str, Any]]:
    output = {}
    for row in rows:
        cid = str(row.get("criterion_id", ""))
        if not cid:
            raise ValueError(f"{label} rubric row missing criterion_id")
        if cid in output:
            raise ValueError(f"{label} rubric has duplicate criterion_id: {cid}")
        output[cid] = row
    return output


def _detect_renames(old: dict[str, Mapping[str, Any]], new: dict[str, Mapping[str, Any]], removed: list[str], added: list[str]) -> list[dict[str, str]]:
    return [
        {"old_id": old_id, "new_id": new_id, "reason": "same criterion text"}
        for old_id in removed
        for new_id in added
        if old[old_id].get("criterion") == new[new_id].get("criterion")
    ]
