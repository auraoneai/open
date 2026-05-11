"""CLI registration hook for reviewer drift."""

from __future__ import annotations

import argparse
import json

from .detector import detect_drift, load_drift_records


def run(args: argparse.Namespace) -> int:
    report = detect_drift(
        load_drift_records(args.batches),
        reviewer_threshold=args.reviewer_threshold,
        criterion_threshold=args.criterion_threshold,
    )
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("drift", help="Detect reviewer or criterion drift from local JSONL batches.")
    parser.add_argument("batches")
    parser.add_argument("--reviewer-threshold", type=float, default=0.35)
    parser.add_argument("--criterion-threshold", type=float, default=0.4)
    parser.set_defaults(func=run)
