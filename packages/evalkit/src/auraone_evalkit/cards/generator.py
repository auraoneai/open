"""Dataset card generator for eval and robotics tutorial data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


EVAL_HEADINGS = [
    "Intended Use",
    "Out Of Scope Use",
    "Data Status",
    "Task Domain",
    "Rubric Design",
    "Scoring",
    "Validation",
    "Leakage Risk",
    "Limitations",
    "License",
    "Citation",
]
ROBOTICS_EXTRA = ["Embodiment", "Sensors", "Task", "Environment", "Failure Modes", "Privacy"]


def load_metadata(path: str | Path) -> dict[str, Any]:
    text = Path(path).read_text()
    if str(path).endswith((".yaml", ".yml")):
        return _parse_simple_yaml(text)
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Card metadata must be an object")
    return data


def generate_card(metadata: Mapping[str, Any], *, card_type: str = "eval") -> str:
    if card_type not in {"eval", "robotics"}:
        raise ValueError("card_type must be 'eval' or 'robotics'")
    title = metadata.get("title", "EvalKit Tutorial Dataset")
    synthetic = bool(metadata.get("synthetic", True))
    validated = bool(metadata.get("human_validated", False))
    lines = [f"# {title}", "", f"**Data status:** {_status(synthetic, validated)}", ""]
    for heading in EVAL_HEADINGS + (ROBOTICS_EXTRA if card_type == "robotics" else []):
        key = heading.lower().replace(" ", "_")
        lines.extend([f"## {heading}", "", _value(metadata.get(key)), ""])
    return "\n".join(lines).rstrip() + "\n"


def write_card(metadata: Mapping[str, Any], out: str | Path, *, card_type: str = "eval") -> Path:
    path = Path(out)
    path.write_text(generate_card(metadata, card_type=card_type))
    return path


def render_dataset_card(dataset_name: str, license_name: str = "MIT", synthetic: bool = True) -> str:
    return generate_card(
        {
            "title": dataset_name,
            "synthetic": synthetic,
            "human_validated": False,
            "intended_use": "Runnable examples for local EvalKit workflows.",
            "out_of_scope_use": "Do not use this tutorial data as a benchmark or validation set.",
            "license": license_name,
            "limitations": ["Not expert-authored, not human-validated, and not a benchmark."],
        }
    )


def _status(synthetic: bool, validated: bool) -> str:
    if synthetic and not validated:
        return "Synthetic tutorial data; not expert-authored, not human-validated, and not a benchmark."
    if not validated:
        return "Not human-validated. Use as documentation, not as a validation stamp."
    return "User-declared human validation status. EvalKit does not independently certify it."


def _value(value: Any) -> str:
    if value in (None, "", [], {}):
        return "Not provided."
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    if isinstance(value, dict):
        return "\n".join(f"- **{key}:** {item}" for key, item in value.items())
    return str(value)


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()
            if value.lower() in {"true", "false"}:
                data[current_key] = value.lower() == "true"
            elif value:
                data[current_key] = value
            else:
                data[current_key] = []
    return data
