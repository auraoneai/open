"""Compatibility namespace for PRD 04 rubric linting paths.

The maintained implementation lives in :mod:`auraone_evalkit.linting`.
This package keeps the originally documented ``auraone_evalkit.lint`` import
paths working without changing the central CLI surface.
"""

from auraone_evalkit.linting.runner import LintFinding, lint_rubric

__all__ = ["LintFinding", "lint_rubric"]
