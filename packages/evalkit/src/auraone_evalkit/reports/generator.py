"""Markdown, HTML, and JSON report generation for local EvalKit outputs."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
from typing import Any, Mapping


REQUIRED_SECTIONS = [
    "executive_summary",
    "rubric_coverage",
    "score_breakdown",
    "unstable_criteria",
    "agreement",
    "drift",
    "limitations",
]


def render_report(score_payload: Mapping[str, Any]) -> str:
    """Compatibility wrapper for the root CLI scaffold.

    If the input looks like a scorer payload, render a compact score report.
    Otherwise use the richer EvalKit report schema.
    """

    if "criterion_summary" not in score_payload:
        return generate_markdown_report(score_payload)
    lines = [
        "# EvalKit Eval Run Report",
        "",
        "Synthetic/tutorial examples are not expert-authored, human-validated, or benchmark-grade.",
        "",
        f"- Schema: `{score_payload.get('schema_version', 'unknown')}`",
        f"- Responses: {score_payload.get('response_count', 0)}",
        f"- Criteria: {score_payload.get('criterion_count', 0)}",
        f"- Overall score: {score_payload.get('overall_score')}",
        f"- Missing labels: {len(score_payload.get('missing_labels', []))}",
        "",
        "## Criterion Summary",
    ]
    for criterion_id, summary in sorted(score_payload.get("criterion_summary", {}).items()):
        mean = summary.get("mean")
        mean_text = f"{mean:.3f}" if isinstance(mean, (int, float)) else "n/a"
        lines.append(f"- `{criterion_id}`: mean={mean_text}, count={summary.get('count')}")
    lines.extend(
        [
            "",
            "## Limitations",
            "This report is a local EvalKit artifact. It is not a model leaderboard or safety certification.",
        ]
    )
    return "\n".join(lines) + "\n"


def load_report_input(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict):
        raise ValueError("Report input must be a JSON object")
    return data


def generate_json_report(data: Mapping[str, Any]) -> dict[str, Any]:
    source = data.get("source", {})
    synthetic = bool(source.get("synthetic", data.get("synthetic", False))) if isinstance(source, Mapping) else False
    sections = {section: data.get(section) for section in REQUIRED_SECTIONS}
    omitted = [section for section, value in sections.items() if value in (None, [], {})]
    return {
        "title": data.get("title", "EvalKit Tutorial Report"),
        "source": source,
        "disclosure": _disclosure(synthetic),
        "sections": sections,
        "omitted_sections": omitted,
    }


def generate_markdown_report(data: Mapping[str, Any]) -> str:
    report = generate_json_report(data)
    lines = [
        f"# {report['title']}",
        "",
        f"**Disclosure:** {report['disclosure']}",
        "",
    ]
    for section in REQUIRED_SECTIONS:
        title = section.replace("_", " ").title()
        value = report["sections"].get(section)
        lines.extend([f"## {title}", ""])
        if value in (None, [], {}):
            lines.extend([f"No {title.lower()} section was provided.", ""])
        else:
            lines.extend([_markdown_value(value), ""])
    if report["omitted_sections"]:
        lines.extend(["## Omitted Sections", "", ", ".join(report["omitted_sections"]), ""])
    return "\n".join(lines).rstrip() + "\n"


def generate_html_report(data: Mapping[str, Any]) -> str:
    markdown = generate_markdown_report(data)
    body = []
    for line in markdown.splitlines():
        if line.startswith("# "):
            body.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("## "):
            body.append(f"<h2>{escape(line[3:])}</h2>")
        elif not line:
            continue
        else:
            body.append(f"<p>{escape(line)}</p>")
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            '<head><meta charset="utf-8"><title>EvalKit Report</title>',
            "<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:40px auto;line-height:1.5}"
            "h1,h2{color:#102033}code,pre{background:#f3f5f7;padding:2px 4px}</style></head>",
            "<body>",
            *body,
            "</body></html>",
        ]
    )


def write_report(data: Mapping[str, Any], out: str | Path) -> Path:
    path = Path(out)
    suffix = path.suffix.lower()
    if suffix == ".html":
        content = generate_html_report(data)
    elif suffix == ".json":
        content = json.dumps(generate_json_report(data), indent=2, sort_keys=True) + "\n"
    else:
        content = generate_markdown_report(data)
    path.write_text(content)
    return path


def _disclosure(synthetic: bool) -> str:
    if synthetic:
        return "Synthetic tutorial data; not expert-authored, not human-validated, and not a benchmark."
    return "User-provided data. EvalKit does not certify validation status."


def _markdown_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(f"- {_inline(item)}" for item in value)
    if isinstance(value, dict):
        return "\n".join(f"- **{key}:** {_inline(item)}" for key, item in value.items())
    return str(value)


def _inline(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return f"`{json.dumps(value, sort_keys=True)}`"
    return str(value)
