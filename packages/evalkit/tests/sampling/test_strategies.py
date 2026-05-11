from pathlib import Path

from auraone_evalkit.sampling.strategies import load_outputs, sample_outputs


ROOT = Path(__file__).resolve().parents[2]


def test_prd_sampling_strategy_is_seed_stable():
    rows = load_outputs(ROOT / "examples/sampling/model_outputs.jsonl")
    left = sample_outputs(rows, strategy="uncertainty", k=3, seed=42)
    right = sample_outputs(rows, strategy="uncertainty", k=3, seed=42)
    assert left == right

