"""Input helpers for reviewer agreement files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .metrics import Annotation


def load_annotations(path: str | Path) -> list[Annotation]:
    """Load annotation rows from JSONL.

    Expected row fields are ``reviewer_id`` or ``annotator_id``, ``item_id``,
    ``criterion_id`` and ``value`` or ``score``. Rows may include an
    ``adjudicated`` boolean used by ``adjudication_rate``.
    """

    rows: list[Annotation] = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {line_no}: {exc.msg}") from exc
        rows.append(Annotation.from_mapping(raw, line_no=line_no))
    return rows


def dump_summary(summary: dict, *, indent: int = 2) -> str:
    return json.dumps(summary, indent=indent, sort_keys=True)


def annotations_from_rows(rows: Iterable[dict]) -> list[Annotation]:
    return [Annotation.from_mapping(row, line_no=index) for index, row in enumerate(rows, start=1)]
