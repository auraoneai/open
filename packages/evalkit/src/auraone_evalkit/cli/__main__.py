"""Allow `python -m auraone_evalkit.cli` after converting CLI to a package."""

from auraone_evalkit.cli import main


if __name__ == "__main__":
    raise SystemExit(main())

