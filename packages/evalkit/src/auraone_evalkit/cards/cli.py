"""CLI registration hook for dataset card generation."""

from __future__ import annotations

import argparse

from .generator import load_metadata, write_card


def run(args: argparse.Namespace) -> int:
    out = write_card(load_metadata(args.metadata), args.out, card_type=args.type)
    print(str(out))
    return 0


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("card", help="Generate an eval or robotics dataset card.")
    parser.add_argument("init", nargs="?", default="init")
    parser.add_argument("--type", choices=["eval", "robotics"], default="eval")
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--out", default="README.md")
    parser.set_defaults(func=run)
