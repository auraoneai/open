import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

const verifier = resolve(
  import.meta.dirname,
  "../verify-publication-controls.mjs",
);

test("accepts a connected npm graph with signed authorization and byte retry verification", () => {
  const result = runVerifier(completeWorkflow("npm"), "npm", "@scope/package");
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Publication controls verified/);
});

test("accepts scoped git authorization tag verification", () => {
  const workflow = completeWorkflow("npm").replace(
    'git verify-tag --raw "${{ vars.OSS_PUBLICATION_AUTHORIZATION_TAG }}"',
    'git -C publication-authorization verify-tag --raw "${{ vars.OSS_PUBLICATION_AUTHORIZATION_TAG }}"',
  );
  const result = runVerifier(workflow, "npm", "@scope/package");
  assert.equal(result.status, 0, result.stderr);
});

test("accepts a connected PyPI graph with signed authorization and filename digest maps", () => {
  const result = runVerifier(
    completeWorkflow("pypi"),
    "pypi",
    "auraone-package",
  );
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Publication controls verified/);
});

test("rejects authorization and digest controls that exist only in comments", () => {
  const workflow = `
on:
  workflow_dispatch:
jobs:
  source:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: |
          git cat-file -t "$TAG"
          git verify-tag --raw "$TAG"
          echo VALIDSIG
          test "$SIGNER" = F909806D13D9CD4CF403FA3C8C61E177EB6329E7
  publish:
    needs: source
    runs-on: ubuntu-latest
    environment: npm
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
      - uses: actions/attest-build-provenance@v3
      - run: |
          # uses: actions/checkout@v4
          # repository: auraoneai/open
          # ref: vars.OSS_PUBLICATION_AUTHORIZATION_TAG
          # path: publication-authorization
          # git verify-tag
          # F909806D13D9CD4CF403FA3C8C61E177EB6329E7
          # verify-publication-authorization.mjs --authorization auth.json
          # --repository repo --source-commit commit --package package
          # --version version --channel npm
          echo "comments are not controls"
      - id: registry
        run: |
          # npm view "@scope/package@$VERSION" dist.integrity
          # createHash("sha512"); readFileSync("package.tgz")
          # if (remote !== local) throw new Error("mismatch")
          echo exists=false
          echo exists=true
      - if: steps.registry.outputs.exists != 'true'
        run: npm publish package.tgz --provenance
  release:
    needs: source
    runs-on: ubuntu-latest
    steps:
      - run: gh release create "$TAG" --verify-tag
  verify:
    needs: publish
    runs-on: ubuntu-latest
    steps:
      - run: npm view "@scope/package@$VERSION" version
`;
  const result = runVerifier(workflow, "npm", "@scope/package");
  assert.notEqual(result.status, 0);
  assert.match(
    result.stderr,
    /separate signed publication authorization checkout/,
  );
  assert.match(
    result.stderr,
    /signed publication authorization verification with all release bindings/,
  );
  assert.match(result.stderr, /semantic byte-matched idempotent registry retry/);
});

test("rejects registry existence checks without byte equality verification", () => {
  const existenceOnly = `
          npm view "@scope/package@$VERSION" version
          echo exists=false
          echo exists=true
`;
  const workflow = completeWorkflow("npm", existenceOnly);
  const result = runVerifier(workflow, "npm", "@scope/package");
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /semantic byte-matched idempotent registry retry/);
});

test("rejects PyPI filename existence checks without local SHA256 equality", () => {
  const existenceOnly = `
          python - <<'PY'
          import json, urllib.request
          payload = json.load(urllib.request.urlopen("https://pypi.org/pypi/auraone-package/1.2.3/json"))
          filenames = [item["filename"] for item in payload["urls"]]
          open("output", "w").write("exists=true\\n" if filenames else "exists=false\\n")
          PY
`;
  const workflow = completeWorkflow("pypi", existenceOnly);
  const result = runVerifier(workflow, "pypi", "auraone-package");
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /semantic byte-matched idempotent registry retry/);
});

test("rejects authorization performed after public provenance attestation", () => {
  const workflow = completeWorkflow("npm", retryRun("npm"), true);
  const result = runVerifier(workflow, "npm", "@scope/package");
  assert.notEqual(result.status, 0);
  assert.match(
    result.stderr,
    /authorization checkout before attestation, registry access, and publication/,
  );
  assert.match(
    result.stderr,
    /authorization verification with all release bindings before attestation, registry access, and publication/,
  );
});

test("rejects independent GitHub Release writes without direct authorization", () => {
  const workflow = completeWorkflow("npm").replace(
    "  release:\n    needs: verify",
    "  release:\n    needs: source",
  );
  const result = runVerifier(workflow, "npm", "@scope/package");
  assert.notEqual(result.status, 0);
  assert.match(
    result.stderr,
    /direct signed publication authorization before independent GitHub Release or distribution writes/,
  );
});

function completeWorkflow(
  registry,
  registryRun = retryRun(registry),
  authorizationAfterAttestation = false,
) {
  const publishStep =
    registry === "npm"
      ? `
      - name: Publish exact tarball
        if: steps.registry.outputs.exists != 'true'
        run: npm publish release/package.tgz --provenance
`
      : `
      - name: Publish exact distributions
        if: steps.registry.outputs.exists != 'true'
        uses: pypa/gh-action-pypi-publish@release/v1
`;
  const verificationStep =
    registry === "npm"
      ? `npm view "@scope/package@$VERSION" version`
      : `pip install --no-cache-dir "auraone-package==$VERSION"`;
  const attestationStep = `
      - uses: actions/attest-build-provenance@v3
`;
  const authorizationSteps = `
      - name: Check out signed coordinated authorization
        uses: actions/checkout@v4
        with:
          repository: auraoneai/open
          ref: \${{ vars.OSS_PUBLICATION_AUTHORIZATION_TAG }}
          path: publication-authorization
          persist-credentials: false
      - name: Verify signed coordinated authorization
        working-directory: publication-authorization
        run: |
          git verify-tag --raw "\${{ vars.OSS_PUBLICATION_AUTHORIZATION_TAG }}"
          test "$SIGNER" = F909806D13D9CD4CF403FA3C8C61E177EB6329E7
          node scripts/verify-publication-authorization.mjs \\
            --authorization release/publication-authorization.json \\
            --repository auraone-open-public \\
            --source-commit 0123456789abcdef0123456789abcdef01234567 \\
            --package "$PACKAGE_NAME" \\
            --version "$VERSION" \\
            --channel ${registry}
`;
  const authorizedAttestationSteps = authorizationAfterAttestation
    ? `${attestationStep}${authorizationSteps}`
    : `${authorizationSteps}${attestationStep}`;

  return `
on:
  workflow_dispatch:
jobs:
  source:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: |
          git cat-file -t "$TAG"
          git verify-tag --raw "$TAG"
          echo VALIDSIG
          test "$SIGNER" = F909806D13D9CD4CF403FA3C8C61E177EB6329E7
  publish:
    needs: source
    runs-on: ubuntu-latest
    environment: ${registry}
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
${authorizedAttestationSteps}
      - name: Check for an exact prior publication
        id: registry
        run: |
${registryRun}
${publishStep}
  release:
    needs: verify
    runs-on: ubuntu-latest
    steps:
      - run: gh release create "$TAG" --verify-tag
  verify:
    needs: publish
    runs-on: ubuntu-latest
    steps:
      - run: ${verificationStep}
`;
}

function retryRun(registry) {
  if (registry === "npm") {
    return `
          node --input-type=module <<'NODE'
          import { createHash } from "node:crypto";
          import { appendFileSync, readFileSync } from "node:fs";
          import { spawnSync } from "node:child_process";
          const spec = "@scope/package@1.2.3";
          const result = spawnSync("npm", ["view", spec, "dist.integrity", "--json"], {
            encoding: "utf8",
          });
          if (result.status !== 0) {
            appendFileSync(process.env.GITHUB_OUTPUT, "exists=false\\n");
            process.exit(0);
          }
          const localIntegrity = \`sha512-\${createHash("sha512")
            .update(readFileSync("release/package.tgz"))
            .digest("base64")}\`;
          if (JSON.parse(result.stdout) !== localIntegrity) {
            throw new Error(\`\${spec} exists with different tarball bytes\`);
          }
          appendFileSync(process.env.GITHUB_OUTPUT, "exists=true\\n");
          NODE
`;
  }
  return `
          python - <<'PY'
          import hashlib, json, os, pathlib, urllib.error, urllib.request
          try:
              with urllib.request.urlopen("https://pypi.org/pypi/auraone-package/1.2.3/json") as response:
                  payload = json.load(response)
          except urllib.error.HTTPError as error:
              if error.code != 404:
                  raise
              open(os.environ["GITHUB_OUTPUT"], "a").write("exists=false\\n")
              raise SystemExit(0)
          remote = {item["filename"]: item["digests"]["sha256"] for item in payload["urls"]}
          local = {
              path.name: hashlib.sha256(path.read_bytes()).hexdigest()
              for path in pathlib.Path("dist").iterdir() if path.is_file()
          }
          if remote != local:
              raise SystemExit("package exists with different distribution bytes")
          open(os.environ["GITHUB_OUTPUT"], "a").write("exists=true\\n")
          PY
`;
}

function runVerifier(workflow, registry, packageName) {
  const directory = mkdtempSync(join(tmpdir(), "publication-controls-"));
  try {
    const path = join(directory, "release.yml");
    writeFileSync(path, workflow);
    return spawnSync(
      process.execPath,
      [
        verifier,
        "--workflow",
        path,
        "--registry",
        registry,
        "--package",
        packageName,
      ],
      { encoding: "utf8" },
    );
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}
