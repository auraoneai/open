from pathlib import Path

from auraone_evalkit.leakage.checker import audit_leakage, load_items


ROOT = Path(__file__).resolve().parents[2]


def test_prd_leakage_checker_finds_seeded_overlap():
    report = audit_leakage(load_items(ROOT / "examples/leakage/tutorial_prompts.jsonl"))
    assert report["finding_count"] > 0

