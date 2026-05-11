"""Offline duplicate and near-duplicate leakage audit."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import re
from typing import Any, Callable, Iterable, Mapping


EmbeddingSimilarity = Callable[[str, str], float]


def load_items(path: str | Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if "item_id" not in row:
            raise ValueError(f"Line {line_no}: missing item_id")
        if "prompt" not in row and "text" not in row:
            raise ValueError(f"Line {line_no}: missing prompt or text")
        items.append(row)
    return items


def audit_leakage(
    items: Iterable[Mapping[str, Any]],
    *,
    reference_items: Iterable[Mapping[str, Any]] | None = None,
    near_duplicate_threshold: float = 0.72,
    embedding_similarity: EmbeddingSimilarity | None = None,
) -> dict[str, Any]:
    rows = list(items)
    refs = list(reference_items or [])
    if not rows:
        raise ValueError("At least one item is required")
    comparisons = []
    all_pairs = [(left, right, "internal") for index, left in enumerate(rows) for right in rows[index + 1 :]]
    all_pairs.extend((left, right, "reference") for left in rows for right in refs)
    for left, right, source in all_pairs:
        left_text = _text(left)
        right_text = _text(right)
        exact = _normalize(left_text) == _normalize(right_text)
        token_score = _jaccard(_tokens(left_text), _tokens(right_text))
        ngram_score = _jaccard(_ngrams(left_text), _ngrams(right_text))
        embedding_score = embedding_similarity(left_text, right_text) if embedding_similarity else None
        score = max(token_score, ngram_score, embedding_score or 0.0, 1.0 if exact else 0.0)
        if exact or score >= near_duplicate_threshold:
            comparisons.append(
                {
                    "left_id": str(left["item_id"]),
                    "right_id": str(right["item_id"]),
                    "source": source,
                    "risk": "exact_duplicate" if exact else "near_duplicate",
                    "similarity": round(score, 6),
                    "evidence": [_snippet(left_text), _snippet(right_text)],
                }
            )
    return {
        "item_count": len(rows),
        "finding_count": len(comparisons),
        "findings": comparisons,
        "clusters": _clusters(comparisons),
        "limitations": [
            "Offline similarity catches obvious overlap; it is not proof that an eval is uncontaminated.",
            "No web search or private benchmark comparison is performed.",
        ],
    }


def _text(row: Mapping[str, Any]) -> str:
    return str(row.get("prompt", row.get("text", "")))


def _normalize(text: str) -> str:
    return " ".join(_tokens(text))


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _ngrams(text: str, n: int = 5) -> set[str]:
    compact = re.sub(r"\s+", " ", text.lower()).strip()
    if len(compact) <= n:
        return {compact}
    return {compact[index : index + n] for index in range(len(compact) - n + 1)}


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _snippet(text: str, limit: int = 120) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _clusters(findings: list[dict[str, Any]]) -> list[list[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for finding in findings:
        graph[finding["left_id"]].add(finding["right_id"])
        graph[finding["right_id"]].add(finding["left_id"])
    seen = set()
    clusters = []
    for node in sorted(graph):
        if node in seen:
            continue
        stack = [node]
        cluster = set()
        while stack:
            current = stack.pop()
            if current in cluster:
                continue
            cluster.add(current)
            stack.extend(graph[current] - cluster)
        seen |= cluster
        clusters.append(sorted(cluster))
    return clusters
