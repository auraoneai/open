"""Test import fallback for concurrent EvalKit scaffolding work.

Worker 2 tests need to import subpackages while other workers may still be
editing the root package exports. If the root import fails, expose a namespace
package pointed at ``src/auraone_evalkit`` so submodule tests can still run.
"""

from __future__ import annotations

from pathlib import Path
import sys
import types


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

try:
    import auraone_evalkit  # noqa: F401
except Exception:
    package = types.ModuleType("auraone_evalkit")
    package.__path__ = [str(SRC / "auraone_evalkit")]
    package.__version__ = "0.1.0"
    sys.modules["auraone_evalkit"] = package
