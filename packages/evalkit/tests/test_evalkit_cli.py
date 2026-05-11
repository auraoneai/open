import json
from pathlib import Path

from auraone_evalkit.cli import build_parser, main

ROOT = Path(__file__).resolve().parents[1]


def test_cli_validate_and_score(tmp_path):
    rubric = ROOT / "examples/tutorial/rubric.jsonl"
    responses = ROOT / "examples/tutorial/model_outputs.jsonl"
    labels = ROOT / "examples/tutorial/labels.jsonl"
    out = tmp_path / "score.json"
    assert main(["validate-rubric", "--rubric", str(rubric)]) == 0
    assert main(["lint-rubric", "--rubric", str(rubric)]) == 0
    assert main(["score", "--rubric", str(rubric), "--responses", str(responses), "--labels", str(labels), "--out", str(out)]) == 0
    assert out.exists()


def test_cli_report_and_card(tmp_path):
    score = tmp_path / "score.json"
    report = tmp_path / "report.md"
    card = tmp_path / "card.md"
    assert main(["score", "--rubric", str(ROOT/"examples/tutorial/rubric.jsonl"), "--responses", str(ROOT/"examples/tutorial/model_outputs.jsonl"), "--labels", str(ROOT/"examples/tutorial/labels.jsonl"), "--out", str(score)]) == 0
    assert main(["report", "--score", str(score), "--out", str(report)]) == 0
    assert main(["dataset-card", "--dataset-name", "auraone/evalkit-tutorial-v0.1", "--out", str(card)]) == 0
    assert "not expert-authored" in card.read_text()


def test_cli_card_init_defaults_to_readme(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert (
        main(
            [
                "card",
                "init",
                "--type",
                "eval",
                "--metadata",
                str(ROOT / "examples/cards/eval/meta.yaml"),
            ]
        )
        == 0
    )

    readme = tmp_path / "README.md"
    assert readme.exists()
    assert "not expert-authored" in readme.read_text()


def test_cli_help_lists_open_source_prd_commands():
    help_text = build_parser().format_help()
    for command in [
        "judge-calibrate",
        "agreement",
        "drift",
        "diff-rubric",
        "leakage-check",
        "sample",
        "weight-calibrate",
    ]:
        assert command in help_text


def test_cli_prd_repair_commands_write_outputs(tmp_path):
    cases = [
        (
            ["judge-calibrate", "examples/judge_calibration/tutorial_judge_outputs.jsonl"],
            tmp_path / "judge.json",
            "unstable_criteria",
        ),
        (
            ["agreement", "examples/agreement/tutorial_labels.jsonl"],
            tmp_path / "agreement.json",
            "per_criterion",
        ),
        (
            ["drift", "examples/drift/tutorial_batches.jsonl"],
            tmp_path / "drift.json",
            "batch_warnings",
        ),
        (
            [
                "diff-rubric",
                "examples/versioning/rubric_v1.jsonl",
                "examples/versioning/rubric_v2.jsonl",
            ],
            tmp_path / "diff.json",
            "comparability_risk",
        ),
        (
            ["leakage-check", "examples/leakage/tutorial_prompts.jsonl"],
            tmp_path / "leakage.json",
            "findings",
        ),
        (
            ["weight-calibrate", "examples/weight_calibration/rubric_weight_scenarios.json"],
            tmp_path / "weights.json",
            "ranking_instability",
        ),
    ]
    for command, out, expected_key in cases:
        assert main([*command, "--out", str(out)]) == 0
        assert expected_key in json.loads(out.read_text())

    sample_out = tmp_path / "sample.jsonl"
    assert (
        main(
            [
                "sample",
                "examples/sampling/model_outputs.jsonl",
                "--strategy",
                "uncertainty",
                "--n",
                "5",
                "--seed",
                "42",
                "--out",
                str(sample_out),
            ]
        )
        == 0
    )
    sample_rows = [json.loads(line) for line in sample_out.read_text().splitlines()]
    assert sample_rows
    assert all("item_id" in row and "rationale" in row for row in sample_rows)
