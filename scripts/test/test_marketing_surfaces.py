from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib
import unittest
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
EVALKIT_ROOT = ROOT / "packages/evalkit"
ROBOTICS_ROOT = ROOT / "robotics-reviewkit"
VIEWER_ROOT = ROBOTICS_ROOT / "viewer/reviewkit-v2"

PRIMARY_READMES = {
    ROOT / "README.md": (
        "## Who This Is For",
        "## Why AuraOne Open",
        "## Install And Run",
        "## Runtime And Data Boundary",
        "## Proof You Can Inspect",
        "## Next Actions",
    ),
    EVALKIT_ROOT / "README.md": (
        "## Who It Is For",
        "## Why EvalKit",
        "## Install",
        "## Runtime And Data Boundary",
        "## Proof And Verification",
        "## Next Actions",
    ),
    ROBOTICS_ROOT / "README.md": (
        "## Who It Is For",
        "## Why ReviewKit",
        "## Supported Run Paths",
        "## Runtime And Data Boundary",
        "## Proof And Verification",
        "## Next Actions",
    ),
}

MARKDOWN_SURFACES = [
    *PRIMARY_READMES,
    EVALKIT_ROOT / "docs/README.md",
    *sorted((EVALKIT_ROOT / "docs").glob("*/README.md")),
    EVALKIT_ROOT / "docs/adapters/inspect.md",
    EVALKIT_ROOT / "docs/architecture/two-package-architecture.md",
    EVALKIT_ROOT / "docs/catalogs/human-data-failure-modes.md",
    EVALKIT_ROOT / "docs/checklists/criterion-quality-checklist.md",
    EVALKIT_ROOT / "docs/leakage-audit.md",
    EVALKIT_ROOT / "docs/methodology/evalkit-technical-methodology.md",
    EVALKIT_ROOT / "docs/reports.md",
    ROBOTICS_ROOT / "docs/README.md",
    ROBOTICS_ROOT / "docs/event-stream-review.md",
    ROBOTICS_ROOT / "docs/failure-viewer.md",
    ROBOTICS_ROOT / "docs/lerobot-adapter.md",
    ROBOTICS_ROOT / "docs/rlds-openx-export.md",
    ROBOTICS_ROOT / "docs/teleop-review-schema.md",
    ROBOTICS_ROOT / "docs/vla-rubric-anchors.md",
]

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class MarketingSurfaceTests(unittest.TestCase):
    def test_primary_readmes_cover_the_discovery_contract(self) -> None:
        for path, headings in PRIMARY_READMES.items():
            text = path.read_text(encoding="utf-8")
            for heading in headings:
                self.assertIn(heading, text, f"{path.relative_to(ROOT)} missing {heading}")
            normalized = text.lower()
            for term in ("local", "synthetic", "next action"):
                self.assertIn(
                    term,
                    normalized,
                    f"{path.relative_to(ROOT)} missing discovery term {term}",
                )

    def test_supported_install_and_run_paths_are_explicit(self) -> None:
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        evalkit_readme = (EVALKIT_ROOT / "README.md").read_text(encoding="utf-8")
        robotics_readme = (ROBOTICS_ROOT / "README.md").read_text(encoding="utf-8")

        for text in (root_readme, evalkit_readme):
            self.assertIn("python -m pip install --upgrade auraone-evalkit", text)
            self.assertIn('python -m pip install -e "./packages/evalkit"', text)
            self.assertIn("latest published", text.lower())

        normalized_robotics = " ".join(robotics_readme.lower().split())
        self.assertIn("npm ci --no-audit --no-fund", robotics_readme)
        self.assertIn("npm run check", robotics_readme)
        self.assertIn("not published", normalized_robotics)
        self.assertIn("not an installable reviewkit npm package", normalized_robotics)

    def test_stale_or_unsupported_discovery_commands_are_absent(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in MARKDOWN_SURFACES
        )
        for unsupported in (
            "opensource/robotics-reviewkit",
            "evalkit robotics export-",
            "evalkit calibrate-weights",
            "--count",
            "auraone.ai/open/private-evals",
            "Intended EvalKit namespace",
        ):
            self.assertNotIn(unsupported, combined)

    def test_local_markdown_links_resolve(self) -> None:
        failures: list[str] = []
        for path in MARKDOWN_SURFACES:
            self.assertTrue(path.exists(), f"missing marketing surface {path}")
            text = path.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK.findall(text):
                target = raw_target.strip().strip("<>")
                if " " in target and not target.startswith(("http://", "https://")):
                    target = target.split(" ", 1)[0]
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    failures.append(
                        f"{path.relative_to(ROOT)} -> {raw_target} "
                        f"({resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else resolved})"
                    )
        self.assertEqual([], failures, "broken local Markdown links:\n" + "\n".join(failures))

    def test_root_package_metadata_describes_a_private_coordinator(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertTrue(package["private"])
        self.assertEqual("MIT", package["license"])
        self.assertIn("documentation verification", package["description"].lower())
        self.assertEqual("https://auraone.ai/open", package["homepage"])
        self.assertEqual(
            "git+https://github.com/auraoneai/open.git",
            package["repository"]["url"],
        )
        self.assertEqual(
            "https://github.com/auraoneai/open/issues",
            package["bugs"]["url"],
        )
        self.assertIn("docs:verify", package["scripts"])
        self.assertTrue(
            {"ai-evaluation", "llm-evaluation", "robotics-review"}
            <= set(package["keywords"])
        )

    def test_evalkit_pypi_metadata_is_complete_and_specific(self) -> None:
        project = tomllib.loads(
            (EVALKIT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        )["project"]

        self.assertEqual("auraone-evalkit", project["name"])
        self.assertEqual("MIT", project["license"])
        self.assertEqual(
            {"file": "README.md", "content-type": "text/markdown"},
            project["readme"],
        )
        self.assertIn("local-first", project["description"].lower())
        self.assertIn("llm evaluation", project["description"].lower())
        self.assertTrue(
            {
                "ai-evaluation",
                "evaluation-rubrics",
                "human-evaluation",
                "offline-evaluation",
                "judge-calibration",
                "benchmark-contamination",
                "evaluation-reports",
            }
            <= set(project["keywords"])
        )
        self.assertTrue(
            {
                "Environment :: Console",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3.11",
                "Programming Language :: Python :: 3.12",
            }
            <= set(project["classifiers"])
        )

        urls = project["urls"]
        self.assertEqual("https://auraone.ai/open", urls["Homepage"])
        self.assertEqual(
            "https://github.com/auraoneai/open/tree/main/packages/evalkit/docs",
            urls["Documentation"],
        )
        self.assertEqual(
            "https://github.com/auraoneai/open/blob/main/CHANGELOG.md",
            urls["Changelog"],
        )
        self.assertEqual(
            "https://github.com/auraoneai/open/tree/main/robotics-reviewkit",
            urls["Robotics ReviewKit"],
        )
        self.assertNotIn("private-evals", json.dumps(urls))

    def test_viewer_metadata_is_private_and_matches_its_runtime(self) -> None:
        package = json.loads((VIEWER_ROOT / "package.json").read_text(encoding="utf-8"))

        self.assertTrue(package["private"])
        self.assertNotIn("publishConfig", package)
        self.assertEqual("MIT", package["license"])
        self.assertIn("private build workspace", package["description"].lower())
        self.assertEqual("^20.19.0 || >=22.12.0", package["engines"]["node"])
        self.assertEqual(
            "robotics-reviewkit/viewer/reviewkit-v2",
            package["repository"]["directory"],
        )
        self.assertTrue(
            {
                "robotics-data-quality",
                "teleoperation-review",
                "vla-evaluation",
                "lerobot",
                "rlds",
                "openx",
                "offline-viewer",
            }
            <= set(package["keywords"])
        )
        self.assertEqual("npm run test && npm run build", package["scripts"]["check"])

    def test_lockfiles_match_owned_package_identity(self) -> None:
        root_package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        root_lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
        viewer_package = json.loads((VIEWER_ROOT / "package.json").read_text(encoding="utf-8"))
        viewer_lock = json.loads((VIEWER_ROOT / "package-lock.json").read_text(encoding="utf-8"))

        for package, lock in (
            (root_package, root_lock),
            (viewer_package, viewer_lock),
        ):
            locked_root = lock["packages"][""]
            self.assertEqual(package["name"], lock["name"])
            self.assertEqual(package["version"], lock["version"])
            self.assertEqual(package["name"], locked_root["name"])
            self.assertEqual(package["version"], locked_root["version"])
            self.assertEqual(package["license"], locked_root["license"])
            self.assertEqual(package["engines"], locked_root["engines"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
