import assert from "node:assert/strict";
import test from "node:test";
import { normalizeSourceFile } from "../lib/source-normalization.mjs";

const path = "auraone-website/tsconfig.json";
const normalizers = [{ path, strategy: "next-tsconfig" }];

function normalize(document) {
  return normalizeSourceFile(
    path,
    Buffer.from(JSON.stringify(document, null, 2)),
    normalizers,
  ).toString("utf8");
}

test("canonicalizes formatting and generated Next type includes", () => {
  const base = {
    compilerOptions: {
      strict: true,
      paths: { "@/*": ["./src/*"] },
    },
    include: ["next-env.d.ts", "src/**/*.ts", "src/**/*.tsx"],
  };
  const generated = {
    compilerOptions: {
      strict: true,
      paths: { "@/*": ["./src/*"] },
    },
    include: [
      ".next-build/types/**/*.ts",
      ".qa-next-4401/types/**/*.ts",
      "next-env.d.ts",
      "src/**/*.ts",
      "src/**/*.tsx",
      ".next/types/**/*.ts",
    ],
  };

  assert.equal(normalize(base), normalize(generated));
});

test("retains compiler options and non-generated includes", () => {
  const base = {
    compilerOptions: { strict: true },
    include: ["next-env.d.ts", "src/**/*.ts"],
  };

  assert.notEqual(
    normalize(base),
    normalize({
      ...base,
      compilerOptions: { strict: false },
    }),
  );
  assert.notEqual(
    normalize(base),
    normalize({
      ...base,
      include: [...base.include, "tests/**/*.ts"],
    }),
  );
});

test("leaves files without a configured normalizer byte-identical", () => {
  const contents = Buffer.from("{\n  \"include\": [\".next/types/**/*.ts\"]\n}\n");
  assert.equal(
    normalizeSourceFile("other/tsconfig.json", contents, normalizers),
    contents,
  );
});

test("fails closed for malformed normalized JSON", () => {
  assert.throws(() =>
    normalizeSourceFile(path, Buffer.from("{"), normalizers),
  );
});
