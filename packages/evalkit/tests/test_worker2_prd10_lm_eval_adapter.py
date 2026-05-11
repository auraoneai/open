import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.adapters.lm_eval import build_task_config, normalize_result


def test_lm_eval_adapter_config_and_result_mapping():
    config = build_task_config([{"criterion_id": "clarity", "item_id": "task-001"}])
    result = normalize_result({"doc_id": "task-001", "acc": 0.5})

    assert config["task"] == "evalkit_tutorial"
    assert config["metadata"]["not_benchmark"] is True
    assert result["item_id"] == "task-001"
    assert result["score"] == 0.5
