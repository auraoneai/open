"""CLI registration hook for leakage audit."""

from __future__ import annotations

import argparse
import json

from .checker import audit_leakage, load_items


def run(args: argparse.Namespace) -> int:
    reference = load_items(args.reference) if args.reference else None
    print(json.dumps(audit_leakage(load_items(args.items), reference_items=reference), indent=2, sort_keys=True))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("leakage-check", help="Audit local eval items for duplicate leakage risk.")
    parser.add_argument("items")
    parser.add_argument("--reference")
    parser.set_defaults(func=run)
