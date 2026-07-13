# Evaluation Framework Adapters

EvalKit adapters help evaluation engineers map local rubric and result files
toward other evaluation frameworks without changing EvalKit's local data
boundary.

## Available Guides

- [Inspect adapter](inspect.md)
- [lm-evaluation-harness adapter](lm-eval-harness.md)

The adapter modules normalize configuration or result shapes. They do not
contact hosted AuraOne services, upload inputs, or turn synthetic tutorial
fixtures into benchmarks. Framework execution, model access, and provider
credentials remain the caller's responsibility.

Use adapters when you already have a framework runner and want to preserve
rubric IDs, criterion metadata, and result provenance around that run.

[EvalKit docs index](../README.md) |
[Package README](../../README.md)
