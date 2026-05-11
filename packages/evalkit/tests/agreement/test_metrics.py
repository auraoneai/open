from pathlib import Path

from auraone_evalkit.agreement.io import load_annotations
from auraone_evalkit.agreement.metrics import analyze_agreement


ROOT = Path(__file__).resolve().parents[2]


def test_prd_agreement_metrics_fixture_has_per_criterion_output():
    summary = analyze_agreement(load_annotations(ROOT / "examples/agreement/tutorial_labels.jsonl"))
    assert summary.per_criterion
    assert summary.annotation_count > 0

