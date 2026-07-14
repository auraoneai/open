# AuraOne Open Source UI/UX Upgrade Blueprint

- **Status:** July 13-14, 2026 public-release reconciliation complete for
  GitHub, all 26 PyPI projects, the current npm packages, macOS DMGs, AuraOne
  marketing, and hosted Studio surfaces. Four tested npm candidates remain
  blocked by registry write authorization and are not presented as published.
  Unsupported channels remain explicitly unavailable.
- **Authoritative design source:** `/Users/gurbakshchahal/AuraOne`
- **AuraFoundry `main`:**
  `93c4cc845c96088a88a2e00a764bf9592a5480e1`
- **AuraFoundry marketing deployment source:**
  `70928471f6fce30c3a3c7e4c92af3e0eee9613bd`
- **Rubric Studio Open `main`:**
  `155947a50d433f6bdf8f0e0e7dfbfb07a690b8b8`
- **Agent Studio Open `main`:**
  `225eb0e194db77e898a02531b6d4b97daa292b31`
- **Robotics Studio Open `main`:**
  `c688023c2858634a3c4c035b589d344bc460369d`
- **Coordinator repository:**
  `/Users/gurbakshchahal/opensource/AuraOne OSS/auraone-open-public`
- **Additional repositories audited without overwriting unrelated local
  changes:**
  - `/Users/gurbakshchahal/opensource/AuraOne OSS/auraoneai-github-app`
  - `/Users/gurbakshchahal/opensource/AuraOne OSS/auraoneai-sdk-python`
  - `/Users/gurbakshchahal/opensource/AuraOne OSS/auraoneai-sdk-typescript`
- **Related product sources reviewed:** `/Users/gurbakshchahal/AuraOne/opensource/**`
- **Historical completion evidence:** `release/evidence/publication-completion.json`

> This document translates the AuraOne Proofline makeover into a complete,
> public-source-safe UI/UX plan for AuraOne Open. It covers the marketing
> website, desktop applications and DMG distribution, browser applications,
> React/TSX workspaces, static viewers, generated HTML reports, GitHub-native
> output, CLI output, SDK documentation, release assets, and shared design
> infrastructure.

**Source-of-truth rule:** The reconciliation below is the current public
release ledger. Later sections preserve the deeper design analysis and the
historical release program, but older checked boxes, versions, commit IDs, or
channel assumptions must not override this section.

## Authoritative Live Reconciliation

This section records what was independently queried from the public
destinations after the July 13, 2026 release work. A release is considered live
only when the exact public registry, repository, release asset, or production
domain can be read back successfully.

### Flagship Studio release matrix

The desktop product, JavaScript registry companion, Python/headless package,
hosted web application, and marketing page are separate release surfaces. Their
version numbers are intentionally independent and must not be collapsed into
one misleading "current version."

| Product | Dedicated GitHub `main` | Product release and macOS artifact | npm companion | Python/headless package | Hosted application | Marketing treatment |
| --- | --- | --- | --- | --- | --- | --- |
| Rubric Studio Open | `155947a50d433f6bdf8f0e0e7dfbfb07a690b8b8` | `v0.2.0`; signed/notarized arm64 DMG | `@auraone/rubric-studio@0.2.1` | `rubric-studio==0.0.3`; wheel and sdist | `rubric-studio.auraone.ai` | One criterion/scoring screenshot; no gallery or collage |
| Agent Studio Open | `225eb0e194db77e898a02531b6d4b97daa292b31` | `v0.2.0`; signed/notarized arm64 DMG | `@auraone/agent-studio@0.2.1`; tested `0.2.2` candidate blocked by npm 2FA | `auraone-agent-studio-open==0.2.1`; wheel and sdist | `agentstudio.auraone.ai` | One trace/replay screenshot; no gallery or collage |
| Robotics Studio Open | `c688023c2858634a3c4c035b589d344bc460369d` | `v0.2.0`; signed/notarized arm64 DMG | `@auraone/robotics-studio@0.2.1` | `robostudio-engine==0.1.2`; wheel and sdist | `robotics-studio.auraone.ai` | One evidence-review screenshot; no gallery or collage |

The current Studio `main` hashes include the final documentation-only registry
truth synchronization. The accepted visual and DMG release sources remain
`1f3db2065a5e9ee5bade84279c8f83d22f636b7f` for Rubric,
`549d0b5093c7555d255bbaf05e5f98487b29502d` for Agent, and
`ac4dda0f786ffe06577a660c2f5adb2a0804f4c7` for Robotics.
The documentation corrections merged through protected pull requests Rubric
`#68`, Agent `#17`, and Robotics `#41`; each required status matrix passed and
the two-approval plus code-owner branch rule was restored immediately after
the exact tested head merged.

The npm packages are supported JavaScript release/validation companions. They
are not substitutes for the desktop DMGs. The Python projects expose the
corresponding CLI, protocol, or headless engine surface; they are not copies of
the browser application.

### Flagship visual and domain verification

- Rubric Studio, Agent Studio, and Robotics Studio use the AuraOne premium
  Aeonik webfont through `/fonts/proofline-brand.css`.
- The hosted Studio applications proxy font requests to the canonical
  `auraone.ai` origin. No proprietary font binary is committed to the public
  OSS repositories or packed into npm/PyPI artifacts.
- Each production root returned HTTP 200 after deployment. The font stylesheet
  returned `text/css`; `Aeonik-Regular-latin.woff2` returned `font/woff2`.
- Each application exposes working `favicon.ico`, `favicon.svg`, and
  `site.webmanifest` resources.
- Desktop and mobile screenshots were captured from the production domains
  after deployment and inspected for blank output, clipping, incoherent
  overlap, navigation breakage, and typography fallback.
- The desktop layouts retain their evidence-dense workbench model. Mobile
  layouts convert the same workflow into a single-column task path with
  reachable primary actions and persistent product navigation.
- The AuraOne marketing routes use exactly one representative product image
  per flagship Studio. Additional screenshots remain QA evidence only and must
  not become a collage, carousel, or repeated page gallery.

### macOS DMG artifact ledger

These are the current downloadable desktop product artifacts for the accepted
`0.2.0` Studio UI. The later `0.2.1` npm publications and canonical hosted-font
proxy correction do not modify the Tauri application bundle, so they do not
justify a cosmetic DMG rebuild or a false desktop version increment.

| Product | Artifact | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Rubric Studio Open | `Rubric.Studio.Open_0.2.0_aarch64.dmg` | 5,037,556 | `7dcb7de67835947b421089eab5fc244bcd8f75d503ebc7e763921c229c68f23d` |
| Agent Studio Open | `Agent.Studio.Open_0.2.0_aarch64.dmg` | 6,020,828 | `30adbf96b107eb221cce5e07514f4ead7ce32046253f89dd5692f77c52c578ca` |
| Robotics Studio Open | `Robotics.Studio.Open_0.2.0_aarch64.dmg` | 4,968,272 | `b6d08f308c7806df2d67dc34d6d12e9df9f33e135afd61ced1cbb16653f4cf05` |

A future Studio change must rebuild and republish its DMG when it changes
bundled UI, Tauri/Rust code, bundled sidecars, application icons, entitlements,
install behavior, or desktop runtime assets. README-only, package-metadata-only,
and hosted-web-only changes must not create a new DMG.

### npm publication ledger

All three expected Studio packages now exist under the `@auraone` organization.
The registry tarballs were downloaded after publication and their package
metadata, repository links, homepages, and CLI versions were inspected.

| Package | Live version | Registry shasum | Canonical repository |
| --- | ---: | --- | --- |
| `@auraone/rubric-studio` | `0.2.1` | `b339d696466e793824b39d6519b0e19a504f2f0b` | `auraoneai/rubric-studio-open` |
| `@auraone/agent-studio` | `0.2.1` | `a390d30452dc8f940f60a985cee40696647e220a` | `auraoneai/agent-studio-open` |
| `@auraone/robotics-studio` | `0.2.1` | `5cd61c6afff8f54ef5cc9d13d02b87578fa785e2` | `auraoneai/robotics-studio-open` |

### Other audited repository and registry surfaces

The original coordinator, GitHub App, and SDK directories were also reconciled
against their public default branches and registries. Their local primary
checkouts were not reset or cleaned because they contain pre-existing worktree
state; release verification used the public repositories and clean temporary
worktrees.

| Repository | Public `main` | Public package/release state |
| --- | --- | --- |
| `auraoneai/open` | `f52e654d9f7e9de26606dc1a3439fa882785c6e8` before this reconciliation update | `auraone-evalkit==0.3.0`, the 26-project PyPI ledger below, and `@auraone/proofline-oss@0.1.0` |
| `auraoneai/open-studio-platform` | `371356d5cca4cac858e6cf6b2267034580ef0d1a` | Public canonical source for Proofline OSS, Aura IDE Kit, Platform Contracts, Rust contracts, Studio templates, and release controls; CI green and protected `main` |
| `auraoneai/github-app` | `ed2682879b67b0097daf512014e4b4289cd6bff7` | `@auraone/github-app@0.2.0` and GitHub Release `v0.2.0` |
| `auraoneai/sdk-python` | `e1d36afb980ce122f0e8c87b61bb60fe4c2fab3a` | `auraone-sdk==0.2.1`, wheel and sdist, and GitHub Release `v0.2.1` |
| `auraoneai/sdk-typescript` | `dce57461607a5d1c148a5c7aca9528ea8113baa1` | `@auraone/sdk@0.2.0` and GitHub Release `v0.2.0` |
| `auraoneai/evalkit-action` | `ef20b9b7f0d10004d39e5159c5cf36d0b3f13b67` | GitHub Release `v0.2.0`, immutable `v0.2.0` and moving `v0` tags, checksummed Action bundle, and CycloneDX SBOM |
| `auraoneai/evalkit-playground` | `40ae44072efbbfad0d0b613e506f6b57f6362733` | GitHub Release `v0.2.0`, checksummed static build, green rendered-browser CI, and production deployment `dpl_9syi8LxLgvuX5VGK2N4oy3FM2fQm` |
| `auraoneai/rubric-pr-bot` | `89d4fb2537507318a97c152476ba0c5d8ccfc376` | GitHub Release `v0.2.0`, immutable `v0.2.0` and moving `v0` tags, checksummed npm tarball, and CycloneDX SBOM |
| `auraoneai/agent-studio-cookbook` | `b8d75e550caf064961b3034e7d8d8f9ff934f9cc` | Current source-only cookbook, refreshed examples, and metadata verification; no package or binary release is implied |

The final live discovery audit covered 41 offerings backed by 34 unique GitHub
repositories. All 41 repository destinations were reachable. Reviewed
descriptions, canonical AuraOne Open homepages, and product-specific topics
were applied to all 34 repositories and read back through the authenticated
GitHub API; the final audit reports zero repositories with missing topics and
zero generic descriptions. PyPI/npm registries were reachable for 28 of 30
registry-backed records; 27 matched the current target exactly. The one
reachable version mismatch is the intentionally staged
`@auraone/proofline-oss@0.1.1` candidate while npm still serves `0.1.0`. The two
unreachable registry records are the never-published Aura IDE Kit and Platform
Contracts npm packages. GitHub social-preview specifications are generated in
`release/github-repository-metadata.json`, but uploading those images remains a
manual repository-settings task because the GitHub repository API does not
provide a social-preview upload operation.

### PyPI publication ledger

All 26 active AuraOne-owned PyPI projects were queried after publication. Each
listed version has both a wheel (`bdist_wheel`) and source distribution
(`sdist`). No listed project currently requires another version solely to
correct the July 13 release. The next release must be scoped by actual source,
metadata, documentation, or dependency changes.

| PyPI project | Live version | Public artifacts | Release assessment |
| --- | ---: | --- | --- |
| `auraone-agent-studio-open` | `0.2.1` | `auraone_agent_studio_open-0.2.1-py3-none-any.whl`; `auraone_agent_studio_open-0.2.1.tar.gz` | Current headless Agent Studio protocol/CLI release; no additional PyPI write required |
| `failure-gallery` | `0.2.1` | `failure_gallery-0.2.1-py3-none-any.whl`; `failure_gallery-0.2.1.tar.gz` | Current gallery validator/build release |
| `datasheet-ci` | `0.2.1` | `datasheet_ci-0.2.1-py3-none-any.whl`; `datasheet_ci-0.2.1.tar.gz` | Current Python validator release; Action tag/version must remain aligned separately |
| `auraone-evalkit` | `0.3.0` | `auraone_evalkit-0.3.0-py3-none-any.whl`; `auraone_evalkit-0.3.0.tar.gz` | Current local-first evaluation toolkit release |
| `auraone-sdk` | `0.2.1` | `auraone_sdk-0.2.1-py3-none-any.whl`; `auraone_sdk-0.2.1.tar.gz` | Current SDK release and GitHub `v0.2.1` release |
| `rubric-studio` | `0.0.3` | `rubric_studio-0.0.3-py3-none-any.whl`; `rubric_studio-0.0.3.tar.gz` | Current reservation/metadata bridge package; do not mirror the desktop version or imply the Studio UI is installed from PyPI |
| `robostudio-engine` | `0.1.2` | `robostudio_engine-0.1.2-py3-none-any.whl`; `robostudio_engine-0.1.2.tar.gz` | Current headless Robotics Studio engine |
| `prompt-rubric-drift` | `0.1.7` | `prompt_rubric_drift-0.1.7-py3-none-any.whl`; `prompt_rubric_drift-0.1.7.tar.gz` | Current package; Action release remains a separate destination |
| `lerobot-quality-gates` | `0.1.7` | `lerobot_quality_gates-0.1.7-py3-none-any.whl`; `lerobot_quality_gates-0.1.7.tar.gz` | Current package; Action release remains a separate destination |
| `otel-eval-bridge` | `0.1.2` | `otel_eval_bridge-0.1.2-py3-none-any.whl`; `otel_eval_bridge-0.1.2.tar.gz` | Current |
| `vla-robustness-kit` | `0.1.2` | `vla_robustness_kit-0.1.2-py3-none-any.whl`; `vla_robustness_kit-0.1.2.tar.gz` | Current |
| `embodiment-card` | `0.1.2` | `embodiment_card-0.1.2-py3-none-any.whl`; `embodiment_card-0.1.2.tar.gz` | Current |
| `robot-recovery-bench` | `0.1.2` | `robot_recovery_bench-0.1.2-py3-none-any.whl`; `robot_recovery_bench-0.1.2.tar.gz` | Current |
| `agent-trace-card` | `0.1.2` | `agent_trace_card-0.1.2-py3-none-any.whl`; `agent_trace_card-0.1.2.tar.gz` | Current |
| `mcp-risk-linter` | `0.1.6` | `mcp_risk_linter-0.1.6-py3-none-any.whl`; `mcp_risk_linter-0.1.6.tar.gz` | Current package; Action release remains a separate destination |
| `tool-call-replay` | `0.1.1` | `tool_call_replay-0.1.1-py3-none-any.whl`; `tool_call_replay-0.1.1.tar.gz` | Current |
| `a2a-contract-test` | `0.1.5` | `a2a_contract_test-0.1.5-py3-none-any.whl`; `a2a_contract_test-0.1.5.tar.gz` | Current package; Action release remains a separate destination |
| `eval-conformance-suite` | `0.1.2` | `eval_conformance_suite-0.1.2-py3-none-any.whl`; `eval_conformance_suite-0.1.2.tar.gz` | Current |
| `eval-adapter` | `0.1.2` | `eval_adapter-0.1.2-py3-none-any.whl`; `eval_adapter-0.1.2.tar.gz` | Current |
| `eval-run-manifest` | `0.1.2` | `eval_run_manifest-0.1.2-py3-none-any.whl`; `eval_run_manifest-0.1.2.tar.gz` | Current |
| `contamination-audit` | `0.1.2` | `contamination_audit-0.1.2-py3-none-any.whl`; `contamination_audit-0.1.2.tar.gz` | Current |
| `synthetic-disagreement` | `0.1.2` | `synthetic_disagreement-0.1.2-py3-none-any.whl`; `synthetic_disagreement-0.1.2.tar.gz` | Current |
| `judge-bench` | `0.1.2` | `judge_bench-0.1.2-py3-none-any.whl`; `judge_bench-0.1.2.tar.gz` | Current |
| `judge-card` | `0.1.2` | `judge_card-0.1.2-py3-none-any.whl`; `judge_card-0.1.2.tar.gz` | Current |
| `iaa-kit` | `0.1.2` | `iaa_kit-0.1.2-py3-none-any.whl`; `iaa_kit-0.1.2.tar.gz` | Current |
| `rubric-spec` | `0.1.2` | `rubric_spec-0.1.2-py3-none-any.whl`; `rubric_spec-0.1.2.tar.gz` | Current |

The wheel and sdist uploads above were read back from PyPI on July 13-14,
2026. A new PyPI version is required only when package code, dependencies,
runtime behavior, metadata embedded in the distribution, or public
documentation shipped inside the distribution changes. Marketing-site-only,
hosted-font-only, screenshot-only, and unrelated npm changes do not justify
another PyPI version.

### Prepared npm candidates and blocker

The following tarballs passed their package-specific test, typecheck, build,
asset, metadata, and `npm pack` inspection gates. They are not public releases:
npm rejected the write because the available login/token did not satisfy the
organization's enforced two-factor or bypass-enabled granular-token
requirement.

| Package | Tested candidate | Current public npm | Required next action |
| --- | ---: | ---: | --- |
| `@auraone/agent-studio` | `0.2.2` | `0.2.1` | Publish with a current OTP or bypass-enabled granular token, then read back version, shasum, metadata, README, and CLI behavior |
| `@auraone/proofline-oss` | `0.1.1` | `0.1.0` | Publish with valid write authorization and verify the packed OSS-safe token/font assets |
| `@auraone/aura-ide-kit` | `0.2.0` | Not published | Perform the first public npm publication with valid write authorization and verify React/SSR/accessibility exports |
| `@auraone/platform-contracts` | `0.3.0` | Not published | Perform the first public npm publication with valid write authorization and verify runtime-neutral contract exports |

Do not change READMEs, marketing pages, badges, or release evidence to claim
these candidate versions are public until `npm view` returns the exact version
and the downloaded registry tarball passes the same checks.

### Supported and unsupported destinations

The current supported publication set is GitHub source/tags/releases, PyPI
wheels and sdists, npm tarballs, signed/notarized macOS arm64 DMGs, the three
canonical Vercel-backed Studio domains, and the AuraOne Open marketing routes.

Do not claim Homebrew, Winget, VS Code Marketplace, MSI, AppImage, `deb`, `rpm`,
Mac Intel, Windows desktop, or Linux desktop availability unless a real
artifact has been produced, installed in a clean environment, checksummed,
published, and read back from that exact destination.

### Required post-update release, marketing, and SEO task

The following task is intentionally left open. It is the reusable release train
for the next OSS change, not a claim that every package must be republished on
every run.

- [ ] `OSS-NEXT-100` Inventory changed source, documentation, package metadata,
  dependencies, screenshots, desktop assets, and hosted routes across
  AuraFoundry, `auraone-open-public`, the GitHub App, both SDK repositories, and
  the dedicated Rubric, Agent, and Robotics repositories.
- [ ] `OSS-NEXT-101` Map each changed file to its real distribution surfaces.
  Republish only affected PyPI projects, npm packages, GitHub repositories,
  GitHub Releases, DMGs, hosted applications, docs, and marketing routes.
- [ ] `OSS-NEXT-102` Perform a complete marketing rewrite for every affected
  offering. The README, package description, docs entry point, release notes,
  install copy, examples, and AuraOne Open page must clearly state the user,
  problem, outcome, differentiator, proof, privacy/runtime boundary, supported
  install path, and next action.
- [ ] `OSS-NEXT-103` Perform a complete discovery and SEO update for every
  affected offering: search-intent title and description, canonical URL, Open
  Graph/Twitter metadata, structured data, sitemap inclusion, internal links,
  GitHub description/topics/social preview, npm keywords/homepage/repository,
  and PyPI summary/classifiers/project URLs/long description.
- [ ] `OSS-NEXT-104` For Rubric Studio, Agent Studio, and Robotics Studio,
  capture one strong production screenshot that communicates the primary
  workflow. Do not publish collages, six-image galleries, duplicate screens, or
  screenshots that make the product look smaller or less polished than the
  application itself.
- [ ] `OSS-NEXT-105` Rebuild a Studio DMG only when the bundled desktop product
  changed. Verify bundle version, arm64 architecture, code signature,
  notarization, stapling, Gatekeeper, offline mount/install/launch/uninstall,
  checksum, release-note accuracy, and the public download after publication.
- [ ] `OSS-NEXT-106` Build Python wheels and sdists with clean metadata; run
  package tests and `twine check`; install each wheel and sdist in clean
  environments; publish with PyPI trusted publishing; verify the exact version,
  files, metadata, project links, and CLI behavior from public PyPI.
- [ ] `OSS-NEXT-107` Build npm tarballs with `npm pack --dry-run`; inspect the
  packed file list and metadata; run clean-install and CLI checks; publish with
  npm trusted publishing/provenance; verify the exact public version, shasum,
  dist-tag, repository, homepage, README, and executable behavior.
- [ ] `OSS-NEXT-108` Push reviewed source to protected `main`, create immutable
  signed tags, publish matching GitHub Releases and checksums, attach only the
  supported artifacts, and verify every tag, release, asset, and default-branch
  commit from the public repository.
- [ ] `OSS-NEXT-109` Deploy affected hosted applications and marketing routes
  to their existing Vercel projects. Preserve
  `rubric-studio.auraone.ai`, `agentstudio.auraone.ai`, and
  `robotics-studio.auraone.ai`; do not create duplicate throwaway projects.
  Verify root responses, routes, fonts, favicons, manifests, canonical tags,
  social metadata, mobile layouts, and production screenshots.
- [ ] `OSS-NEXT-110` Record one final release ledger containing exact commit
  SHAs, versions, registry hashes, artifact checksums, release URLs, deployment
  IDs, verification timestamps, blocked channels, and rollback steps. Never
  mark the task complete from a local build or an unverified publish command.
- [ ] `OSS-NEXT-111` Revoke any token pasted into a chat, terminal transcript,
  issue, log, or document. Replace long-lived npm/PyPI credentials with trusted
  publishing or narrowly scoped automation credentials; never commit or echo
  secrets while producing release evidence.
- [ ] `OSS-NEXT-112` Reconcile all 26 PyPI projects before each coordinated
  release. Compare source and embedded metadata against the live version,
  produce both a universal wheel and sdist where the project remains
  platform-independent, record SHA-256 checksums, run clean installs from both
  artifacts, and skip publication when no distribution-owned content changed.
- [ ] `OSS-NEXT-113` Close the npm authorization gap for
  `@auraone/agent-studio@0.2.2`, `@auraone/proofline-oss@0.1.1`,
  `@auraone/aura-ide-kit@0.2.0`, and
  `@auraone/platform-contracts@0.3.0`. Use npm trusted publishing where
  possible; otherwise use a narrowly scoped granular token with required 2FA
  policy. After publication, verify public tarballs and update this ledger,
  GitHub releases, READMEs, docs, marketing evidence, and discovery records in
  one reviewed change.

## Historical Blueprint Execution Ledger

This ledger is the implementation and verification record for the blueprint.
An item is checked only after the relevant source changes and focused quality
gates have completed. A delivery-decision item may close only when every
applicable destination is either independently verified live or explicitly
recorded as blocked/not applicable with an owner and next action. Preparing a
workflow is not equivalent to publishing a release, and a blocked destination
must never be presented as available.

- [x] `OSS-000` Audit the committed AuraOne Proofline marketing and dashboard
  design changes and inventory every public offering and distribution surface.
- [x] `OSS-001` Define the OSS-safe semantic color, type, spacing, geometry,
  motion, status, identity, accessibility, and data-boundary contracts.
- [x] `OSS-010` Implement and test the shared Proofline OSS token and component
  foundation, including checks for private fonts and legacy glass styling.
- [x] `OSS-011` Migrate Aura IDE Kit from AuraGlass-era primitives to the
  shared semantic Proofline foundation.
- [x] `OSS-020` Migrate Rubric Studio Open, first run, settings, evidence,
  responsive states, release surfaces, and installer metadata.
- [x] `OSS-021` Migrate Agent Studio Open, first run, settings, traces,
  evidence, responsive states, release surfaces, and installer metadata.
- [x] `OSS-022` Migrate Robotics Studio Open, first run, settings, episode
  review, evidence, responsive states, release surfaces, and installer metadata.
- [x] `OSS-023` Implement and validate flagship updater UX, cross-platform
  release manifests, checksum/signature fields, package-manager metadata, and
  fail-closed unavailable-artifact states.
- [x] `OSS-030` Replace EvalKit Playground's dark-glass interface with the
  responsive Proofline evaluation workspace and explicit workflow states.
- [x] `OSS-031` Consolidate Robotics ReviewKit into one canonical accessible,
  responsive evidence-review implementation.
- [x] `OSS-032` Replace EvalKit's report output with one deterministic,
  self-contained, responsive, printable Proofline evidence template.
- [x] `OSS-033` Consolidate Failure Gallery into one generated source and
  implement searchable, filterable, reproducible evidence UX.
- [x] `OSS-034` Migrate official VS Code webviews and remaining generated
  browser/static artifacts to the shared contract.
- [x] `OSS-040` Build the generated Open catalog, product detail routes,
  Trust Toolkit grouping, SDK/integration routes, and release-evidence states.
- [x] `OSS-041` Add verified product captures and structured metadata that
  identify version, commit, capture date, and data provenance.
- [x] `OSS-050` Upgrade the GitHub App to actionable Check Runs and one
  idempotent, safely escaped pull-request evidence summary.
- [x] `OSS-051` Standardize EvalKit and hosted Python SDK terminal UX for
  human, JSON, and JSONL consumers with no-color and actionable errors.
- [x] `OSS-052` Standardize Python and TypeScript SDK documentation,
  examples, package metadata, and versioned release guidance.
- [x] `OSS-060` Add design lint, accessibility, responsive, reduced-motion,
  print, measured network/layout-shift, package-integrity, and release-manifest
  quality gates.
- [x] `OSS-061` Remove duplicate viewers/templates, hard-coded release URLs,
  private/remote fonts, obsolete marks, and global glass/gradient styling.
- [x] `OSS-070` Prepare coordinated PyPI, npm, GitHub Release, desktop,
  package-manager, marketplace, and hosted-web release automation.
- [x] `OSS-071` Run the cross-repository build, test, lint, package, and
  clean-consumption preflight and attach local evidence.
- [x] `OSS-080` Execute and record the release decision for every applicable
  destination in Section 27, publishing verified channels or explicitly
  recording blocked/not-applicable channels.
- [x] `OSS-090` Redesign Rubric Studio Open around a dominant criterion and
  calibration workspace, remove flat or duplicated chrome, and pass a fresh
  desktop/mobile visual acceptance review.
- [x] `OSS-091` Redesign Agent Studio Open as a compact operator workbench,
  replace promotional and empty capture states with populated trace, replay,
  comparison, and export evidence, and pass desktop/mobile visual acceptance.
- [x] `OSS-092` Redesign Robotics Studio Open as an evidence-first review
  cockpit with real deterministic synthetic sensor scenes, a dominant media
  canvas, compact failure triage, ordered export confirmation, and a
  purpose-built mobile decision path.
- [x] `OSS-093` Regenerate all 26 flagship desktop/mobile product captures,
  synchronize the three route-compatible Robotics wrappers and both provenance
  manifests, and pass cross-product geometry, accessibility, responsive,
  reduced-motion, forced-color, and visual-quality review.
- [x] `OSS-094` Rewrite the marketing and product-positioning system for every
  AuraOne Open offering across the Open catalog, product routes, repository
  READMEs, docs entry points, package pages, release notes, installers, and
  download surfaces. Each offering must state the job, audience, differentiator,
  proof, runtime/data boundary, supported install path, and next action without
  unsupported adoption or availability claims.
- [x] `OSS-095` Complete the cross-channel discovery and technical SEO upgrade
  for all AuraOne Open offerings: evidence-based search-intent mapping; page
  titles and descriptions; canonical, Open Graph, Twitter, sitemap, robots, and
  structured-data coverage; internal docs and product cross-links; GitHub
  descriptions, topics, social-preview specifications, and release metadata;
  npm keywords and package fields; PyPI summaries, classifiers, project URLs,
  and long descriptions; plus measurable install, clone, package, DMG, and
  documentation conversion events. Validate rendered metadata, registry package
  contents, link integrity, mobile performance, and claim truthfulness. The
  GitHub descriptions, canonical homepages, and topics are live; social-preview
  image upload remains a documented manual repository-settings action.
- [x] `OSS-096` Rebuild Rubric Studio Open, Agent Studio Open, and Robotics
  Studio Open macOS DMGs from the final accepted UI source; verify bundle
  version, architecture, offline install and launch, checksum, package contents,
  uninstall behavior, and signing/notarization state; then synchronize the
  verified or explicitly blocked download evidence without silently publishing.
- [x] `OSS-097` Commit and push the coordinated release source, use a signed
  time-bounded publication authorization, and publish the planned PyPI, npm,
  GitHub Release, and notarized macOS DMG destinations.
- [x] `OSS-098` Deploy the AuraOne Open marketing routes and the Rubric Studio,
  Agent Studio, Robotics Studio, and EvalKit Playground browser applications;
  verify canonical domains, production HTTP responses, premium-font delivery,
  and one representative product image per marketing route.
- [x] `OSS-099` Record registry integrity, GitHub Release assets, deployment
  commits, DMG checksums, remaining unsupported channels, and post-publication
  authorization revocation in a committed completion record.

### Historical pre-publication acceptance evidence

This subsection preserves the authoritative local acceptance snapshot that
existed before public writes were authorized. Present-tense blocked statements
inside this historical snapshot are superseded by Section 0.2 and
`release/evidence/publication-completion.json`.

`release/evidence/flagship-uiux-acceptance.json` is the authoritative local
acceptance record for `OSS-090` through `OSS-096`.

- Rubric Studio Open, Agent Studio Open, and Robotics Studio Open each have an
  accepted desktop/mobile visual verdict. Rubric centers the active criterion
  and scoring decision; Agent centers populated trace, replay, comparison, and
  export evidence; Robotics centers a deterministic synthetic sensor scene,
  failure/recovery triage, reviewer decision, and ordered export workflow.
- The final evidence set contains 10 Rubric, 10 Agent, and six Robotics raster
  captures. The website manifest contains 29 records: those 26 captures plus
  three route-compatible Robotics wrappers. All records identify source state,
  viewport, capture date, content hash, and deterministic synthetic-data
  provenance.
- Each flagship website route and README uses exactly one representative
  screenshot. The remaining captures are retained only as versioned QA and
  provenance evidence; no product page or README uses a collage or repeated
  screenshot gallery.
- Official premium typography was used only through a temporary private
  loopback capture boundary backed by `auraone-website/public/fonts`. No private
  font binary was copied into OSS source, npm or PyPI packages, desktop bundles,
  or public repository assets.
- Lighthouse 13.4.0 mobile production-build checks record performance/LCP/CLS
  results of `94 / 2478 ms / 0.01357` for Rubric, `95 / 2421 ms / 0.00009` for
  Agent, and `94 / 2478 ms / 0.01206` for Robotics, all with `0 ms` total
  blocking time. The production Playwright matrix passes 15 checks across 12
  Open routes and three flagship mobile paths.
- The final canonical execute preflight in
  `release/evidence/preflight-execute.json` records `qualityReady: true`,
  `publicationReady: false`, all 60 configured repository quality commands plus
  release-contract validation passing across five coordinated repositories,
  and zero quality failures. `ready` remains false because protected
  publication is intentionally blocked.
- `release/version-surfaces.json` and `npm run versions:verify` align 17
  products across 33 authoritative version files.
- `npm run design:lint` verifies the public UI source inventory, and
  `npm run workflows:lint` records Actionlint in the coordinated command matrix
  across 23 workflow files in the public repository, SDKs, GitHub App, Actions,
  bot, validator, playground, shared packages, Agent Studio, and Failure
  Gallery.
- Marketing and discovery validation covers 41 offerings, 34 website entities,
  193 explicit offering/destination decisions, and seven conversion events
  across the Open catalog, product routes, repository READMEs, docs, npm, PyPI,
  GitHub metadata, installers, and download surfaces. Canonical, Open Graph,
  Twitter, sitemap, robots, structured data, internal links, registry package
  contents, and claim-truthfulness checks pass. GitHub social-preview upload is
  explicitly blocked as an authorized manual repository update, with owner and
  next action recorded.
- Open Studio distribution verification validates three current staged `0.2.0`
  records and preserves the three historical records. The following local
  macOS arm64 artifacts are signed, notarized, stapled, Gatekeeper accepted,
  checksum verified, and offline mount/install/Launch Services
  launch/quit/uninstall tested:
  - `Rubric.Studio.Open_0.2.0_aarch64.dmg`, 5,037,556 bytes, SHA-256
    `7dcb7de67835947b421089eab5fc244bcd8f75d503ebc7e763921c229c68f23d`,
    notary submission `52e973b5-44d7-40a6-8b7c-f2d2dedfc09f`.
  - `Agent.Studio.Open_0.2.0_aarch64.dmg`, 6,020,828 bytes, SHA-256
    `30adbf96b107eb221cce5e07514f4ead7ce32046253f89dd5692f77c52c578ca`,
    notary submission `e571b0f8-0b94-471c-add8-6bb14569a08f`; its bundled
    sidecar is also signed and verified.
  - `Robotics.Studio.Open_0.2.0_aarch64.dmg`, 4,968,272 bytes, SHA-256
    `b6d08f308c7806df2d67dc34d6d12e9df9f33e135afd61ced1cbb16653f4cf05`,
    notary submission `73b6d597-4321-42ec-9dc0-dcca49eaf053`.
- At this pre-publication snapshot, those DMGs were local release evidence
  rather than public downloads. Publication remained blocked until the exact
  reviewed source was committed and pushed, protected authorization granted
  the exact release bindings, and the macOS artifacts were rebuilt or
  byte-compared from that commit.
- `release/evidence/publication-decision.json` is the authoritative historical
  decision record for the pre-publication snapshot across 41 offerings, 193
  explicit offering/destination pairs, and 17 required evidence classes.
- Dirty source is identified as
  `<commit>+worktree.<content-fingerprint>` in the preflight report. That
  identity makes the tested local state distinguishable, but it is correctly
  recorded as non-reproducible until the exact worktree is committed and
  pushed.
- Every repository declares validated `sourceRoots`. Dedicated repositories
  bind their complete worktrees; the AuraOne monorepo binds the four release
  workflows, root dependency manifests, all affected OSS products, and the Open
  catalog and Buying Toolkit source, tests, captures, and token surfaces.
  Contract validation also requires every changed offering's evidence source
  to lie inside one of these boundaries. Unrelated concurrent monorepo work
  cannot invalidate or silently enter this release identity.
- Source identity canonicalizes only Next.js-generated
  `.next*/types/**/*.ts` and `.qa*/types/**/*.ts` entries in the website
  `tsconfig.json`; compiler options, path aliases, and non-generated includes
  remain hashed, so `next build` cannot create false source drift.
- Capture verification is read-only: it derives expected Robotics SVG wrapper
  bytes from the verified desktop WebP captures and fails on any mismatch
  without rewriting the wrapper, website manifest, or evidence mirror. Both
  manifest copies are included in the AuraOne release source boundary.
- All seven registry publication workflows require an exact configured GPG
  signer fingerprint, verify annotated signed tags, attest the exact downloaded
  artifacts, and implement retry-safe publication. Existing npm or PyPI
  versions are accepted only when their registry integrity or filename/digest
  map exactly matches the locally verified artifacts.
- Every registry, GitHub Release, Agent Studio desktop, R2, and updater write is
  operationally gated by `release/publication-authorization.json`. Publishers
  check out `auraoneai/open` at the repository
  `OSS_PUBLICATION_AUTHORIZATION_TAG`, verify that annotated tag against the
  exact release signer, and require a current authorization matching the exact
  repository, clean source commit, package, version, and channel before public
  provenance attestation or publication. The checked-in authorization remains
  blocked and granted no release at the time of this snapshot.
- npm publishers explicitly map stable releases to `latest` and approved
  prerelease identifiers to `alpha`, `beta`, `rc`, `next`, or `canary`;
  unsupported prerelease identifiers fail before publication.
- Agent Studio Open's release path validates 39 release/configuration surfaces,
  signs the MSI before rebuilding and signing the Tauri updater ZIP, verifies
  embedded Authenticode, enforces stable/beta/nightly channel agreement, mirrors
  immutable artifacts and `latest.json` to R2 with byte comparison, checks the
  live updater response, and verifies every manifest artifact URL before a
  draft GitHub Release can advance.
- Private PyPI authentication, `npm whoami`, and authenticated GitHub API probes
  pass. Credential availability is not publication authorization and does not
  override the blocked authorization record.
- At the time of this snapshot, no package, tag, GitHub Release, desktop
  artifact, marketplace listing, or production deployment had been published.

### Historical public release completion

This section supersedes the pre-publication blocked state above. The coordinated
primary release completed on July 13, 2026, and the machine-readable record is
`release/evidence/publication-completion.json`.

**Source and authorization**

- The UI/UX release tags and binary artifacts bind to AuraFoundry commit
  `56bb6329f02b1c9f35be6e43093f0e532e3a11e3`.
- Standalone browser deployment hardening and the final Rubric browser-toolbar
  fit correction were deployed from
  `7c61d05a17d5b5fdd8bf0ab956923f1196617757`. The subsequent flagship README
  release-truth and canonical-domain corrections are on AuraFoundry `main` at
  `abcdcc9847cd270423183b415cb53af2d6612210`.
- Dedicated release commits are `60ad0ab1ad7aa4a62ea0d3be6b7dcf34bd66dc01`
  for EvalKit, `ed2682879b67b0097daf512014e4b4289cd6bff7` for the
  GitHub App, `e1d36afb980ce122f0e8c87b61bb60fe4c2fab3a` for the
  Python SDK, and `dce57461607a5d1c148a5c7aca9528ea8113baa1` for the
  TypeScript SDK.
- Public writes used the signed, exact-source, time-bounded tag
  `oss-publication-authorization-20260713T195025Z`. After verification, the
  checked-in authorization was changed to `revoked`; the signed closure tag is
  `oss-publication-authorization-closed-20260713T203131Z`.

**Registries and GitHub Releases**

- PyPI reports `auraone-evalkit 0.3.0`, `auraone-sdk 0.2.1`,
  `auraone-agent-studio-open 0.2.1`, `failure-gallery 0.2.1`, and
  `datasheet-ci 0.2.1` as the current published versions. The complete
  26-project live-version and artifact ledger is authoritative above.
- npm reports `@auraone/github-app 0.2.0`, `@auraone/sdk 0.2.0`, and
  `@auraone/proofline-oss 0.1.0`; their registry SHA-1 values match the
  verified publication record.
- Eighteen non-draft, non-prerelease GitHub Releases are live: four dedicated
  repository releases and 14 AuraFoundry component releases. The complete tag
  inventory is recorded in `publication-completion.json`.
- Release assets include Python wheels and source distributions, npm tarballs,
  checksums, CycloneDX SBOMs where applicable, and the three notarized macOS
  DMGs.

**Desktop downloads**

- `Rubric.Studio.Open_0.2.0_aarch64.dmg` is live with SHA-256
  `7dcb7de67835947b421089eab5fc244bcd8f75d503ebc7e763921c229c68f23d`.
- `Agent.Studio.Open_0.2.0_aarch64.dmg` is live with SHA-256
  `30adbf96b107eb221cce5e07514f4ead7ce32046253f89dd5692f77c52c578ca`.
- `Robotics.Studio.Open_0.2.0_aarch64.dmg` is live with SHA-256
  `b6d08f308c7806df2d67dc34d6d12e9df9f33e135afd61ced1cbb16653f4cf05`.
- All three artifacts were byte-verified after GitHub upload and retain the
  signed, notarized, stapled, Gatekeeper-accepted, offline-install evidence
  described in Section 0.1.

**Production web**

- The AuraOne marketing deployment `dpl_EsbCAf81Cfgvrd8i393aXymaWSmL`
  serves `auraone.ai` and `www.auraone.ai`. The three flagship Open routes and
  `/fonts/proofline-brand.css` return HTTP 200.
- Rubric Studio Open deployment `dpl_HKXYjA2hCdmhXpc4fDnQN5BA9qTh` is live
  at `rubric-studio.auraone.ai`.
- Agent Studio Open deployment `dpl_5Lyh41P8iKjc7bFUTPbqefWaU86m` is live
  at `agentstudio.auraone.ai`.
- Robotics Studio Open deployment `dpl_7F9i8t4BEiaAJppydb4qk6j6DPjs` is live
  at `robotics-studio.auraone.ai`.
- EvalKit Playground deployment `dpl_9syi8LxLgvuX5VGK2N4oy3FM2fQm` is live
  at `playground.auraone.ai` and `evalkit-playground.vercel.app`.
- The obsolete Vercel projects `rubric-studio-open-docs-root`,
  `agent-studio-open-demo`, `auraone-rubric-studio-docs`,
  `auraone-agent-studio-docs`, and `auraone-robotics-studio-docs` were deleted.
  The remaining canonical Studio projects are `rubric-studio-open-editor`,
  `agent-studio-open`, and `robotics-studio`; there is no
  `dist-kappa-two-91` project in the pre-cleanup 67-project account inventory.
- Fresh production Playwright screenshots were reviewed for Rubric, Agent,
  Robotics, and EvalKit. Rubric's crowded browser toolbar at 1440 px was found
  during this review, corrected, and revalidated with the full responsive
  geometry matrix, browser smoke test, production build, and a second live
  screenshot. Agent and Robotics retain their dense operator-workbench and
  evidence-cockpit designs without card or screenshot overload.
- Each flagship marketing page and README continues to use exactly one
  representative screenshot. The larger capture set remains QA evidence only.
  Premium fonts are served through the website boundary and are not bundled as
  private font binaries in OSS source, packages, or DMGs.

**Explicitly blocked secondary channels**

- Windows MSI and Winget remain unpublished pending Windows signing,
  installation, update, and uninstall verification.
- Linux AppImage, deb, and rpm remain unpublished pending Linux-native package
  and runtime verification.
- Homebrew, VS Code Marketplace, GitHub Marketplace, desktop auto-updater/R2,
  and GitHub social-preview publication remain separate maintainer-owned tasks.
- No unavailable secondary channel is presented as live in the completion
  record. The release plan is `verified` because every primary publication was
  independently checked and every unsupported destination has an explicit
  reason and next owner boundary.

## 1. Executive Decision

AuraOne Open should adopt the same product philosophy as the upgraded
AuraFoundry experience:

**Open tools should make source, work, review, decision, release, and outcome
inspectable.**

The OSS redesign must not be a superficial recolor. It must replace the
current mix of dark glass, cyan-violet gradients, bespoke studio themes,
one-off inline styles, oversized cards, and inconsistent marks with a shared,
light-first operating system for technical evidence.

The redesign has four system goals:

1. **One AuraOne identity:** every official tool is visibly part of AuraOne
   without erasing the tool's job or open-source independence.
2. **One evidence grammar:** status, provenance, limitations, release state,
   local/network boundaries, and next actions use the same vocabulary.
3. **One OSS-safe token layer:** public source uses redistributable fonts and
   assets; official AuraOne builds may inject licensed brand fonts only through
   an approved private build boundary.
4. **One release experience:** website, GitHub release, package registry,
   installer, first run, generated artifact, and in-product update state tell
   the same versioned story.

### Required outcome

A user should be able to move from `auraone.ai/open` to source, package,
download, first run, local workflow, generated evidence, and optional AuraOne
handoff without encountering a different visual identity or contradictory
release claim at each step.

## 2. Reference Design Upgrade Analysis

The primary committed design sources used for this analysis are:

- `DESIGN.md`;
- `docs/design/AURAONE_FINAL_MAKEOVER.md`;
- `docs/design/makeover/decision-log.md`;
- `apps/src/design-system/foundation/tokens.css`;
- `apps/src/design-system/proofline/**`;
- `apps/src/design-system/modern/tokens.ts`;
- `auraone-website/DESIGN.md`;
- `auraone-website/src/styles/proofline-theme.css`;
- `auraone-website/src/styles/makeover.css`;
- `auraone-website/src/components/home/HomepageHero.tsx`;
- `auraone-website/src/components/home/HomepageProductAtlas.tsx`;
- `auraone-website/src/app/open/**`.

Legacy files remain in the repository for compatibility. In particular,
`auraone-website/src/styles/design-tokens.css` still contains dark/glass-era
tokens and is not the authoritative target for the OSS redesign.

### 2.1 Brand and product-positioning change

The AuraOne makeover moves from an atmosphere-led AI brand to an evidence-led
operating platform.

The new public category statement is:

> AuraOne is the operating platform for AI work.

The approved product model is:

| Level | Approved model |
| --- | --- |
| Brand | AuraOne |
| Product families | Human Data, Models, Compute, App Data |
| Adoption and proof | Open Source, Proof, Resources |
| Role areas | Worker, Admin |

Open Source is not a fifth enterprise product family. It is the inspectable
adoption and proof layer across AuraOne's product system.

### 2.2 Visual-direction change

The reference system replaces:

- dark, near-black global canvases;
- glass panels and backdrop blur;
- glow, ambient orbs, bokeh, and decorative gradients;
- equal-priority dashboard cards;
- all-caps technical noise;
- status encoded only by colored dots;
- generic AI imagery and abstract interface previews;
- separate persona color systems;
- boxed `A1` and legacy Aura Foundry glow marks.

It introduces:

- a cool, light-first canvas;
- solid white and inset-gray work surfaces;
- quiet borders and limited elevation;
- compact radii of 8 px or less for ordinary product UI;
- direct page regions instead of cards inside cards;
- one dominant work area per screen;
- task-based navigation and explicit product context;
- sentence-case labels and compact data hierarchy;
- real evidence, real outputs, real workflows, and real product captures;
- the Proofline sequence: Source, Work, Review, Decision, Release, Outcome;
- explicit state labels, icons, timestamps, owners, evidence, and next actions;
- a new Proof Fold identity representing four product records folding into one
  governed decision spine.

### 2.3 Marketing-site change

The upgraded marketing system is not a conventional card-grid SaaS site. Its
core changes are:

1. **Literal category hero.** The product name and category are visible in the
   first viewport.
2. **Product taxonomy before feature taxonomy.** Human Data, Models, Compute,
   and App Data are the primary discovery model.
3. **Inspectable product evidence.** Product pages use captures, artifacts,
   release records, criteria, and workflow states instead of decorative
   dashboards.
4. **Full-width bands.** Sections are unframed page regions with constrained
   content, not floating cards on a decorative background.
5. **Claim governance.** Quantitative or comparative claims require source,
   owner, scope, date, and approval state.
6. **Honest readiness.** Source availability, package availability, release
   verification, hosted-preview state, and support are separate facts.
7. **Shared shell.** One light header, one Products menu, one mobile hierarchy,
   one search model, and one footer.
8. **Performance as design.** Media, font, bundle, and route budgets are part
   of the visual system.

### 2.4 Dashboard and product-UI change

The upgraded authenticated platform uses a work-first composition:

- stable organization and product shell;
- page title, purpose, status, and actions in one page header;
- tabs or segmented controls for actual modes;
- filters and saved views close to the data they affect;
- tables for exact values and repeated operational records;
- inspectors for selected-record detail;
- explicit universal states for loading, empty, no results, error, offline,
  stale, partial data, unavailable, and permission denied;
- charts only for comparison, change, distribution, or relationships;
- tabular or textual alternatives for every chart;
- 44 px mobile touch targets;
- restrained desktop density using 36, 44, and 52 px table rows;
- no product-level permanent rail inside the shared platform shell;
- compatibility renderers for old `Glass*` APIs while visual behavior becomes
  solid and token-based.

### 2.5 Latest-commit normalization

The final reference commit specifically normalizes mobile and compatibility
behavior:

- ordinary cards are capped at an 8 px radius;
- buttons become 44 px high on mobile while retaining denser desktop heights;
- icon buttons become 44 by 44 px on mobile;
- inputs and clear controls become 44 px high on mobile;
- literal `text-white` usage is replaced with semantic inverse-text tokens;
- Proofline primitives and legacy Glass compatibility renderers converge on
  the same semantic token contract;
- mobile route captures and route-ledger coverage are expanded.

This matters for OSS because the desktop tools currently assume wide fixed
windows, while browser viewers and playgrounds need a credible narrow-screen
mode.

## 3. Canonical Proofline Foundations

### 3.1 Reference platform tokens

The committed platform foundation defines the following core values:

| Role | Value |
| --- | --- |
| Canvas | `#f5f7fa` |
| Canvas subtle | `#f8fafc` |
| Surface | `#ffffff` |
| Inset surface | `#eef2f6` |
| Hover surface | `#f0f4f7` |
| Pressed surface | `#e5ebf0` |
| Selected surface | `#dceff1` |
| Primary text | `#101820` |
| Secondary text | `#3f4b59` |
| Muted text | `#626f7e` |
| Disabled text | `#8a95a3` |
| Brand | `#007582` |
| Brand hover | `#006a75` |
| Brand soft | `#dceff1` |
| Focus | `#0b6cff` |
| Border subtle | `#e3e8ee` |
| Border default | `#d5dde6` |
| Border strong | `#b8c3cf` |
| Success | `#1e7a52` |
| Info | `#1769a6` |
| Review | `#6d4dc1` |
| Warning | `#8b5b00` |
| Danger | `#b4233c` |
| Blocked | `#5f6b7a` |

Product-family colors communicate context, never status:

| Family | Accent | Soft |
| --- | --- | --- |
| Human Data | `#a33955` | `#f5e5ea` |
| Models | `#4f46c6` | `#e9e8fa` |
| Compute | `#1769a6` | `#e3eef7` |
| App Data | `#14785f` | `#e2f0eb` |

### 3.2 Spacing, geometry, and motion

- Spacing uses a 4 px base.
- Ordinary controls and compact surfaces use 4, 6, or 8 px radii.
- Major contained tools may use 12 px, but marketing and dashboard surfaces
  should not drift back to 18-28 px glass cards.
- Standard shell dimensions:
  - expanded sidebar: 240 px;
  - collapsed sidebar: 64 px;
  - desktop header: 56 px;
  - mobile header: 52 px;
  - desktop content padding: 24 px;
  - mobile content padding: 16 px;
  - inspector: 360 px;
  - tab row: 44 px;
  - desktop control: 40 px;
  - mobile control: 44 px.
- Motion uses 80, 180, 240, and 400 ms tiers.
- Motion is limited to transform and opacity where possible.
- Reduced-motion mode removes nonessential animation.

### 3.3 Typography

The private AuraOne system uses:

- Aeonik for brand and display;
- Whitney for body and product UI;
- Whitney Numeric for metrics;
- IBM Plex Mono for code;
- GT Sectra only for restricted editorial/report use.

Public OSS source must not copy licensed font files from the private AuraOne
repository.

The OSS typography contract should be:

| Role | Public-source default | Official AuraOne build override |
| --- | --- | --- |
| Display | system UI sans, `Segoe UI`, Arial | Aeonik |
| UI/body | system UI sans, `Segoe UI`, Arial | Whitney |
| Numeric | UI fallback with tabular numerals | Whitney Numeric |
| Code | `ui-monospace`, `SFMono-Regular`, Consolas | IBM Plex Mono |
| Editorial | `Source Serif 4`, Georgia | Approved report-only family |

Required rules:

- public source exposes only generic `--pl-official-font-*` override tokens and
  an optional `VITE_AURAONE_OFFICIAL_STYLE_URL`; it does not name, copy, or
  package private font binaries;
- official hosted and capture builds may load the approved stylesheet from the
  private `auraone-website/public/fonts` boundary;
- deterministic product capture must serve that private boundary through a
  temporary loopback server, record its SHA-256 digest, and wait for the
  stylesheet and fonts before taking a screenshot;
- desktop, DMG, offline, fork, and ordinary public-source builds must work
  without the override URL and must make no default remote font request;
- no remote Google Fonts dependency in desktop products;
- vend only fonts with a redistribution-compatible license;
- no proprietary font binary in public git history, npm, PyPI, VSIX, DMG
  source payloads, or web assets without explicit legal approval;
- use `font-variant-numeric: tabular-nums` for comparable values;
- do not set an entire IDE in monospace;
- keep body text at 14 px or larger;
- use zero letter spacing for ordinary text;
- reserve display type for product name, page title, or first-run identity.

## 4. OSS-Safe Shared Design Architecture

### 4.1 Create one shared package

Create an OSS-safe design package under:

`/Users/gurbakshchahal/AuraOne/opensource/open-studio-platform/packages/proofline-oss`

Implemented package name:

`@auraone/proofline-oss`

It should contain:

```text
packages/proofline-oss/
  package.json
  README.md
  src/
    index.ts
    tokens.css
    themes.css
    typography.css
    status.ts
    icons.ts
    react/
      actions.tsx
      forms.tsx
      navigation.tsx
      surfaces.tsx
      states.tsx
      data.tsx
      evidence.tsx
      overlays.tsx
      charts.tsx
  tests/
    tokens.test.ts
    contrast.test.ts
    components.test.tsx
    no-private-fonts.test.ts
```

The package should be usable in:

- Tauri/Vite applications;
- standalone React/Vite viewers;
- browser playgrounds;
- VS Code webviews;
- static HTML through emitted CSS;
- generated HTML reports through a compact embedded stylesheet.

### 4.2 Do not fork the token system per tool

The current studios each define their own token language:

- Agent Studio: cream canvas, serif/mono identity, gradients, noise, and
  custom `--as-*` variables;
- Robotics Studio: dark-first `--accent-*`, glass-like panels, and gradient
  product mark;
- Rubric Studio: a closer light system, but separate `--rs-*`, legacy cyan
  naming, multiple visual modes, and extensive one-off CSS;
- Aura IDE Kit: dark-first `--ag-*` glass tokens and large radii;
- EvalKit Playground: dark glass, radial gradients, 18 px cards;
- Failure Gallery: dark glass marketing page;
- ReviewKit v2: inline style objects and hard-coded colors.

These should map to one semantic contract:

```css
--pl-canvas
--pl-canvas-subtle
--pl-surface
--pl-surface-inset
--pl-surface-hover
--pl-surface-pressed
--pl-surface-selected
--pl-text-primary
--pl-text-secondary
--pl-text-muted
--pl-text-disabled
--pl-text-inverse
--pl-border-subtle
--pl-border-default
--pl-border-strong
--pl-brand
--pl-brand-hover
--pl-brand-soft
--pl-focus
--pl-state-success
--pl-state-info
--pl-state-review
--pl-state-warning
--pl-state-danger
--pl-state-blocked
--pl-chart-1 through --pl-chart-8
--pl-radius-control
--pl-radius-surface
--pl-shadow-1 through --pl-shadow-3
--pl-control-height
--pl-control-height-mobile
```

Legacy aliases may remain for one release, but new UI must not introduce new
tool-specific color primitives.

### 4.3 Shared component contract

The shared OSS kit should mirror the proven platform categories:

| Module | Required primitives |
| --- | --- |
| Actions | Button, LinkButton, IconButton, ButtonGroup, MenuButton |
| Forms | Field, Input, Select, TextArea, Checkbox, Switch, FilePicker |
| Navigation | Breadcrumbs, Tabs, SegmentedControl, Menu, CommandPalette |
| Surfaces | AppShell, PageHeader, Section, Surface, Toolbar, Inspector |
| States | Status, Alert, Skeleton, UniversalState |
| Data | DataTable, FilterBar, SavedViewControl, Pagination |
| Evidence | Proofline, EvidencePacket, DecisionGate, AuditTimeline |
| Charts | ChartFrame, Legend, data-table alternative |
| Overlays | Dialog, Drawer, Popover, Tooltip |

All icon-only actions require:

- an accessible name;
- a tooltip;
- a 44 by 44 px mobile hit target;
- visible keyboard focus;
- no layout shift on hover or loading.

## 5. Public Offering Inventory

### 5.1 Flagship desktop and browser products

| Offering | Primary surfaces | Current state |
| --- | --- | --- |
| Rubric Studio Open | React/Vite, Tauri, DMG, hosted browser preview, VS Code extension | Light-first but independently branded and heavily custom |
| Agent Studio Open | React/Vite, Tauri, DMG, hosted browser/demo, VS Code extension, CLI | Light cream/serif/mono system with decorative gradients and noise |
| Robotics Studio Open | React/Vite, Tauri, DMG, Linux/Windows bundles | Dark-first dense IDE with separate gradient identity |
| EvalKit Playground | React/Vite browser app | Dark glass workspace with nested cards |
| Robotics ReviewKit | Legacy static viewer and React v2 viewer | Split implementations and inconsistent styling |
| Failure Gallery | Static marketing/gallery HTML and AuraOne website route | Dark glass presentation |
| Rubric PR Bot | GitHub App/check UI and public static page | Separate GitHub-native and static surfaces |

### 5.2 Local tools, CI tools, schemas, and artifact generators

The reference monorepo also exposes:

- AuraOne EvalKit;
- rubric-spec;
- iaa-kit;
- judge-bench;
- judge-card;
- eval-adapter;
- eval-conformance-suite;
- eval-run-manifest;
- evalkit-action;
- datasheet-ci;
- contamination-audit;
- prompt-rubric-drift;
- synthetic-disagreement;
- agent-trace-card;
- tool-call-replay;
- otel-eval-bridge;
- mcp-risk-linter;
- a2a-contract-test;
- embodiment-card;
- lerobot-quality-gates;
- robot-recovery-bench;
- vla-robustness-kit;
- robostudio-engine;
- Agent Studio Cookbook;
- Open Studio Platform;
- Buying Toolkit and public writing resources.

Most of these do not need a standalone app. They do need consistent:

- README hierarchy;
- command examples;
- terminal output;
- HTML/Markdown artifacts;
- badges;
- GitHub summaries;
- limitation and data-boundary notices;
- links into the Open catalog;
- release metadata.

### 5.3 Public repositories reviewed

| Repository | Latest reviewed commit | Direct visual surface |
| --- | --- | --- |
| `auraone-open-public` | `f142537`, July 7, 2026 | EvalKit HTML reports, Robotics ReviewKit static viewer, React v2 viewer |
| `auraoneai-github-app` | `fdbb292`, July 7, 2026 | Commit status, PR comment, README |
| `auraoneai-sdk-python` | `87a84d7`, July 7, 2026 | CLI output, README, docs examples |
| `auraoneai-sdk-typescript` | `e4a9a10`, July 7, 2026 | README, package documentation, generated developer examples |

## 6. Marketing Website Plan

### 6.1 Open catalog

The current `/open` page already follows important Proofline principles:

- literal Open Source positioning;
- tool comparison table;
- explicit license, data boundary, and release-evidence columns;
- source and release treated as separate facts;
- release-evidence Proofline.

It should be extended into the canonical OSS release catalog.

Required additions:

1. Replace static release prose with a generated release manifest.
2. Add verified states for:
   - source available;
   - package published;
   - browser preview available;
   - macOS signed;
   - macOS notarized;
   - checksum published;
   - Windows package available;
   - Linux package available;
   - current maintainer;
   - security policy;
   - support boundary.
3. Add version and verification date to every tool row.
4. Add filters for product type, runtime, license, platform, and release state.
5. Add a compare view that remains a table on desktop and record list on
   mobile.
6. Add a direct path to install only when the release manifest passes.
7. Add a "Build from source" action when binary proof is incomplete.
8. Make stale release evidence visually explicit instead of silently falling
   back to generic copy.

### 6.2 Product detail pages

Rubric Studio, Agent Studio, and Robotics Studio pages should share this
template:

1. Literal hero with product name.
2. One-sentence job statement.
3. Platform and release status.
4. Primary action selected from:
   - Download verified build;
   - Open browser preview;
   - Build from source.
5. Secondary action: inspect source.
6. Data-boundary summary.
7. Workflow Proofline.
8. Real product captures with version and capture date.
9. Inputs and outputs.
10. Local, optional-network, and hosted behavior table.
11. Release integrity block.
12. System requirements.
13. First-run path.
14. Documentation and troubleshooting.
15. Limitations and non-claims.

Do not use a marketing hero made from an abstract studio logo or gradient.
Use a legible, current product capture or a meaningful workflow composition.

### 6.3 Trust Toolkit page

The Trust Toolkit should not appear as one undifferentiated list of repositories.
Group tools by job:

| Job | Tools |
| --- | --- |
| Define | rubric-spec, judge-card, datasheet-ci, embodiment-card |
| Validate | EvalKit, mcp-risk-linter, a2a-contract-test |
| Measure | iaa-kit, judge-bench, contamination-audit |
| Compare | prompt-rubric-drift, eval-adapter, eval-conformance-suite |
| Reproduce | eval-run-manifest, tool-call-replay, agent-trace-card |
| Operate in CI | evalkit-action, datasheet-ci, Rubric PR Bot |
| Review robotics | ReviewKit, LeRobot gates, recovery and robustness tools |

Each tool needs:

- job statement;
- input;
- output;
- install command;
- license;
- runtime/network boundary;
- maturity state;
- latest verified version;
- source;
- docs;
- example artifact.

### 6.4 SDK and GitHub App pages

Create or refresh developer pages for:

- Python SDK;
- TypeScript SDK;
- AuraOne GitHub App;
- EvalKit CLI;
- EvalKit Playground.

These pages should use code as evidence, not decoration:

- language tabs;
- copyable install commands;
- a working quickstart;
- expected output;
- authentication and data-movement boundary;
- error example;
- version and runtime requirements;
- one path to local OSS and one path to hosted AuraOne;
- no ambiguous mixing of `aura`, `auraone-sdk`, `auraone-evalkit`, and
  `@auraone/sdk`.

### 6.5 Marketing assets

Create a capture manifest for every OSS image:

```json
{
  "product": "Rubric Studio Open",
  "version": "0.1.0",
  "surface": "desktop",
  "view": "calibration",
  "viewport": "1440x960",
  "theme": "light",
  "data": "synthetic",
  "capturedAt": "2026-07-13",
  "sourceCommit": "<sha>",
  "alt": "<purposeful description>"
}
```

Required capture families:

- first run;
- main workbench;
- selected record and inspector;
- error state;
- empty state;
- export/release state;
- settings and data movement;
- narrow desktop;
- browser/tablet where supported.

The complete capture family is QA and release evidence, not a marketing
gallery. Public product pages must:

- select the strongest representative workflow state for the product;
- render exactly one product screenshot, once, in the hero;
- use the matching portrait capture through `<picture>` on mobile;
- never repeat that screenshot below the hero;
- never present the complete evidence set as a collage, carousel, tiled
  gallery, or sequence of near-duplicate views;
- let product copy, workflow, artifacts, and release evidence explain the
  remaining capabilities.

The selected flagship marketing states are:

- Rubric Studio Open: populated scoring preview;
- Agent Studio Open: populated tool-trace inspector;
- Robotics Studio Open: synchronized episode review.

## 7. Desktop and DMG Experience

### 7.1 Shared desktop shell

Rubric Studio, Agent Studio, and Robotics Studio must share:

- canonical AuraOne Proof Fold mark;
- product name treatment;
- menu and command palette behavior;
- update state;
- local/network status;
- telemetry and crash-reporting state;
- project/dataset/session identity;
- help and documentation access;
- status bar vocabulary;
- first-run structure;
- error and recovery patterns;
- about dialog;
- release version and build identity.

The shell must remain product-dense. It should not become a marketing layout.

### 7.2 macOS DMG visual design

The current Tauri configurations target DMG but do not define a coherent
cross-product install presentation.

For all three DMGs:

- use one Finder-window layout;
- provide the app icon on the left and Applications alias on the right;
- use a quiet light background with the product name and one short instruction;
- avoid gradients, glow, glass, screenshots, and legal paragraphs in the DMG;
- include accessible icon contrast at 16, 32, 128, 256, 512, and 1024 px;
- use the AuraOne mark as the family signal and a restrained product glyph as
  the product differentiator;
- ensure mounted-volume names are consistent;
- ensure file names use one convention:
  `AuraOne.<Product>.Open_<version>_<arch>.dmg`;
- publish SHA-256, signature, notarization result, build commit, and minimum OS;
- link the website download action to a manifest, not directly to a guessed
  filename.

### 7.3 First-run flow

Every desktop application should use a maximum four-step first run:

1. **Choose local input:** open project, trace, rubric, or dataset; or use a
   bundled synthetic sample.
2. **Confirm data boundary:** local-only default, optional network/provider
   connections, telemetry off by default.
3. **Run the primary workflow:** author, replay, review, or validate.
4. **Export evidence:** local artifact first; AuraOne handoff remains explicit.

The first-run experience must:

- be dismissible;
- be recoverable from Help;
- avoid a modal carousel;
- preserve keyboard order;
- expose sample-data status;
- never require an AuraOne account for the open local workflow.

### 7.4 Update UX

Updater states should be standardized:

- checking;
- current;
- update available;
- downloading;
- ready to restart;
- failed;
- unsupported;
- signature invalid.

Each state needs text, icon, version, and action. A colored dot alone is not
sufficient.

## 8. Rubric Studio Open

Sections 8 through 13 retain the pre-migration product audit that drove the
implementation. Subsections labeled "Baseline gaps addressed" describe the
starting source state; the execution ledger and evidence in Section 0 describe
the current verified state.

### 8.1 Current strengths

- Light-first base already exists.
- Product has a real workbench with authoring, preview, calibration, diff,
  export, settings, first run, dialogs, and VS Code support.
- Controls generally use compact radii.
- Tauri packaging, updater, deep links, accessibility tests, browser tests,
  and design tests exist.
- The workflow already fits Proofline well: source rubric, authoring, review,
  calibration, decision, export.

### 8.2 Baseline gaps addressed

- Token names and values are independent from Proofline.
- `cyan` remains the primary semantic name even where the color is blue.
- `redesign.css` and `styles.css` create overlapping systems.
- Some report and metric typography is stylistically separate.
- Pill badges and cards are overused.
- The source supports light, dark, and high-contrast themes, but official
  marketing capture and first-run default are not governed by one contract.
- Product identity and AuraOne identity are not aligned with the new mark.
- The browser preview contains a hard-coded DMG URL instead of consuming
  verified release data.

### 8.3 Required changes

Files:

- `opensource/rubric-studio-open/src/App.tsx`
- `opensource/rubric-studio-open/src/styles.css`
- `opensource/rubric-studio-open/src/redesign.css`
- `opensource/rubric-studio-open/src/reference-fonts.css`
- `opensource/rubric-studio-open/src/components/**`
- `opensource/rubric-studio-open/src-tauri/tauri.conf.json`
- `opensource/rubric-studio-open/vscode-extension/**`

Actions:

1. Import `@auraone/proofline-oss`.
2. Replace primitive `--rs-*` color values with semantic aliases.
3. Merge the two visual stylesheets into component and layout layers.
4. Make the authoring workspace the dominant region.
5. Move project health, validation, and selected-criterion detail into one
   inspector contract.
6. Use a table for calibration values and preserve a chart only when it adds
   comparison or distribution.
7. Represent diff severity with state label, icon, and explanation.
8. Turn export into a release-evidence workspace:
   - artifact;
   - schema/version;
   - validation;
   - limitations;
   - checksum;
   - destination.
9. Replace the hard-coded DMG URL with a release-manifest client.
10. Use the canonical first-run flow.
11. Update VS Code webview styles from the same tokens.
12. Add visual tests for authoring, calibration, diff, export, first run,
    browser preview, dark exception, and high contrast.

## 9. Agent Studio Open

### 9.1 Current strengths

- Light-first default.
- Strong local-first product boundary.
- Substantial command palette, trace, replay, compare, provider, settings,
  telemetry, export, and error-state functionality.
- Browser demo, desktop build, VS Code extension, CLI, and packaged resources
  exist.
- Product naturally maps to evidence: connection, manifest, run, trace,
  replay, comparison, regression artifact.

### 9.2 Baseline gaps addressed

- The visual system uses cream/beige canvas, serif headings, and monospace for
  almost the entire UI.
- Decorative radial gradients, noise, and background grids conflict with the
  Proofline direction.
- Product identity uses a framed image mark rather than the canonical AuraOne
  mark.
- The 260 px fixed sidebar and desktop-first layout need narrow-window behavior.
- Status, context chips, provider state, health, and notices use separate local
  vocabularies.
- Many local helper components duplicate the intended shared OSS kit.
- Google Fonts are loaded remotely, which is inappropriate for reliable
  offline desktop behavior.

### 9.3 Required changes

Files:

- `opensource/agent-studio-open/app/src/App.tsx`
- `opensource/agent-studio-open/app/src/App.css`
- `opensource/agent-studio-open/app/src/aura-ide-kit.css`
- `opensource/agent-studio-open/desktop/src-tauri/tauri.conf.json`
- `opensource/agent-studio-open/vscode/**`
- `opensource/agent-studio-open/cli/**`

Actions:

1. Remove remote font imports.
2. Replace beige canvas with canonical cool canvas.
3. Use sans for UI and body; reserve mono for code, IDs, paths, logs, and
   shortcuts.
4. Remove decorative noise, radial background atmosphere, and grid wallpaper.
5. Replace framed app-image identity with AuraOne mark plus product name.
6. Map Connection, Traces, Replay, Compare, and Ship into the Proofline flow.
7. Keep code/log viewers as approved dark contrast islands.
8. Convert context chips into explicit key-value metadata or statuses.
9. Use one selected-trace inspector rather than multiple equal-priority panels.
10. Add collapsible sidebar behavior below 1180 px.
11. Add bottom-sheet or full-screen inspector behavior below 820 px for the
    browser demo.
12. Standardize provider-key states and network boundary notices.
13. Make export artifacts show source trace, replay state, regression result,
    checksum, and destination.
14. Update the command palette, status bar, VS Code webview, and CLI text to
    share labels.

## 10. Robotics Studio Open

### 10.1 Current strengths

- Dense, functional desktop IDE with browse, scrub, failure, compare, VLA
  probe, sensor QA, export, and settings modes.
- Real data-workbench structure with left navigation, central work area, and
  context rail.
- Strong keyboard and command coverage.
- Tauri packaging targets macOS, Windows, and Linux.
- Product already distinguishes datasets, sensors, failures, QA, readiness,
  and export.

### 10.2 Baseline gaps addressed

- Dark mode is the initial state.
- The UI uses global gradients, glass-like translucent panels, glow rings, and
  a custom cyan-green-yellow gradient logo.
- Product status relies heavily on colored dots.
- The primary action "Send to AuraOne Programs" is visually dominant before
  the local review/export workflow is complete.
- Fixed minimum width of 1120 px and three-column layout limit smaller laptop
  and windowed use.
- Local token system and status colors do not match Proofline.
- Several views are presented as tabs even when some are workflow steps or
  tools.

### 10.3 Required changes

Files:

- `opensource/robotics-studio/src/App.tsx`
- `opensource/robotics-studio/src/styles.css`
- `opensource/robotics-studio/src-tauri/tauri.conf.json`
- `opensource/robotics-studio/src/components/**` when extracted
- `opensource/robostudio-engine/**` generated artifacts
- `opensource/robotics-reviewkit/**` linked viewer surfaces

Actions:

1. Set light mode as the first-run and server/browser default.
2. Keep dark mode as an explicit media-inspection mode, not the global default.
3. Replace the gradient RS mark with AuraOne family identity and a restrained
   robotics glyph.
4. Convert status dots to icon-plus-label statuses.
5. Keep Browse, Review/Scrub, Failures, Compare, QA, and Export as primary
   modes; move Probe and Settings into Tools and app settings where appropriate.
6. Make episode media the dominant work area.
7. Use the right inspector for selected episode, sensors, labels, QA, and
   review decision.
8. Move dataset-level health above the episode table or into a compact summary,
   not a permanent equal-priority card grid.
9. Change the hosted handoff to a secondary explicit destination in Export.
10. Add layouts:
    - wide: sidebar, work area, inspector;
    - medium: collapsed sidebar, work area, inspector drawer;
    - narrow: work area with modal/drawer navigation and inspector.
11. Reduce Tauri minimum width after responsive validation.
12. Add a media dark-surface token that preserves semantic status colors.
13. Add ordered text/table alternatives for timeline, sensor, and cluster
    visualizations.
14. Align export manifests and embodiment cards with the shared generated
    artifact design.

## 11. EvalKit Playground

### 11.1 Baseline gaps addressed

The playground is the clearest legacy visual mismatch:

- dark global canvas;
- multiple radial gradients;
- grid wallpaper;
- glass panels and blur;
- 18 px radii;
- cards inside cards;
- boxed `A` brand mark;
- separate playground marketing strip inside the workbench;
- status encoded through decorative color;
- three competing visual priorities: scenario rail, editor cards, and result
  cards.

### 11.2 New workspace

The first screen should be the usable scoring workspace:

- compact AuraOne/Open header;
- example selector;
- rubric editor;
- responses editor;
- results;
- run action;
- local/browser runtime status;
- share action.

Recommended composition:

```text
Header: identity | example | runtime | share | Run
Main:
  left 42%: rubric and responses tabs
  right 58%: results, diagnostics, evidence
Footer/status: local-only disclosure | EvalKit version | permalink state
```

Required changes:

- light canvas;
- solid editors and result surfaces;
- no marketing switcher inside the workbench;
- move AuraGlass link to the Open navigation or footer;
- use tabs for Rubric and Responses on narrow widths;
- use status labels for ready, running, complete, and failed;
- include validation issues with file/row/field/fix structure;
- include exact score table before visual summary;
- show source, criteria count, response count, missing labels, and runtime;
- use a dark surface only inside Monaco/code editors if selected;
- preserve 320 px reflow without page-level horizontal scrolling;
- add loading, invalid JSON, no responses, permalink error, and runtime failure
  states;
- remove the boxed `A` mark.

## 12. Robotics ReviewKit

### 12.1 Consolidate viewers

The public repository currently has:

- `viewer/index.html`, a minimal static page;
- `viewer/reviewkit.html`, the fuller legacy viewer;
- `viewer/reviewkit-viewer.css`;
- `viewer/reviewkit-v2/`, a React viewer;
- inline hard-coded style objects in the React app.

The React v2 viewer should become canonical. The legacy viewer should become a
small compatibility redirect or a built output of the same source.

### 12.2 Canonical ReviewKit layout

```text
Page header:
  episode ID | task | synthetic/permissioned status | version | open file

Workspace:
  left: source JSON / schema issues
  center: event timeline and event table
  right inspector: rubric anchors, intervention density, release decision

Bottom:
  provenance, limitations, export options
```

Required changes:

- replace inline styles with Proofline OSS CSS;
- add responsive breakpoints;
- use the canonical chart palette;
- do not assign a unique hard-coded color to state without text/icon;
- add file upload and drag/drop;
- add schema-validation error paths;
- add selected-event inspector;
- add zoom and keyboard navigation for timeline;
- include an ordered event table as the nonvisual source of truth;
- show synthetic data disclosure persistently but quietly;
- expose LeRobot and RLDS/OpenX export as explicit artifacts with boundaries;
- use one generated build for static hosting and local file use;
- update viewer smoke tests and screenshot tests.

## 13. EvalKit Generated Reports

### 13.1 Baseline gaps addressed

The current HTML template is nearly unstyled, while the Python generator emits
a separate minimal inline stylesheet. The template and generator can diverge.
Reports lack:

- report identity;
- source metadata;
- generated timestamp;
- run version;
- evidence sequence;
- structured metric tables;
- explicit missing and omitted states;
- print rules;
- accessible chart alternatives;
- limitation prominence;
- stable anchors and table of contents.

### 13.2 New report contract

Every generated HTML report should include:

1. AuraOne EvalKit identity.
2. Report title and disclosure.
3. Source and generation metadata.
4. Executive decision.
5. Rubric coverage table.
6. Score breakdown table.
7. Unstable criteria.
8. Reviewer agreement.
9. Drift and leakage warnings.
10. Missing/omitted evidence.
11. Limitations.
12. Reproduction command.
13. Artifact checksum and EvalKit version where available.

Use the Proofline sequence as section navigation, not as a decorative progress
bar.

Implementation:

- make the Jinja template canonical;
- have `generate_html_report()` render the canonical template;
- embed a compact OSS-safe stylesheet;
- support `prefers-color-scheme` only as an optional report viewer preference;
- print in light mode;
- use no JavaScript for the base report;
- add semantic tables and `details` only for long payloads;
- include anchor links and skip link;
- test with long criterion names, missing values, large tables, and print/PDF.

Files:

- `packages/evalkit/src/auraone_evalkit/reports/templates/html.html.j2`
- `packages/evalkit/src/auraone_evalkit/reports/generator.py`
- `packages/evalkit/examples/reports/tutorial_report.html`
- `packages/evalkit/tests/reports/**`

## 14. Failure Gallery

The current static gallery duplicates the old dark/glass marketing language.

Replace it with:

- light AuraOne/Open header;
- literal "Failure Gallery" title;
- filterable record index;
- record cards only for repeated failure cases;
- exact fields for domain, tool, source, failure, reproduction, expected
  behavior, evidence, and limitations;
- no glass hero card;
- no decorative metric panel;
- no grid wallpaper;
- dark code blocks only;
- direct links to reproduce locally;
- clear synthetic/approved-data label;
- canonical route on `auraone.ai/open/robotics-studio/failure-gallery`;
- static export generated from the same data as the AuraOne website route.

Do not maintain two hand-edited HTML copies in `site/` and `docs/`.

## 15. GitHub-Native UX

### 15.1 AuraOne GitHub App

The GitHub App currently uses:

- a commit status;
- a Markdown PR comment;
- emoji pass/fail markers;
- one average score;
- a fixed table;
- a generic dashboard link.

Move to GitHub Checks as the primary surface.

Required Check Run:

- name: `AuraOne evaluation`;
- summary: decision, score, threshold, evaluated commit, configuration path;
- text: template-level evidence;
- annotations: file/line annotations where evidence can be mapped;
- details URL: exact evaluation evidence page;
- actions: rerun, inspect configuration, open documentation where supported;
- states: queued, in progress, passed, failed, neutral/skipped, action required,
  and error.

PR comment should be optional and idempotently updated, not appended on every
synchronize event.

Recommended comment structure:

```markdown
## AuraOne evaluation

**Decision:** Action required
**Score:** 76.4% against an 80.0% threshold
**Commit:** `abc1234`
**Configuration:** `.auraone.yml`

| Evaluation | Score | State | Evidence |
| --- | ---: | --- | --- |
| Tool use | 82.0% | Passed | View run |
| Safety | 70.8% | Review | 3 findings |

### Next action
Review the safety findings, then rerun the check.

Generated by AuraOne. Data and network behavior depend on the configured
AuraOne endpoint and repository settings.
```

Avoid emoji as the only state signal. Escape all user-controlled template names
and error text before inserting Markdown.

### 15.2 EvalKit Action, Datasheet CI, and Rubric PR Bot

All GitHub Actions and bots should share:

- one check naming convention;
- one summary order;
- one state vocabulary;
- one annotation severity map;
- one artifact link pattern;
- one skipped/no-config state;
- one remediation section;
- one footer and version identifier.

## 16. CLI and Terminal UX

### 16.1 Hosted Python SDK CLI

The current `aura` CLI prints raw objects or tab-delimited rows.

Upgrade without making terminal output decorative:

- sentence-case command help;
- explicit hosted-service label;
- table output for humans;
- `--format table|json|jsonl`;
- `--no-color`;
- semantic exit codes;
- progress only on TTY;
- stable machine output on non-TTY;
- clear authentication, network, and organization context;
- request/evaluation ID in every result;
- next action after failures;
- no spinner in CI logs;
- no emoji required for meaning.

Example:

```text
Evaluation created

ID          eval_01J...
Template    cartpole-v1
State       queued
Organization public
Endpoint    https://api.auraone.ai

Next: aura evaluations get eval_01J...
```

### 16.2 EvalKit CLI

Apply the same structure to local EvalKit:

- command identity;
- local-only disclosure where relevant;
- issue table with row, field, severity, message, fix;
- exact output path;
- summary after detail;
- deterministic JSON schemas;
- `NO_COLOR` support;
- accessible ANSI contrast;
- no color-only pass/fail.

### 16.3 Cross-product naming

The docs and CLI must clearly separate:

| Name | Purpose |
| --- | --- |
| `evalkit` | Local open-source evaluation and judgment tooling |
| `aura` | Hosted AuraOne Python CLI |
| `auraone-sdk` | Hosted AuraOne Python SDK |
| `@auraone/sdk` | Hosted AuraOne TypeScript/Node SDK |
| AuraOne GitHub App | Hosted evaluation integration for GitHub |

## 17. SDK Documentation UX

The SDK repositories do not need an application UI, but their documentation is
a product surface.

### 17.1 README standard

Use the same section order:

1. Product name and one-sentence job.
2. Local versus hosted boundary.
3. Install.
4. Five-minute quickstart.
5. Expected output.
6. Authentication.
7. Primary workflows.
8. Error handling.
9. Runtime compatibility.
10. Data/network behavior.
11. API reference links.
12. Versioning and migration.
13. Support, security, contributing, license.

### 17.2 Code-example standard

- use one realistic canonical example across Python and TypeScript;
- use the same template IDs and output concepts;
- never include a key-shaped example that could be mistaken for a real secret;
- show timeout, retry, and error handling;
- show how to close async clients;
- show idempotency for evaluation creation;
- show expected output;
- include direct local EvalKit alternative where hosted access is unnecessary.

### 17.3 Documentation website

The AuraOne developer website should provide:

- language selector;
- version selector;
- install command;
- API/client initialization;
- service navigation;
- method signature;
- request example;
- response example;
- error states;
- authentication requirement;
- rate-limit and retry behavior;
- linked source;
- "Open in GitHub" and "Report docs issue".

The developer docs should use the same light Proofline shell, but code blocks
may remain dark.

## 18. Buying Toolkit and Document Resources

The Buying Toolkit is currently primarily Markdown. Its UI upgrade belongs in
the website and generated document layer.

Each resource page should provide:

- purpose;
- intended user;
- planning-only or legal boundary;
- version and review date;
- editable/downloadable format;
- source Markdown;
- section preview;
- related resources;
- print/PDF view;
- owner and update policy.

Use a document layout, not a card catalog. Provide a compact table of contents,
clear headings, checklist controls for browser use where appropriate, and
print-safe styling.

## 19. Identity and Icon System

### 19.1 Brand

Use the canonical AuraOne Proof Fold mark on:

- desktop title and about surfaces;
- browser headers;
- website product pages;
- favicons and app icons;
- GitHub social preview;
- report headers;
- release assets.

Do not restore:

- boxed `A1`;
- boxed `A`;
- blue-purple Aura Foundry glow mark;
- separate RS gradient monogram;
- framed decorative studio marks;
- orb identity.

### 19.2 Product differentiation

The AuraOne mark identifies the family. A simple product glyph identifies the
tool:

- Rubric Studio: criteria/checklist glyph;
- Agent Studio: trace/branch glyph;
- Robotics Studio: episode/sensor glyph;
- EvalKit: scored-record glyph;
- Trust Toolkit: evidence/package glyph.

Product glyphs must:

- work in one color;
- remain legible at 16 px;
- avoid gradients;
- use consistent stroke or fill language;
- not compete with the AuraOne mark.

### 19.3 Icons

Use Lucide for interface commands. Custom icons are reserved for:

- AuraOne mark;
- product glyphs;
- domain-specific visualization symbols not covered by Lucide.

## 20. Responsive and Window Behavior

### 20.1 Browser breakpoints

Use behavior-based breakpoints:

- under 640 px: single-column, 44 px controls, drawers/full-screen overlays;
- 640-819 px: compact two-region layouts where useful;
- 820-1179 px: collapsed navigation and inspector drawer;
- 1180 px and above: full desktop workbench.

### 20.2 Desktop windows

Desktop apps must support:

- full primary layout at 1440 by 960;
- usable layout at 1180 by 760;
- minimum compact mode near 980 by 720 where the product allows it;
- no clipped toolbar labels;
- no inaccessible inspector content;
- stable editor/media region;
- drawers for secondary context before shrinking the main work area below a
  useful size.

Robotics Studio should lower its 1120 px minimum only after the inspector
drawer and collapsed sidebar are implemented.

### 20.3 Mobile website

Every marketing hero must leave the next section visible. Tables must become
record layouts or remain keyboard-focusable scroll regions. Download and source
actions must not overflow. Product screenshots need stable aspect ratios and
captions.

## 21. Accessibility Requirements

All surfaces must meet:

- WCAG 2.2 AA;
- keyboard-only operation;
- 200% zoom;
- 320 CSS px reflow for web surfaces;
- visible focus;
- forced-colors support;
- reduced-motion support;
- text-spacing overrides;
- screen-reader labels for icon controls;
- focus restoration for dialogs and drawers;
- no color-only state;
- minimum 44 px mobile targets;
- ordered alternatives for timelines, charts, canvases, and media annotations.

Desktop-specific requirements:

- native menu access where available;
- logical title-bar and toolbar order;
- no global shortcut interception while typing in editors;
- shortcuts configurable or disabled when they conflict;
- screen-reader announcements for long-running local operations;
- persistent operation log for users who miss transient toasts.

## 22. State Vocabulary

Use one cross-product set:

| State | Meaning |
| --- | --- |
| Draft | Created but not ready for review |
| Ready | Meets prerequisites for the next operation |
| Running | Operation is active |
| Queued | Accepted but not started |
| Review | Human action or decision required |
| Passed | Criteria met |
| Released | Approved output is available |
| Warning | Degraded, stale, or near a limit |
| Failed | Operation or criteria failed |
| Blocked | Cannot proceed until a dependency changes |
| Unavailable | Capability or data is not available |
| Restricted | Access or policy prevents use |
| Stale | Older data is displayed |
| Partial | Some required data is missing |

Every state instance should answer:

- what state is this;
- why;
- who or what owns it;
- when it changed;
- what evidence supports it;
- what the user can do next.

## 23. Data and Network Boundary UX

Local-first is a product behavior, not a slogan.

Every application and website page should state:

| Boundary | Required disclosure |
| --- | --- |
| Local files | What is read, indexed, cached, and deleted |
| Provider API | Destination, trigger, credential storage, and payload |
| Telemetry | Default, fields, destination, retention, and opt-out |
| Crash reports | Default, content, destination, and opt-out |
| AuraOne handoff | Exact artifact, destination, account requirement |
| Updates | Endpoint, signature verification, and failure behavior |

Settings should include a "Data and network" view with:

- current mode;
- configured destinations;
- stored credential locations;
- telemetry state;
- crash state;
- updater state;
- recent network operations;
- clear local data action.

## 24. Release Evidence Contract

Create one machine-readable manifest per release:

```json
{
  "product": "Agent Studio Open",
  "version": "0.1.0",
  "sourceCommit": "<sha>",
  "releasedAt": "<ISO-8601>",
  "license": "MIT",
  "artifacts": [
    {
      "platform": "macos",
      "arch": "aarch64",
      "type": "dmg",
      "url": "<release URL>",
      "sha256": "<digest>",
      "signed": true,
      "notarized": true,
      "minimumOS": "<version>"
    }
  ],
  "browserPreview": {
    "url": "<URL>",
    "sourceCommit": "<sha>",
    "verifiedAt": "<ISO-8601>"
  },
  "securityPolicy": "<URL>",
  "support": "<boundary>",
  "status": "verified"
}
```

Consumers:

- `auraone.ai/open`;
- product detail pages;
- in-app About and Update views;
- Homebrew casks;
- Winget metadata;
- GitHub release notes;
- download buttons;
- launch operations status.

No UI should construct a release URL from a version string.

## 25. File-Level Implementation Map

### 25.1 Reference monorepo

| Area | Files |
| --- | --- |
| Shared OSS system | `opensource/open-studio-platform/packages/aura-ide-kit/**`, new `packages/proofline-oss/**` |
| Rubric Studio | `opensource/rubric-studio-open/src/**`, `src-tauri/tauri.conf.json`, `vscode-extension/**` |
| Agent Studio | `opensource/agent-studio-open/app/src/**`, `desktop/src-tauri/tauri.conf.json`, `vscode/**`, `cli/**` |
| Robotics Studio | `opensource/robotics-studio/src/**`, `src-tauri/tauri.conf.json` |
| Playground | `opensource/evalkit-playground/src/**` |
| Failure Gallery | `opensource/failure-gallery/site/index.html`, `docs/index.html`, generator source |
| ReviewKit mirror | `opensource/robotics-reviewkit/viewer/**` |
| Distribution | `opensource/open-studio-platform/distribution/**`, `installers/**` |
| Marketing | `auraone-website/src/app/open/**`, `src/components/makeover/OpenSourceProduct.tsx`, Open Source data |

### 25.2 `auraone-open-public`

| Area | Files |
| --- | --- |
| EvalKit report design | `packages/evalkit/src/auraone_evalkit/reports/**` |
| Report examples | `packages/evalkit/examples/reports/**` |
| ReviewKit React viewer | `robotics-reviewkit/viewer/reviewkit-v2/**` |
| ReviewKit compatibility viewer | `robotics-reviewkit/viewer/reviewkit.html`, `reviewkit-viewer.css`, `reviewkit-viewer.js` |
| Minimal viewer | `robotics-reviewkit/viewer/index.html`, `style.css`, `viewer.js` |
| Docs and README | root README, EvalKit README, ReviewKit README, Buying Toolkit README |

### 25.3 `auraoneai-github-app`

| Area | Files |
| --- | --- |
| GitHub check/comment UX | `src/app.js` |
| Contract tests | `__tests__/app.test.js` |
| Product docs | `README.md`, `CHANGELOG.md` |

### 25.4 `auraoneai-sdk-python`

| Area | Files |
| --- | --- |
| CLI UX | `aura/cli.py` |
| Hosted client examples | `README.md` |
| Errors and structured output | `aura/client.py`, `aura_one/exceptions.py`, service types |
| Tests | add CLI snapshot and JSON-output tests |

### 25.5 `auraoneai-sdk-typescript`

| Area | Files |
| --- | --- |
| Developer-doc UX | `README.md` |
| Example consistency | `src/index.ts`, service docs and TSDoc |
| Error/status vocabulary | `src/utils/HttpClient.ts`, exported types |
| Package metadata | `package.json` |

## 26. Migration Phases

### Phase 0: Governance and capture

- freeze canonical product names;
- approve OSS font and asset boundary;
- create release manifest schema;
- create visual baseline captures;
- create token and component inventory;
- mark generated files versus source files;
- select canonical ReviewKit and Failure Gallery source.

### Phase 1: Shared foundation

- build `@auraone/proofline-oss`;
- migrate Aura IDE Kit to semantic tokens;
- add identity assets;
- add status vocabulary;
- add common app shell, controls, states, and evidence components;
- add no-private-font and no-legacy-glass checks.

### Phase 2: Flagship desktop apps

Order:

1. Rubric Studio Open, because it is closest to the target.
2. Agent Studio Open, because its light system needs structural typography and
   decoration removal.
3. Robotics Studio Open, because it requires the largest responsive and
   dark-first conversion.

For each app:

- migrate shell;
- migrate primary workflow;
- migrate inspector and states;
- migrate settings/data boundary;
- migrate first run;
- migrate export/release;
- migrate DMG and release assets;
- capture and test.

### Phase 3: Browser tools and artifacts

- EvalKit Playground;
- ReviewKit v2;
- EvalKit HTML reports;
- Failure Gallery;
- VS Code webviews;
- static documentation artifacts.

### Phase 4: Website and release catalog

- generated Open catalog;
- product pages;
- Trust Toolkit grouping;
- SDK and integration pages;
- verified download actions;
- capture manifest;
- SEO and structured data.

### Phase 5: GitHub, CLI, and documentation

- GitHub Checks;
- Action summaries;
- Python CLI;
- EvalKit CLI;
- SDK README standard;
- docs website language/version experience.

### Phase 6: Remove compatibility

- delete duplicated static viewer sources;
- remove obsolete gradient/glass tokens;
- remove legacy marks;
- remove hard-coded release URLs;
- remove duplicate report HTML generation;
- remove compatibility aliases after one documented deprecation cycle.

### Phase 7: Coordinated release update

- execute the coordinated post-upgrade release task in Section 27;
- publish packages and binaries only after all UI/UX, accessibility, release,
  integrity, and registry-specific gates pass;
- update the Open catalog from verified live registry and release evidence;
- run clean-install and package-consumption smoke tests against the published
  versions;
- record final release URLs, versions, checksums, deployment commits, and
  verification timestamps.

## 27. Coordinated Post-Upgrade Release Task

### 27.1 Task objective

After the UI/UX upgrade is merged and verified, perform one coordinated release
update across every registry, marketplace, binary channel, hosted preview, and
GitHub repository that distributes an affected AuraOne Open offering.

This task is complete only when:

- versions are updated consistently;
- release notes describe the actual UI/UX and behavior changes;
- packages and artifacts are built from the tagged source commit;
- every destination is published or explicitly recorded as blocked/not
  applicable with an owner and next action;
- live package and installer smoke tests pass for every published destination;
- blocked destinations retain no live availability claim;
- `auraone.ai/open` displays verified current evidence or an accurate
  blocked/stale state.

### 27.2 Release owner and change record

Create one release issue or release PR named:

`release(oss): publish Proofline UI/UX upgrade across all channels`

The issue or PR must contain:

- release owner;
- target release date;
- source commit for every repository;
- old and new version for every offering;
- semantic-versioning rationale;
- changelog links;
- registry and marketplace checklist;
- signing/notarization status;
- release-blocker list;
- rollback owner;
- final verification evidence.

Do not use one version number for unrelated packages unless the repositories
already follow a synchronized release train. Each package keeps its own
semantic version, but the release record links them as one UI/UX program.

### 27.3 Release destination matrix

The machine-readable source of truth is
`release/offering-destinations.json`, validated by
`release/offering-destinations.schema.json`. It contains all 41 offerings and
all 193 destination pairs. `release/evidence/publication-decision.json`
records a state, owner, reason, next action, and evidence reference for every
pair. The table below is the human-readable inventory; no grouped row replaces
an individual destination decision in the machine-readable record.

| Offering | Package/artifact identity | Required destinations |
| --- | --- | --- |
| AuraOne EvalKit | `auraone-evalkit` | PyPI, GitHub Release, repository tag, Open catalog |
| AuraOne Python SDK | `auraone-sdk` | PyPI, GitHub Release, repository tag, developer docs |
| AuraOne TypeScript SDK | `@auraone/sdk` | npm, GitHub Release, repository tag, developer docs |
| AuraOne GitHub App | `@auraone/github-app` | npm if retained as a public package, GitHub Release, repository tag, integration docs |
| Open Studio Platform | shared source and release contracts | source release train, GitHub Release, repository tag |
| Proofline OSS | `@auraone/proofline-oss` | npm, matching GitHub Release, repository tag, Open catalog |
| Aura IDE Kit | `@auraone/aura-ide-kit` | public source release train; tested first npm candidate `0.2.0` pending valid npm write authorization |
| Platform Contracts | `@auraone/platform-contracts` | public source release train; tested first npm candidate `0.3.0` pending valid npm write authorization |
| Rubric Studio Open | desktop/web/VS Code artifacts | GitHub Release, DMG, MSI, AppImage, deb, rpm, Homebrew cask, Winget, VS Code Marketplace where applicable, hosted preview, Open catalog |
| Agent Studio Open | desktop/web/CLI/VS Code artifacts | GitHub Release, DMG, MSI, AppImage, deb, rpm, Homebrew cask, Winget, VS Code Marketplace, PyPI CLI if released, hosted browser/demo, Open catalog |
| Agent Studio CLI | `auraone-agent-studio-open` / `agentstudio` | PyPI, matching Agent Studio GitHub Release, repository tag, CLI docs |
| Robotics Studio Open | desktop artifacts | GitHub Release, DMG, MSI, AppImage, deb, rpm, Homebrew cask, Winget, Open catalog |
| EvalKit Playground | static browser build | production hosting, GitHub deployment record/release, Open catalog |
| Robotics ReviewKit | source and static viewer | GitHub Release for `auraone-open-public`, deployed viewer, Open catalog/docs |
| Failure Gallery | `failure-gallery` plus generated static output | PyPI, matching GitHub Release, deployed gallery, Open catalog/docs |
| EvalKit Action | GitHub Action release | immutable commit tag, moving major tag such as `v1` only after verification, GitHub Marketplace listing |
| Datasheet CI | GitHub Action and Python validator | GitHub Action release/Marketplace and PyPI only if the package is independently published |
| Rubric PR Bot | GitHub App/check integration | GitHub Release, GitHub App listing/update, installation and permission verification |
| Open catalog and developer docs | `auraone.ai/open` and developer routes | AuraOne production, developer docs, Open catalog |
| rubric-spec | `rubric-spec` | PyPI, GitHub Release, repository tag, Open catalog |
| iaa-kit | `iaa-kit` | PyPI, GitHub Release, repository tag, Open catalog |
| judge-bench | `judge-bench` | PyPI, GitHub Release, repository tag, Open catalog |
| judge-card | `judge-card` | PyPI, GitHub Release, repository tag, Open catalog |
| eval-adapter | `eval-adapter` | PyPI, GitHub Release, repository tag, Open catalog |
| eval-conformance-suite | `eval-conformance-suite` | PyPI, GitHub Release, repository tag, Open catalog |
| eval-run-manifest | `eval-run-manifest` | PyPI, GitHub Release, repository tag, Open catalog |
| contamination-audit | `contamination-audit` | PyPI, GitHub Release, repository tag, Open catalog |
| prompt-rubric-drift | `prompt-rubric-drift` plus `action.yml` | PyPI, GitHub Release, immutable Action tag, moving major tag and GitHub Marketplace explicitly N/A this train, Open catalog |
| synthetic-disagreement | `synthetic-disagreement` | PyPI, GitHub Release, repository tag, Open catalog |
| agent-trace-card | `agent-trace-card` | PyPI, GitHub Release, repository tag, Open catalog |
| tool-call-replay | `tool-call-replay` | PyPI, GitHub Release, repository tag, Open catalog |
| otel-eval-bridge | `otel-eval-bridge` | PyPI, GitHub Release, repository tag, Open catalog |
| mcp-risk-linter | `mcp-risk-linter` plus `action.yml` | PyPI, GitHub Release, immutable Action tag, moving major tag and GitHub Marketplace explicitly N/A this train, Open catalog |
| a2a-contract-test | `a2a-contract-test` plus `action.yml` | PyPI, GitHub Release, immutable Action tag, moving major tag and GitHub Marketplace explicitly N/A this train, Open catalog |
| embodiment-card | `embodiment-card` | PyPI, GitHub Release, repository tag, Open catalog |
| lerobot-quality-gates | `lerobot-quality-gates` plus `action.yml` | PyPI, GitHub Release, immutable Action tag, moving major tag and GitHub Marketplace explicitly N/A this train, Open catalog |
| robot-recovery-bench | `robot-recovery-bench` | PyPI, GitHub Release, repository tag, Open catalog |
| vla-robustness-kit | `vla-robustness-kit` | PyPI, GitHub Release, repository tag, Open catalog |
| robostudio-engine | `robostudio-engine` | PyPI, GitHub Release, repository tag, Open catalog |
| Agent Studio Cookbook | source and examples | repository tag, developer docs, Open catalog |
| Buying Toolkit and public writing | public resource artifacts | AuraOne production resources, public resource docs, Open catalog |

### 27.4 Pre-release version and metadata update

For each affected repository:

1. Select the release type:
   - patch for visual fixes with no public contract change;
   - minor for new UI surfaces, generated artifact structures, CLI options,
     component APIs, or backward-compatible release metadata;
   - major for removed public APIs, renamed CLI commands, incompatible report
     schemas, or unsupported legacy formats.
2. Update every authoritative version source:
   - `pyproject.toml`;
   - `package.json` and lockfile;
   - Tauri `tauri.conf.json`;
   - Cargo package metadata where applicable;
   - VS Code extension manifest;
   - Homebrew and Winget templates;
   - updater manifests;
   - browser build metadata;
   - generated report/version constants;
   - release manifest.
3. Update `CHANGELOG.md` with:
   - Proofline visual-system adoption;
   - light-first behavior;
   - accessibility and responsive changes;
   - generated report or GitHub output changes;
   - release and installer changes;
   - migration or compatibility notes;
   - known limitations.
4. Update README screenshots, install commands, supported runtime versions,
   package names, and download links.
5. Confirm package metadata points to the correct repository, homepage,
   documentation, issue tracker, license, and security policy.
6. Generate or refresh SBOM, dependency inventory, license report, provenance,
   checksums, and release evidence.

### 27.5 Unified preflight gate

Create a root release orchestrator or documented command that can run in dry-run
mode before any tag is pushed.

Recommended command:

```bash
pnpm run release:oss:preflight -- --release-plan <release-plan.json>
```

The preflight must:

- verify clean or intentionally scoped worktrees;
- verify every target commit is pushed;
- verify package versions do not already exist in the destination registry;
- run all repository tests, type checks, lint, design lint, accessibility
  tests, visual regression tests, and builds;
- build Python wheels and source distributions;
- run `twine check` or equivalent metadata validation;
- build npm tarballs and inspect them with `npm pack --dry-run`;
- reject private font files or unapproved assets;
- verify GitHub Action metadata and immutable commit references;
- build desktop artifacts on their target operating systems;
- verify signatures, notarization, stapling, Gatekeeper, Authenticode, and GPG
  signatures where applicable;
- verify checksums and SBOMs;
- test updater manifests;
- validate Homebrew casks;
- validate Winget manifests;
- build and test VS Code extensions;
- build browser deployments and run production smoke tests;
- generate a proposed release-evidence manifest without publishing it.

No publication job may run if the unified preflight is incomplete.

The coordinator records local engineering evidence and publication readiness
separately. `qualityReady: true` means the cross-repository command matrix and
registry-availability checks passed. `publicationReady: true` additionally
requires clean, exact pushed source and every publication-only gate. Running
with `--allow-dirty` may produce local evidence, but it cannot set
`publicationReady` or `publicationAllowed`.

#### Signed publication authorization

No publisher may treat a dispatch input, signed source tag, or protected
environment name as sufficient authorization by itself.

After the strict execute preflight and destination decision are approved:

1. Update `release/publication-authorization.json` to `decision: "approved"`
   and `publicationAllowed: true`.
2. Bind every grant to one exact repository, clean pushed source commit,
   package/artifact identity, semantic version, and allowed channel.
3. Record at least one accountable approver, `authorizedAt`, and a short
   `expiresAt`; expired, future, duplicate, malformed, or partial grants fail.
4. Commit the authorization in `auraoneai/open` and create an immutable,
   annotated GPG-signed authorization tag using the configured release signer.
5. Set `OSS_PUBLICATION_AUTHORIZATION_TAG` in each affected repository to that
   exact tag. Do not move or reuse the tag for different source commits.
6. Let each publisher independently fetch and verify the tag and authorization
   before provenance attestation, registry access, GitHub Release writes, R2
   writes, or updater publication.
7. Revoke or expire the authorization immediately after the coordinated
   release window and preserve the signed authorization with final evidence.

The blocked template is the default state. A blocked or revoked authorization,
missing variable, lightweight or unsigned tag, wrong signer, stale source
commit, wrong package/version/channel, or expired window fails closed.

### 27.6 Publication order

Publish in dependency order:

1. Shared contracts and intentionally public shared packages.
2. EvalKit and SDK libraries.
3. GitHub Actions, apps, bots, and extensions that consume those libraries.
4. Browser applications and static viewers.
5. Desktop GitHub Release artifacts.
6. Homebrew, Winget, Linux repositories/listings, and VS Code Marketplace.
7. AuraOne website Open catalog and product pages.
8. Final cross-channel announcement and documentation update.

The website must not advertise a package or binary as available until the live
registry or release artifact has been independently fetched and verified.

### 27.7 PyPI publication tasks

#### AuraOne EvalKit

Repository:

`/Users/gurbakshchahal/opensource/AuraOne OSS/auraone-open-public`

Workflow:

`.github/workflows/release-python.yml`

Checklist:

- update `packages/evalkit/pyproject.toml`;
- build wheel and source distribution;
- install the wheel in a clean environment;
- run CLI and report-generation smoke tests from the installed wheel;
- verify package contents do not include private fonts, local artifacts, test
  output, or unrelated monorepo files;
- publish through PyPI trusted publishing;
- verify `pip install auraone-evalkit==<version>`;
- run `evalkit --version`, rubric validation, scoring, and HTML report smoke;
- create a matching GitHub Release.

#### AuraOne Python SDK

Repository:

`/Users/gurbakshchahal/opensource/AuraOne OSS/auraoneai-sdk-python`

Workflow:

`.github/workflows/release-python.yml`

Checklist:

- update `pyproject.toml` and `aura_one/version.py`;
- confirm any legacy `aura` package version exposure remains consistent;
- build and inspect wheel/sdist;
- install in clean Python 3.9, 3.10, 3.11, and 3.12 environments;
- run import, CLI, service-client, async-client, and error-format smoke tests;
- publish through PyPI trusted publishing;
- verify `pip install auraone-sdk==<version>`;
- create a matching GitHub Release and update developer docs.

For every PyPI release, confirm the trusted-publisher environment, repository,
workflow filename, tag pattern, and PyPI project binding before tagging.

### 27.8 npm publication tasks

#### AuraOne TypeScript SDK

Repository:

`/Users/gurbakshchahal/opensource/AuraOne OSS/auraoneai-sdk-typescript`

Workflow:

`.github/workflows/release-npm.yml`

Checklist:

- update `package.json` and `package-lock.json`;
- run typecheck, lint, tests, and Rollup build;
- inspect the tarball with `npm pack --dry-run`;
- test ESM, CommonJS, and TypeScript declarations from the packed tarball;
- publish `@auraone/sdk` with public access;
- prefer npm trusted publishing/provenance when available and migrate away from
  a long-lived `NPM_TOKEN` where operationally supported;
- verify `npm view @auraone/sdk@<version>`;
- install the published package in clean Node 18, 20, and 22 projects;
- create a matching GitHub Release and update developer docs.

#### AuraOne GitHub App

Repository:

`/Users/gurbakshchahal/opensource/AuraOne OSS/auraoneai-github-app`

Implemented release state:

The repository now includes `.github/workflows/release-npm.yml` with exact
tag/version validation, protected npm OIDC publication, provenance, package
verification, and an independently gated GitHub Release step. Live execution
remains blocked until the reviewed source is committed/pushed and a maintainer
authorizes the protected environment.

Checklist:

- decide whether `@auraone/github-app` remains a supported public npm package;
- if yes, add `.github/workflows/release-npm.yml`;
- update `package.json` version and package contents;
- add a lockfile or make the release install path deterministic;
- run lint, tests, package-content inspection, and clean-package consumption
  tests;
- publish with provenance/trusted publishing where available;
- verify `npm view @auraone/github-app@<version>`;
- install and start the package in a clean test project;
- create a matching GitHub Release;
- verify the GitHub App webhook, Check Run, permissions, and installation flow;
- if npm publication is discontinued, remove npm badges and install
  instructions and document source/container deployment instead.

#### Proofline and shared OSS packages

Publish `@auraone/proofline-oss`, platform contracts, or IDE kit packages only
if they have:

- a documented public API;
- independent semantic versioning;
- package-level tests;
- package exports;
- redistribution-safe fonts and assets;
- a support and compatibility policy.

Internal-only shared packages should not be published merely because the
flagship applications use them.

### 27.9 GitHub Release and repository tasks

For every affected repository:

- create an annotated, signed tag using the repository's existing tag
  convention;
- create a GitHub Release from the exact tag;
- attach source-independent artifacts where applicable;
- attach checksums, signatures, SBOMs, provenance, and release manifest;
- include install, upgrade, migration, rollback, and known-issue notes;
- link the release to the coordinated release issue;
- verify source archives do not expose secrets or private build assets;
- verify release links from README and website;
- mark pre-releases accurately;
- never move an immutable version tag after publication.

GitHub Action releases may additionally update a moving major tag such as `v1`
only after the immutable version tag passes live smoke tests. The moving tag
must point to the verified release commit.

### 27.10 Desktop and package-manager tasks

For Rubric Studio, Agent Studio, and Robotics Studio:

Implemented local release state:

The Agent Studio Open protected release workflow builds signed desktop targets
and tests the Tauri updater signature, validates the full manifest contract,
uploads immutable versioned artifacts to R2, byte-verifies the mirrored
manifest, verifies the live channel endpoint and every artifact URL, and only
then permits the draft GitHub Release stage. Live signing, notarization,
registry, package-manager, marketplace, and installation evidence remains
blocked until the exact reviewed source is committed, pushed, and executed in
protected environments.

1. Build signed artifacts:
   - macOS DMG;
   - Windows MSI;
   - Linux AppImage;
   - deb;
   - rpm.
2. Verify:
   - macOS Developer ID signature;
   - Apple notarization and stapling;
   - Gatekeeper acceptance;
   - Windows Authenticode/EV signature;
   - clean Windows install/uninstall;
   - Linux detached signatures;
   - SHA-256 values;
   - updater signature and manifest.
3. Publish artifacts to the corresponding GitHub Release.
4. Update:
   - `opensource/open-studio-platform/distribution/releases/**`;
   - Homebrew casks;
   - Winget manifests;
   - Linux metadata/listings;
   - updater `latest.json` and platform manifests.
5. Run:
   - Homebrew audit/install smoke;
   - Winget validation and clean-install smoke;
   - AppImage, deb, and rpm installation smoke;
   - in-app update smoke from the previous public version.
6. Publish VS Code extensions where the affected UI is included.
7. Publish hosted browser previews from the same tagged source commit.

Do not submit Homebrew, Winget, marketplace, or updater metadata containing
placeholder checksums, placeholder URLs, placeholder product codes, or
unverified signing claims.

### 27.11 Hosted website and browser publication

After package and binary verification:

- deploy the EvalKit Playground;
- deploy Agent Studio browser/demo builds;
- deploy ReviewKit and Failure Gallery generated builds;
- deploy AuraOne marketing and developer-documentation updates;
- update `/open` and product pages from the release manifests;
- purge stale download caches where necessary;
- verify canonical URLs, metadata, structured data, sitemap, and search;
- run desktop and mobile production screenshots;
- verify every download button resolves to the intended live artifact;
- verify stale or blocked channels remain labeled accurately.

### 27.12 Post-publication verification

The release owner must independently verify live distribution:

```text
PyPI:
  pip install auraone-evalkit==<version>
  pip install auraone-sdk==<version>

npm:
  npm install @auraone/sdk@<version>
  npm install @auraone/github-app@<version>   # if retained

GitHub:
  fetch release assets and verify SHA-256/signatures

Desktop:
  install from DMG/MSI/AppImage/deb/rpm
  launch, complete first run, update from previous version, uninstall

Marketplaces:
  install through Homebrew, Winget, VS Code, and GitHub Marketplace paths

Web:
  open production playgrounds, viewers, docs, and Open catalog
```

Verification must use fresh environments and public URLs, not local build
outputs.

Record:

- command or install path;
- resolved version;
- public URL;
- checksum where applicable;
- platform/runtime;
- result;
- timestamp;
- verifier.

### 27.13 Failure and rollback rules

- Stop downstream publication if a foundational package fails.
- Do not delete or overwrite an already published package version.
- Publish a corrective patch for registry packages.
- Mark broken GitHub releases or browser deployments clearly and restore the
  last verified website manifest.
- Roll back website availability claims independently from source
  availability.
- Revoke or replace compromised signing material according to the security
  policy.
- Preserve the failed release evidence for audit.
- Update the coordinated release issue with the failure, affected channels,
  user impact, and next action.

### 27.14 Release task execution-decision checklist

- [x] All affected versions and changelogs are updated.
- [x] The source-commit gate is evaluated; uncommitted or unpushed source is
  recorded as a publication blocker.
- [x] Every public-write workflow requires a time-bounded, exact-source
  authorization from a separately verified signed `auraoneai/open` tag. The
  approved tag was consumed for this release, and the current checked-in
  authorization is revoked after publication.
- [x] The local quality command matrix and release contracts pass; clean pushed
  source, protected registry publication, GitHub Releases, notarized DMGs, and
  production web destinations were independently verified.
- [x] Every PyPI destination is published and clean-install verified or
  explicitly blocked with an owner and next action.
- [x] Every npm destination is published and clean-install verified or
  explicitly blocked with an owner and next action.
- [x] Every GitHub Release and signed-tag destination is verified or explicitly
  blocked with an owner and next action.
- [x] GitHub Actions, Apps, and Marketplace destinations are verified or
  explicitly blocked/not applicable.
- [x] DMG, MSI, AppImage, deb, and rpm destinations are verified or explicitly
  blocked with missing evidence identified.
- [x] Homebrew, Winget, Linux, updater, and VS Code destinations are verified or
  explicitly blocked/not applicable.
- [x] Browser applications and static artifacts are deployed and verified or
  explicitly blocked.
- [x] AuraOne website and developer-doc destinations are deployed and verified
  or explicitly blocked.
- [x] Open catalog release manifests reflect verified live evidence or an
  accurate stale/blocked state.
- [x] Screenshots and product captures identify the current source version,
  commit basis, date, source state, and data provenance.
- [x] Configured package-content and private-font gates pass for every changed
  package; the global secret/license attestation remains explicitly blocked in
  the required publication-evidence record and is not claimed as complete.
- [x] Rollback instructions and owners are recorded.
- [x] Final cross-channel verification evidence is attached.
- [x] The coordinated primary release record closes only after every planned
  primary channel is verified and every unsupported secondary destination is
  explicitly documented with its owner boundary and missing evidence.

## 28. Priority Backlog

### P0

- OSS-safe font/legal boundary.
- Shared Proofline OSS tokens.
- Canonical AuraOne identity assets.
- Release manifest schema.
- Light-first defaults.
- Remove global glass, blur, glow, and gradient backgrounds.
- Replace hard-coded release URLs.
- Consolidate generated versus source HTML.
- 44 px mobile controls and visible focus.
- Explicit status labels.

### P1

- Shared app shell and first run.
- Flagship workbench migrations.
- ReviewKit v2 canonicalization.
- EvalKit report redesign.
- GitHub Check Run migration.
- Marketing catalog generated from release evidence.
- Data and network settings.

### P2

- SDK docs website improvements.
- Buying Toolkit interactive/print views.
- optional dark media/code modes;
- advanced chart and evidence components;
- cross-product command palette consistency;
- visual regression automation across every release artifact.

## 29. Verification and Quality Gates

### 29.1 Design lint

Fail CI for:

- new raw hex colors outside token files;
- proprietary font binaries in public packages;
- new backdrop blur or glass utility use;
- radii above 12 px in ordinary product UI;
- icon-only controls without accessible names;
- hard-coded release URLs;
- status dots without text/icon alternatives;
- new inline style objects for visual tokens;
- remote font imports in desktop apps.

### 29.2 Automated tests

Required:

- unit tests for tokens and status definitions;
- component keyboard tests;
- axe tests;
- visual regression at wide, medium, and narrow viewports;
- forced-colors screenshots;
- reduced-motion tests;
- long-content tests;
- report print/PDF tests;
- DMG artifact naming and manifest tests;
- GitHub Markdown escaping tests;
- CLI TTY/non-TTY snapshots;
- release-manifest stale and failure states.

### 29.3 Manual QA

For each flagship:

- clean install;
- first run;
- sample workflow;
- real local file workflow;
- offline mode;
- provider/network mode;
- telemetry off/on;
- update available/failure;
- export;
- keyboard-only use;
- VoiceOver;
- 200% zoom where applicable;
- minimum window;
- uninstall and local-data behavior.

### 29.4 Performance budgets

- no decorative media preload;
- no remote font fetch for desktop;
- no more than two UI font families plus mono in OSS source;
- browser LCP under 2.5 seconds on representative mobile;
- CLS under 0.10;
- avoid shipping duplicate static and React viewer bundles;
- lazy-load Monaco, large schemas, and media tools;
- virtualize large trace, episode, and issue lists;
- keep generated HTML reports usable without JavaScript.

## 30. Definition of Done

The OSS UI/UX migration is complete only when:

- every official visual surface uses the shared semantic token contract;
- light Proofline is the default;
- code/media dark surfaces are bounded exceptions;
- public source contains no unapproved proprietary font;
- AuraOne identity is consistent across website, app, installer, report, and
  GitHub output;
- all three desktop products have coherent staged cross-platform release
  metadata, and unavailable binaries remain explicitly blocked;
- Rubric, Agent, and Robotics Studio share shell and state behavior;
- EvalKit Playground no longer uses dark glass or card nesting;
- ReviewKit has one canonical implementation;
- EvalKit reports use one canonical template;
- Failure Gallery has one canonical generated source;
- GitHub integration uses Check Runs with actionable evidence;
- CLI output is structured for both humans and automation;
- SDK documentation uses a shared information architecture;
- status is never encoded only by color;
- responsive, accessibility, measured network/layout-shift, and
  release-evidence gates pass;
- the marketing Open catalog is generated from current release evidence;
- every product capture identifies version, commit, date, and synthetic or
  approved data status;
- the coordinated post-upgrade release task has published and verified every
  available channel and explicitly recorded an owner, reason, and next action
  for every blocked/not-applicable PyPI, npm, GitHub, desktop, marketplace,
  and hosted-web channel.

## 31. Final Product Principle

AuraOne Open should not look like a collection of unrelated demos or side
projects. It should look like one coherent open technical system whose tools
can be inspected independently and whose evidence can move between them.

The visual test is simple:

> At every step, can the user identify the source, current work, review state,
> decision, release artifact, and next action without relying on decoration or
> brand familiarity?

If the answer is yes, the OSS experience is aligned with the AuraOne Proofline
upgrade. If the answer is no, changing colors, fonts, or logos is not enough.
