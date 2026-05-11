from auraone_evalkit.adapters.inspect.scorer import inspect_score_record, to_inspect_sample


def test_prd_inspect_adapter_maps_sample_and_score_record():
    row = {"item_id": "o1", "prompt": "Review this code.", "criterion_id": "c1", "output": "Looks ok."}
    sample = to_inspect_sample(row)
    result = inspect_score_record(row, 1.0, "tutorial score")
    assert sample["id"] == "o1"
    assert result["score"] == 1.0
