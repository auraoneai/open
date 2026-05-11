from pathlib import Path

from auraone_evalkit.cli import main


ROOT = Path(__file__).resolve().parents[2]


def test_prd_lint_cli_path_runs_on_bad_rubric():
    assert main(["lint-rubric", str(ROOT / "examples/bad_rubrics/compound.jsonl"), "--fail-on", "none"]) == 0

