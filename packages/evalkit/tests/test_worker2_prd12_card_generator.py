import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.cards.generator import generate_card, load_metadata


def test_card_generator_places_synthetic_status_near_top():
    metadata = load_metadata(ROOT / "examples/quality/cards/eval/meta.yaml")
    card = generate_card(metadata, card_type="eval")

    assert card.splitlines()[2].startswith("**Data status:** Synthetic tutorial data")
    assert "## Intended Use" in card
    assert "## Leakage Risk" in card


def test_robotics_card_includes_robotics_sections():
    metadata = load_metadata(ROOT / "examples/quality/cards/robotics/meta.yaml")
    card = generate_card(metadata, card_type="robotics")

    assert "## Embodiment" in card
    assert "## Sensors" in card
    assert "## Privacy" in card
