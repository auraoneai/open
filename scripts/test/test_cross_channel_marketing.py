from __future__ import annotations

import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import tomllib
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
DISCOVERY_PATH = ROOT / "release/discovery-surfaces.json"
DESTINATIONS_PATH = ROOT / "release/offering-destinations.json"
AURAONE_ROOT = (ROOT / "../../../AuraOne").resolve()

MARKETING_SURFACE_OVERRIDES = {
    "Rubric Studio Open": AURAONE_ROOT / "opensource/rubric-studio-open/README.md",
    "Agent Studio Open": AURAONE_ROOT / "opensource/agent-studio-open/README.md",
    "Robotics Studio Open": AURAONE_ROOT / "opensource/robotics-studio/README.md",
    "Robotics ReviewKit": ROOT / "robotics-reviewkit/README.md",
    "AuraOne Open catalog and developer documentation": (
        AURAONE_ROOT / "auraone-website/src/app/open/page.tsx"
    ),
    "Buying Toolkit and public writing resources": (
        AURAONE_ROOT / "auraone-website/src/app/resources/buying-toolkit/page.tsx"
    ),
}

FLAGSHIP_OFFERINGS = {
    "Rubric Studio Open",
    "Agent Studio Open",
    "Robotics Studio Open",
}

UNSUPPORTED_TRACTION = re.compile(
    r"(?:trusted by|used by)\s+(?:thousands|millions|\d[\d,]*\+?)|"
    r"\b\d[\d,.]*[kKmM]\+?\s+(?:downloads|installs|stars|users|customers|teams)\b|"
    r"\b(?:industry[- ]leading|best[- ]in[- ]class|number one|#1)\b",
    re.IGNORECASE,
)

MARKDOWN_FENCE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
MARKDOWN_REFERENCE = re.compile(r"^[ ]{0,3}\[[^\]]+\]:[ \t]*(.*)$", re.MULTILINE)
MARKDOWN_TITLE = re.compile(
    r"""(?sx)
    ^(.*?)
    [ \t\r\n]+
    (?:
        "(?:\\.|[^"])*"
        |
        '(?:\\.|[^'])*'
        |
        \((?:\\.|[^)])*\)
    )
    [ \t\r\n]*$
    """
)
MARKDOWN_ESCAPED_PUNCTUATION = re.compile(
    r"""\\([!"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~\\ ])"""
)
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_evidence(path: str) -> Path:
    return (ROOT / path).resolve()


def inferred_readme(evidence: Path) -> Path | None:
    if evidence.name.lower() == "readme.md":
        return evidence
    if evidence.is_dir():
        candidate = evidence / "README.md"
        return candidate if candidate.exists() else None
    candidate = evidence.parent / "README.md"
    return candidate if candidate.exists() else None


def normalized_keys(value: dict) -> set[str]:
    return {str(key).strip().lower() for key in value}


def without_fenced_code(text: str) -> str:
    output: list[str] = []
    fence_character = ""
    fence_length = 0

    for line in text.splitlines(keepends=True):
        match = MARKDOWN_FENCE.match(line)
        if not fence_character:
            if match:
                fence = match.group(1)
                fence_character = fence[0]
                fence_length = len(fence)
                output.append("\n" if line.endswith("\n") else "")
            else:
                output.append(line)
            continue

        if (
            match
            and match.group(1)[0] == fence_character
            and len(match.group(1)) >= fence_length
        ):
            fence_character = ""
            fence_length = 0
        output.append("\n" if line.endswith("\n") else "")

    return "".join(output)


def without_inline_code(text: str) -> str:
    output = list(text)
    index = 0

    while index < len(text):
        if text[index] != "`":
            index += 1
            continue

        run_end = index
        while run_end < len(text) and text[run_end] == "`":
            run_end += 1
        run_length = run_end - index

        cursor = run_end
        closing_start = -1
        while cursor < len(text):
            if text[cursor] != "`":
                cursor += 1
                continue
            closing_end = cursor
            while closing_end < len(text) and text[closing_end] == "`":
                closing_end += 1
            if closing_end - cursor == run_length:
                closing_start = cursor
                break
            cursor = closing_end

        if closing_start < 0:
            index = run_end
            continue

        closing_end = closing_start + run_length
        for position in range(index, closing_end):
            if output[position] not in "\r\n":
                output[position] = " "
        index = closing_end

    return "".join(output)


def markdown_destination(payload: str) -> str:
    value = payload.strip()
    if not value:
        return ""

    if value.startswith("<"):
        escaped = False
        for index, character in enumerate(value[1:], start=1):
            if character == ">" and not escaped:
                return value[1:index]
            escaped = character == "\\" and not escaped
            if character != "\\":
                escaped = False
        return ""

    title = MARKDOWN_TITLE.match(value)
    if title:
        value = title.group(1).rstrip()
    return value


def inline_markdown_payloads(text: str):
    index = 0
    while True:
        close_label = text.find("](", index)
        if close_label < 0:
            return

        backslashes = 0
        cursor = close_label - 1
        while cursor >= 0 and text[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2:
            index = close_label + 2
            continue

        cursor = close_label + 2
        depth = 0
        escaped = False
        in_angle_destination = False
        seen_destination_character = False
        while cursor < len(text):
            character = text[cursor]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif in_angle_destination:
                if character == ">":
                    in_angle_destination = False
            elif not seen_destination_character and character.isspace():
                pass
            elif not seen_destination_character and character == "<":
                seen_destination_character = True
                in_angle_destination = True
            elif character == "(":
                seen_destination_character = True
                depth += 1
            elif character == ")":
                if depth == 0:
                    yield text[close_label + 2 : cursor]
                    index = cursor + 1
                    break
                depth -= 1
            else:
                seen_destination_character = True
            cursor += 1
        else:
            return


def markdown_link_targets(text: str):
    visible_text = re.sub(
        r"<!--.*?-->",
        "",
        without_inline_code(without_fenced_code(text)),
        flags=re.DOTALL,
    )
    for payload in inline_markdown_payloads(visible_text):
        target = markdown_destination(payload)
        if target:
            yield target
    for match in MARKDOWN_REFERENCE.finditer(visible_text):
        target = markdown_destination(match.group(1))
        if target:
            yield target


def local_markdown_path(raw_target: str) -> str | None:
    target = MARKDOWN_ESCAPED_PUNCTUATION.sub(r"\1", raw_target.strip())
    if not target or target.startswith(("#", "?", "/", "\\")):
        return None
    if URI_SCHEME.match(target):
        return None

    try:
        parsed = urlsplit(target)
    except ValueError:
        return None
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return unquote(parsed.path)


def broken_local_markdown_links(path: Path) -> list[tuple[str, Path]]:
    failures: list[tuple[str, Path]] = []
    text = path.read_text(encoding="utf-8")
    for raw_target in markdown_link_targets(text):
        target = local_markdown_path(raw_target)
        if target is None:
            continue
        resolved = (path.parent / target).resolve()
        try:
            exists = resolved.exists()
        except (OSError, ValueError):
            exists = False
        if not exists:
            failures.append((raw_target, resolved))
    return failures


class CrossChannelMarketingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.discovery = load_json(DISCOVERY_PATH)["offerings"]
        cls.destinations = load_json(DESTINATIONS_PATH)["offerings"]
        cls.discovery_by_name = {
            offering["offering"]: offering for offering in cls.discovery
        }
        cls.destination_by_name = {
            offering["offering"]: offering for offering in cls.destinations
        }

    def marketing_surface(self, offering: str) -> Path:
        if offering in MARKETING_SURFACE_OVERRIDES:
            return MARKETING_SURFACE_OVERRIDES[offering]
        evidence = resolve_evidence(self.destination_by_name[offering]["evidence"])
        readme = inferred_readme(evidence)
        self.assertIsNotNone(readme, f"{offering} has no discoverable README")
        return readme

    def test_every_offering_has_one_concrete_marketing_surface(self) -> None:
        self.assertEqual(41, len(self.discovery_by_name))
        self.assertEqual(
            set(self.discovery_by_name),
            set(self.destination_by_name),
        )

        surfaces: dict[str, Path] = {}
        for offering in self.discovery_by_name:
            surface = self.marketing_surface(offering)
            self.assertTrue(surface.exists(), f"{offering} missing {surface}")
            surfaces[offering] = surface

        self.assertEqual(41, len(surfaces))

    def test_mapped_markdown_surfaces_have_valid_local_links(self) -> None:
        failures: list[str] = []
        markdown_surface_count = 0

        for offering in self.discovery_by_name:
            surface = self.marketing_surface(offering)
            if surface.suffix.lower() != ".md":
                continue
            markdown_surface_count += 1
            for raw_target, resolved in broken_local_markdown_links(surface):
                failures.append(
                    f"{offering}: {surface} -> {raw_target} ({resolved})"
                )

        self.assertEqual(39, markdown_surface_count)
        self.assertEqual(
            [],
            failures,
            "broken local links in mapped Markdown marketing surfaces:\n"
            + "\n".join(failures),
        )

    def test_markdown_link_resolution_covers_images_spaces_and_nonlocal_urls(
        self,
    ) -> None:
        with TemporaryDirectory(prefix="auraone markdown links ") as directory:
            root = Path(directory)
            docs = root / "docs with spaces"
            images = root / "screenshots with spaces"
            docs.mkdir()
            images.mkdir()
            (docs / "local guide.md").write_text("# Guide\n", encoding="utf-8")
            (images / "working image.webp").write_bytes(b"image")
            readme = root / "README.md"
            readme.write_text(
                "\n".join(
                    (
                        "[angle path](<docs with spaces/local guide.md>)",
                        "[encoded path](docs%20with%20spaces/local%20guide.md#usage)",
                        "[raw path](docs with spaces/local guide.md)",
                        "![working](<screenshots with spaces/working image.webp>)",
                        "[external](https://example.com/missing.md)",
                        "![external image](data:image/svg+xml;base64,missing)",
                        "[protocol relative](//example.com/missing.png)",
                        "[site root](/docs/missing.md)",
                        "[anchor](#local-section)",
                        "[query](?view=local)",
                        "[reference][guide]",
                        "[guide]: <docs with spaces/local guide.md> \"Guide\"",
                        "`![inline example](screenshots/missing-inline.png)`",
                        "```md",
                        "![example only](screenshots/missing-in-code.png)",
                        "```",
                    )
                )
                + "\n",
                encoding="utf-8",
            )

            self.assertEqual([], broken_local_markdown_links(readme))

            readme.write_text(
                readme.read_text(encoding="utf-8")
                + "[missing document](docs with spaces/missing guide.md)\n"
                + "![missing screenshot](screenshots with spaces/missing image.webp)\n",
                encoding="utf-8",
            )
            failures = broken_local_markdown_links(readme)
            self.assertEqual(
                {
                    "docs with spaces/missing guide.md",
                    "screenshots with spaces/missing image.webp",
                },
                {target for target, _ in failures},
            )

    def test_repository_readmes_cover_the_marketing_contract(self) -> None:
        failures: list[str] = []
        for offering in self.discovery_by_name:
            surface = self.marketing_surface(offering)
            if surface.suffix != ".md":
                continue

            text = surface.read_text(encoding="utf-8")
            normalized = " ".join(text.lower().split())
            headings = "\n".join(
                line.lower() for line in text.splitlines() if line.startswith("## ")
            )

            checks = {
                "audience/job": any(
                    phrase in normalized
                    for phrase in (
                        "built for",
                        "who it is for",
                        "who this is for",
                        "choose this package when",
                        "**for:**",
                        " is for ",
                        "## the job",
                    )
                )
                or re.search(r"\bfor\b", normalized[:1200]),
                "install/run path": re.search(
                    r"## .*(?:install|quick ?start|run from source|run locally|"
                    r"supported run paths|prerequisite|current source development|"
                    r"usage|self-hosted setup|first useful workflow)",
                    headings,
                ),
                "inspectable proof": re.search(
                    r"\b(?:proof|inspectable output|verified quickstart|"
                    r"source and release proof|what ships|visual workflow)\b",
                    normalized,
                ),
                "runtime/data boundary": (
                    "boundary" in normalized
                    and any(
                        term in normalized
                        for term in ("runtime", "data", "network", "credential")
                    )
                )
                or any(
                    phrase in normalized
                    for phrase in (
                        "credentials stay on the server",
                        "server-side credentials",
                    )
                ),
                "release truth": any(
                    phrase in normalized
                    for phrase in (
                        "release truth",
                        "release status",
                        "release proof",
                        "release and source proof",
                        "source and release proof",
                        "release and registry truth",
                        "publication status",
                        "not published",
                        "latest published",
                        "viewer source version",
                    )
                ),
                "next action": re.search(r"\bnext actions?\b", normalized),
            }

            for requirement, passed in checks.items():
                if not passed:
                    failures.append(
                        f"{offering}: {surface} missing {requirement}"
                    )

            if len(text) < 600:
                failures.append(
                    f"{offering}: {surface} is too short for a complete product surface"
                )
            if UNSUPPORTED_TRACTION.search(text):
                failures.append(
                    f"{offering}: {surface} contains an unsupported traction claim"
                )

        self.assertEqual([], failures, "\n".join(failures))

    def test_flagship_readmes_use_one_representative_screenshot(self) -> None:
        for offering in FLAGSHIP_OFFERINGS:
            surface = self.marketing_surface(offering)
            image_count = len(re.findall(r"!\[[^\]]*]\([^)]+\)", surface.read_text()))
            self.assertEqual(
                1,
                image_count,
                f"{offering} should use one best screenshot, not a gallery",
            )

    def test_pypi_metadata_is_specific_and_complete(self) -> None:
        failures: list[str] = []
        for offering, record in self.discovery_by_name.items():
            registry = record.get("registry", "")
            if "pypi.org/project/" not in registry:
                continue

            evidence = resolve_evidence(self.destination_by_name[offering]["evidence"])
            if evidence.name != "pyproject.toml":
                failures.append(f"{offering}: PyPI evidence is not pyproject.toml")
                continue

            project = tomllib.loads(evidence.read_text(encoding="utf-8"))["project"]
            description = str(project.get("description", "")).strip()
            keywords = project.get("keywords", [])
            classifiers = project.get("classifiers", [])
            urls = project.get("urls", {})
            url_keys = normalized_keys(urls)
            package_name = str(project.get("name", "")).lower()

            if len(description) < 55:
                failures.append(f"{offering}: PyPI description is not specific enough")
            if not project.get("readme"):
                failures.append(f"{offering}: PyPI readme is missing")
            if not project.get("license"):
                failures.append(f"{offering}: PyPI license is missing")
            if len(keywords) < 5:
                failures.append(f"{offering}: PyPI keywords need at least five terms")
            if "Operating System :: OS Independent" not in classifiers:
                failures.append(f"{offering}: OS-independent classifier is missing")
            if "Programming Language :: Python :: 3" not in classifiers:
                failures.append(f"{offering}: Python 3 classifier is missing")
            if not ({"homepage", "documentation"} <= url_keys):
                failures.append(f"{offering}: homepage/documentation URLs are missing")
            if not ({"repository", "source"} & url_keys):
                failures.append(f"{offering}: repository/source URL is missing")
            if "issues" not in url_keys:
                failures.append(f"{offering}: issue tracker URL is missing")
            if package_name not in registry.lower():
                failures.append(
                    f"{offering}: PyPI URL does not match package {package_name}"
                )

        self.assertEqual([], failures, "\n".join(failures))

    def test_npm_metadata_is_specific_and_complete(self) -> None:
        failures: list[str] = []
        for offering, record in self.discovery_by_name.items():
            registry = record.get("registry", "")
            if "npmjs.com/package/" not in registry:
                continue

            evidence = resolve_evidence(self.destination_by_name[offering]["evidence"])
            if evidence.name != "package.json":
                failures.append(f"{offering}: npm evidence is not package.json")
                continue

            package = load_json(evidence)
            description = str(package.get("description", "")).strip()
            package_name = str(package.get("name", "")).lower()

            if len(description) < 55:
                failures.append(f"{offering}: npm description is not specific enough")
            if len(package.get("keywords", [])) < 5:
                failures.append(f"{offering}: npm keywords need at least five terms")
            for field in ("license", "homepage", "repository", "bugs"):
                if not package.get(field):
                    failures.append(f"{offering}: npm {field} is missing")
            if package_name.replace("/", "%2f") not in registry.lower().replace(
                "%40", "@"
            ):
                plain_registry = registry.lower().replace("%40", "@").replace("%2f", "/")
                if package_name not in plain_registry:
                    failures.append(
                        f"{offering}: npm URL does not match package {package_name}"
                    )

        self.assertEqual([], failures, "\n".join(failures))


if __name__ == "__main__":
    unittest.main(verbosity=2)
