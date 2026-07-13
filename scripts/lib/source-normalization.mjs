const NEXT_GENERATED_TYPES =
  /^(?:\.next[^/]*|\.qa[^/]*)\/types\/\*\*\/\*\.ts$/;

export function normalizeSourceFile(
  relativePath,
  contents,
  sourceNormalizers = [],
) {
  const normalizer = sourceNormalizers.find(
    (candidate) => candidate.path === relativePath,
  );
  if (!normalizer) return contents;
  if (normalizer.strategy === "next-tsconfig") {
    const document = JSON.parse(contents.toString("utf8"));
    if (Array.isArray(document.include)) {
      document.include = document.include.filter(
        (entry) => !NEXT_GENERATED_TYPES.test(entry),
      );
    }
    return Buffer.from(JSON.stringify(document));
  }
  return contents;
}
