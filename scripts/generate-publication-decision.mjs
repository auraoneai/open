#!/usr/bin/env node
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import {
  existsSync,
  lstatSync,
  readFileSync,
  readlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { normalizeSourceFile } from "./lib/source-normalization.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const plan = readJson("release/release-plan.json");
const inventory = readJson(plan.destinationInventory);
const report = readJson("release/evidence/preflight-execute.json");
const qualityEvidence = "release/evidence/preflight-execute.json";
const qualityClaims = new Map(
  plan.qualityEvidenceClaims.map((claim) => [claim.name, claim.commands]),
);
const commandResults = new Map(
  report.repositories.flatMap((repository) =>
    repository.commands.map((result) => [result.command, result]),
  ),
);

assertCurrentQualityReport();
assertQualityClaims();

const channels = inventory.offerings.flatMap((offering) =>
  offering.destinations.map((destination) => {
    const state =
      destination.state ??
      (offering.releaseScope === "unchanged" ? "not-applicable" : "blocked");
    if (state === "not-applicable") {
      const evidence = offering.evidence;
      return {
        offering: offering.offering,
        destinationId: destination.id,
        destination: destination.label,
        targetVersion: offering.targetVersion,
        state,
        owner: offering.owner,
        reason:
          offering.releaseScope === "unchanged"
            ? `This offering has no source, version, UI, or public-contract change in the Proofline UI/UX release train; ${destination.label} remains on its existing independent release.`
            : `${destination.label} is not an independently supported destination for this release train.`,
        nextAction:
          offering.releaseScope === "unchanged"
            ? "Retain the current release and create a separate coordinated record when this offering changes."
            : "Keep this destination source-coupled and document a support-policy change before any independent publication.",
        evidence,
        evidenceKind: "not-applicable",
        evidenceSha256: sha256File(evidence),
        verifiedAt: report.generatedAt,
      };
    }
    return {
      offering: offering.offering,
      destinationId: destination.id,
      destination: destination.label,
      targetVersion: offering.targetVersion,
      state: "blocked",
      owner: offering.owner,
      reason: `Local quality passed, but ${destination.label} has not been published and independently verified from clean, exact pushed release source.`,
      nextAction: `Push the reviewed release commit, execute the protected ${destination.label} workflow or submission, and attach immutable live verification evidence.`,
      evidence: qualityEvidence,
      evidenceKind: "blocker",
      evidenceSha256: null,
      verifiedAt: null,
    };
  }),
);

const requiredEvidence = plan.requiredEvidence.map((name) => {
  const claimChecks = qualityClaims.get(name) ?? [];
  const state = claimChecks.length ? "verified" : "blocked";
  return {
    name,
    state,
    owner:
      state === "verified"
        ? "AuraOne Open maintainers"
        : name.includes("signature") || name.includes("SBOM")
          ? "AuraOne release security owner"
          : "AuraOne release owner",
    reason:
      state === "verified"
        ? `${name} is covered by the local quality report or checked release documentation.`
        : `${name} is not yet available as immutable, independently verified publication evidence.`,
    nextAction:
      state === "verified"
        ? "Preserve this evidence with the reviewed release commit."
        : `Produce and independently verify ${name} from the exact pushed release source before approving publication.`,
    evidence:
      state === "verified"
        ? qualityEvidence
        : "release/evidence/publication-decision.json",
    evidenceKind: state === "verified" ? "quality" : "blocker",
    evidenceSha256: state === "verified" ? sha256File(qualityEvidence) : null,
    verifiedAt: state === "verified" ? report.generatedAt : null,
    claimChecks,
  };
});

const decision = {
  $schema: "../publication-decision.schema.json",
  schemaVersion: "1.0.0",
  releasePlan: plan.name,
  destinationInventory: plan.destinationInventory,
  releaseOwner: plan.releaseOwner,
  rollbackOwner: plan.rollbackOwner,
  decidedAt: report.generatedAt,
  decision: "blocked",
  publicationAllowed: false,
  qualityPreflight: report.qualityReady ? "passed" : "failed",
  qualityEvidence,
  blockers: [...new Set([
    ...report.publicationBlockers,
    "Locally verified signed and notarized macOS artifacts exist, but exact-pushed-commit macOS rebuild evidence and required Windows and Linux artifacts do not yet exist for every target.",
    "Local macOS checksums exist; cross-platform checksums, SBOMs, updater evidence, package-manager evidence, and live deployment verification remain incomplete.",
    "No protected registry, GitHub Release, marketplace, GitHub App, or production deployment job has been authorized.",
  ])],
  requiredEvidence,
  channels,
};

writeFileSync(
  resolve(root, plan.publicationDecision),
  `${JSON.stringify(decision, null, 2)}\n`,
);
console.log(
  `Generated ${channels.length} destination decisions for ${inventory.offerings.length} offerings.`,
);

function readJson(path) {
  return JSON.parse(readFileSync(resolve(root, path), "utf8"));
}

function sha256File(path) {
  return createHash("sha256")
    .update(readFileSync(resolve(root, path)))
    .digest("hex");
}

function assertCurrentQualityReport() {
  if (
    report.mode !== "execute" ||
    report.qualityReady !== true ||
    report.failures.length !== 0
  ) {
    throw new Error(
      "publication decisions require a successful execute-mode quality report",
    );
  }

  const reportRepositories = new Map(
    report.repositories.map((repository) => [repository.id, repository]),
  );
  for (const repository of plan.repositories) {
    const recorded = reportRepositories.get(repository.id);
    if (!recorded) {
      throw new Error(`quality report is missing repository ${repository.id}`);
    }
    if (
      JSON.stringify(recorded.sourceRoots) !==
      JSON.stringify(repository.sourceRoots)
    ) {
      throw new Error(
        `quality report has a stale source boundary for ${repository.id}`,
      );
    }
    if (
      JSON.stringify(recorded.sourceNormalizers ?? []) !==
      JSON.stringify(repository.sourceNormalizers ?? [])
    ) {
      throw new Error(
        `quality report has stale source normalization for ${repository.id}`,
      );
    }
    const repositoryRoot = resolve(root, repository.path);
    const current = currentSourceIdentity(
      repositoryRoot,
      repository.sourceRoots,
      repository.sourceNormalizers,
    );
    if (
      recorded.sourceCommit !== current.sourceCommit ||
      recorded.worktreeFingerprint !== current.worktreeFingerprint ||
      recorded.testedSourceIdentity !== current.testedSourceIdentity
    ) {
      throw new Error(
        `quality report is stale for ${repository.id}; rerun the execute preflight`,
      );
    }
  }
}

function assertQualityClaims() {
  for (const [name, commands] of qualityClaims) {
    if (!plan.requiredEvidence.includes(name)) {
      throw new Error(`quality claim is not required publication evidence: ${name}`);
    }
    for (const command of commands) {
      const result = commandResults.get(command);
      if (!result) {
        throw new Error(`quality claim ${name} references an unreported command: ${command}`);
      }
      if (result.status !== 0) {
        throw new Error(`quality claim ${name} did not pass: ${command}`);
      }
    }
  }
}

function currentSourceIdentity(
  repositoryRoot,
  sourceRoots,
  sourceNormalizers = [],
) {
  const sourceCommit = git(repositoryRoot, ["rev-parse", "HEAD"]).trim();
  const status = git(repositoryRoot, [
    "status",
    "--porcelain",
    "--",
    ...sourceRoots,
  ]);
  const dirty = Boolean(status.trim());
  const worktreeFingerprint = dirty
    ? fingerprintWorktree(
        repositoryRoot,
        status.trim(),
        sourceRoots,
        sourceNormalizers,
      )
    : null;
  return {
    sourceCommit,
    worktreeFingerprint,
    testedSourceIdentity:
      dirty && worktreeFingerprint
        ? `${sourceCommit}+worktree.${worktreeFingerprint.slice(0, 16)}`
        : sourceCommit,
  };
}

function fingerprintWorktree(
  repositoryRoot,
  statusOutput,
  sourceRoots,
  sourceNormalizers = [],
) {
  const listed = git(repositoryRoot, [
    "ls-files",
    "--modified",
    "--deleted",
    "--others",
    "--exclude-standard",
    "-z",
    "--",
    ...sourceRoots,
  ]);
  const hash = createHash("sha256");
  hash.update(statusOutput);
  for (const relativePath of listed.split("\0").filter(Boolean).sort()) {
    const path = resolve(repositoryRoot, relativePath);
    hash.update("\0");
    hash.update(relativePath);
    if (!existsSync(path)) {
      hash.update("\0deleted");
      continue;
    }
    const stat = lstatSync(path);
    if (stat.isSymbolicLink()) {
      hash.update("\0symlink\0");
      hash.update(readlinkSync(path));
    } else if (stat.isFile()) {
      hash.update("\0file\0");
      hash.update(
        normalizeSourceFile(relativePath, readFileSync(path), sourceNormalizers),
      );
    }
  }
  return hash.digest("hex");
}

function git(repositoryRoot, args) {
  const result = spawnSync("git", args, {
    cwd: repositoryRoot,
    encoding: "utf8",
  });
  if (result.status !== 0) {
    throw new Error(
      `git ${args.join(" ")} failed in ${repositoryRoot}: ${result.stderr.trim()}`,
    );
  }
  return result.stdout;
}
