"""Command line interface for the local EvalKit package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from auraone_evalkit import __version__
from auraone_evalkit.cards.generator import render_dataset_card
from auraone_evalkit.agreement.io import load_annotations
from auraone_evalkit.agreement.metrics import analyze_agreement
from auraone_evalkit.calibration.weights import analyze_weight_scenarios, load_weight_scenarios
from auraone_evalkit.drift.detector import detect_drift, load_drift_records
from auraone_evalkit.judge.calibrate import calibrate_file
from auraone_evalkit.leakage.checker import audit_leakage, load_items
from auraone_evalkit.linting.runner import lint_rubric
from auraone_evalkit.reports.generator import render_report
from auraone_evalkit.sampling.strategies import load_outputs, sample_outputs
from auraone_evalkit.schema.validate import format_issues_text, validate_rubric_file
from auraone_evalkit.scoring.engine import ScoringError, score_from_files, write_score_output
from auraone_evalkit.versioning.diff import diff_files, render_markdown


DESCRIPTION = (
    "Local AuraOne EvalKit tools for rubric validation, scoring, judge calibration, "
    "agreement, drift, leakage, sampling, and versioning. This is not the hosted "
    "aura CLI and does not require an API key."
)

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
TUTORIAL_PATH_ALIASES = {
    "examples/judge_calibration/tutorial_judge_outputs.jsonl": "examples/quality/judge/tutorial_judge_outputs.jsonl",
    "examples/agreement/tutorial_labels.jsonl": "examples/quality/agreement/tutorial_labels.jsonl",
    "examples/drift/tutorial_batches.jsonl": "examples/quality/drift/tutorial_batches.jsonl",
    "examples/versioning/rubric_v1.jsonl": "examples/quality/versioning/rubric_v1.jsonl",
    "examples/versioning/rubric_v2.jsonl": "examples/quality/versioning/rubric_v2.jsonl",
    "examples/leakage/tutorial_prompts.jsonl": "examples/quality/leakage/tutorial_prompts.jsonl",
    "examples/sampling/model_outputs.jsonl": "examples/quality/sampling/model_outputs.jsonl",
    "examples/weight_calibration/rubric_weight_scenarios.json": "examples/quality/calibration/rubric_weight_scenarios.json",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evalkit", description=DESCRIPTION)
    parser.add_argument("--version", action="version", version=f"evalkit {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate-rubric",
        help="Validate a rubric JSONL or JSON array file.",
        description="Validate AuraOne EvalKit rubric files locally without API keys.",
    )
    validate.add_argument("path", nargs="?", type=Path, help="Rubric JSONL or JSON array path.")
    validate.add_argument("--rubric", type=Path, help="Compatibility alias for the rubric path.")
    validate.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for validation results.",
    )
    validate.set_defaults(func=_cmd_validate_rubric)

    lint = subparsers.add_parser(
        "lint-rubric",
        help="Lint rubric criteria for common authoring issues.",
        description="Run deterministic rubric lint rules locally without API keys.",
    )
    lint.add_argument("path", nargs="?", type=Path, help="Rubric JSONL or JSON array path.")
    lint.add_argument("--rubric", type=Path, help="Compatibility alias for the rubric path.")
    lint.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for lint findings.",
    )
    lint.add_argument(
        "--disable-rule",
        action="append",
        default=[],
        help="Rule ID to disable. Repeat to disable multiple rules.",
    )
    lint.add_argument(
        "--fail-on",
        choices=["info", "warning", "error", "none"],
        default="error",
        help="Minimum finding severity that returns a non-zero exit code.",
    )
    lint.set_defaults(func=_cmd_lint_rubric)

    score = subparsers.add_parser(
        "score",
        help="Score model outputs against rubric labels.",
        description="Aggregate per-criterion tutorial labels into deterministic scores.",
    )
    score.add_argument("--rubric", required=True, type=Path, help="Rubric file path.")
    score.add_argument(
        "--responses",
        required=True,
        type=Path,
        help="Model outputs JSONL or JSON array path.",
    )
    score.add_argument(
        "--labels",
        type=Path,
        help="Labels JSONL or JSON array path. Defaults to labels.jsonl next to responses.",
    )
    score.add_argument(
        "--out",
        type=Path,
        help="Output path. Defaults to stdout.",
    )
    score.add_argument(
        "--format",
        choices=["json", "jsonl", "csv", "report-json"],
        default="json",
        help="Score output format.",
    )
    score.add_argument(
        "--pass-threshold",
        type=float,
        default=0.75,
        help="Score threshold used for pass/fail and pass-rate summary.",
    )
    score.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any rubric criterion is missing a label for an output.",
    )
    score.set_defaults(func=_cmd_score)

    report = subparsers.add_parser("report", help="Generate a Markdown eval run report from score JSON.")
    report.add_argument("--score", type=Path, help="Score JSON file path.")
    report.add_argument("--input", type=Path, help="Compatibility alias for a report input JSON file.")
    report.add_argument("--out", required=True, type=Path, help="Markdown output path.")
    report.set_defaults(func=_cmd_report)

    card = subparsers.add_parser("dataset-card", help="Generate a dataset card with tutorial disclosure.")
    card.add_argument("--dataset-name", required=True)
    card.add_argument("--license", default="MIT")
    card.add_argument("--out", required=True, type=Path)
    card.set_defaults(func=_cmd_dataset_card)

    card_root = subparsers.add_parser("card", help="Dataset card compatibility commands.")
    card_subparsers = card_root.add_subparsers(dest="card_command", required=True)
    card_init = card_subparsers.add_parser("init", help="Generate a dataset card from metadata.")
    card_init.add_argument("--type", choices=["eval", "robotics"], default="eval")
    card_init.add_argument("--metadata", type=Path, help="Metadata YAML or JSON path.")
    card_init.add_argument("--dataset-name", default="auraone/evalkit-tutorial-v0.1")
    card_init.add_argument("--license", default="MIT")
    card_init.add_argument("--out", type=Path, default=Path("README.md"))
    card_init.set_defaults(func=_cmd_card_init)

    judge = subparsers.add_parser(
        "judge-calibrate",
        help="Analyze saved judge outputs locally; no model provider or AuraOne key required.",
        description="Calibrate saved synthetic/tutorial judge outputs and write deterministic JSON.",
    )
    judge.add_argument("outputs", type=Path, help="Judge output JSONL path.")
    judge.add_argument("--out", type=Path, help="JSON output path. Defaults to stdout.")
    judge.set_defaults(func=_cmd_judge_calibrate)

    agreement = subparsers.add_parser(
        "agreement",
        help="Compute local reviewer agreement metrics without an AuraOne API key.",
        description="Compute percent agreement, kappa, alpha, and per-criterion metrics from JSONL labels.",
    )
    agreement.add_argument("labels", type=Path, help="Reviewer annotation JSONL path.")
    agreement.add_argument("--out", type=Path, help="JSON output path. Defaults to stdout.")
    agreement.set_defaults(func=_cmd_agreement)

    drift = subparsers.add_parser(
        "drift",
        help="Detect reviewer or criterion drift from local JSONL batches.",
        description="Detect seeded reviewer drift and criterion instability from local batch records.",
    )
    drift.add_argument("batches", type=Path, help="Drift batch JSONL path.")
    drift.add_argument("--reviewer-threshold", type=float, default=0.35)
    drift.add_argument("--criterion-threshold", type=float, default=0.4)
    drift.add_argument("--out", type=Path, help="JSON output path. Defaults to stdout.")
    drift.set_defaults(func=_cmd_drift)

    diff = subparsers.add_parser(
        "diff-rubric",
        help="Compare two local rubric JSONL versions.",
        description="Compare rubric criteria and classify cosmetic versus scoring-impact changes.",
    )
    diff.add_argument("old", type=Path, help="Old rubric JSONL path.")
    diff.add_argument("new", type=Path, help="New rubric JSONL path.")
    diff.add_argument("--format", choices=["json", "markdown"], default="json")
    diff.add_argument("--out", type=Path, help="Output path. Defaults to stdout.")
    diff.set_defaults(func=_cmd_diff_rubric)

    leakage = subparsers.add_parser(
        "leakage-check",
        help="Audit local eval items for duplicate leakage risk.",
        description="Run offline exact and near-duplicate leakage checks against local JSONL inputs.",
    )
    leakage.add_argument("items", type=Path, help="Eval item JSONL path.")
    leakage.add_argument("--reference", type=Path, help="Optional local reference corpus JSONL path.")
    leakage.add_argument("--near-duplicate-threshold", type=float, default=0.72)
    leakage.add_argument("--out", type=Path, help="JSON output path. Defaults to stdout.")
    leakage.set_defaults(func=_cmd_leakage_check)

    sample = subparsers.add_parser(
        "sample",
        help="Select model outputs for deeper local review.",
        description="Select model outputs with deterministic strategies and write JSON or JSONL.",
    )
    sample.add_argument("outputs", type=Path, help="Model output JSONL path.")
    sample.add_argument(
        "--strategy",
        required=True,
        choices=[
            "random",
            "stratified",
            "diversity",
            "failure-heavy",
            "judge-disagreement-heavy",
            "uncertainty",
            "regression",
        ],
        help="Sampling strategy.",
    )
    sample.add_argument("--n", "-n", "-k", dest="n", type=int, default=5, help="Number of items to select.")
    sample.add_argument("--seed", type=int, default=13, help="Deterministic random seed.")
    sample.add_argument("--strata-field", default="criterion_id", help="Field used by stratified sampling.")
    sample.add_argument("--format", choices=["json", "jsonl"], help="Output format. Defaults from --out suffix or json.")
    sample.add_argument("--out", type=Path, help="Output path. .jsonl writes one selected item per line.")
    sample.set_defaults(func=_cmd_sample)

    weights = subparsers.add_parser(
        "weight-calibrate",
        help="Analyze synthetic rubric weight sensitivity.",
        description="Analyze how rubric weight scenarios affect aggregate model ranking.",
    )
    weights.add_argument("scenarios", type=Path, help="Weight scenario JSON path.")
    weights.add_argument("--out", type=Path, help="JSON output path. Defaults to stdout.")
    weights.set_defaults(func=_cmd_weight_calibrate)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


def _cmd_validate_rubric(args: argparse.Namespace) -> int:
    path = _rubric_path(args)
    issues = validate_rubric_file(path)
    if args.format == "json":
        print(json.dumps({"valid": not issues, "issues": [i.to_dict() for i in issues]}, indent=2))
    elif issues:
        print(format_issues_text(issues), file=sys.stderr)
    else:
        print(f"OK: {path}")
    return 1 if issues else 0


def _cmd_lint_rubric(args: argparse.Namespace) -> int:
    path = _rubric_path(args)
    findings = lint_rubric(path, disabled_rules=set(args.disable_rule))
    if args.format == "json":
        print(json.dumps({"ok": not _should_fail(findings, args.fail_on), "findings": [f.to_dict() for f in findings]}, indent=2))
    elif findings:
        for finding in findings:
            print(
                f"{finding.severity.upper()} {finding.rule_id} "
                f"{finding.criterion_id or '<rubric>'}: {finding.message}",
                file=sys.stderr,
            )
            print(f"  fix: {finding.suggested_fix}", file=sys.stderr)
    else:
        print(f"OK: {path}")
    return 1 if _should_fail(findings, args.fail_on) else 0


def _rubric_path(args: argparse.Namespace) -> Path:
    path = args.path or args.rubric
    if path is None:
        raise SystemExit("rubric path required")
    return path


def _cmd_score(args: argparse.Namespace) -> int:
    labels_path = args.labels or args.responses.with_name("labels.jsonl")
    try:
        result = score_from_files(
            rubric_path=args.rubric,
            responses_path=args.responses,
            labels_path=labels_path,
            pass_threshold=args.pass_threshold,
            strict=args.strict,
        )
    except ScoringError as exc:
        print(f"score failed: {exc}", file=sys.stderr)
        return 1
    write_score_output(result, args.out, args.format)
    if args.out:
        print(f"Wrote {args.format} scores to {args.out}")
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    input_path = args.score or args.input
    if input_path is None:
        print("report failed: --score or --input is required", file=sys.stderr)
        return 1
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_report(payload), encoding="utf-8")
    print(f"Wrote markdown report to {args.out}")
    return 0


def _cmd_dataset_card(args: argparse.Namespace) -> int:
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_dataset_card(args.dataset_name, args.license), encoding="utf-8")
    print(f"Wrote dataset card to {args.out}")
    return 0


def _cmd_card_init(args: argparse.Namespace) -> int:
    from auraone_evalkit.cards.generator import generate_card, load_metadata

    if args.metadata:
        try:
            metadata = load_metadata(_input_path(args.metadata))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"card init failed: {exc}", file=sys.stderr)
            return 1
        text = generate_card(metadata, card_type=args.type)
    else:
        text = render_dataset_card(args.dataset_name, args.license)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"Wrote dataset card to {args.out}")
    return 0


def _cmd_judge_calibrate(args: argparse.Namespace) -> int:
    try:
        payload = calibrate_file(_input_path(args.outputs))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"judge-calibrate failed: {exc}", file=sys.stderr)
        return 1
    _write_json(payload, args.out, "judge calibration")
    return 0


def _cmd_agreement(args: argparse.Namespace) -> int:
    try:
        payload = analyze_agreement(load_annotations(_input_path(args.labels))).to_dict()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"agreement failed: {exc}", file=sys.stderr)
        return 1
    _write_json(payload, args.out, "agreement metrics")
    return 0


def _cmd_drift(args: argparse.Namespace) -> int:
    try:
        payload = detect_drift(
            _load_drift_records_cli(_input_path(args.batches)),
            reviewer_threshold=args.reviewer_threshold,
            criterion_threshold=args.criterion_threshold,
        ).to_dict()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"drift failed: {exc}", file=sys.stderr)
        return 1
    _write_json(payload, args.out, "drift report")
    return 0


def _cmd_diff_rubric(args: argparse.Namespace) -> int:
    try:
        payload = diff_files(_input_path(args.old), _input_path(args.new))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"diff-rubric failed: {exc}", file=sys.stderr)
        return 1
    if args.format == "markdown":
        _write_text(render_markdown(payload), args.out, "rubric diff")
    else:
        _write_json(payload, args.out, "rubric diff")
    return 0


def _cmd_leakage_check(args: argparse.Namespace) -> int:
    try:
        reference = load_items(_input_path(args.reference)) if args.reference else None
        payload = audit_leakage(
            load_items(_input_path(args.items)),
            reference_items=reference,
            near_duplicate_threshold=args.near_duplicate_threshold,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"leakage-check failed: {exc}", file=sys.stderr)
        return 1
    _write_json(payload, args.out, "leakage audit")
    return 0


def _cmd_sample(args: argparse.Namespace) -> int:
    try:
        payload = sample_outputs(
            _load_outputs_cli(_input_path(args.outputs)),
            strategy=args.strategy,
            k=args.n,
            seed=args.seed,
            strata_field=args.strata_field,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"sample failed: {exc}", file=sys.stderr)
        return 1
    output_format = args.format or ("jsonl" if args.out and args.out.suffix == ".jsonl" else "json")
    if output_format == "jsonl":
        rows = [
            {
                "strategy": payload["strategy"],
                "seed": payload["seed"],
                **selected,
            }
            for selected in payload["selected"]
        ]
        _write_jsonl(rows, args.out, "sample")
    else:
        _write_json(payload, args.out, "sample")
    return 0


def _cmd_weight_calibrate(args: argparse.Namespace) -> int:
    try:
        payload = analyze_weight_scenarios(_load_weight_scenarios_cli(_input_path(args.scenarios)))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"weight-calibrate failed: {exc}", file=sys.stderr)
        return 1
    _write_json(payload, args.out, "weight calibration")
    return 0


def _should_fail(findings: Sequence[object], fail_on: str) -> bool:
    if fail_on == "none":
        return False
    severity_rank = {"info": 0, "warning": 1, "error": 2}
    minimum = severity_rank[fail_on]
    return any(severity_rank.get(getattr(f, "severity", "info"), 0) >= minimum for f in findings)


def _input_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.exists():
        return candidate
    package_relative = PACKAGE_ROOT / candidate
    if package_relative.exists():
        return package_relative
    normalized = candidate.as_posix()
    alias = TUTORIAL_PATH_ALIASES.get(normalized)
    if alias:
        alias_path = PACKAGE_ROOT / alias
        if alias_path.exists():
            return alias_path
    return candidate


def _write_json(payload: Mapping[str, Any] | list[Any], out: Path | None, label: str) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    _write_text(text, out, label)


def _write_jsonl(rows: Sequence[Mapping[str, Any]], out: Path | None, label: str) -> None:
    text = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    _write_text(text, out, label)


def _write_text(text: str, out: Path | None, label: str) -> None:
    if out is None:
        print(text, end="")
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {label} to {out}")


def _load_drift_records_cli(path: Path) -> list[Any]:
    try:
        return load_drift_records(path)
    except ValueError as exc:
        if "missing drift field(s): item_id" not in str(exc):
            raise
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        row.setdefault("item_id", row.get("id", f"row-{line_no}"))
        rows.append(row)
    return _load_drift_records_from_rows(rows)


def _load_outputs_cli(path: Path) -> list[dict[str, Any]]:
    try:
        return load_outputs(path)
    except ValueError as exc:
        if "missing item_id" not in str(exc):
            raise
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if "item_id" not in row and "output_id" in row:
            row["item_id"] = row["output_id"]
        if "judge_disagreement" not in row and "disagreement" in row:
            row["judge_disagreement"] = row["disagreement"]
        if "failure_score" not in row and "failure" in row:
            row["failure_score"] = 1.0 if row["failure"] else 0.0
        if "criterion_id" not in row and "stratum" in row:
            row["criterion_id"] = row["stratum"]
        rows.append(row)
    return rows


def _load_weight_scenarios_cli(path: Path) -> dict[str, Any]:
    data = load_weight_scenarios(path)
    if data.get("criteria") and data.get("models"):
        return data
    items = data.get("items")
    scenarios = data.get("scenarios")
    if not isinstance(items, list) or not isinstance(scenarios, list):
        return data
    criterion_ids = sorted(
        {
            criterion_id
            for item in items
            for criterion_id in (item.get("criterion_scores") or {}).keys()
        }
    )
    return {
        **data,
        "criteria": [{"criterion_id": criterion_id} for criterion_id in criterion_ids],
        "models": [
            {
                "model_id": str(item.get("model_id", item.get("item_id", f"item-{index}"))),
                "scores": item.get("criterion_scores", {}),
            }
            for index, item in enumerate(items, start=1)
        ],
    }


def _load_drift_records_from_rows(rows: Sequence[Mapping[str, Any]]) -> list[Any]:
    from auraone_evalkit.drift.models import DriftRecord

    return [DriftRecord.from_mapping(row, line_no=index) for index, row in enumerate(rows, start=1)]


if __name__ == "__main__":
    raise SystemExit(main())
