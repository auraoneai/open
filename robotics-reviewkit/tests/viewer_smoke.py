#!/usr/bin/env python3
"""Static smoke check for the canonical ReviewKit viewer and compatibility routes."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def smoke_check() -> dict[str, bool]:
    compatibility_html = (ROOT / "viewer/reviewkit.html").read_text(encoding="utf-8").lower()
    canonical_html = (ROOT / "viewer/reviewkit-v2/index.html").read_text(encoding="utf-8").lower()
    app = (ROOT / "viewer/reviewkit-v2/src/App.tsx").read_text(encoding="utf-8").lower()
    css = (ROOT / "viewer/reviewkit-v2/src/proofline.css").read_text(encoding="utf-8").lower()
    episode = (ROOT / "examples/teleop_review_mock_episode.json").read_text(encoding="utf-8").lower()

    return {
        "mock_disclosure": "synthetic tutorial metadata" in app and "not human validated" in episode,
        "viewer_shell": all(
            marker in app
            for marker in (
                "session-rail",
                "review-canvas",
                "inspector",
                "evidence timeline",
                "ordered event record",
                "source json",
            )
        ),
        "timeline_layer": all(marker in app for marker in ("failure_annotations", "interventions", "segments")),
        "canonical_redirect": "./app/index.html" in compatibility_html and "canonical proofline viewer" in compatibility_html,
        "proofline_tokens": all(marker in css for marker in ("--canvas: #f5f7fa", "--brand: #007582", "--focus: #0b6cff")),
        "accessible_controls": all(marker in app for marker in ("skip to event table", "onkeydown", "aria-live", "schema issue")),
        "evidence_exports": all(marker in app for marker in ("lerobot metadata", "rlds/openx metadata", "metadata_only")),
        "canonical_identity": "auraone robotics reviewkit" in canonical_html,
    }


def main() -> int:
    result = smoke_check()
    failed = [name for name, passed in result.items() if not passed]
    if failed:
        print(f"viewer smoke failed: {', '.join(failed)}")
        return 1
    print("viewer smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
