"""Verify EvalKit source and distribution artifacts before publication."""

from __future__ import annotations

import argparse
from email.parser import BytesParser
from pathlib import Path
import re
import tarfile
import tomllib
import zipfile


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_FONT_EXTENSIONS = {".otf", ".ttf", ".woff", ".woff2", ".eot"}
REQUIRED_WHEEL_PATHS = {
    "auraone_evalkit/reports/templates/html.html.j2",
    "auraone_evalkit/schema/rubric.schema.json",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dist", nargs="?", type=Path, default=PACKAGE_ROOT / "dist")
    parser.add_argument("--expected-version")
    args = parser.parse_args()

    version = _source_version()
    if args.expected_version and version != args.expected_version:
        raise SystemExit(
            f"Expected release version {args.expected_version}, found {version}"
        )
    _verify_no_private_fonts()
    artifacts = sorted(path for path in args.dist.iterdir() if path.is_file())
    wheel = _one(args.dist.glob(f"auraone_evalkit-{version}-*.whl"), "wheel")
    sdist = _one(args.dist.glob(f"auraone_evalkit-{version}.tar.gz"), "source distribution")
    unexpected = [
        path.name
        for path in artifacts
        if path != wheel and path != sdist
    ]
    if unexpected:
        raise SystemExit(f"Unexpected release files: {', '.join(unexpected)}")
    _verify_wheel(wheel, version)
    _verify_sdist(sdist, version)
    print(f"Verified auraone-evalkit {version}: {wheel.name}, {sdist.name}")
    return 0


def _source_version() -> str:
    project = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project_version = str(project["project"]["version"])
    init_text = (
        PACKAGE_ROOT / "src/auraone_evalkit/__init__.py"
    ).read_text(encoding="utf-8")
    match = re.search(r'^__version__ = "([^"]+)"$', init_text, re.MULTILINE)
    if not match:
        raise SystemExit("Unable to find auraone_evalkit.__version__")
    if match.group(1) != project_version:
        raise SystemExit(
            f"Version mismatch: pyproject={project_version}, __version__={match.group(1)}"
        )
    return project_version


def _verify_no_private_fonts() -> None:
    found = sorted(
        path.relative_to(PACKAGE_ROOT).as_posix()
        for path in PACKAGE_ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in PRIVATE_FONT_EXTENSIONS
        and not any(part in {".git", ".venv", "dist", "build"} for part in path.parts)
    )
    if found:
        raise SystemExit(f"Private font assets are not allowed: {', '.join(found)}")


def _verify_wheel(path: Path, version: str) -> None:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        missing = REQUIRED_WHEEL_PATHS - names
        if missing:
            raise SystemExit(f"Wheel is missing package data: {', '.join(sorted(missing))}")
        metadata_name = _one(
            (name for name in names if name.endswith(".dist-info/METADATA")),
            "wheel METADATA",
        )
        metadata = BytesParser().parsebytes(archive.read(metadata_name.as_posix()))
        if metadata["Name"] != "auraone-evalkit":
            raise SystemExit(
                f"Wheel name mismatch: expected auraone-evalkit, found {metadata['Name']}"
            )
        if metadata["Version"] != version:
            raise SystemExit(
                f"Wheel version mismatch: expected {version}, found {metadata['Version']}"
            )
        dependencies = metadata.get_all("Requires-Dist", [])
        if not any(dependency.lower().startswith("jinja2") for dependency in dependencies):
            raise SystemExit("Wheel metadata does not declare the Jinja2 report dependency")


def _verify_sdist(path: Path, version: str) -> None:
    with tarfile.open(path, "r:gz") as archive:
        names = archive.getnames()
        for required in (
            "src/auraone_evalkit/reports/templates/html.html.j2",
            "src/auraone_evalkit/schema/rubric.schema.json",
            "CHANGELOG.md",
        ):
            if not any(name.endswith(required) for name in names):
                raise SystemExit(f"Source distribution is missing {required}")
        metadata_name = _one(
            (
                name
                for name in names
                if name.count("/") == 1 and name.endswith("/PKG-INFO")
            ),
            "source distribution PKG-INFO",
        )
        extracted = archive.extractfile(metadata_name.as_posix())
        if extracted is None:
            raise SystemExit("Unable to read source distribution PKG-INFO")
        metadata = BytesParser().parsebytes(extracted.read())
        if metadata["Name"] != "auraone-evalkit":
            raise SystemExit(
                "Source distribution name mismatch: "
                f"expected auraone-evalkit, found {metadata['Name']}"
            )
        if metadata["Version"] != version:
            raise SystemExit(
                "Source distribution version mismatch: "
                f"expected {version}, found {metadata['Version']}"
            )


def _one(values: object, label: str) -> Path:
    matches = [Path(value) for value in values]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one {label}, found {len(matches)}")
    return matches[0]


if __name__ == "__main__":
    raise SystemExit(main())
