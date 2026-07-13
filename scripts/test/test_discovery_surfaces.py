#!/usr/bin/env python3
"""Validate the cross-channel AuraOne Open discovery contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DESTINATIONS_PATH = ROOT / "release" / "offering-destinations.json"
DISCOVERY_PATH = ROOT / "release" / "discovery-surfaces.json"

REQUIRED_TEXT_FIELDS = (
    "offering",
    "targetVersion",
    "slug",
    "category",
    "audience",
    "job",
    "differentiator",
    "proof",
    "boundary",
    "nextAction",
    "websitePath",
    "repository",
)

PROHIBITED_MARKETING_PATTERNS = (
    re.compile(r"\btrusted by\b", re.IGNORECASE),
    re.compile(r"\bused by thousands\b", re.IGNORECASE),
    re.compile(r"\bproduction[- ]ready\b", re.IGNORECASE),
    re.compile(r"\bindustry[- ]leading\b", re.IGNORECASE),
    re.compile(r"\bbest[- ]in[- ]class\b", re.IGNORECASE),
)

EXPECTED_CONVERSION_EVENTS = {
    "catalog_detail",
    "documentation",
    "download",
    "install_command",
    "registry",
    "release_evidence",
    "source",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    destinations = load_json(DESTINATIONS_PATH)
    discovery = load_json(DISCOVERY_PATH)

    destination_records = destinations["offerings"]
    discovery_records = discovery["offerings"]

    if discovery.get("schemaVersion") != "auraone.discovery-surfaces.v1":
        fail("Unexpected discovery schema version")

    if set(discovery.get("conversionEvents", [])) != EXPECTED_CONVERSION_EVENTS:
        fail("Conversion event contract is incomplete or contains unknown events")

    if len(destination_records) != 41:
        fail(f"Expected 41 destination offerings, found {len(destination_records)}")
    if len(discovery_records) != 41:
        fail(f"Expected 41 discovery offerings, found {len(discovery_records)}")

    destination_by_name = {
        record["offering"]: record for record in destination_records
    }
    discovery_by_name = {
        record["offering"]: record for record in discovery_records
    }

    if set(destination_by_name) != set(discovery_by_name):
        missing = sorted(set(destination_by_name) - set(discovery_by_name))
        extra = sorted(set(discovery_by_name) - set(destination_by_name))
        fail(f"Discovery inventory mismatch; missing={missing}, extra={extra}")

    slugs: set[str] = set()
    website_locations: set[str] = set()

    for offering, record in discovery_by_name.items():
        for field in REQUIRED_TEXT_FIELDS:
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"{offering}: required field {field!r} is empty")

        expected_version = str(destination_by_name[offering]["targetVersion"])
        if str(record["targetVersion"]) != expected_version:
            fail(
                f"{offering}: targetVersion {record['targetVersion']!r} "
                f"does not match release inventory {expected_version!r}"
            )

        slug = record["slug"]
        if slug in slugs:
            fail(f"Duplicate discovery slug: {slug}")
        slugs.add(slug)

        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            fail(f"{offering}: invalid slug {slug!r}")

        search_intent = record.get("searchIntent")
        if (
            not isinstance(search_intent, list)
            or len(search_intent) < 2
            or any(not isinstance(term, str) or not term.strip() for term in search_intent)
        ):
            fail(f"{offering}: searchIntent must contain at least two phrases")

        normalized_intent = [term.casefold() for term in search_intent]
        if len(normalized_intent) != len(set(normalized_intent)):
            fail(f"{offering}: duplicate search-intent phrase")

        install = record.get("install")
        if not isinstance(install, dict):
            fail(f"{offering}: install contract is missing")
        for field in ("kind", "command", "state"):
            value = install.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"{offering}: install.{field} is empty")

        website_path = record["websitePath"]
        if not website_path.startswith("/"):
            fail(f"{offering}: websitePath must be root-relative")
        website_locations.add(website_path)

        repository = record["repository"]
        if not re.fullmatch(r"https://github\.com/auraoneai/[A-Za-z0-9_.-]+", repository):
            fail(f"{offering}: repository is not an AuraOneAI GitHub URL")

        registry = record.get("registry")
        if registry is not None and not (
            isinstance(registry, str)
            and (
                registry.startswith("https://pypi.org/project/")
                or registry.startswith("https://www.npmjs.com/package/")
            )
        ):
            fail(f"{offering}: unsupported registry URL {registry!r}")

        combined_copy = " ".join(
            str(record[field])
            for field in (
                "audience",
                "job",
                "differentiator",
                "proof",
                "boundary",
                "nextAction",
            )
        )
        for pattern in PROHIBITED_MARKETING_PATTERNS:
            if pattern.search(combined_copy):
                fail(
                    f"{offering}: unsupported marketing pattern "
                    f"{pattern.pattern!r}"
                )

        if len(record["job"]) > 240:
            fail(f"{offering}: job copy is too long for catalog use")
        if len(record["differentiator"]) > 320:
            fail(f"{offering}: differentiator copy is too long for catalog use")
        if len(record["boundary"]) > 320:
            fail(f"{offering}: boundary copy is too long for catalog use")

    if len(website_locations) < 15:
        fail("Discovery contract does not expose enough stable website entities")

    print(
        "Validated "
        f"{len(discovery_records)} discovery offerings, "
        f"{len(website_locations)} website entities, and "
        f"{len(EXPECTED_CONVERSION_EVENTS)} conversion events."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"Discovery validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
