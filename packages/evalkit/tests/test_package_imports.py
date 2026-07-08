from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import auraone_evalkit

ROOT = Path(__file__).resolve().parents[1]


def test_package_metadata_and_public_api() -> None:
    assert auraone_evalkit.__version__ == "0.2.1"
    assert hasattr(auraone_evalkit, "load_rubric")
    assert hasattr(auraone_evalkit, "score_outputs")
    assert hasattr(auraone_evalkit, "lint_rubric")


def test_cli_help_and_version() -> None:
    help_result = subprocess.run(
        [sys.executable, "-m", "auraone_evalkit.cli", "--help"],
        check=True,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
    )
    assert "validate-rubric" in help_result.stdout
    assert "lint-rubric" in help_result.stdout
    assert "score" in help_result.stdout
    assert "does not require an API key" in help_result.stdout

    version_result = subprocess.run(
        [sys.executable, "-m", "auraone_evalkit.cli", "--version"],
        check=True,
        text=True,
        capture_output=True,
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
    )
    assert version_result.stdout.strip() == "evalkit 0.2.1"
