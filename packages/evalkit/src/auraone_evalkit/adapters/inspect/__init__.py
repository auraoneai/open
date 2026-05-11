"""Inspect AI adapter shims that work without Inspect installed."""

from .scorer import inspect_score_record, to_inspect_sample

__all__ = ["inspect_score_record", "to_inspect_sample"]
