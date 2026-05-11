from pathlib import Path

from auraone_evalkit.reports.generator import load_report_input, write_report


ROOT = Path(__file__).resolve().parents[2]


def test_prd_report_generator_writes_markdown(tmp_path):
    out = tmp_path / "report.md"
    write_report(load_report_input(ROOT / "examples/reports/tutorial_input.json"), out)
    text = out.read_text(encoding="utf-8")
    assert "Disclosure" in text

