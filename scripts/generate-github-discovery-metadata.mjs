#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const projectRoot = resolve(scriptDir, "..");
const discovery = JSON.parse(
  await readFile(resolve(projectRoot, "release/discovery-surfaces.json"), "utf8"),
);
const audit = JSON.parse(
  await readFile(
    resolve(projectRoot, "release/evidence/discovery-live-audit.json"),
    "utf8",
  ),
);
const outputPath = resolve(
  projectRoot,
  "release/github-repository-metadata.json",
);
const apply = process.argv.includes("--apply");
const verify = process.argv.includes("--verify");
const confirmed =
  process.env.AURAONE_CONFIRM_GITHUB_METADATA ===
  "apply-reviewed-auraone-metadata";

const auditBySlug = new Map(
  audit.results.map((record) => [record.slug, record]),
);
const byRepository = new Map();

for (const offering of discovery.offerings) {
  const repository = offering.repository;
  const existing = byRepository.get(repository) ?? {
    repository,
    offerings: [],
  };
  existing.offerings.push(offering);
  byRepository.set(repository, existing);
}

const repositories = [...byRepository.values()]
  .map(({ repository, offerings }) => {
    const live = auditBySlug.get(offerings[0].slug)?.repository;
    const repositoryName = repository.split("/").at(-1);
    const currentTopics =
      live?.status === "reachable" && Array.isArray(live.topics)
        ? live.topics
        : [];
    const desiredTopics = buildTopics(offerings, currentTopics);
    const primary = offerings[0];
    const homepage = `https://auraone.ai${primary.websitePath.split("#")[0]}`;

    return {
      repository,
      repositoryName,
      sourceOfferings: offerings.map((offering) => offering.offering),
      currentState:
        live?.status === "reachable"
          ? {
              status: "reachable",
              description: live.description,
              homepage: live.homepage,
              topics: currentTopics,
            }
          : {
              status: live?.status ?? "not-audited",
              description: null,
              homepage: null,
              topics: [],
            },
      desired: {
        description: buildDescription(repository, offerings),
        homepage,
        topics: desiredTopics,
        socialPreview: {
          sourceUrl: `${homepage}/opengraph-image`,
          alt: `${primary.offering} by AuraOne Open`,
          applyState:
            live?.status === "reachable"
              ? "manual-after-release-authorization"
              : "blocked-repository-not-public",
          owner: "AuraOne Open maintainers",
          reason:
            live?.status === "reachable"
              ? "GitHub does not expose a supported repository social-preview upload endpoint in its public REST API."
              : "The target repository is not publicly reachable.",
          nextAction:
            live?.status === "reachable"
              ? "After exact-source release authorization, download the verified Open Graph image and upload it in the repository Social preview settings, then record the live image checksum and verification timestamp."
              : "Publish or restore the repository before assigning a GitHub social preview.",
        },
      },
      applyState:
        live?.status === "reachable"
          ? "ready-after-release-authorization"
          : "blocked-repository-not-public",
    };
  })
  .sort((left, right) => left.repository.localeCompare(right.repository));

const output = {
  schemaVersion: "auraone.github-repository-discovery.v1",
  observedAt: audit.observedAt,
  publicationPolicy:
    "Generated desired metadata only. Applying it mutates public GitHub repository settings and requires the explicit --apply flag plus AURAONE_CONFIRM_GITHUB_METADATA=apply-reviewed-auraone-metadata.",
  repositories,
};
const serialized = `${JSON.stringify(output, null, 2)}\n`;

if (verify) {
  const existing = await readFile(outputPath, "utf8");
  if (existing !== serialized) {
    throw new Error(
      "GitHub discovery metadata is stale. Run `node scripts/generate-github-discovery-metadata.mjs`.",
    );
  }
  console.log(`Verified ${repositories.length} GitHub metadata records.`);
} else {
  await writeFile(outputPath, serialized, "utf8");
  console.log(`Generated ${repositories.length} GitHub metadata records.`);
}

if (apply) {
  if (!confirmed) {
    throw new Error(
      "Refusing to mutate GitHub metadata without AURAONE_CONFIRM_GITHUB_METADATA=apply-reviewed-auraone-metadata.",
    );
  }

  for (const record of repositories) {
    if (record.applyState !== "ready-after-release-authorization") {
      console.log(`Skipped ${record.repository}: ${record.applyState}`);
      continue;
    }
    const [owner, repository] = new URL(record.repository).pathname
      .replace(/^\/+/u, "")
      .split("/");
    execFileSync(
      "gh",
      [
        "api",
        "--method",
        "PATCH",
        `repos/${owner}/${repository}`,
        "-f",
        `description=${record.desired.description}`,
        "-f",
        `homepage=${record.desired.homepage}`,
      ],
      { stdio: "inherit" },
    );
    execFileSync(
      "gh",
      [
        "api",
        "--method",
        "PUT",
        `repos/${owner}/${repository}/topics`,
        "-H",
        "Accept: application/vnd.github+json",
        "--input",
        "-",
      ],
      {
        input: JSON.stringify({ names: record.desired.topics }),
        stdio: ["pipe", "inherit", "inherit"],
      },
    );
  }
}

function buildDescription(repository, offerings) {
  if (repository === "https://github.com/auraoneai/open") {
    return "Local-first AI evaluation and robotics review tools: EvalKit, Robotics ReviewKit, release evidence, and technical buying resources.";
  }
  if (repository.endsWith("/open-studio-platform")) {
    return "Shared Proofline UI, runtime contracts, keychain, updater, and release infrastructure for AuraOne Open desktop Studios.";
  }

  const description = offerings[0].job.replace(/\.$/u, "");
  return `${description}.`.slice(0, 160);
}

function buildTopics(offerings, currentTopics) {
  const candidates = new Set([
    "auraone",
    ...currentTopics,
    ...offerings.flatMap((offering) => [
      offering.category,
      ...offering.searchIntent.flatMap((phrase) => phrase.split(/\s+/u)),
    ]),
  ]);
  const stopWords = new Set([
    "a",
    "ai",
    "and",
    "for",
    "in",
    "of",
    "open",
    "source",
    "the",
    "to",
    "tool",
  ]);

  return [...candidates]
    .map((topic) =>
      topic
        .toLowerCase()
        .replace(/[^a-z0-9]+/gu, "-")
        .replace(/^-+|-+$/gu, ""),
    )
    .filter(
      (topic) =>
        topic &&
        !stopWords.has(topic) &&
        topic.length <= 50 &&
        /^[a-z0-9][a-z0-9-]*$/u.test(topic),
    )
    .filter((topic, index, all) => all.indexOf(topic) === index)
    .slice(0, 20);
}
