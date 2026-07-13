#!/usr/bin/env node
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { basename, dirname, extname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const localOnly = process.argv.includes("--local-only");
const config = JSON.parse(
  readFileSync(resolve(root, "release/design-lint.json"), "utf8"),
);
const ignored = new Set(config.ignoredDirectories);
const sourceExtensions = new Set([".css", ".html", ".js", ".jsx", ".ts", ".tsx"]);
const failures = [];

const rules = [
  {
    id: "private-font",
    pattern: /aeonik|whitney|gt[-_ ]?sectra/i,
    message: "private AuraOne font reference",
  },
  {
    id: "remote-font",
    pattern: /fonts\.(?:googleapis|gstatic)\.com/i,
    message: "remote font dependency",
  },
  {
    id: "glass-blur",
    pattern: /backdrop-filter\s*:/i,
    message: "backdrop blur or glass styling",
  },
  {
    id: "decorative-gradient",
    pattern: /background(?:-image)?\s*:[^;]*(?:radial|linear)-gradient/i,
    message: "decorative background gradient",
  },
  {
    id: "hard-coded-release",
    pattern: /github\.com\/[^"'`\s]+\/releases\/download\//i,
    message: "hard-coded GitHub release download URL",
  },
];

function isTokenFile(path) {
  return config.tokenFilePatterns.some((pattern) => basename(path) === pattern);
}

function inspect(path) {
  const content = readFileSync(path, "utf8");
  const lines = content.split(/\r?\n/);
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    for (const rule of rules) {
      if (rule.pattern.test(line)) {
        failures.push({
          rule: rule.id,
          path,
          line: index + 1,
          message: rule.message,
        });
      }
    }
    for (const match of line.matchAll(/border-radius\s*:\s*(\d+(?:\.\d+)?)px/gi)) {
      const radius = Number(match[1]);
      if (radius > 12 && radius < 999) {
        failures.push({
          rule: "oversized-radius",
          path,
          line: index + 1,
          message: `ordinary radius exceeds 12px (${match[1]}px)`,
        });
      }
    }
    if (
      !isTokenFile(path) &&
      /\.(?:jsx|tsx)$/.test(path) &&
      /style=\{\{[^}]*?(?:#[0-9a-f]{3,8}|rgba?\()/i.test(line)
    ) {
      failures.push({
        rule: "inline-visual-token",
        path,
        line: index + 1,
        message: "raw color in an inline TSX style object",
      });
    }
  }
}

function walk(path) {
  if (!existsSync(path)) {
    failures.push({
      rule: "missing-root",
      path,
      line: 0,
      message: "configured source root does not exist",
    });
    return;
  }
  const stat = statSync(path);
  if (!stat.isDirectory()) {
    if (sourceExtensions.has(extname(path))) inspect(path);
    return;
  }
  for (const entry of readdirSync(path)) {
    if (ignored.has(entry)) continue;
    walk(resolve(path, entry));
  }
}

for (const entry of config.roots) {
  if (localOnly && entry.path !== ".") continue;
  const repository = resolve(root, entry.path);
  for (const include of entry.include) {
    walk(resolve(repository, include));
  }
}

if (failures.length) {
  for (const failure of failures) {
    const location = failure.line ? `:${failure.line}` : "";
    console.error(
      `${failure.rule} ${relative(root, failure.path)}${location} ${failure.message}`,
    );
  }
  console.error(`Design lint failed with ${failures.length} finding(s).`);
  process.exit(1);
}

console.log("Proofline OSS design lint passed.");
