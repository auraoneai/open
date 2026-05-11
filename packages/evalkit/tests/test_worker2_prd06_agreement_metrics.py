import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.agreement.io import load_annotations
from auraone_evalkit.agreement.metrics import (
    InsufficientAgreementData,
    analyze_agreement,
    krippendorffs_alpha,
)


def test_agreement_summary_matches_platform_shared_cases():
    annotations = load_annotations(ROOT / "examples/quality/agreement/tutorial_labels.jsonl")
    summary = analyze_agreement(annotations)

    assert summary.item_count == 4
    assert summary.reviewer_count == 2
    assert summary.percent_agreement == 0.5
    assert 0 < summary.cohen_kappa < 1
    assert summary.per_reviewer["r1"]["total_annotations"] == 4


def test_krippendorff_alpha_perfect_and_sparse_errors():
    perfect = [
        {"reviewer_id": "a", "item_id": "1", "value": 1},
        {"reviewer_id": "b", "item_id": "1", "value": 1},
        {"reviewer_id": "a", "item_id": "2", "value": 2},
        {"reviewer_id": "b", "item_id": "2", "value": 2},
    ]
    assert krippendorffs_alpha(perfect) == 1.0

    sparse = [
        {"reviewer_id": "a", "item_id": "1", "value": 1},
        {"reviewer_id": "b", "item_id": "2", "value": 1},
    ]
    with pytest.raises(InsufficientAgreementData):
        krippendorffs_alpha(sparse)
