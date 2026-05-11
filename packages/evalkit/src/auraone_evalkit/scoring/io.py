"""Input helpers for scoring files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_records(path: Path | str) -> list[dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist")
    text = file_path.read_text(encoding="utf-8")
    if not text.strip():
        return []
    if text.lstrip().startswith("["):
        parsed = json.loads(text)
        if not isinstance(parsed, list):
            raise ValueError(f"{file_path} must contain a JSON array or JSONL records")
        if not all(isinstance(item, dict) for item in parsed):
            raise ValueError(f"{file_path} must contain only JSON objects")
        return parsed
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ValueError(f"{file_path}:{line_number} must be a JSON object")
        records.append(item)
    return records

