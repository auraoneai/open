from auraone_evalkit.adapters.lm_eval.task import build_task_config


def test_prd_lm_eval_adapter_builds_task_config():
    config = build_task_config(
        [{"item_id": "o1", "prompt": "Review this code.", "criterion_id": "code_review.correctness"}],
        task_name="auraone_tutorial",
    )
    assert config["task"] == "auraone_tutorial"
    assert config["metadata"]["criteria"] == ["code_review.correctness"]
