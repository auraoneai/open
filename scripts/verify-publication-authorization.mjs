#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const EXPECTED_SCHEMA = "./publication-authorization.schema.json";
const EXPECTED_SCHEMA_VERSION = "1.0.0";
const EXPECTED_RELEASE_PLAN =
  "release(oss): publish Proofline UI/UX upgrade across all channels";
const TOP_LEVEL_FIELDS = new Set([
  "$schema",
  "schemaVersion",
  "releasePlan",
  "decision",
  "publicationAllowed",
  "authorizedAt",
  "expiresAt",
  "approvers",
  "releases",
  "reason",
]);
const REQUIRED_FIELDS = [
  "$schema",
  "schemaVersion",
  "releasePlan",
  "decision",
  "publicationAllowed",
  "authorizedAt",
  "expiresAt",
  "approvers",
  "releases",
];
const RELEASE_FIELDS = new Set([
  "repository",
  "sourceCommit",
  "package",
  "version",
  "channels",
]);
const SOURCE_COMMIT = /^[0-9a-f]{40}$/;
const SEMVER =
  /^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/;
const ISO_DATE_TIME =
  /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})$/;

try {
  const options = parseArguments(process.argv.slice(2));
  const errors = [];
  validateInputOptions(options, errors);

  let authorization;
  if (!errors.length) {
    try {
      authorization = JSON.parse(
        readFileSync(resolve(process.cwd(), options.authorization), "utf8"),
      );
    } catch (error) {
      errors.push(`cannot read authorization JSON: ${error.message}`);
    }
  }

  const now = parseDateTime(options.now ?? new Date().toISOString(), "--now", errors);
  if (authorization !== undefined) {
    validateAuthorization(authorization, now, options, errors);
  }

  if (errors.length) {
    throw new Error([...new Set(errors)].join("; "));
  }

  console.log(
    `Publication authorized for ${options.package}@${options.version} on ${options.channel} from ${options.repository}@${options.sourceCommit}.`,
  );
} catch (error) {
  console.error(`Publication authorization rejected: ${error.message}`);
  process.exitCode = 1;
}

function parseArguments(args) {
  const supported = new Set([
    "--authorization",
    "--repository",
    "--source-commit",
    "--package",
    "--version",
    "--channel",
    "--now",
  ]);
  const options = {};

  for (let index = 0; index < args.length; index += 2) {
    const flag = args[index];
    const value = args[index + 1];
    if (!supported.has(flag)) {
      throw new Error(`unsupported argument: ${flag ?? "<missing>"}`);
    }
    if (Object.hasOwn(options, flag.slice(2))) {
      throw new Error(`duplicate argument: ${flag}`);
    }
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`missing value for ${flag}`);
    }
    options[flag.slice(2)] = value;
  }

  return {
    authorization: options.authorization,
    repository: options.repository,
    sourceCommit: options["source-commit"],
    package: options.package,
    version: options.version,
    channel: options.channel,
    now: options.now,
  };
}

function validateInputOptions(options, errors) {
  for (const field of [
    "authorization",
    "repository",
    "sourceCommit",
    "package",
    "version",
    "channel",
  ]) {
    if (!isNonemptyString(options[field])) {
      errors.push(`missing or empty --${toFlag(field)}`);
    }
  }
  if (
    options.sourceCommit !== undefined &&
    !SOURCE_COMMIT.test(options.sourceCommit)
  ) {
    errors.push("--source-commit must be exactly 40 lowercase hexadecimal characters");
  }
  if (options.version !== undefined && !SEMVER.test(options.version)) {
    errors.push("--version must be a valid semantic version");
  }
}

function validateAuthorization(document, now, options, errors) {
  if (!isPlainObject(document)) {
    errors.push("authorization must be a JSON object");
    return;
  }

  rejectUnknownFields(document, TOP_LEVEL_FIELDS, "authorization", errors);
  for (const field of REQUIRED_FIELDS) {
    if (!Object.hasOwn(document, field)) {
      errors.push(`authorization.${field} is required`);
    }
  }
  if (document.$schema !== EXPECTED_SCHEMA) {
    errors.push(`authorization.$schema must equal ${EXPECTED_SCHEMA}`);
  }
  if (document.schemaVersion !== EXPECTED_SCHEMA_VERSION) {
    errors.push(
      `authorization.schemaVersion must equal ${EXPECTED_SCHEMA_VERSION}`,
    );
  }
  if (document.releasePlan !== EXPECTED_RELEASE_PLAN) {
    errors.push("authorization.releasePlan does not match the release plan");
  }
  if (!["blocked", "approved", "revoked"].includes(document.decision)) {
    errors.push("authorization.decision must be blocked, approved, or revoked");
  }
  if (typeof document.publicationAllowed !== "boolean") {
    errors.push("authorization.publicationAllowed must be a boolean");
  }
  if (
    Object.hasOwn(document, "reason") &&
    !isNonemptyString(document.reason)
  ) {
    errors.push("authorization.reason must be a nonempty string");
  }

  const authorizedAt = parseNullableDateTime(
    document.authorizedAt,
    "authorization.authorizedAt",
    errors,
  );
  const expiresAt = parseNullableDateTime(
    document.expiresAt,
    "authorization.expiresAt",
    errors,
  );

  validateApprovers(document.approvers, errors);
  validateReleases(document.releases, errors);
  validateDecisionState(document, errors);

  if (
    authorizedAt !== null &&
    expiresAt !== null &&
    Number.isFinite(authorizedAt) &&
    Number.isFinite(expiresAt) &&
    authorizedAt >= expiresAt
  ) {
    errors.push("authorization.expiresAt must be later than authorizedAt");
  }

  if (document.decision === "approved") {
    if (Number.isFinite(authorizedAt) && Number.isFinite(now) && authorizedAt > now) {
      errors.push("authorization.authorizedAt is in the future");
    }
    if (Number.isFinite(expiresAt) && Number.isFinite(now) && expiresAt <= now) {
      errors.push("authorization has expired");
    }
  }

  if (document.decision !== "approved") {
    errors.push(`authorization decision is ${document.decision}, not approved`);
  }
  if (document.publicationAllowed !== true) {
    errors.push("authorization.publicationAllowed is not true");
  }

  if (Array.isArray(document.releases)) {
    const matchingBindings = document.releases.filter(
      (release) =>
        isPlainObject(release) &&
        release.repository === options.repository &&
        release.sourceCommit === options.sourceCommit &&
        release.package === options.package &&
        release.version === options.version,
    );
    const exactMatches = matchingBindings.filter(
      (release) =>
        Array.isArray(release.channels) &&
        release.channels.includes(options.channel),
    );
    if (exactMatches.length !== 1) {
      errors.push(
        exactMatches.length === 0
          ? "no exact authorized release entry includes the requested channel"
          : "more than one exact authorized release entry matches the request",
      );
    }
  }
}

function validateApprovers(approvers, errors) {
  if (!Array.isArray(approvers)) {
    errors.push("authorization.approvers must be an array");
    return;
  }
  const seen = new Set();
  for (const [index, approver] of approvers.entries()) {
    if (!isNonemptyString(approver)) {
      errors.push(`authorization.approvers[${index}] must be a nonempty string`);
      continue;
    }
    if (seen.has(approver)) {
      errors.push(`authorization.approvers contains duplicate ${JSON.stringify(approver)}`);
    }
    seen.add(approver);
  }
}

function validateReleases(releases, errors) {
  if (!Array.isArray(releases)) {
    errors.push("authorization.releases must be an array");
    return;
  }

  const bindings = new Set();
  for (const [index, release] of releases.entries()) {
    const path = `authorization.releases[${index}]`;
    if (!isPlainObject(release)) {
      errors.push(`${path} must be an object`);
      continue;
    }
    rejectUnknownFields(release, RELEASE_FIELDS, path, errors);
    for (const field of RELEASE_FIELDS) {
      if (!Object.hasOwn(release, field)) {
        errors.push(`${path}.${field} is required`);
      }
    }
    for (const field of ["repository", "package"]) {
      if (!isNonemptyString(release[field])) {
        errors.push(`${path}.${field} must be a nonempty string`);
      }
    }
    if (!SOURCE_COMMIT.test(release.sourceCommit ?? "")) {
      errors.push(
        `${path}.sourceCommit must be exactly 40 lowercase hexadecimal characters`,
      );
    }
    if (!SEMVER.test(release.version ?? "")) {
      errors.push(`${path}.version must be a valid semantic version`);
    }
    validateChannels(release.channels, path, errors);

    const binding = [
      release.repository,
      release.sourceCommit,
      release.package,
      release.version,
    ].join("\u0000");
    if (bindings.has(binding)) {
      errors.push(`${path} duplicates an existing release binding`);
    }
    bindings.add(binding);
  }
}

function validateChannels(channels, path, errors) {
  if (!Array.isArray(channels) || channels.length === 0) {
    errors.push(`${path}.channels must be a nonempty array`);
    return;
  }
  const seen = new Set();
  for (const [index, channel] of channels.entries()) {
    if (!isNonemptyString(channel)) {
      errors.push(`${path}.channels[${index}] must be a nonempty string`);
      continue;
    }
    if (seen.has(channel)) {
      errors.push(`${path}.channels contains duplicate ${JSON.stringify(channel)}`);
    }
    seen.add(channel);
  }
}

function validateDecisionState(document, errors) {
  if (document.decision === "approved") {
    if (document.publicationAllowed !== true) {
      errors.push("approved authorization must set publicationAllowed to true");
    }
    if (document.authorizedAt === null || document.expiresAt === null) {
      errors.push("approved authorization requires authorizedAt and expiresAt");
    }
    if (!Array.isArray(document.approvers) || document.approvers.length === 0) {
      errors.push("approved authorization requires at least one approver");
    }
    if (!Array.isArray(document.releases) || document.releases.length === 0) {
      errors.push("approved authorization requires at least one release");
    }
    return;
  }

  if (document.publicationAllowed === true) {
    errors.push(`${document.decision} authorization cannot allow publication`);
  }
  if (!isNonemptyString(document.reason)) {
    errors.push(`${document.decision} authorization requires a reason`);
  }
  if (document.decision === "blocked") {
    if (document.authorizedAt !== null || document.expiresAt !== null) {
      errors.push("blocked authorization must use null authorization times");
    }
    if (Array.isArray(document.approvers) && document.approvers.length !== 0) {
      errors.push("blocked authorization must have no approvers");
    }
    if (Array.isArray(document.releases) && document.releases.length !== 0) {
      errors.push("blocked authorization must have no releases");
    }
  }
}

function parseNullableDateTime(value, label, errors) {
  if (value === null) return null;
  if (typeof value !== "string") {
    errors.push(`${label} must be an ISO date-time string or null`);
    return Number.NaN;
  }
  return parseDateTime(value, label, errors);
}

function parseDateTime(value, label, errors) {
  if (typeof value !== "string") {
    errors.push(`${label} must be an ISO date-time string`);
    return Number.NaN;
  }
  const match = ISO_DATE_TIME.exec(value);
  if (!match) {
    errors.push(`${label} must be a valid ISO date-time`);
    return Number.NaN;
  }
  const [, yearText, monthText, dayText, hourText, minuteText, secondText, , zone] =
    match;
  const year = Number(yearText);
  const month = Number(monthText);
  const day = Number(dayText);
  const hour = Number(hourText);
  const minute = Number(minuteText);
  const second = Number(secondText);
  const zoneHour = zone === "Z" ? 0 : Number(zone.slice(1, 3));
  const zoneMinute = zone === "Z" ? 0 : Number(zone.slice(4, 6));
  const daysInMonth = [
    31,
    isLeapYear(year) ? 29 : 28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31,
  ];
  if (
    month < 1 ||
    month > 12 ||
    day < 1 ||
    day > (daysInMonth[month - 1] ?? 0) ||
    hour > 23 ||
    minute > 59 ||
    second > 59 ||
    zoneHour > 23 ||
    zoneMinute > 59
  ) {
    errors.push(`${label} must be a valid ISO date-time`);
    return Number.NaN;
  }
  const timestamp = Date.parse(value);
  if (!Number.isFinite(timestamp)) {
    errors.push(`${label} must be a valid ISO date-time`);
  }
  return timestamp;
}

function rejectUnknownFields(value, allowed, path, errors) {
  for (const field of Object.keys(value)) {
    if (!allowed.has(field)) {
      errors.push(`${path}.${field} is not allowed`);
    }
  }
}

function isPlainObject(value) {
  return (
    value !== null &&
    typeof value === "object" &&
    !Array.isArray(value) &&
    Object.getPrototypeOf(value) === Object.prototype
  );
}

function isNonemptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isLeapYear(year) {
  return year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
}

function toFlag(field) {
  return field.replace(/[A-Z]/g, (character) => `-${character.toLowerCase()}`);
}
