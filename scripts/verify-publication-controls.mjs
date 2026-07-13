#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { parse } from "yaml";

const AUTHORIZATION_REPOSITORY = "auraoneai/open";
const AUTHORIZATION_TAG_VARIABLE = "vars.OSS_PUBLICATION_AUTHORIZATION_TAG";
const AUTHORIZATION_SIGNER =
  "F909806D13D9CD4CF403FA3C8C61E177EB6329E7";
const AUTHORIZATION_FLAGS = [
  "--authorization",
  "--repository",
  "--source-commit",
  "--package",
  "--version",
  "--channel",
];

const args = process.argv.slice(2);
const workflow = valueFor("--workflow");
const registry = valueFor("--registry");
const packageName = valueFor("--package");

if (!workflow || !registry || !packageName) {
  console.error(
    "Usage: verify-publication-controls.mjs --workflow path --registry npm|pypi --package name",
  );
  process.exit(2);
}
if (!["npm", "pypi"].includes(registry)) {
  throw new Error(`unsupported registry: ${registry}`);
}

const workflowPath = resolve(process.cwd(), workflow);
if (!existsSync(workflowPath)) {
  throw new Error(`publication workflow does not exist: ${workflowPath}`);
}

const document = parse(readFileSync(workflowPath, "utf8"), {
  maxAliasCount: 50,
  prettyErrors: true,
});
const failures = [];
const jobs = Object.entries(document.jobs ?? {});

if (!Object.hasOwn(document.on ?? {}, "workflow_dispatch")) {
  failures.push("workflow_dispatch trigger");
}
if (!jobs.length) {
  failures.push("jobs");
}

const sourceJobs = jobs.filter(([, job]) => {
  const checkout = (job.steps ?? []).find((step) =>
    String(step.uses ?? "").startsWith("actions/checkout@"),
  );
  const runText = jobRunText(job);
  return (
    checkout &&
    isFalse(checkout.with?.["persist-credentials"]) &&
    runText.includes("git cat-file -t") &&
    runText.includes("git verify-tag") &&
    runText.includes("VALIDSIG") &&
    runText.includes(AUTHORIZATION_SIGNER)
  );
});
if (!sourceJobs.length) {
  failures.push(
    "one source-verification job with credential-free checkout, annotated tag, and exact signer fingerprint checks",
  );
}
const sourceJobIds = new Set(sourceJobs.map(([id]) => id));

const publisherJobs = jobs.filter(([, job]) =>
  (job.steps ?? []).some((step) => isRegistryPublishStep(step)),
);
if (!publisherJobs.length) {
  failures.push(`${registry} publication step`);
}

for (const [jobId, job] of publisherJobs) {
  const steps = job.steps ?? [];
  const publishIndex = steps.findIndex((step) => isRegistryPublishStep(step));
  const downloadIndex = steps.findIndex((step) =>
    String(step.uses ?? "").startsWith("actions/download-artifact@v4"),
  );
  const attestIndex = steps.findIndex((step) =>
    String(step.uses ?? "").startsWith("actions/attest-build-provenance@v3"),
  );
  const authorizationCheckoutIndex = steps.findIndex(
    (step) => isAuthorizationCheckout(step),
  );
  const authorizationVerificationIndex = steps.findIndex(
    (step, index) =>
      index > authorizationCheckoutIndex &&
      hasAuthorizationVerification(step),
  );
  const registryStepIndex = steps.findIndex((step) => step.id === "registry");
  const registryIndex =
    registryStepIndex >= 0 &&
    hasByteMatchedRetryVerification(steps[registryStepIndex])
      ? registryStepIndex
      : -1;
  const authorizationTargets = [attestIndex, registryStepIndex, publishIndex];
  const authorizationCheckoutIsFirst = isBeforeEvery(
    authorizationCheckoutIndex,
    authorizationTargets,
  );
  const authorizationVerificationIsFirst = isBeforeEvery(
    authorizationVerificationIndex,
    authorizationTargets,
  );
  const publishCondition = String(steps[publishIndex]?.if ?? "");
  if (!job.environment) {
    failures.push(`${jobId} protected environment`);
  }
  if (effectivePermission(job, "id-token") !== "write") {
    failures.push(`${jobId} id-token: write permission`);
  }
  if (downloadIndex < 0 || downloadIndex > publishIndex) {
    failures.push(`${jobId} immutable artifact download before publication`);
  }
  if (attestIndex < 0 || attestIndex > publishIndex) {
    failures.push(`${jobId} provenance attestation before publication`);
  }
  if (!authorizationCheckoutIsFirst) {
    failures.push(
      `${jobId} separate signed publication authorization checkout before attestation, registry access, and publication`,
    );
  }
  if (!authorizationVerificationIsFirst) {
    failures.push(
      `${jobId} signed publication authorization verification with all release bindings before attestation, registry access, and publication`,
    );
  }
  if (
    registryIndex < 0 ||
    !publishCondition.includes("steps.registry.outputs.exists")
  ) {
    failures.push(
      `${jobId} semantic byte-matched idempotent registry retry control`,
    );
  }
  if (!hasAncestor(jobId, sourceJobIds)) {
    failures.push(`${jobId} dependency on verified immutable release source`);
  }
}

const releaseJobs = jobs.filter(([, job]) =>
  (job.steps ?? []).some((step) => {
    const run = String(step.run ?? "");
    return run.includes("gh release create") && run.includes("--verify-tag");
  }),
);
if (!releaseJobs.length) {
  failures.push("verified GitHub Release creation");
}
for (const [jobId] of releaseJobs) {
  if (!hasAncestor(jobId, sourceJobIds)) {
    failures.push(`${jobId} GitHub Release dependency on verified source`);
  }
  if (!hasAncestor(jobId, new Set(publisherJobs.map(([id]) => id)))) {
    const job = document.jobs[jobId];
    const steps = job.steps ?? [];
    const firstPublicWriteIndex = steps.findIndex((step) => {
      const run = operationalRunText(step);
      return (
        String(step.uses ?? "").startsWith(
          "actions/attest-build-provenance@v3",
        ) ||
        run.includes("gh release create") ||
        run.includes("gh release upload") ||
        run.includes("gh release edit") ||
        run.includes("wrangler r2 object put")
      );
    });
    const authorizationCheckoutIndex = steps.findIndex(
      (step, index) =>
        index < firstPublicWriteIndex && isAuthorizationCheckout(step),
    );
    const authorizationVerificationIndex = steps.findIndex(
      (step, index) =>
        index < firstPublicWriteIndex &&
        index > authorizationCheckoutIndex &&
        hasAuthorizationVerification(step),
    );
    if (
      firstPublicWriteIndex < 0 ||
      authorizationCheckoutIndex < 0 ||
      authorizationVerificationIndex < 0
    ) {
      failures.push(
        `${jobId} direct signed publication authorization before independent GitHub Release or distribution writes`,
      );
    }
  }
}

const verificationJobs = jobs.filter(([, job]) =>
  (job.steps ?? []).some((step) => {
    if (step.id === "registry") return false;
    const run = String(step.run ?? "");
    const registryProbe =
      registry === "npm"
        ? run.includes("npm view")
        : run.includes("pip install") &&
          run.includes("--no-cache-dir") &&
          run.includes("==");
    return registryProbe && run.includes(packageName);
  }),
);
if (!verificationJobs.length) {
  failures.push(`${registry} clean-install/live verification for ${packageName}`);
}
const publisherJobIds = new Set(publisherJobs.map(([id]) => id));
for (const [jobId] of verificationJobs) {
  if (!hasAncestor(jobId, publisherJobIds)) {
    failures.push(`${jobId} dependency on completed ${registry} publication`);
  }
}

if (failures.length) {
  throw new Error(
    `${workflow} is missing operational publication controls: ${[
      ...new Set(failures),
    ].join(", ")}`,
  );
}

console.log(
  `Publication controls verified for ${packageName} in ${workflow}.`,
);

function valueFor(flag) {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : null;
}

function isRegistryPublishStep(step) {
  if (registry === "pypi") {
    return String(step.uses ?? "").startsWith(
      "pypa/gh-action-pypi-publish@release/v1",
    );
  }
  const run = String(step.run ?? "");
  return run.includes("npm publish") && run.includes("--provenance");
}

function jobRunText(job) {
  return (job.steps ?? []).map((step) => operationalRunText(step)).join("\n");
}

function effectivePermission(job, permission) {
  const permissions = job.permissions ?? document.permissions ?? {};
  return typeof permissions === "object" ? permissions[permission] : null;
}

function hasAncestor(jobId, expectedIds) {
  const visited = new Set();
  const queue = [...needsFor(jobId)];
  while (queue.length) {
    const current = queue.shift();
    if (expectedIds.has(current)) return true;
    if (visited.has(current)) continue;
    visited.add(current);
    queue.push(...needsFor(current));
  }
  return false;
}

function needsFor(jobId) {
  const job = document.jobs?.[jobId];
  if (!job?.needs) return [];
  return Array.isArray(job.needs) ? job.needs : [job.needs];
}

function isFalse(value) {
  return value === false || value === "false";
}

function isAuthorizationCheckout(step) {
  if (String(step.uses ?? "") !== "actions/checkout@v4") return false;
  const repository = String(step.with?.repository ?? "").trim();
  const ref = String(step.with?.ref ?? "").replace(/\s/g, "");
  const path = String(step.with?.path ?? "").trim().replace(/\/+$/, "");
  return (
    repository === AUTHORIZATION_REPOSITORY &&
    ref === `\${{${AUTHORIZATION_TAG_VARIABLE}}}` &&
    path.length > 0 &&
    ![".", "${{ github.workspace }}"].includes(path)
  );
}

function hasAuthorizationVerification(step) {
  const run = operationalRunText(step);
  const tagVerification =
    /(?:^|\n)\s*(?:[A-Za-z_][A-Za-z0-9_]*="\$\()?git(?:\s+-C\s+\S+)?\s+verify-tag\b/m;
  const signerAssertion = new RegExp(
    String.raw`(?:\btest\b|\[\[|\bgrep\b)[^\n]*${AUTHORIZATION_SIGNER}`,
  );
  const verifierInvocation =
    /(?:^|\n)\s*(?:node(?:\s+--[^\s]+)*\s+\S*verify-publication-authorization\.mjs\b|(?:\.{1,2}\/|\/)\S*verify-publication-authorization\.mjs\b)/m;
  return (
    tagVerification.test(run) &&
    signerAssertion.test(run) &&
    verifierInvocation.test(run) &&
    AUTHORIZATION_FLAGS.every((flag) => run.includes(flag))
  );
}

function hasByteMatchedRetryVerification(step) {
  const run = operationalRunText(step);
  if (!run.includes("exists=false") || !run.includes("exists=true")) {
    return false;
  }
  return registry === "npm"
    ? hasNpmByteVerification(run)
    : hasPypiByteVerification(run);
}

function hasNpmByteVerification(run) {
  const remoteIndex = run.indexOf("dist.integrity");
  const localHashIndex = firstMatchIndex(run, [
    /\bcreateHash\(\s*["']sha512["']\s*\)/i,
    /\bsha512sum\b/i,
    /\bshasum\s+-a\s+512\b/i,
    /\bopenssl\b[^\n]*\bsha512\b/i,
  ]);
  const localBytesIndex = firstMatchIndex(run, [
    /\breadFileSync\s*\(/,
    /\bcreateReadStream\s*\(/,
    /\breadFile\s*\(/,
    /\bsha512sum\b[^\n]*\.(?:tgz|tar\.gz)\b/i,
    /\bshasum\b[^\n]*\.(?:tgz|tar\.gz)\b/i,
    /\bopenssl\b[^\n]*\.(?:tgz|tar\.gz)\b/i,
  ]);
  const comparisonIndex = firstMatchIndexAfter(run, localHashIndex, [
    /!==/,
    /!=/,
    /\bnotEqual\b/,
    /\btimingSafeEqual\b/,
  ]);
  const mismatchFailureIndex = firstMatchIndexAfter(run, comparisonIndex, [
    /\bthrow\s+new\s+Error\b/,
    /\bprocess\.exit\(\s*1\s*\)/,
    /(?:^|\n)\s*exit\s+1(?:\s|$)/,
  ]);
  const mismatchMessageIndex = firstMatchIndexAfter(run, comparisonIndex, [
    /\bdifferent\b/i,
    /\bmismatch\b/i,
    /\bdoes not match\b/i,
    /\bintegrity (?:check )?(?:failed|invalid)\b/i,
  ]);
  const existsIndex = run.indexOf("exists=true");

  return (
    remoteIndex >= 0 &&
    localHashIndex > remoteIndex &&
    localBytesIndex >= 0 &&
    localBytesIndex <= comparisonIndex &&
    comparisonIndex > localHashIndex &&
    mismatchFailureIndex >= comparisonIndex &&
    mismatchMessageIndex >= comparisonIndex &&
    existsIndex > mismatchFailureIndex
  );
}

function hasPypiByteVerification(run) {
  const remoteFilenameIndex = firstMatchIndex(run, [
    /\[\s*["']filename["']\s*\]/,
    /\.get\(\s*["']filename["']\s*\)/,
  ]);
  const remoteDigestIndex = firstMatchIndex(run, [
    /\[\s*["']digests["']\s*\]\s*\[\s*["']sha256["']\s*\]/,
    /\.get\(\s*["']sha256["']\s*\)/,
  ]);
  const localHashIndex = run.indexOf("hashlib.sha256");
  const localFilenameIndex = firstMatchIndex(run, [
    /\bpath\.name\b/,
    /\bos\.path\.basename\s*\(/,
  ]);
  const localDigestIndex = firstMatchIndex(run, [
    /\.hexdigest\s*\(\s*\)/,
    /\.digest\s*\(\s*\)/,
  ]);
  const comparisonIndex = firstMatchIndexAfter(run, localDigestIndex, [
    /\bif\s+[A-Za-z_][A-Za-z0-9_]*\s*!=\s*[A-Za-z_][A-Za-z0-9_]*\s*:/,
    /\bif\s+not\s+[A-Za-z_][A-Za-z0-9_]*\s*==\s*[A-Za-z_][A-Za-z0-9_]*\s*:/,
  ]);
  const mismatchFailureIndex = firstMatchIndexAfter(run, comparisonIndex, [
    /\braise\s+SystemExit\b/,
    /\braise\s+(?:RuntimeError|ValueError|AssertionError)\b/,
  ]);
  const mismatchMessageIndex = firstMatchIndexAfter(run, comparisonIndex, [
    /\bdifferent\b/i,
    /\bmismatch\b/i,
    /\bdoes not match\b/i,
    /\bdigest (?:check )?(?:failed|invalid)\b/i,
  ]);
  const existsIndex = run.indexOf("exists=true");

  return (
    remoteFilenameIndex >= 0 &&
    remoteDigestIndex > remoteFilenameIndex &&
    localHashIndex > remoteDigestIndex &&
    localFilenameIndex >= 0 &&
    localFilenameIndex <= comparisonIndex &&
    localDigestIndex > localHashIndex &&
    comparisonIndex > localDigestIndex &&
    mismatchFailureIndex >= comparisonIndex &&
    mismatchMessageIndex >= comparisonIndex &&
    existsIndex > mismatchFailureIndex
  );
}

function operationalRunText(step) {
  return String(step.run ?? "")
    .split("\n")
    .filter((line) => !/^\s*#/.test(line))
    .join("\n");
}

function firstMatchIndex(value, patterns) {
  let first = -1;
  for (const pattern of patterns) {
    const match = pattern.exec(value);
    if (match && (first < 0 || match.index < first)) {
      first = match.index;
    }
  }
  return first;
}

function firstMatchIndexAfter(value, after, patterns) {
  if (after < 0) return -1;
  const offset = after + 1;
  const index = firstMatchIndex(value.slice(offset), patterns);
  return index < 0 ? -1 : offset + index;
}

function isBeforeEvery(index, targets) {
  return index >= 0 && targets.every((target) => target >= 0 && index < target);
}
