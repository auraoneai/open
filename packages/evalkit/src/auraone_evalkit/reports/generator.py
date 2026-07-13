"""Deterministic Markdown, HTML, and JSON evidence report generation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, StrictUndefined

from auraone_evalkit import __version__


REPORT_SCHEMA_VERSION = "auraone.evalkit.report.v1"
LEGACY_SECTIONS = (
    "executive_summary",
    "rubric_coverage",
    "score_breakdown",
    "unstable_criteria",
    "agreement",
    "drift",
    "leakage",
    "limitations",
)
GATE_STATUSES = {"passed", "warning", "failed", "not_run"}
FINDING_SEVERITIES = {"info", "review", "warning", "danger", "blocked"}


def render_report(score_payload: Mapping[str, Any]) -> str:
    """Render the backward-compatible Markdown report used by the root CLI."""

    return generate_markdown_report(score_payload)


def load_report_input(path: str | Path) -> dict[str, Any]:
    """Load a report input and require a top-level JSON object."""

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Report input must be a JSON object")
    return data


def generate_json_report(data: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize legacy, score, or v1 report input into the stable v1 contract."""

    source = _mapping(data.get("source"))
    synthetic = bool(source.get("synthetic", data.get("synthetic", False)))
    sections = {section: data.get(section) for section in LEGACY_SECTIONS}
    score_input = _is_score_payload(data)

    summary = _normalize_summary(data, score_input)
    gates = _normalize_gates(data, score_input)
    findings = _normalize_findings(data, score_input)
    evidence = _normalize_evidence(data, score_input)
    reproduce = _normalize_reproduce(data)
    metadata = _normalize_metadata(data)
    omitted = _omitted_evidence(sections, data, gates, evidence, reproduce)

    normalized: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "title": str(data.get("title") or "EvalKit Eval Run Report"),
        "decision": _normalize_decision(data, gates),
        "disclosure": str(data.get("disclosure") or _disclosure(synthetic)),
        "source": _sorted_mapping(source),
        "metadata": metadata,
        "summary": summary,
        "gates": gates,
        "findings": findings,
        "evidence": evidence,
        "reproduce": reproduce,
        "sections": sections,
        "omitted_evidence": omitted,
    }
    normalized["metadata"]["input_sha256"] = sha256(
        _canonical_json(normalized).encode("utf-8")
    ).hexdigest()
    return normalized


def generate_markdown_report(data: Mapping[str, Any]) -> str:
    """Render a deterministic Markdown evidence report."""

    report = generate_json_report(data)
    decision = report["decision"]
    lines = [
        f"# {report['title']}",
        "",
        f"**Decision:** {decision['label']}",
        f"**Disclosure:** {report['disclosure']}",
        "",
        "## Summary",
        "",
        report["summary"]["headline"],
        "",
    ]

    if report["summary"]["metrics"]:
        lines.extend(
            f"- **{metric['label']}:** {_inline(metric['value'])}"
            for metric in report["summary"]["metrics"]
        )
        lines.append("")

    lines.extend(["## Quality Gates", ""])
    if report["gates"]:
        lines.extend(
            f"- **{gate['label']}:** {gate['status'].replace('_', ' ').title()}"
            + (f" - {gate['detail']}" if gate["detail"] else "")
            for gate in report["gates"]
        )
    else:
        lines.append("No quality gates were supplied.")
    lines.append("")

    lines.extend(["## Findings", ""])
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(
                f"- **{finding['severity'].title()} - {finding['title']}:** "
                f"{finding['detail']}"
            )
    else:
        lines.append("No findings were reported.")
    lines.append("")

    lines.extend(["## Evidence", ""])
    if report["evidence"]:
        for item in report["evidence"]:
            lines.append(f"- **{item['label']}:** {_inline(item['value'])}")
    else:
        lines.append("No evidence records were supplied.")
    lines.append("")

    for section in LEGACY_SECTIONS:
        value = report["sections"].get(section)
        if value in (None, [], {}):
            continue
        lines.extend([f"## {_markdown_section_title(section)}", "", _markdown_value(value), ""])

    lines.extend(["## Reproduce", ""])
    if report["reproduce"]["command"]:
        lines.extend(["```bash", report["reproduce"]["command"], "```", ""])
    else:
        lines.extend(["No reproduction command was supplied.", ""])
    if report["reproduce"]["inputs"]:
        lines.extend(
            f"- **{key}:** `{value}`"
            for key, value in report["reproduce"]["inputs"].items()
        )
        lines.append("")

    lines.extend(["## Missing Or Omitted Evidence", ""])
    if report["omitted_evidence"]:
        lines.extend(f"- {item}" for item in report["omitted_evidence"])
    else:
        lines.append("No required report evidence is marked as omitted.")
    lines.append("")

    metadata = report["metadata"]
    lines.extend(
        [
            "## Artifact Metadata",
            "",
            f"- **Report schema:** `{report['schema_version']}`",
            f"- **EvalKit version:** `{metadata['evalkit_version']}`",
            f"- **Input SHA-256:** `{metadata['input_sha256']}`",
        ]
    )
    if metadata.get("generated_at"):
        lines.append(f"- **Generated at:** `{metadata['generated_at']}`")
    if metadata.get("run_id"):
        lines.append(f"- **Run ID:** `{metadata['run_id']}`")
    if metadata.get("artifact_sha256"):
        lines.append(f"- **Artifact SHA-256:** `{metadata['artifact_sha256']}`")
    return "\n".join(lines).rstrip() + "\n"


def generate_html_report(data: Mapping[str, Any]) -> str:
    """Render the canonical, self-contained Proofline HTML report."""

    report = generate_json_report(data)
    environment = Environment(
        loader=PackageLoader("auraone_evalkit", "reports/templates"),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.filters["display_value"] = _display_value
    environment.filters["section_title"] = _section_title
    environment.filters["json_pretty"] = lambda value: json.dumps(
        value, indent=2, sort_keys=True, ensure_ascii=True
    )
    return environment.get_template("html.html.j2").render(report=report).rstrip() + "\n"


def write_report(
    data: Mapping[str, Any],
    out: str | Path,
    output_format: str | None = None,
) -> Path:
    """Write a report, inferring its format from the destination when omitted."""

    path = Path(out)
    resolved_format = output_format or _format_from_path(path)
    if resolved_format == "html":
        content = generate_html_report(data)
    elif resolved_format == "json":
        content = json.dumps(
            generate_json_report(data), indent=2, sort_keys=True, ensure_ascii=True
        ) + "\n"
    elif resolved_format == "markdown":
        content = generate_markdown_report(data)
    else:
        raise ValueError(f"Unsupported report format: {resolved_format}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def _normalize_summary(data: Mapping[str, Any], score_input: bool) -> dict[str, Any]:
    provided = _mapping(data.get("summary"))
    if score_input:
        headline = str(
            data.get("executive_summary")
            or provided.get("headline")
            or "Deterministic scoring completed for the supplied outputs and labels."
        )
        metrics = [
            _metric("average-score", "Average score", provided.get("average_score")),
            _metric("pass-rate", "Pass rate", provided.get("pass_rate")),
            _metric("scored-outputs", "Scored outputs", provided.get("scored_outputs")),
            _metric("criteria", "Criteria", provided.get("criterion_count")),
            _metric("missing-labels", "Missing labels", provided.get("missing_label_count")),
        ]
    else:
        raw_metrics = provided.get("metrics", [])
        metrics = [
            _normalize_metric(item, index)
            for index, item in enumerate(_sequence(raw_metrics), start=1)
        ]
        if not metrics:
            metrics = _legacy_metrics(data)
        headline = str(
            provided.get("headline")
            or data.get("executive_summary")
            or "Review the available evidence and quality gates before making a release decision."
        )
    return {"headline": headline, "metrics": [item for item in metrics if item["value"] is not None]}


def _normalize_gates(data: Mapping[str, Any], score_input: bool) -> list[dict[str, Any]]:
    raw_gates = _sequence(data.get("gates"))
    if raw_gates:
        return [_normalize_gate(item, index) for index, item in enumerate(raw_gates, start=1)]
    if not score_input:
        return []

    summary = _mapping(data.get("summary"))
    average = _number(summary.get("average_score"))
    pass_rate = _number(summary.get("pass_rate"))
    missing = int(_number(summary.get("missing_label_count")) or 0)
    threshold = _number(data.get("pass_threshold"))
    return [
        {
            "id": "average-score",
            "label": "Average score threshold",
            "status": "passed" if average is not None and threshold is not None and average >= threshold else "failed",
            "observed": average,
            "threshold": threshold,
            "detail": "Average score compared with the configured pass threshold.",
        },
        {
            "id": "label-coverage",
            "label": "Label coverage",
            "status": "passed" if missing == 0 else "warning",
            "observed": missing,
            "threshold": 0,
            "detail": "Missing criterion labels across scored outputs.",
        },
        {
            "id": "output-pass-rate",
            "label": "Output pass rate",
            "status": "passed" if pass_rate == 1 else ("warning" if pass_rate else "failed"),
            "observed": pass_rate,
            "threshold": 1,
            "detail": "Share of outputs meeting the configured pass threshold.",
        },
    ]


def _normalize_findings(data: Mapping[str, Any], score_input: bool) -> list[dict[str, Any]]:
    raw_findings = _sequence(data.get("findings"))
    findings = [
        _normalize_finding(item, index)
        for index, item in enumerate(raw_findings, start=1)
    ]
    if findings or not score_input:
        return findings

    for output in _sequence(data.get("outputs")):
        if not isinstance(output, Mapping):
            continue
        output_id = str(output.get("output_id", "unknown output"))
        missing = _sequence(output.get("missing_criteria"))
        if missing:
            findings.append(
                {
                    "id": f"missing-labels-{_slug(output_id)}",
                    "severity": "warning",
                    "title": f"Missing labels for {output_id}",
                    "detail": ", ".join(str(item) for item in missing),
                    "criterion_id": None,
                    "evidence_refs": [f"output-{_slug(output_id)}"],
                }
            )
        if output.get("passed") is False:
            findings.append(
                {
                    "id": f"failed-output-{_slug(output_id)}",
                    "severity": "review",
                    "title": f"Output below threshold: {output_id}",
                    "detail": f"Observed score: {_display_value(output.get('score'))}.",
                    "criterion_id": None,
                    "evidence_refs": [f"output-{_slug(output_id)}"],
                }
            )
    return findings


def _normalize_evidence(data: Mapping[str, Any], score_input: bool) -> list[dict[str, Any]]:
    raw_evidence = _sequence(data.get("evidence"))
    evidence = [
        _normalize_evidence_item(item, index)
        for index, item in enumerate(raw_evidence, start=1)
    ]
    if evidence or not score_input:
        return evidence
    for output in _sequence(data.get("outputs")):
        if not isinstance(output, Mapping):
            continue
        output_id = str(output.get("output_id", "unknown"))
        evidence.append(
            {
                "id": f"output-{_slug(output_id)}",
                "label": f"Scored output {output_id}",
                "kind": "score",
                "value": {
                    "score": output.get("score"),
                    "passed": output.get("passed"),
                    "missing_criteria": output.get("missing_criteria", []),
                },
                "href": None,
                "sha256": None,
            }
        )
    return evidence


def _normalize_reproduce(data: Mapping[str, Any]) -> dict[str, Any]:
    reproduce = _mapping(data.get("reproduce"))
    inputs = _mapping(reproduce.get("inputs"))
    environment = _mapping(reproduce.get("environment"))
    return {
        "command": str(reproduce.get("command", "")).strip(),
        "inputs": _sorted_mapping(inputs),
        "environment": _sorted_mapping(environment),
    }


def _normalize_metadata(data: Mapping[str, Any]) -> dict[str, Any]:
    supplied = _mapping(data.get("metadata"))
    return {
        "evalkit_version": str(supplied.get("evalkit_version") or __version__),
        "generated_at": _optional_string(supplied.get("generated_at")),
        "run_id": _optional_string(supplied.get("run_id")),
        "commit": _optional_string(supplied.get("commit")),
        "artifact_sha256": _optional_string(supplied.get("artifact_sha256")),
    }


def _normalize_decision(
    data: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]
) -> dict[str, str]:
    supplied = data.get("decision")
    if isinstance(supplied, Mapping):
        status = str(supplied.get("status", "review")).lower()
        return {
            "status": status if status in {"pass", "review", "fail", "blocked"} else "review",
            "label": str(supplied.get("label") or status.replace("_", " ").title()),
            "detail": str(supplied.get("detail", "")),
        }
    statuses = {str(gate.get("status")) for gate in gates}
    if "failed" in statuses:
        return {"status": "fail", "label": "Action required", "detail": "One or more quality gates failed."}
    if statuses & {"warning", "not_run"}:
        return {"status": "review", "label": "Review required", "detail": "One or more quality gates need review."}
    if gates:
        return {"status": "pass", "label": "Gates passed", "detail": "All supplied quality gates passed."}
    return {"status": "review", "label": "Decision not supplied", "detail": "No quality gates were supplied."}


def _normalize_metric(item: Any, index: int) -> dict[str, Any]:
    if isinstance(item, Mapping):
        return {
            "id": str(item.get("id") or f"metric-{index}"),
            "label": str(item.get("label") or item.get("id") or f"Metric {index}"),
            "value": item.get("value"),
            "detail": str(item.get("detail", "")),
        }
    return _metric(f"metric-{index}", f"Metric {index}", item)


def _normalize_gate(item: Any, index: int) -> dict[str, Any]:
    gate = _mapping(item)
    status = str(gate.get("status", "not_run")).lower().replace("-", "_")
    return {
        "id": str(gate.get("id") or f"gate-{index}"),
        "label": str(gate.get("label") or gate.get("id") or f"Gate {index}"),
        "status": status if status in GATE_STATUSES else "not_run",
        "observed": gate.get("observed"),
        "threshold": gate.get("threshold"),
        "detail": str(gate.get("detail", "")),
    }


def _normalize_finding(item: Any, index: int) -> dict[str, Any]:
    finding = _mapping(item)
    severity = str(finding.get("severity", "info")).lower()
    return {
        "id": str(finding.get("id") or f"finding-{index}"),
        "severity": severity if severity in FINDING_SEVERITIES else "info",
        "title": str(finding.get("title") or finding.get("id") or f"Finding {index}"),
        "detail": str(finding.get("detail") or finding.get("message") or ""),
        "criterion_id": _optional_string(finding.get("criterion_id")),
        "evidence_refs": [str(value) for value in _sequence(finding.get("evidence_refs"))],
    }


def _normalize_evidence_item(item: Any, index: int) -> dict[str, Any]:
    evidence = _mapping(item)
    return {
        "id": str(evidence.get("id") or f"evidence-{index}"),
        "label": str(evidence.get("label") or evidence.get("id") or f"Evidence {index}"),
        "kind": str(evidence.get("kind", "record")),
        "value": evidence.get("value"),
        "href": _safe_href(evidence.get("href")),
        "sha256": _optional_string(evidence.get("sha256")),
    }


def _legacy_metrics(data: Mapping[str, Any]) -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    coverage = _mapping(data.get("rubric_coverage"))
    for key, value in coverage.items():
        metrics.append(_metric(f"coverage-{_slug(str(key))}", str(key).replace("_", " ").title(), value))
    return metrics


def _omitted_evidence(
    sections: Mapping[str, Any],
    data: Mapping[str, Any],
    gates: Sequence[Any],
    evidence: Sequence[Any],
    reproduce: Mapping[str, Any],
) -> list[str]:
    omitted = [
        _section_title(section)
        for section, value in sections.items()
        if value in (None, [], {})
    ]
    if not gates:
        omitted.append("Quality gates")
    if not evidence:
        omitted.append("Evidence records")
    if not reproduce.get("command"):
        omitted.append("Reproduction command")
    metadata = _mapping(data.get("metadata"))
    if not metadata.get("generated_at"):
        omitted.append("Generation timestamp")
    supplied = _sequence(data.get("omitted_evidence"))
    omitted.extend(str(item) for item in supplied)
    return list(dict.fromkeys(omitted))


def _metric(metric_id: str, label: str, value: Any) -> dict[str, Any]:
    return {"id": metric_id, "label": label, "value": value, "detail": ""}


def _is_score_payload(data: Mapping[str, Any]) -> bool:
    return isinstance(data.get("summary"), Mapping) and isinstance(data.get("outputs"), list)


def _format_from_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".html":
        return "html"
    if suffix == ".json":
        return "json"
    return "markdown"


def _disclosure(synthetic: bool) -> str:
    if synthetic:
        return "Synthetic tutorial data; not expert-authored, not human-validated, and not a benchmark."
    return "User-provided data. EvalKit does not certify validation status."


def _markdown_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(f"- {_inline(item)}" for item in value)
    if isinstance(value, Mapping):
        return "\n".join(
            f"- **{key}:** {_inline(item)}" for key, item in value.items()
        )
    return str(value)


def _inline(value: Any) -> str:
    if isinstance(value, (Mapping, list)):
        return f"`{json.dumps(value, sort_keys=True, ensure_ascii=True)}`"
    return str(value)


def _display_value(value: Any) -> str:
    if value is None:
        return "Not provided"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, float):
        if 0 <= value <= 1:
            return f"{value:.1%}"
        return f"{value:,.3f}".rstrip("0").rstrip(".")
    if isinstance(value, (Mapping, list)):
        return json.dumps(value, sort_keys=True, ensure_ascii=True)
    return str(value)


def _section_title(value: str) -> str:
    titles = {
        "agreement": "Reviewer Agreement",
        "drift": "Drift Warnings",
        "leakage": "Leakage Warnings",
    }
    return titles.get(value, value.replace("_", " ").title())


def _markdown_section_title(value: str) -> str:
    """Preserve v0.1 Markdown headings while HTML uses expanded labels."""

    if value == "agreement":
        return "Agreement"
    return _section_title(value)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sorted_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): value[key] for key in sorted(value, key=str)}


def _sequence(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _number(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def _optional_string(value: Any) -> str | None:
    return str(value) if value not in (None, "") else None


def _safe_href(value: Any) -> str | None:
    href = _optional_string(value)
    if href is None:
        return None
    return href if href.startswith(("https://", "http://", "#")) else None


def _slug(value: str) -> str:
    slug = "".join(character.lower() if character.isalnum() else "-" for character in value)
    return "-".join(part for part in slug.split("-") if part) or "record"
