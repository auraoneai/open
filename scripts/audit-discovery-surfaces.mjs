#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const projectRoot = resolve(scriptDir, "..");
const discoveryPath = resolve(
  projectRoot,
  "release/discovery-surfaces.json",
);
const outputPath = resolve(
  projectRoot,
  "release/evidence/discovery-live-audit.json",
);
const strict = process.argv.includes("--strict");

const discovery = JSON.parse(await readFile(discoveryPath, "utf8"));
const githubCache = new Map();
const registryCache = new Map();

const results = [];
for (const offering of discovery.offerings) {
  const [github, registry] = await Promise.all([
    inspectGitHubRepository(offering.repository),
    inspectRegistry(offering.registry),
  ]);

  results.push({
    offering: offering.offering,
    slug: offering.slug,
    targetVersion: offering.targetVersion,
    repository: github,
    registry,
  });
}

for (const result of results) {
  if (result.registry?.status === "reachable") {
    result.registry.targetVersionMatches =
      result.registry.publicVersion === result.targetVersion;
  }
}

const summary = {
  offerings: results.length,
  githubReachable: results.filter(
    (result) => result.repository.status === "reachable",
  ).length,
  githubMissingTopics: results.filter(
    (result) =>
      result.repository.status === "reachable" &&
      result.repository.topics.length === 0,
  ).length,
  githubGenericDescriptions: results.filter(
    (result) =>
      result.repository.status === "reachable" &&
      /^AuraOne open-source /u.test(result.repository.description ?? ""),
  ).length,
  registriesDeclared: results.filter((result) => result.registry).length,
  registriesReachable: results.filter(
    (result) => result.registry?.status === "reachable",
  ).length,
  registryTargetMatches: results.filter(
    (result) => result.registry?.targetVersionMatches === true,
  ).length,
};

const report = {
  schemaVersion: "auraone.discovery-live-audit.v1",
  observedAt: new Date().toISOString(),
  source: "release/discovery-surfaces.json",
  summary,
  results,
};

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");

console.log(
  `Audited ${summary.offerings} offerings: ` +
    `${summary.githubReachable} GitHub repositories reachable, ` +
    `${summary.registriesReachable}/${summary.registriesDeclared} registries reachable, ` +
    `${summary.registryTargetMatches} registry versions match the candidate target.`,
);
console.log(`Wrote ${outputPath}`);

if (
  strict &&
  (summary.githubReachable !== summary.offerings ||
    summary.registriesReachable !== summary.registriesDeclared)
) {
  process.exitCode = 1;
}

async function inspectGitHubRepository(repositoryUrl) {
  if (githubCache.has(repositoryUrl)) {
    return githubCache.get(repositoryUrl);
  }

  const match = repositoryUrl.match(
    /^https:\/\/github\.com\/([^/]+)\/([^/#]+)$/u,
  );
  if (!match) {
    return { status: "invalid-url", url: repositoryUrl };
  }

  const [, owner, repository] = match;
  const result = await requestJson(
    `https://api.github.com/repos/${owner}/${repository}`,
    {
      Accept: "application/vnd.github+json",
      "User-Agent": "AuraOne-Discovery-Audit",
      "X-GitHub-Api-Version": "2022-11-28",
    },
  );

  const normalized =
    result.status === "reachable"
      ? {
          status: "reachable",
          url: repositoryUrl,
          defaultBranch: result.body.default_branch,
          description: result.body.description,
          homepage: result.body.homepage,
          license: result.body.license?.spdx_id ?? null,
          topics: Array.isArray(result.body.topics) ? result.body.topics : [],
          stars: result.body.stargazers_count,
          forks: result.body.forks_count,
          openIssues: result.body.open_issues_count,
          archived: result.body.archived,
          updatedAt: result.body.updated_at,
        }
      : {
          status: result.status,
          url: repositoryUrl,
          httpStatus: result.httpStatus,
          error: result.error,
        };

  githubCache.set(repositoryUrl, normalized);
  return normalized;
}

async function inspectRegistry(registryUrl) {
  if (!registryUrl) {
    return null;
  }
  if (registryCache.has(registryUrl)) {
    return registryCache.get(registryUrl);
  }

  let normalized;
  if (registryUrl.startsWith("https://pypi.org/project/")) {
    const packageName = registryUrl
      .slice("https://pypi.org/project/".length)
      .replace(/\/+$/u, "");
    const result = await requestJson(
      `https://pypi.org/pypi/${encodeURIComponent(packageName)}/json`,
    );
    normalized =
      result.status === "reachable"
        ? {
            status: "reachable",
            kind: "pypi",
            url: registryUrl,
            packageName,
            publicVersion: result.body.info?.version ?? null,
            summary: result.body.info?.summary ?? null,
            keywords: normalizeKeywords(result.body.info?.keywords),
            classifiers: result.body.info?.classifiers ?? [],
            projectUrls: result.body.info?.project_urls ?? {},
            targetVersionMatches: false,
          }
        : registryFailure("pypi", registryUrl, packageName, result);
  } else if (registryUrl.startsWith("https://www.npmjs.com/package/")) {
    const packageName = decodeURIComponent(
      registryUrl
        .slice("https://www.npmjs.com/package/".length)
        .replace(/\/+$/u, ""),
    );
    const result = await requestJson(
      `https://registry.npmjs.org/${encodeURIComponent(packageName)}`,
    );
    const latest =
      result.status === "reachable"
        ? result.body["dist-tags"]?.latest ?? null
        : null;
    const latestMetadata =
      result.status === "reachable" && latest
        ? result.body.versions?.[latest] ?? {}
        : {};
    normalized =
      result.status === "reachable"
        ? {
            status: "reachable",
            kind: "npm",
            url: registryUrl,
            packageName,
            publicVersion: latest,
            summary: latestMetadata.description ?? null,
            keywords: normalizeKeywords(latestMetadata.keywords),
            repository: latestMetadata.repository ?? null,
            homepage: latestMetadata.homepage ?? null,
            targetVersionMatches: false,
          }
        : registryFailure("npm", registryUrl, packageName, result);
  } else {
    normalized = {
      status: "unsupported-registry",
      url: registryUrl,
    };
  }

  registryCache.set(registryUrl, normalized);
  return normalized;
}

function registryFailure(kind, url, packageName, result) {
  return {
    status: result.status,
    kind,
    url,
    packageName,
    httpStatus: result.httpStatus,
    error: result.error,
    targetVersionMatches: false,
  };
}

function normalizeKeywords(value) {
  if (Array.isArray(value)) {
    return value.filter((item) => typeof item === "string" && item.trim());
  }
  if (typeof value === "string") {
    return value
      .split(/[,\s]+/u)
      .map((item) => item.trim())
      .filter(Boolean);
  }
  return [];
}

async function requestJson(url, headers = {}) {
  try {
    const response = await fetch(url, {
      headers,
      signal: AbortSignal.timeout(15_000),
    });
    if (!response.ok) {
      return {
        status: response.status === 404 ? "not-found" : "http-error",
        httpStatus: response.status,
        error: response.statusText,
      };
    }
    return { status: "reachable", body: await response.json() };
  } catch (error) {
    return {
      status: "network-error",
      error: error instanceof Error ? error.message : String(error),
    };
  }
}
