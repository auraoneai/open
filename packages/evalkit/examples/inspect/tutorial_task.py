"""Synthetic tutorial Inspect-style task mapping for EvalKit.

This file demonstrates adapter shape only. It does not require Inspect AI,
does not call hosted services, and is not a benchmark task.
"""

from auraone_evalkit.adapters.inspect import to_inspect_sample


TUTORIAL_ROW = {
    "output_id": "out-001",
    "prompt": "Review this synthetic parser change.",
    "output": "The change handles empty input and cites parser.py.",
    "metadata": {"synthetic": True, "benchmark": False},
}


def samples():
    return [to_inspect_sample(TUTORIAL_ROW)]
