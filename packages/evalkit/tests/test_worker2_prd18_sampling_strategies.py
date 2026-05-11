import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.sampling.strategies import load_outputs, sample_outputs


def test_sampling_fixed_seed_and_priority_strategies_are_deterministic():
    rows = load_outputs(ROOT / "examples/quality/sampling/model_outputs.jsonl")

    first = sample_outputs(rows, strategy="random", k=3, seed=7)
    second = sample_outputs(rows, strategy="random", k=3, seed=7)
    uncertain = sample_outputs(rows, strategy="uncertainty", k=2)
    disagreement = sample_outputs(rows, strategy="judge-disagreement-heavy", k=1)

    assert first == second
    assert uncertain["selected"][0]["item_id"] == "out-005"
    assert disagreement["selected"][0]["item_id"] == "out-005"
