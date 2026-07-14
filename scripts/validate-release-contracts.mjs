#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { isAbsolute, relative, resolve, sep } from "node:path";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const root = process.cwd();
const auraoneRoot = process.env.AURAONE_ROOT
  ? resolve(process.env.AURAONE_ROOT)
  : resolve(root, "../../../AuraOne");
const preflight = process.argv.includes("--preflight");
const releaseRoot = resolve(root, "release");
const plan = readJson("release/release-plan.json");
const inventory = readJson(plan.destinationInventory);
const publicationDecision = readJson(plan.publicationDecision);
const publicationAuthorization = readJson(plan.publicationAuthorization);
const planSchema = readJson("release/release-plan.schema.json");
const inventorySchema = readJson("release/offering-destinations.schema.json");
const publicationSchema = readJson("release/publication-decision.schema.json");
const authorizationSchema = readJson(
  "release/publication-authorization.schema.json",
);
const channelEvidenceSchema = readJson(
  "release/publication-channel-evidence.schema.json",
);
const requirementEvidenceSchema = readJson(
  "release/publication-requirement-evidence.schema.json",
);
readJson("release/release-evidence.schema.json");

const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);
const errors = [];

validateSchema("release plan", planSchema, plan);
validateSchema("offering inventory", inventorySchema, inventory);
validateSchema("publication decision", publicationSchema, publicationDecision);
validateSchema(
  "publication authorization",
  authorizationSchema,
  publicationAuthorization,
);

const repositoryIds = new Set();
const plannedRepositories = new Map();
const planCommandCounts = new Map();
const repositorySourceBoundaries = [];
for (const repository of plan.repositories ?? []) {
  if (repositoryIds.has(repository.id)) {
    errors.push(`duplicate repository id ${repository.id}`);
  }
  repositoryIds.add(repository.id);
  plannedRepositories.set(repository.id, repository);
  const repositoryRoot = resolveConfigPath(repository.path);
  repositorySourceBoundaries.push({
    id: repository.id,
    root: repositoryRoot,
    sourceRoots: repository.sourceRoots ?? [],
  });
  for (const sourceRoot of repository.sourceRoots ?? []) {
    const resolvedSourceRoot = resolve(repositoryRoot, sourceRoot);
    const relativeSourceRoot = relative(repositoryRoot, resolvedSourceRoot);
    if (
      isAbsolute(sourceRoot) ||
      relativeSourceRoot === ".." ||
      relativeSourceRoot.startsWith(`..${sep}`) ||
      isAbsolute(relativeSourceRoot)
    ) {
      errors.push(`${repository.id} source root escapes its repository: ${sourceRoot}`);
      continue;
    }
    if (!existsSync(resolvedSourceRoot)) {
      errors.push(`${repository.id} source root does not exist: ${sourceRoot}`);
    }
  }
  const normalizedPaths = new Set();
  for (const normalizer of repository.sourceNormalizers ?? []) {
    if (normalizedPaths.has(normalizer.path)) {
      errors.push(
        `${repository.id} has duplicate source normalizer ${normalizer.path}`,
      );
      continue;
    }
    normalizedPaths.add(normalizer.path);
    const normalizedPath = resolve(repositoryRoot, normalizer.path);
    const relativeNormalizedPath = relative(repositoryRoot, normalizedPath);
    if (
      isAbsolute(normalizer.path) ||
      relativeNormalizedPath === ".." ||
      relativeNormalizedPath.startsWith(`..${sep}`) ||
      isAbsolute(relativeNormalizedPath)
    ) {
      errors.push(
        `${repository.id} source normalizer escapes its repository: ${normalizer.path}`,
      );
      continue;
    }
    if (!existsSync(normalizedPath)) {
      errors.push(
        `${repository.id} source normalizer path does not exist: ${normalizer.path}`,
      );
    }
    if (
      !(repository.sourceRoots ?? []).some((sourceRoot) =>
        pathContains(resolve(repositoryRoot, sourceRoot), normalizedPath),
      )
    ) {
      errors.push(
        `${repository.id} source normalizer is outside sourceRoots: ${normalizer.path}`,
      );
    }
  }
  for (const release of repository.releases ?? []) {
    if (!/^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$/.test(release.to ?? "")) {
      errors.push(`${repository.id} has invalid target version ${release.to}`);
    }
  }
  for (const command of repository.commands ?? []) {
    planCommandCounts.set(command, (planCommandCounts.get(command) ?? 0) + 1);
  }
}

if (publicationAuthorization.releasePlan !== plan.name) {
  errors.push("publication authorization references the wrong release plan");
}
if (
  publicationAuthorization.publicationAllowed !==
  (publicationAuthorization.decision === "approved")
) {
  errors.push(
    "publication authorization is allowed if and only if its decision is approved",
  );
}
if (
  publicationAuthorization.publicationAllowed &&
  !publicationDecision.publicationAllowed
) {
  errors.push(
    "publication authorization cannot override a blocked publication decision",
  );
}
for (const authorization of publicationAuthorization.releases ?? []) {
  const repository = plannedRepositories.get(authorization.repository);
  if (!repository) {
    errors.push(
      `publication authorization references unknown repository ${authorization.repository}`,
    );
    continue;
  }
  const release = repository.releases.find(
    (candidate) =>
      candidate.name === authorization.package &&
      candidate.to === authorization.version,
  );
  if (!release) {
    errors.push(
      `publication authorization references unplanned release ${authorization.repository} ${authorization.package}@${authorization.version}`,
    );
  }
  for (const channel of authorization.channels ?? []) {
    if (!repository.channels.includes(channel)) {
      errors.push(
        `publication authorization references unsupported channel ${authorization.repository} ${channel}`,
      );
    }
  }
}

const qualityClaims = new Map();
for (const claim of plan.qualityEvidenceClaims ?? []) {
  if (qualityClaims.has(claim.name)) {
    errors.push(`duplicate quality evidence claim ${claim.name}`);
    continue;
  }
  qualityClaims.set(claim.name, claim);
  if (!plan.requiredEvidence.includes(claim.name)) {
    errors.push(`quality evidence claim is not required: ${claim.name}`);
  }
  for (const command of claim.commands) {
    if (!planCommandCounts.has(command)) {
      errors.push(`${claim.name} quality claim references an unknown command: ${command}`);
    }
  }
}

let qualityReport = null;
if (!existsSync(resolveConfigPath(publicationDecision.qualityEvidence))) {
  errors.push("publication decision quality evidence does not exist");
} else {
  qualityReport = readJson(publicationDecision.qualityEvidence);
  if (!preflight && publicationDecision.decidedAt !== qualityReport.generatedAt) {
    errors.push("publication decision timestamp must match its quality report");
  }
  if (
    !preflight &&
    publicationDecision.qualityPreflight === "passed" &&
    (qualityReport.mode !== "execute" ||
      qualityReport.qualityReady !== true ||
      qualityReport.failures.length !== 0)
  ) {
    errors.push(
      "passed quality evidence must be a successful execute-mode preflight report",
    );
  }
  if (!preflight && publicationAuthorization.publicationAllowed) {
    const reports = new Map(
      qualityReport.repositories.map((repository) => [
        repository.id,
        repository,
      ]),
    );
    for (const authorization of publicationAuthorization.releases ?? []) {
      const repository = reports.get(authorization.repository);
      if (
        !repository ||
        repository.sourceCommit !== authorization.sourceCommit ||
        repository.dirty !== false ||
        repository.pushed !== true
      ) {
        errors.push(
          `publication authorization is not bound to clean pushed quality evidence for ${authorization.repository}`,
        );
      }
    }
  }
}

const inventoryOfferings = new Map();
const expectedDestinations = new Map();
for (const offering of inventory.offerings ?? []) {
  if (inventoryOfferings.has(offering.offering)) {
    errors.push(`duplicate inventory offering ${offering.offering}`);
    continue;
  }
  inventoryOfferings.set(offering.offering, offering);
  if (!existsSync(resolveConfigPath(offering.evidence))) {
    errors.push(`${offering.offering} evidence path does not exist: ${offering.evidence}`);
  }
  if (offering.releaseScope === "changed") {
    validateChangedOfferingSourceBoundary(offering);
  }
  const ids = new Set();
  for (const destination of offering.destinations) {
    if (ids.has(destination.id)) {
      errors.push(`${offering.offering} has duplicate destination ${destination.id}`);
    }
    ids.add(destination.id);
    expectedDestinations.set(pairKey(offering.offering, destination.id), {
      offering,
      destination,
    });
  }
}

const actualDestinations = new Map();
for (const channel of publicationDecision.channels ?? []) {
  const key = pairKey(channel.offering, channel.destinationId);
  if (actualDestinations.has(key)) {
    errors.push(`duplicate publication destination ${key}`);
    continue;
  }
  actualDestinations.set(key, channel);
  const expected = expectedDestinations.get(key);
  if (!expected) {
    errors.push(`unexpected publication destination ${key}`);
    continue;
  }
  if (channel.destination !== expected.destination.label) {
    errors.push(`${key} destination label does not match the inventory`);
  }
  if (channel.targetVersion !== expected.offering.targetVersion) {
    errors.push(`${key} target version does not match the inventory`);
  }
  if (channel.owner !== expected.offering.owner) {
    errors.push(`${key} owner does not match the inventory`);
  }
  validateEvidenceReference(channel, `publication destination ${key}`, {
    verifiedKind: "live",
  });
  if (
    channel.state === "not-applicable" &&
    expected.offering.releaseScope !== "unchanged" &&
    expected.destination.state !== "not-applicable"
  ) {
    errors.push(`${key} is not explicitly justified as not applicable`);
  }
  if (channel.state === "verified") {
    validateLiveChannelEvidence(channel, key);
  }
}
for (const key of expectedDestinations.keys()) {
  if (!actualDestinations.has(key)) {
    errors.push(`publication decision is missing ${key}`);
  }
}

const requiredEvidence = new Map();
for (const entry of publicationDecision.requiredEvidence ?? []) {
  if (requiredEvidence.has(entry.name)) {
    errors.push(`duplicate required evidence record ${entry.name}`);
  }
  requiredEvidence.set(entry.name, entry);
  validateEvidenceReference(entry, `required evidence ${entry.name}`, {
    verifiedKind: null,
  });
  validateRequiredEvidenceBinding(entry);
}
for (const name of plan.requiredEvidence ?? []) {
  if (!requiredEvidence.has(name)) {
    errors.push(`publication decision is missing required evidence: ${name}`);
  }
}
for (const name of requiredEvidence.keys()) {
  if (!plan.requiredEvidence.includes(name)) {
    errors.push(`publication decision has unexpected required evidence: ${name}`);
  }
}

if (publicationDecision.destinationInventory !== plan.destinationInventory) {
  errors.push("publication decision references the wrong destination inventory");
}
if (publicationDecision.releasePlan !== plan.name) {
  errors.push("publication decision references the wrong release plan");
}
const destinationsComplete = [...actualDestinations.values()].every((entry) =>
  ["verified", "not-applicable"].includes(entry.state),
);
const evidenceComplete = [...requiredEvidence.values()].every((entry) =>
  ["verified", "not-applicable"].includes(entry.state),
);
const approvalConsistent =
  plan.status === "verified" &&
  publicationDecision.decision === "approved" &&
  publicationDecision.qualityPreflight === "passed" &&
  publicationDecision.blockers.length === 0 &&
  destinationsComplete &&
  evidenceComplete;

if (publicationDecision.publicationAllowed !== approvalConsistent) {
  errors.push(
    "publicationAllowed must equal the verified plan, approved decision, destination, and evidence state",
  );
}
if (publicationDecision.decision === "blocked") {
  if (!publicationDecision.blockers.length) {
    errors.push("blocked publication decision must record release blockers");
  }
  if (publicationDecision.publicationAllowed) {
    errors.push("blocked publication decision cannot allow publication");
  }
}
if (
  publicationDecision.decision !== "approved" &&
  publicationDecision.publicationAllowed
) {
  errors.push("only an approved publication decision can allow publication");
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
console.log(
  `Release contracts valid: ${plan.repositories.length} repositories, ` +
    `${plan.repositories.flatMap((entry) => entry.releases).length} releases, ` +
    `${inventory.offerings.length} offerings, ` +
    `${expectedDestinations.size} destinations, and ` +
    `${plan.requiredEvidence.length} evidence requirements.`,
);

function readJson(path) {
  return JSON.parse(readFileSync(resolve(root, path), "utf8"));
}

function resolveConfigPath(path) {
  const auraonePrefix = "../../../AuraOne";
  if (path === auraonePrefix) {
    return auraoneRoot;
  }
  if (path.startsWith(`${auraonePrefix}/`)) {
    return resolve(auraoneRoot, path.slice(auraonePrefix.length + 1));
  }
  return resolve(root, path);
}

function validateSchema(label, schema, document) {
  const validate = ajv.compile(schema);
  if (validate(document)) return;
  for (const error of validate.errors ?? []) {
    errors.push(`${label}${error.instancePath || "/"} ${error.message}`);
  }
}

function pairKey(offering, destinationId) {
  return `${offering}::${destinationId}`;
}

function validateChangedOfferingSourceBoundary(offering) {
  const evidencePath = resolveConfigPath(offering.evidence);
  const repository = repositorySourceBoundaries
    .filter((candidate) => pathContains(candidate.root, evidencePath))
    .sort((left, right) => right.root.length - left.root.length)[0];
  if (!repository) {
    errors.push(
      `${offering.offering} changed evidence is outside every repository source boundary`,
    );
    return;
  }
  const covered = repository.sourceRoots.some((sourceRoot) =>
    pathContains(resolve(repository.root, sourceRoot), evidencePath),
  );
  if (!covered) {
    errors.push(
      `${offering.offering} changed evidence is not covered by ${repository.id} sourceRoots: ${offering.evidence}`,
    );
  }
}

function pathContains(parent, candidate) {
  const relativePath = relative(parent, candidate);
  return (
    relativePath === "" ||
    (relativePath !== ".." &&
      !relativePath.startsWith(`..${sep}`) &&
      !isAbsolute(relativePath))
  );
}

function validateEvidenceReference(entry, label, { verifiedKind }) {
  const evidencePath = resolveConfigPath(entry.evidence);
  if (!existsSync(evidencePath)) {
    errors.push(`${label} evidence does not exist: ${entry.evidence}`);
    return;
  }

  const complete = ["verified", "not-applicable", "rolled-back"].includes(
    entry.state,
  );
  if (!complete) {
    if (entry.evidenceKind !== "blocker") {
      errors.push(`${label} blocked evidence must use evidenceKind=blocker`);
    }
    if (entry.evidenceSha256 !== null || entry.verifiedAt !== null) {
      errors.push(`${label} blocked evidence cannot claim a digest or verification time`);
    }
    return;
  }

  if (!entry.evidenceSha256 || !entry.verifiedAt) {
    errors.push(`${label} complete evidence requires a digest and verification time`);
    return;
  }
  if (!preflight) {
    const actualHash = createHash("sha256")
      .update(readFileSync(evidencePath))
      .digest("hex");
    if (actualHash !== entry.evidenceSha256) {
      errors.push(`${label} evidence digest does not match ${entry.evidence}`);
    }
  }
  if (entry.state === "verified" && verifiedKind && entry.evidenceKind !== verifiedKind) {
    errors.push(`${label} verified evidence must use evidenceKind=${verifiedKind}`);
  }
  if (
    entry.state === "verified" &&
    entry.evidence === publicationDecision.qualityEvidence &&
    verifiedKind === "live"
  ) {
    errors.push(`${label} live verification cannot reuse local quality evidence`);
  }
  if (entry.state === "not-applicable" && entry.evidenceKind !== "not-applicable") {
    errors.push(`${label} not-applicable evidence must use evidenceKind=not-applicable`);
  }
}

function validateRequiredEvidenceBinding(entry) {
  if (entry.evidenceKind !== "quality" && entry.claimChecks.length) {
    errors.push(`required evidence ${entry.name} has claim checks without quality evidence`);
  }
  if (entry.state !== "verified") return;

  if (entry.evidenceKind === "quality") {
    const claim = qualityClaims.get(entry.name);
    if (!claim) {
      errors.push(`required evidence ${entry.name} has no declared quality claim`);
      return;
    }
    if (entry.evidence !== publicationDecision.qualityEvidence) {
      errors.push(`required evidence ${entry.name} must use the quality report`);
    }
    if (!sameStrings(entry.claimChecks, claim.commands)) {
      errors.push(`required evidence ${entry.name} claim checks do not match the plan`);
    }
    if (preflight || !qualityReport) return;
    if (entry.verifiedAt !== qualityReport.generatedAt) {
      errors.push(`required evidence ${entry.name} has the wrong quality timestamp`);
    }
    for (const command of claim.commands) {
      const expectedCount = planCommandCounts.get(command) ?? 0;
      const results = qualityReport.repositories
        .flatMap((repository) => repository.commands)
        .filter((result) => result.command === command);
      if (
        results.length !== expectedCount ||
        results.some((result) => result.status !== 0)
      ) {
        errors.push(
          `required evidence ${entry.name} is not backed by every passing command: ${command}`,
        );
      }
    }
    return;
  }

  if (entry.evidenceKind === "live") {
    validateLiveRequirementEvidence(entry);
    return;
  }

  errors.push(
    `verified required evidence ${entry.name} must use quality or live evidence`,
  );
}

function validateLiveChannelEvidence(entry, key) {
  const document = readEvidenceJson(entry.evidence, `publication destination ${key}`);
  if (!document) return;
  validateSchema(`publication destination ${key} live evidence`, channelEvidenceSchema, document);
  if (document.offering !== entry.offering) {
    errors.push(`${key} live evidence offering does not match`);
  }
  if (document.destinationId !== entry.destinationId) {
    errors.push(`${key} live evidence destination does not match`);
  }
  if (document.targetVersion !== entry.targetVersion) {
    errors.push(`${key} live evidence target version does not match`);
  }
  if (document.verifiedAt !== entry.verifiedAt) {
    errors.push(`${key} live evidence verification time does not match`);
  }
  if (
    !preflight &&
    qualityReport &&
    !qualityReport.repositories.some(
      (repository) => repository.sourceCommit === document.sourceCommit,
    )
  ) {
    errors.push(`${key} live evidence source commit was not quality-tested`);
  }
}

function validateLiveRequirementEvidence(entry) {
  const label = `required evidence ${entry.name}`;
  const document = readEvidenceJson(entry.evidence, label);
  if (!document) return;
  validateSchema(`${label} live evidence`, requirementEvidenceSchema, document);
  if (document.releasePlan !== plan.name) {
    errors.push(`${label} live evidence release plan does not match`);
  }
  if (document.requirement !== entry.name) {
    errors.push(`${label} live evidence requirement does not match`);
  }
  if (document.verifiedAt !== entry.verifiedAt) {
    errors.push(`${label} live evidence verification time does not match`);
  }
  if (!preflight && qualityReport) {
    const testedCommits = qualityReport.repositories
      .map((repository) => repository.sourceCommit)
      .sort();
    if (!sameStrings(document.sourceCommits, testedCommits)) {
      errors.push(`${label} live evidence does not cover every quality-tested commit`);
    }
  }
}

function readEvidenceJson(path, label) {
  try {
    return readJson(path);
  } catch (error) {
    errors.push(
      `${label} must reference structured JSON evidence: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
    return null;
  }
}

function sameStrings(left, right) {
  return (
    left.length === right.length &&
    [...left].sort().every((value, index) => value === [...right].sort()[index])
  );
}
