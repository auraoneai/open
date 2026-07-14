#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const auraoneRoot = process.env.AURAONE_ROOT
  ? resolve(process.env.AURAONE_ROOT)
  : resolve(root, "../../../AuraOne");
const localOnly = process.argv.includes("--local-only");
const contract = JSON.parse(
  readFileSync(resolve(root, "release/version-surfaces.json"), "utf8"),
);
const failures = [];
let checkedProducts = 0;
let checkedSurfaces = 0;

for (const product of contract.products) {
  const surfaces = product.surfaces.filter((surface) => {
    const path = resolveContractPath(surface.path);
    return !localOnly || path === root || path.startsWith(`${root}/`);
  });
  if (!surfaces.length) continue;
  checkedProducts += 1;

  const changelogPath = resolveContractPath(product.changelog);
  const changelog = readFileSync(changelogPath, "utf8");
  if (!changelog.includes(product.expected)) {
    failures.push(
      `${product.name}: ${product.changelog}: missing ${product.expected} changelog entry`,
    );
  }

  for (const surface of surfaces) {
    checkedSurfaces += 1;
    const path = resolveContractPath(surface.path);
    let observed;
    try {
      observed = readVersion(path, surface.format);
    } catch (error) {
      failures.push(
        `${product.name}: ${surface.path}: ${error instanceof Error ? error.message : String(error)}`,
      );
      continue;
    }
    if (observed !== product.expected) {
      failures.push(
        `${product.name}: ${surface.path}: expected ${product.expected}, observed ${observed}`,
      );
    }
  }
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(
  `Version surfaces aligned: ${checkedProducts} products, ` +
    `${checkedSurfaces} authoritative files${localOnly ? " in this repository" : ""}.`,
);

function readVersion(path, format) {
  const source = readFileSync(path, "utf8");
  if (format === "json") return JSON.parse(source).version;
  if (format === "json-platform") return JSON.parse(source).platformVersion;
  if (format === "toml-project") return readTomlSectionVersion(source, "project");
  if (format === "toml-package") return readTomlSectionVersion(source, "package");
  if (format === "python-version") {
    return matchVersion(source, /__version__\s*=\s*["']([^"']+)["']/);
  }
  if (format === "typescript-version") {
    return matchVersion(
      source,
      /(?:SDK_VERSION|VERSION)\s*=\s*["']([^"']+)["']/,
    );
  }
  throw new Error(`unsupported version format ${format}`);
}

function resolveContractPath(path) {
  const auraonePrefix = "../../../AuraOne/";
  if (path.startsWith(auraonePrefix)) {
    return resolve(auraoneRoot, path.slice(auraonePrefix.length));
  }
  return resolve(root, path);
}

function readTomlSectionVersion(source, section) {
  const match = source.match(
    new RegExp(
      `^\\[${escapeRegExp(section)}\\][\\s\\S]*?^version\\s*=\\s*["']([^"']+)["']`,
      "m",
    ),
  );
  if (!match) throw new Error(`missing [${section}] version`);
  return match[1];
}

function matchVersion(source, pattern) {
  const match = source.match(pattern);
  if (!match) throw new Error("missing version constant");
  return match[1];
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
