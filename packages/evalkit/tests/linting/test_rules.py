from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from auraone_evalkit.linting.runner import lint_rubric


ROOT = Path(__file__).resolve().parents[2]
CLI_ENV = {"PYTHONPATH": str(ROOT / "src")}


def test_tutorial_rubric_has_no_lint_errors() -> None:
    findings = lint_rubric(ROOT / "examples/tutorial/rubric.jsonl")
    assert [finding for finding in findings if finding.severity == "error"] == []


def test_linter_reports_actionable_rule_findings(tmp_path: Path) -> None:
    bad_row = {
        "criterion_id": "demo.bad",
        "domain": "tutorial",
        "task_type": "demo",
        "criterion": "Judge whether the answer is good and beautiful using private customer data.",
        "weight": 0.8,
        "severity": "warning",
        "scoring_type": "scale_0_3",
        "examples": [{"positive": "good", "negative": "bad"}],
        "edge_cases": ["none"],
        "disagreement_risk": {"level": "medium", "notes": "subjective"},
    }
    path = tmp_path / "bad.jsonl"
    path.write_text(json.dumps(bad_row) + "\n", encoding="utf-8")

    findings = lint_rubric(path)
    rule_ids = {finding.rule_id for finding in findings}

    assert "R001_COMPOUND_CRITERIA" in rule_ids
    assert "R002_VAGUE_WORDING" in rule_ids
    assert "R008_UNSCORABLE_LANGUAGE" in rule_ids
    assert "R009_UNAVAILABLE_CONTEXT" in rule_ids
    assert "R010_UNCLEAR_SCORING_BOUNDARY" in rule_ids
    assert "R011_WEIGHT_TOTAL" in rule_ids
    assert all(finding.suggested_fix for finding in findings)


def test_linter_duplicate_rules(tmp_path: Path) -> None:
    row = {
        "criterion_id": "demo.duplicate",
        "domain": "tutorial",
        "task_type": "demo",
        "criterion": "Identify a concrete problem with evidence from the supplied output.",
        "weight": 0.5,
        "severity": "warning",
        "scoring_type": "binary",
        "examples": [{"positive": "names behavior", "negative": "generic"}],
        "edge_cases": ["Use only supplied text."],
        "disagreement_risk": {"level": "low", "notes": "visible"},
    }
    other = dict(row)
    other["severity"] = "error"
    path = tmp_path / "duplicate.jsonl"
    path.write_text(json.dumps(row) + "\n" + json.dumps(other) + "\n", encoding="utf-8")

    rule_ids = {finding.rule_id for finding in lint_rubric(path)}

    assert "R005_DUPLICATE_ID" in rule_ids
    assert "R006_DUPLICATE_TEXT" in rule_ids
    assert "R007_INCONSISTENT_SEVERITY" in rule_ids


def test_lint_cli_json_output(tmp_path: Path) -> None:
    path = tmp_path / "missing.jsonl"
    path.write_text(json.dumps({"criterion_id": "demo.missing", "criterion": "Too short"}) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "auraone_evalkit.cli",
            "lint-rubric",
            str(path),
            "--format",
            "json",
            "--fail-on",
            "none",
        ],
        check=True,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env=CLI_ENV,
    )

    payload = json.loads(result.stdout)
    assert payload["findings"]
    assert any(finding["rule_id"] == "R000_SCHEMA" for finding in payload["findings"])
