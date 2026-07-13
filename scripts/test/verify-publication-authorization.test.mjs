import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

const verifier = resolve(
  import.meta.dirname,
  "../verify-publication-authorization.mjs",
);
const repository = "auraone-open-public";
const sourceCommit = "0123456789abcdef0123456789abcdef01234567";
const packageName = "@auraone/example";
const version = "1.2.3";
const channel = "npm";
const now = "2026-07-12T12:00:00Z";

test("accepts one current exact approved release binding", () => {
  const result = runVerifier(approvedAuthorization());
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Publication authorized/);
});

test("rejects the fail-closed blocked authorization template", () => {
  const template = JSON.parse(
    readFileSync(
      resolve(import.meta.dirname, "../../release/publication-authorization.json"),
      "utf8",
    ),
  );
  const result = runVerifier(template);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /decision is blocked, not approved/);
  assert.match(result.stderr, /publicationAllowed is not true/);
});

test("rejects repository, commit, package, version, and channel mismatches", async (t) => {
  const mismatches = [
    ["repository", { repository: "different-repository" }],
    ["source commit", { sourceCommit: "f".repeat(40) }],
    ["package", { package: "@auraone/different" }],
    ["version", { version: "1.2.4" }],
    ["channel", { channel: "pypi" }],
  ];
  for (const [name, overrides] of mismatches) {
    await t.test(name, () => {
      const result = runVerifier(approvedAuthorization(), overrides);
      assert.notEqual(result.status, 0);
      assert.match(
        result.stderr,
        /no exact authorized release entry includes the requested channel/,
      );
    });
  }
});

test("rejects invalid, expired, future, and inverted authorization windows", async (t) => {
  await t.test("invalid date", () => {
    const authorization = approvedAuthorization();
    authorization.authorizedAt = "2026-02-30T11:00:00Z";
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /authorizedAt must be a valid ISO date-time/);
  });
  await t.test("expired", () => {
    const authorization = approvedAuthorization();
    authorization.expiresAt = now;
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /authorization has expired/);
  });
  await t.test("future authorizedAt", () => {
    const authorization = approvedAuthorization();
    authorization.authorizedAt = "2026-07-12T12:00:01Z";
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /authorizedAt is in the future/);
  });
  await t.test("expires before authorizedAt", () => {
    const authorization = approvedAuthorization();
    authorization.expiresAt = "2026-07-12T10:59:59Z";
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /expiresAt must be later than authorizedAt/);
  });
});

test("rejects duplicate release bindings and duplicate channels", async (t) => {
  await t.test("duplicate release binding", () => {
    const authorization = approvedAuthorization();
    authorization.releases.push(structuredClone(authorization.releases[0]));
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /duplicates an existing release binding/);
  });
  await t.test("duplicate channel", () => {
    const authorization = approvedAuthorization();
    authorization.releases[0].channels.push(channel);
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /channels contains duplicate/);
  });
});

test("rejects malformed commits, versions, empty approvers, and unknown fields", async (t) => {
  const cases = [
    [
      "malformed commit",
      (authorization) => {
        authorization.releases[0].sourceCommit = "not-a-commit";
      },
      /sourceCommit must be exactly 40 lowercase hexadecimal/,
    ],
    [
      "malformed version",
      (authorization) => {
        authorization.releases[0].version = "01.2.3";
      },
      /version must be a valid semantic version/,
    ],
    [
      "empty approver",
      (authorization) => {
        authorization.approvers = ["   "];
      },
      /approvers\[0\] must be a nonempty string/,
    ],
    [
      "unknown field",
      (authorization) => {
        authorization.unreviewedOverride = true;
      },
      /unreviewedOverride is not allowed/,
    ],
  ];
  for (const [name, mutate, expected] of cases) {
    await t.test(name, () => {
      const authorization = approvedAuthorization();
      mutate(authorization);
      const result = runVerifier(authorization);
      assert.notEqual(result.status, 0);
      assert.match(result.stderr, expected);
    });
  }
});

test("rejects inconsistent approved, blocked, and revoked states", async (t) => {
  await t.test("approved but publication disallowed", () => {
    const authorization = approvedAuthorization();
    authorization.publicationAllowed = false;
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(
      result.stderr,
      /approved authorization must set publicationAllowed to true/,
    );
  });
  await t.test("blocked but publication allowed", () => {
    const authorization = approvedAuthorization();
    authorization.decision = "blocked";
    authorization.reason = "Blocked after review.";
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /blocked authorization cannot allow publication/);
  });
  await t.test("revoked but publication allowed", () => {
    const authorization = approvedAuthorization();
    authorization.decision = "revoked";
    authorization.reason = "Authorization was revoked.";
    const result = runVerifier(authorization);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /revoked authorization cannot allow publication/);
  });
});

test("rejects malformed CLI binding values", async (t) => {
  await t.test("source commit", () => {
    const result = runVerifier(approvedAuthorization(), {
      sourceCommit: "ABC",
    });
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /--source-commit must be exactly 40 lowercase/);
  });
  await t.test("semantic version", () => {
    const result = runVerifier(approvedAuthorization(), {
      version: "v1.2.3",
    });
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /--version must be a valid semantic version/);
  });
});

function approvedAuthorization() {
  return {
    $schema: "./publication-authorization.schema.json",
    schemaVersion: "1.0.0",
    releasePlan:
      "release(oss): publish Proofline UI/UX upgrade across all channels",
    decision: "approved",
    publicationAllowed: true,
    authorizedAt: "2026-07-12T11:00:00Z",
    expiresAt: "2026-07-12T13:00:00Z",
    approvers: ["AuraOne release owner"],
    releases: [
      {
        repository,
        sourceCommit,
        package: packageName,
        version,
        channels: [channel, "github-release"],
      },
    ],
  };
}

function runVerifier(authorization, overrides = {}) {
  const directory = mkdtempSync(join(tmpdir(), "publication-authorization-"));
  try {
    const path = join(directory, "authorization.json");
    writeFileSync(path, `${JSON.stringify(authorization, null, 2)}\n`);
    return spawnSync(
      process.execPath,
      [
        verifier,
        "--authorization",
        path,
        "--repository",
        overrides.repository ?? repository,
        "--source-commit",
        overrides.sourceCommit ?? sourceCommit,
        "--package",
        overrides.package ?? packageName,
        "--version",
        overrides.version ?? version,
        "--channel",
        overrides.channel ?? channel,
        "--now",
        overrides.now ?? now,
      ],
      { encoding: "utf8" },
    );
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}
