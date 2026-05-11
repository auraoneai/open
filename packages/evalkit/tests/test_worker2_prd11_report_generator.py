import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auraone_evalkit.reports.generator import generate_html_report, generate_markdown_report, load_report_input


def test_report_generator_includes_sections_and_disclosure():
    data = load_report_input(ROOT / "examples/quality/reports/tutorial_input.json")
    markdown = generate_markdown_report(data)
    html = generate_html_report(data)

    assert "# EvalKit Synthetic Tutorial Report" in markdown
    assert "Synthetic tutorial data" in markdown
    assert "## Agreement" in markdown
    assert "<h1>EvalKit Synthetic Tutorial Report</h1>" in html
