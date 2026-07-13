#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readlinkSync,
  readdirSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { normalizeSourceFile } from "./lib/source-normalization.mjs";

const coordinatorRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const execute = args.includes("--execute");
const allowDirty = args.includes("--allow-dirty");
const planFlag = args.indexOf("--release-plan");
const reportFlag = args.indexOf("--report");
const planPath = resolve(
  coordinatorRoot,
  planFlag >= 0 ? args[planFlag + 1] : "release/release-plan.json",
);
const reportPath = resolve(
  coordinatorRoot,
  reportFlag >= 0
    ? args[reportFlag + 1]
    : "release/evidence/preflight-report.json",
);

if (!existsSync(planPath)) {
  console.error(`Release plan not found: ${planPath}`);
  process.exit(2);
}

const plan = JSON.parse(readFileSync(planPath, "utf8"));
const destinationInventory = JSON.parse(
  readFileSync(resolve(coordinatorRoot, plan.destinationInventory), "utf8"),
);
const publicationDecision = JSON.parse(
  readFileSync(resolve(coordinatorRoot, plan.publicationDecision), "utf8"),
);
const publicationAuthorization = JSON.parse(
  readFileSync(resolve(coordinatorRoot, plan.publicationAuthorization), "utf8"),
);
const failures = [];
const publicationBlockers = [];
const repositories = [];
const forbiddenFontNames = /aeonik|whitney|gt[-_ ]?sectra/i;
const fontExtensions = new Set([".otf", ".ttf", ".woff", ".woff2"]);

function run(command, cwd) {
  const result = spawnSync(command, {
    cwd,
    shell: true,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 24,
  });
  return {
    command,
    status: result.status,
    stdout: result.stdout.trim(),
    stderr: result.stderr.trim(),
  };
}

function runGit(args, cwd) {
  const result = spawnSync("git", args, {
    cwd,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 24,
  });
  return {
    command: `git ${args.join(" ")}`,
    status: result.status,
    stdout: (result.stdout ?? "").trim(),
    stderr: (result.stderr ?? "").trim(),
  };
}

function checkRegistry(channel, name, version, cwd) {
  if (channel === "npm") {
    const result = run(`npm view '${name}@${version}' version --json`, cwd);
    if (result.status === 0) {
      return { channel, name, version, available: false, reason: "version already exists" };
    }
    if (/E404|not found/i.test(`${result.stdout}\n${result.stderr}`)) {
      return { channel, name, version, available: true, reason: "version is available" };
    }
    return {
      channel,
      name,
      version,
      available: false,
      reason: result.stderr || "npm registry check failed",
    };
  }
  const url = `https://pypi.org/pypi/${encodeURIComponent(name)}/${encodeURIComponent(version)}/json`;
  const result = spawnSync(
    "curl",
    [
      "--silent",
      "--show-error",
      "--output",
      "/dev/null",
      "--write-out",
      "%{http_code}",
      "--max-time",
      "20",
      url,
    ],
    {
      cwd,
      encoding: "utf8",
    },
  );
  if (result.status !== 0) {
    return {
      channel,
      name,
      version,
      available: false,
      reason: result.stderr.trim() || "PyPI registry check failed",
    };
  }
  const status = Number.parseInt(result.stdout.trim(), 10);
  if (status === 404) {
    return { channel, name, version, available: true, reason: "version is available" };
  }
  if (status === 200) {
    return { channel, name, version, available: false, reason: "version already exists" };
  }
  return {
    channel,
    name,
    version,
    available: false,
    reason: `PyPI registry returned HTTP ${status || "unknown"}`,
  };
}

function scanPublicAssets(root) {
  const findings = [];
  function walk(directory) {
    if (!existsSync(directory)) {
      return;
    }
    if (!statSync(directory).isDirectory()) {
      const entry = directory.split("/").at(-1) ?? directory;
      if (
        fontExtensions.has(extname(entry).toLowerCase()) &&
        forbiddenFontNames.test(entry)
      ) {
        findings.push(directory);
      }
      return;
    }
    for (const entry of readdirSync(directory)) {
      if (
        entry === ".git" ||
        entry === "node_modules" ||
        entry === ".venv" ||
        entry === "dist" ||
        entry === "target"
      ) {
        continue;
      }
      const path = resolve(directory, entry);
      const stat = statSync(path);
      if (stat.isDirectory()) {
        walk(path);
      } else if (
        fontExtensions.has(extname(entry).toLowerCase()) &&
        forbiddenFontNames.test(entry)
      ) {
        findings.push(path);
      }
    }
  }
  walk(root);
  return findings;
}

function fingerprintWorktree(
  root,
  statusOutput,
  sourceRoots,
  sourceNormalizers = [],
) {
  const listed = runGit(
    [
      "ls-files",
      "--modified",
      "--deleted",
      "--others",
      "--exclude-standard",
      "-z",
      "--",
      ...sourceRoots,
    ],
    root,
  );
  if (listed.status !== 0) return null;
  const hash = createHash("sha256");
  hash.update(statusOutput);
  const paths = listed.stdout.split("\0").filter(Boolean).sort();
  for (const relativePath of paths) {
    const path = resolve(root, relativePath);
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

const contractValidation = run(
  "npm run release:contracts -- --preflight",
  coordinatorRoot,
);
if (contractValidation.status !== 0) {
  failures.push("coordinated release contracts failed schema or coverage validation");
}

for (const entry of plan.repositories ?? []) {
  const root = resolve(coordinatorRoot, entry.path);
  const repository = {
    id: entry.id,
    root,
    exists: existsSync(root),
    sourceCommit: null,
    testedSourceIdentity: null,
    worktreeFingerprint: null,
    reproducible: false,
    upstreamCommit: null,
    pushed: false,
    dirty: null,
    channels: entry.channels,
    packages: entry.packages,
    releases: entry.releases,
    sourceRoots: entry.sourceRoots,
    sourceNormalizers: entry.sourceNormalizers ?? [],
    assetFindings: [],
    registryChecks: [],
    commands: [],
    publicationChecks: [],
    ready: true,
    qualityReady: false,
    publicationReady: false,
  };

  if (!repository.exists) {
    repository.ready = false;
    failures.push(`${entry.id}: repository path does not exist`);
    repositories.push(repository);
    continue;
  }

  const commit = run("git rev-parse HEAD", root);
  const upstream = run("git rev-parse '@{upstream}'", root);
  const status = runGit(
    ["status", "--porcelain", "--", ...entry.sourceRoots],
    root,
  );
  repository.sourceCommit = commit.status === 0 ? commit.stdout : null;
  repository.upstreamCommit = upstream.status === 0 ? upstream.stdout : null;
  repository.pushed = Boolean(
    repository.sourceCommit &&
      repository.upstreamCommit &&
      repository.sourceCommit === repository.upstreamCommit,
  );
  repository.dirty = status.status === 0 ? Boolean(status.stdout) : null;
  repository.worktreeFingerprint = repository.dirty
    ? fingerprintWorktree(
        root,
        status.stdout,
        entry.sourceRoots,
        entry.sourceNormalizers,
      )
    : null;
  repository.testedSourceIdentity = repository.sourceCommit
    ? repository.dirty && repository.worktreeFingerprint
      ? `${repository.sourceCommit}+worktree.${repository.worktreeFingerprint.slice(0, 16)}`
      : repository.sourceCommit
    : null;
  const sourceIdentityBeforeChecks = repository.testedSourceIdentity;
  repository.reproducible =
    repository.dirty === false && repository.pushed && Boolean(repository.sourceCommit);
  repository.assetFindings = entry.assetRoots.flatMap((assetRoot) =>
    scanPublicAssets(resolve(root, assetRoot)),
  );

  if (!repository.sourceCommit) {
    repository.ready = false;
    failures.push(`${entry.id}: source commit could not be resolved`);
  }
  if (status.status !== 0) {
    repository.ready = false;
    failures.push(`${entry.id}: release-owned worktree status could not be resolved`);
  }
  if (repository.dirty && !repository.worktreeFingerprint) {
    repository.ready = false;
    failures.push(`${entry.id}: release-owned worktree could not be fingerprinted`);
  }
  if (repository.dirty && !allowDirty) {
    repository.ready = false;
    failures.push(`${entry.id}: worktree is not clean`);
  }
  if (repository.dirty) {
    publicationBlockers.push(`${entry.id}: worktree contains uncommitted release changes`);
  }
  if (!repository.pushed) {
    publicationBlockers.push(
      `${entry.id}: checked-out source commit is not the exact upstream commit`,
    );
  }
  if (repository.assetFindings.length) {
    repository.ready = false;
    failures.push(`${entry.id}: unapproved private font assets found`);
  }

  if (execute) {
    for (const release of entry.releases) {
      const channel = release.registry ?? null;
      if (!channel) {
        continue;
      }
      const check = checkRegistry(channel, release.name, release.to, root);
      repository.registryChecks.push(check);
      if (!check.available) {
        repository.ready = false;
        failures.push(
          `${entry.id}: ${channel} ${release.name}@${release.to}: ${check.reason}`,
        );
      }
    }
  }

  for (const command of entry.commands) {
    const result = execute
      ? run(command, root)
      : { command, status: null, stdout: "", stderr: "", dryRun: true };
    repository.commands.push(result);
    if (execute && result.status !== 0) {
      repository.ready = false;
      failures.push(`${entry.id}: command failed: ${command}`);
    }
  }
  for (const command of entry.publicationChecks ?? []) {
    const result = execute
      ? run(command, root)
      : { command, status: null, stdout: "", stderr: "", dryRun: true };
    repository.publicationChecks.push(result);
    if (execute && result.status !== 0) {
      publicationBlockers.push(`${entry.id}: publication check failed: ${command}`);
    }
  }
  const statusAfterChecks = runGit(
    ["status", "--porcelain", "--", ...entry.sourceRoots],
    root,
  );
  const dirtyAfterChecks =
    statusAfterChecks.status === 0 ? Boolean(statusAfterChecks.stdout) : null;
  const fingerprintAfterChecks = dirtyAfterChecks
    ? fingerprintWorktree(
        root,
        statusAfterChecks.stdout,
        entry.sourceRoots,
        entry.sourceNormalizers,
      )
    : null;
  const sourceIdentityAfterChecks = repository.sourceCommit
    ? dirtyAfterChecks && fingerprintAfterChecks
      ? `${repository.sourceCommit}+worktree.${fingerprintAfterChecks.slice(0, 16)}`
      : repository.sourceCommit
    : null;
  if (execute && sourceIdentityAfterChecks !== sourceIdentityBeforeChecks) {
    repository.ready = false;
    failures.push(`${entry.id}: worktree changed while quality checks were running`);
  }
  if (statusAfterChecks.status !== 0) {
    repository.ready = false;
    failures.push(
      `${entry.id}: release-owned worktree status could not be resolved after checks`,
    );
  }
  if (dirtyAfterChecks && !fingerprintAfterChecks) {
    repository.ready = false;
    failures.push(
      `${entry.id}: release-owned worktree could not be fingerprinted after checks`,
    );
  }
  repository.dirty = dirtyAfterChecks;
  repository.worktreeFingerprint = fingerprintAfterChecks;
  repository.testedSourceIdentity = sourceIdentityAfterChecks;
  const qualityChecksPassed = repository.ready;
  repository.qualityReady = execute && qualityChecksPassed;
  repository.publicationReady =
    execute &&
    qualityChecksPassed &&
    repository.dirty === false &&
    repository.pushed &&
    repository.publicationChecks.every((result) => result.status === 0);
  repository.ready = repository.publicationReady;
  repositories.push(repository);
}

const destinationsComplete = publicationDecision.channels.every((entry) =>
  ["verified", "not-applicable"].includes(entry.state),
);
const evidenceComplete = publicationDecision.requiredEvidence.every((entry) =>
  ["verified", "not-applicable"].includes(entry.state),
);
const publicationDecisionReady =
  plan.status === "verified" &&
  publicationDecision.decision === "approved" &&
  publicationDecision.qualityPreflight === "passed" &&
  publicationDecision.blockers.length === 0 &&
  destinationsComplete &&
  evidenceComplete;
const publicationAuthorizationReady =
  publicationAuthorization.releasePlan === plan.name &&
  publicationAuthorization.decision === "approved" &&
  publicationAuthorization.publicationAllowed === true &&
  publicationAuthorization.releases.length > 0;
const publicationContractReady =
  publicationDecisionReady &&
  publicationDecision.publicationAllowed === true &&
  publicationAuthorizationReady;
if (plan.status !== "verified") {
  publicationBlockers.push(`release plan status is ${plan.status}, not verified`);
}
if (!publicationContractReady) {
  publicationBlockers.push(
    "coordinated destination decision, signed authorization, or required publication evidence is incomplete",
  );
}
for (const repository of repositories) {
  repository.publicationReady =
    repository.publicationReady && publicationContractReady;
  repository.ready = repository.publicationReady;
}

const planValidated = contractValidation.status === 0 && failures.length === 0;
const qualityReady = execute && planValidated;
const publicationReady =
  execute &&
  qualityReady &&
  publicationContractReady &&
  publicationBlockers.length === 0;
const invocationSucceeded = execute
  ? allowDirty
    ? qualityReady
    : publicationReady
  : planValidated;

const report = {
  schemaVersion: "1.0.0",
  releasePlan: plan.name,
  mode: execute ? "execute" : "dry-run",
  generatedAt: new Date().toISOString(),
  allowDirty,
  planValidated,
  contractValidation,
  destinationInventory: plan.destinationInventory,
  publicationAuthorization: plan.publicationAuthorization,
  offeringCount: destinationInventory.offerings.length,
  destinationCount: publicationDecision.channels.length,
  publicationAuthorizationReady,
  publicationContractReady,
  qualityReady,
  publicationReady,
  ready: publicationReady,
  requiredEvidence: plan.requiredEvidence,
  repositories,
  failures,
  publicationBlockers,
  publicationAllowed: publicationReady,
};

mkdirSync(dirname(reportPath), { recursive: true });
writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));
process.exit(invocationSucceeded ? 0 : 1);
