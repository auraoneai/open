"""CLI registration hook for rubric weight calibration."""

from __future__ import annotations

import argparse
import json

from .weights import analyze_weight_scenarios, load_weight_scenarios


def run(args: argparse.Namespace) -> int:
    print(json.dumps(analyze_weight_scenarios(load_weight_scenarios(args.scenarios)), indent=2, sort_keys=True))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("calibrate-weights", help="Analyze synthetic rubric weight sensitivity.")
    parser.add_argument("scenarios")
    parser.set_defaults(func=run)
