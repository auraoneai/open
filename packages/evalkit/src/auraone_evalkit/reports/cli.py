"""CLI registration hook for report generation."""

from __future__ import annotations

import argparse

from .generator import load_report_input, write_report


def run(args: argparse.Namespace) -> int:
    path = write_report(load_report_input(args.input), args.out, getattr(args, "format", None))
    print(str(path))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("report", help="Generate a local EvalKit report from JSON input.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--format", choices=["markdown", "html", "json"])
    parser.set_defaults(func=run)
