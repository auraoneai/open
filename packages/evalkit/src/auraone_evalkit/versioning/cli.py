"""CLI registration hook for rubric diffs."""

from __future__ import annotations

import argparse
import json

from .diff import diff_files, render_markdown


def run(args: argparse.Namespace) -> int:
    result = diff_files(args.old, args.new)
    print(json.dumps(result, indent=2, sort_keys=True) if args.format == "json" else render_markdown(result))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("diff-rubric", help="Compare two local rubric JSONL versions.")
    parser.add_argument("old")
    parser.add_argument("new")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.set_defaults(func=run)
