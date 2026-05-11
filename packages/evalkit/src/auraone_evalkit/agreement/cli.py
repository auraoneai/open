"""CLI registration hook for Worker 1 integration."""

from __future__ import annotations

import argparse

from .io import dump_summary, load_annotations
from .metrics import analyze_agreement


def run(args: argparse.Namespace) -> int:
    summary = analyze_agreement(load_annotations(args.labels))
    print(dump_summary(summary.to_dict()))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "agreement",
        help="Compute local reviewer agreement metrics without an AuraOne API key.",
    )
    parser.add_argument("labels", help="Path to synthetic/tutorial JSONL annotation labels.")
    parser.set_defaults(func=run)
