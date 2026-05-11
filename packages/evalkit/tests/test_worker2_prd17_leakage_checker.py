import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.leakage.checker import audit_leakage, load_items


def test_leakage_checker_detects_seeded_duplicates():
    items = load_items(ROOT / "examples/quality/leakage/tutorial_prompts.jsonl")
    result = audit_leakage(items)

    assert result["finding_count"] >= 1
    assert any(finding["risk"] == "exact_duplicate" for finding in result["findings"])
    assert any({"prompt-001", "prompt-002"}.issubset(set(cluster)) for cluster in result["clusters"])
