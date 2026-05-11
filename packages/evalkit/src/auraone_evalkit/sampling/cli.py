"""CLI registration hook for sampling."""

from __future__ import annotations

import argparse
import json

from .strategies import load_outputs, sample_outputs


def run(args: argparse.Namespace) -> int:
    result = sample_outputs(load_outputs(args.outputs), strategy=args.strategy, k=args.k, seed=args.seed)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("sample", help="Select model outputs for deeper local review.")
    parser.add_argument("outputs")
    parser.add_argument("--strategy", required=True)
    parser.add_argument("-k", type=int, default=5)
    parser.add_argument("--seed", type=int, default=13)
    parser.set_defaults(func=run)
