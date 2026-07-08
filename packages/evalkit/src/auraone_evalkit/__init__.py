"""AuraOne EvalKit local open-source evaluation tools."""

from auraone_evalkit.linting.runner import LintFinding, lint_rubric
from auraone_evalkit.schema.models import RubricCriterion, ValidationIssue
from auraone_evalkit.schema.validate import load_rubric, validate_rubric_file
from auraone_evalkit.scoring.engine import ScoreResult, score_eval, score_outputs

__version__ = "0.2.1"

__all__ = [
    "__version__",
    "LintFinding",
    "RubricCriterion",
    "ScoreResult",
    "ValidationIssue",
    "lint_rubric",
    "load_rubric",
    "score_eval",
    "score_outputs",
    "validate_rubric_file",
]
