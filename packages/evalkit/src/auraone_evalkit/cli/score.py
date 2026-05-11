"""Compatibility module for PRD 03.

The public console script remains `evalkit`; this module exists so the
PRD-named path `src/auraone_evalkit/cli/score.py` is importable.
"""

from auraone_evalkit.cli import main

__all__ = ["main"]

