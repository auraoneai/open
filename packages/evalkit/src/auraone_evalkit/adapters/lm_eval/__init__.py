"""LM Eval Harness adapter shims that work without lm-eval installed."""

from .task import build_task_config, normalize_result

__all__ = ["build_task_config", "normalize_result"]
