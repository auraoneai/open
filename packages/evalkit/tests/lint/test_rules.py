from pathlib import Path

from auraone_evalkit.linting.runner import lint_rubric


ROOT = Path(__file__).resolve().parents[2]


def test_prd_lint_rules_path_detects_compound_example():
    findings = lint_rubric(ROOT / "examples/bad_rubrics/compound.jsonl")
    assert findings
    assert any("compound" in f.rule_id.lower() or "multi" in f.rule_id.lower() for f in findings)
