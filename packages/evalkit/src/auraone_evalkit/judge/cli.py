"""CLI registration hook for judge calibration."""

from __future__ import annotations

import argparse
import json

from .calibrate import calibrate_file


def run(args: argparse.Namespace) -> int:
    print(json.dumps(calibrate_file(args.outputs), indent=2, sort_keys=True))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "judge-calibrate",
        help="Analyze saved judge outputs locally; no model provider or AuraOne key required.",
    )
    parser.add_argument("outputs", help="Path to synthetic/tutorial judge output JSONL.")
    parser.set_defaults(func=run)
