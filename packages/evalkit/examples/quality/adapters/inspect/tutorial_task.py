"""Synthetic tutorial Inspect-style task mapping for EvalKit.

This file is an example shim. It does not require Inspect AI to import.
"""

from auraone_evalkit.adapters.inspect import to_inspect_sample


TUTORIAL_ROW = {
    "item_id": "task-001",
    "prompt": "Summarize the provided release notes in three concise bullets.",
    "expected_output": "A concise three-bullet summary.",
    "criterion_id": "clarity",
    "synthetic": True,
}


def build_sample():
    return to_inspect_sample(TUTORIAL_ROW)
