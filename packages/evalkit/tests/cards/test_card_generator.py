from pathlib import Path

from auraone_evalkit.cards.generator import generate_card, load_metadata


ROOT = Path(__file__).resolve().parents[2]


def test_prd_card_generator_uses_eval_metadata():
    card = generate_card(load_metadata(ROOT / "examples/cards/eval/meta.yaml"), card_type="eval")
    assert "Data status" in card
    assert "not expert-authored" in card

