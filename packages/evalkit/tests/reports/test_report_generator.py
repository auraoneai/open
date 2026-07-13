from pathlib import Path

import json

from auraone_evalkit.reports.generator import (
    REPORT_SCHEMA_VERSION,
    generate_html_report,
    generate_json_report,
    load_report_input,
    write_report,
)


ROOT = Path(__file__).resolve().parents[2]


def test_prd_report_generator_writes_markdown(tmp_path):
    out = tmp_path / "report.md"
    write_report(load_report_input(ROOT / "examples/reports/tutorial_input.json"), out)
    text = out.read_text(encoding="utf-8")
    assert "Disclosure" in text


def test_report_contract_is_deterministic_and_complete():
    data = load_report_input(ROOT / "examples/reports/tutorial_input.json")
    first = generate_json_report(data)
    second = generate_json_report(json.loads(json.dumps(data)))

    assert first == second
    assert first["schema_version"] == REPORT_SCHEMA_VERSION
    assert first["summary"]["headline"]
    assert first["gates"][0]["status"] == "passed"
    assert first["findings"][0]["evidence_refs"] == ["agreement-output"]
    assert first["evidence"][0]["kind"] == "metric"
    assert first["reproduce"]["command"].startswith("evalkit report")
    assert len(first["metadata"]["input_sha256"]) == 64


def test_html_report_is_self_contained_accessible_and_escaped():
    data = load_report_input(ROOT / "examples/reports/tutorial_input.json")
    data["title"] = '<script>alert("x")</script>'
    data["unstable_criteria"] = ["criterion-" + "long-name-" * 30]
    html = generate_html_report(data)

    assert html.startswith("<!doctype html>")
    assert '<meta name="viewport"' in html
    assert 'href="#report-content"' in html
    assert 'aria-label="Report sections"' in html
    assert "@media print" in html
    assert "@media (prefers-reduced-motion: reduce)" in html
    assert "<script" not in html
    assert "&lt;script&gt;" in html
    assert "https://fonts" not in html
    assert "http://fonts" not in html


def test_score_payload_derives_gates_findings_and_evidence():
    report = generate_json_report(
        {
            "schema_version": "auraone.evalkit.score.v0.1",
            "pass_threshold": 0.75,
            "summary": {
                "average_score": 0.7,
                "pass_rate": 0.5,
                "scored_outputs": 2,
                "criterion_count": 3,
                "missing_label_count": 1,
            },
            "outputs": [
                {
                    "output_id": "answer-1",
                    "score": 0.7,
                    "passed": False,
                    "missing_criteria": ["grounding"],
                }
            ],
        }
    )

    assert report["decision"]["status"] == "fail"
    assert {gate["id"] for gate in report["gates"]} == {
        "average-score",
        "label-coverage",
        "output-pass-rate",
    }
    assert any(item["severity"] == "warning" for item in report["findings"])
    assert report["evidence"][0]["id"] == "output-answer-1"


def test_write_report_honors_explicit_format(tmp_path):
    data = load_report_input(ROOT / "examples/reports/tutorial_input.json")
    output = tmp_path / "report.artifact"
    write_report(data, output, "json")

    assert json.loads(output.read_text(encoding="utf-8"))["schema_version"] == REPORT_SCHEMA_VERSION
