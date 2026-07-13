#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { existsSync, readdirSync, statSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const localOnly = process.argv.includes("--local-only");
const workflowLocations = [
  resolve(root, ".github/workflows"),
  ...(!localOnly
    ? [
        resolve(root, "../auraoneai-github-app/.github/workflows"),
        resolve(root, "../auraoneai-sdk-python/.github/workflows"),
        resolve(root, "../auraoneai-sdk-typescript/.github/workflows"),
        resolve(root, "../../../AuraOne/opensource/open-studio-platform/.github/workflows"),
        resolve(root, "../../../AuraOne/opensource/evalkit-action/.github/workflows"),
        resolve(root, "../../../AuraOne/opensource/datasheet-ci/.github/workflows"),
        resolve(root, "../../../AuraOne/opensource/rubric-pr-bot/.github/workflows"),
        resolve(root, "../../../AuraOne/opensource/evalkit-playground/.github/workflows"),
        resolve(root, "../../../AuraOne/opensource/failure-gallery/.github/workflows"),
        resolve(root, "../../../AuraOne/.github/workflows/proofline-oss-release.yml"),
        resolve(root, "../../../AuraOne/.github/workflows/agent-studio-open-release.yml"),
        resolve(root, "../../../AuraOne/.github/workflows/oss-uiux-release-contracts.yml"),
        resolve(
          root,
          "../../../AuraOne/.github/workflows/agent-studio-open-release-readiness.yml",
        ),
      ]
    : []),
];

const workflows = [];
for (const location of workflowLocations) {
  if (!existsSync(location)) {
    throw new Error(`workflow path does not exist: ${location}`);
  }
  if (statSync(location).isFile()) {
    workflows.push(location);
    continue;
  }
  for (const entry of readdirSync(location).sort()) {
    if (/\.ya?ml$/i.test(entry)) workflows.push(resolve(location, entry));
  }
}

if (!workflows.length) throw new Error("no GitHub Actions workflows found");

const binary = spawnSync("actionlint", ["-version"], { encoding: "utf8" });
const command =
  binary.status === 0
    ? ["actionlint", workflows]
    : [
        "go",
        [
          "run",
          "github.com/rhysd/actionlint/cmd/actionlint@v1.7.7",
          ...workflows,
        ],
      ];
const [executable, commandArgs] = command;
const result = spawnSync(executable, commandArgs, {
  cwd: root,
  encoding: "utf8",
  stdio: "inherit",
});
if (result.error) {
  console.error(`Unable to run Actionlint: ${result.error.message}`);
  process.exit(1);
}
if (result.status !== 0) process.exit(result.status ?? 1);
console.log(`Actionlint passed for ${workflows.length} release workflows.`);
