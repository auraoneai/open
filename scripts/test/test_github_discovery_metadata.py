#!/usr/bin/env python3
"""Validate staged GitHub repository descriptions, homepages, and topics."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DISCOVERY = json.loads(
    (ROOT / "release" / "discovery-surfaces.json").read_text(encoding="utf-8")
)
GITHUB = json.loads(
    (ROOT / "release" / "github-repository-metadata.json").read_text(
        encoding="utf-8"
    )
)


def main() -> None:
    source_repositories = {
        offering["repository"] for offering in DISCOVERY["offerings"]
    }
    records = GITHUB["repositories"]

    assert GITHUB["schemaVersion"] == "auraone.github-repository-discovery.v1"
    assert len(records) == len(source_repositories)
    assert {record["repository"] for record in records} == source_repositories

    for record in records:
        desired = record["desired"]
        assert 30 <= len(desired["description"]) <= 160, record["repository"]
        assert desired["homepage"].startswith("https://auraone.ai/"), record[
            "repository"
        ]
        social_preview = desired["socialPreview"]
        assert social_preview["sourceUrl"] == (
            f'{desired["homepage"]}/opengraph-image'
        ), record["repository"]
        assert 10 <= len(social_preview["alt"]) <= 125, record["repository"]
        assert social_preview["owner"] == "AuraOne Open maintainers"
        assert social_preview["reason"]
        assert social_preview["nextAction"]
        assert social_preview["applyState"] in {
            "manual-after-release-authorization",
            "blocked-repository-not-public",
        }
        assert 4 <= len(desired["topics"]) <= 20, record["repository"]
        assert len(desired["topics"]) == len(set(desired["topics"])), record[
            "repository"
        ]
        for topic in desired["topics"]:
            assert re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", topic), (
                record["repository"],
                topic,
            )
        assert record["applyState"] in {
            "ready-after-release-authorization",
            "blocked-repository-not-public",
        }

    print(f"Validated {len(records)} staged GitHub repository metadata records.")


if __name__ == "__main__":
    main()
