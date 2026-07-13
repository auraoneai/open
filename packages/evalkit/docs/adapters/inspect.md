# Inspect AI Adapter

The Inspect adapter maps EvalKit tutorial records to Inspect-like sample and score dictionaries. Importing `auraone_evalkit.adapters.inspect` does not require Inspect AI.

Example:

```python
from auraone_evalkit.adapters.inspect import to_inspect_sample

sample = to_inspect_sample({
    "item_id": "task-001",
    "prompt": "Summarize the release notes.",
    "expected_output": "A concise summary.",
    "criterion_id": "clarity",
    "synthetic": True,
})
```

Install Inspect separately in the environment that runs Inspect tasks. EvalKit
does not currently declare an `inspect` optional dependency.

## Limitations

This adapter is a bridge, not a benchmark. Tutorial records are synthetic and not human-validated.
