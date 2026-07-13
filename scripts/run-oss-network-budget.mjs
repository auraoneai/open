#!/usr/bin/env node
import { spawn } from "node:child_process";
import { createServer } from "node:net";
import { once } from "node:events";
import { resolve } from "node:path";

const repositoryRoot = process.cwd();
const websiteRoot = resolve(repositoryRoot, "auraone-website");
const host = "127.0.0.1";
const port = await availablePort(host);
const url = `http://${host}:${port}`;
let server = null;

try {
  server = spawn(
    "npm",
    ["run", "start", "--", "--hostname", host, "--port", String(port)],
    {
      cwd: websiteRoot,
      detached: process.platform !== "win32",
      env: { ...process.env, CI: "1" },
      stdio: ["ignore", "pipe", "pipe"],
    },
  );
  server.stdout.pipe(process.stdout);
  server.stderr.pipe(process.stderr);
  await waitForServer(server, url, 120_000);

  const test = spawn(
    "pnpm",
    [
      "exec",
      "playwright",
      "test",
      "tests/e2e/oss-release-network-budget.spec.ts",
      "--project=chromium",
      "--workers=1",
      "--reporter=line",
    ],
    {
      cwd: websiteRoot,
      env: {
        ...process.env,
        APP_URL: url,
        CI: "1",
        E2E_BROWSERS: "chromium",
      },
      stdio: "inherit",
    },
  );
  const [code, signal] = await once(test, "exit");
  if (signal) {
    throw new Error(`Playwright terminated by ${signal}`);
  }
  process.exitCode = code ?? 1;
} finally {
  await stopProcessTree(server);
}

async function availablePort(hostname) {
  const listener = createServer();
  listener.unref();
  await new Promise((resolveListen, reject) => {
    listener.once("error", reject);
    listener.listen(0, hostname, resolveListen);
  });
  const address = listener.address();
  if (!address || typeof address === "string") {
    listener.close();
    throw new Error("Could not reserve a local port");
  }
  const selectedPort = address.port;
  await new Promise((resolveClose, reject) => {
    listener.close((error) => (error ? reject(error) : resolveClose()));
  });
  return selectedPort;
}

async function waitForServer(child, serverUrl, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (child.exitCode !== null) {
      throw new Error(`Marketing server exited with status ${child.exitCode}`);
    }
    try {
      const response = await fetch(serverUrl, { redirect: "manual" });
      if (response.status < 500) return;
    } catch {
      // The server is still starting.
    }
    await new Promise((resolveWait) => setTimeout(resolveWait, 250));
  }
  throw new Error(`Marketing server did not become ready at ${serverUrl}`);
}

async function stopProcessTree(child) {
  if (!child || child.exitCode !== null) return;
  const target = process.platform === "win32" ? child.pid : -child.pid;
  try {
    process.kill(target, "SIGTERM");
  } catch {
    return;
  }
  await Promise.race([
    once(child, "exit"),
    new Promise((resolveWait) => setTimeout(resolveWait, 5_000)),
  ]);
  if (child.exitCode !== null) return;
  try {
    process.kill(target, "SIGKILL");
  } catch {
    // The process exited between the check and the signal.
  }
}
