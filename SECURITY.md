# Security Policy

## Scope

This policy covers the contents of this repository:

- `packages/evalkit/` — the `auraone-evalkit` Python package and `evalkit` CLI.
- `robotics-reviewkit/` — schemas, exporters, validators, and the static viewer.
- `resources/` — open documents and writing.

The hosted AuraOne platform (https://auraone.ai), its APIs, and its infrastructure are out of scope for this repository's security policy. For platform security reports, email security@auraone.ai.

## Supported versions

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |

## Reporting a vulnerability

Please report security issues privately. Do not open a public GitHub issue.

- Email: security@auraone.ai
- Subject: `[auraone-open] <short description>`

Include:

- The component affected (`evalkit`, `robotics-reviewkit`, etc.).
- A description of the issue and its impact.
- Steps to reproduce, ideally with a minimal proof-of-concept.
- Any suggested mitigation.

We will acknowledge receipt within 3 business days and aim to provide an initial assessment within 10 business days.

## What we consider a vulnerability here

- Arbitrary code execution from processing a rubric, dataset, episode JSON, or other user-supplied input.
- Path traversal or unsafe file writes from CLI commands.
- Insecure deserialization in schema or exporter code.
- Supply-chain issues in published artifacts (PyPI wheel/sdist).

## What is not a vulnerability

- Defaults that surprise you but are documented.
- Behavior of the hosted AuraOne platform (report via security@auraone.ai instead).
- Issues in third-party tools we wrap but do not maintain.

## Disclosure

We prefer coordinated disclosure. We will work with you on a timeline that gives users time to upgrade before public details are published.
