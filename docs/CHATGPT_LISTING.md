# The ChatGPT plugin listing (WP-CG3.1)

**Preflight update, 2026-10-05:** prepared version 0.2.1; countries US, GB, AU, NZ; seven malformed skill
front matters corrected; draft ZIP inspected. Review materials, production readiness and portal scans remain
separate. See `docs/CHATGPT_SUBMISSION.md` for the current workflow.

What the package for the ChatGPT Plugins dashboard is, where each listing field comes from, the search
terms the directory should match, and what the owner supplies at submission (WP-CG3.4). The plan is
`docs/CHATGPT_DISCOVERY_BUILD_PLAN.md` in the harness repo; nothing here concerns the Claude listing.

## The package

```
uv run --no-project --with jsonschema --with pyyaml python -I scripts/build_openai_zip.py --draft
```

runs the local source and final ZIP checks (`scripts/check_openai_package.py`, which needs
`jsonschema` and `PyYAML`, and fails when a required dependency is missing; `-I` keeps a broken user site out of the way) and
writes `dist/ask-lifesight-chatgpt.zip`:

| Path | What it is | Source |
|---|---|---|
| `plugin.json` | the manifest, the open `agent-plugins.org` 1.0.0 schema with OpenAI's `extensions.com.openai.interface` block | this repo |
| `mcp.json` | the MCP mapping: `ask-lifesight` over streamable HTTP at `https://ask.lifesight.io/mcp` (D-10 as amended 2026-09-23) | this repo |
| `skills/` | the twelve workflow skills with valid YAML; no generated scheduled-task promise is added | source files, checked again inside the ZIP |
| `assets/icon.svg`, `assets/logo.svg` | the square Lifesight mark (a 100 by 100 viewBox, SVG; OpenAI asks for a square logo of at least 48 pixels, PNG, JPEG, WebP or SVG under 5 MiB, rasters at most 4096 pixels a side) | the console's `public/logos/lifesight-icon.svg` |

Left out on purpose: `.claude-plugin/`, `.mcp.json`, `server.json`, `hooks/`, `guidance/`, `docs/`, `README.md`
(Claude Code, the MCP Registry and this repo's own readers). A ZIP carrying app references (`apps` or an
`.app.json`) or lifecycle hooks cannot be submitted (submission page, read 2026-10-02): `mcp.json` is the one
route to the server, and the checker refuses a package with either. The schemas the checker validates against
are vendored in `scripts/schemas/` from `https://agent-plugins.org/schemas/1.0.0/` (byte-identical to the live
copies on 2026-10-02).

## The listing fields, with their limits

Read from `developers.openai.com/plugins/deploy/submission` and `/plugins/build/plugins` on 2026-10-02.

| Field | Limit | Value | Count |
|---|---|---|---|
| `displayName` | 30 | Ask Lifesight (D-21) | 13 |
| `shortDescription` | 30 | MMM, incrementality, budgets | 28 |
| `longDescription` | 4000 | the jobs in the member's words (the twelve workflows), the terms of art, who it is for and that a workspace seat is needed for everything, the two sentences on writes and on promotion, the limitations | see the checker's output |
| `developerName` | 80 | Lifesight | 9 |
| `category` | one of the dashboard's titles | Productivity, **a placeholder**: the dashboard's list is not published; the owner picks at submission | |
| `capabilities` | 20, each 120 | seven, one per thing the tools do | |
| `defaultPrompt` | 3, each 128 | three starters, each "Use Ask Lifesight to ..." and figure-free | |
| `websiteURL`, `supportURL`, `privacyPolicyURL`, `termsOfServiceURL` | HTTPS, 1024; `supportURL` required for MCP review | `https://lifesight.io`, `https://support.lifesight.io/en/`, `https://lifesight.io/privacy-policy/`, `https://lifesight.io/terms-of-service/` (all answered 200 on 2026-10-02; `www.lifesight.io` redirects to the bare host; `lifesight.io/contact` is a 404, so support is the help centre) | |
| `logo`, `composerIcon` | square, 48 px or more | `./assets/logo.svg`, `./assets/icon.svg` | |
| `brandColor` | | `#1b3a5c`, the mark's own | |

The plan asked for a subtitle carrying the search terms; the field is 30 characters, so the terms live in the
description and in `keywords`.

The root `description` and the `longDescription` are the plugin's portable identity: the directory is shared by
ChatGPT and Codex, so neither names a host (the checker refuses "ChatGPT", "Claude" or "Codex" in either).

The copy rules the guidelines state and the checker holds: no "MCP" or "Plugin" in the name; no pricing,
subscription, trial, tier, fee, discount or promotional-offer language ("promotion" is the product's word for
making a plan the workspace default and appears once, in the sentence OpenAI requires); nothing that steers the
model toward this plugin or against another (best, recommended, official, rather than, instead of); no digit at
all in the listing copy (model-visible prose is not provenance); no tab or control character; every `keywords`
entry present in the description; one version across `plugin.json` and `.claude-plugin/plugin.json`.

## The search terms (for CG3.6's post-listing search check)

`keywords` in `plugin.json`, each also present in the description (the checker asserts it): marketing mix
modeling, MMM, media mix modeling, incrementality, causal attribution, geo lift experiments, budget optimisation,
budget optimization, budget reallocation, saturation, diminishing returns, ROAS, marginal ROI, marginal ROAS,
attribution, marketing measurement, spend anomalies, data health. CG3.6 searches the directory for each and
records the rank.

## What the owner supplies at submission (CG3.4), not in this package

The submission itself, step by step with every input and attestation, is `docs/CHATGPT_SUBMISSION.md`. Since CG3.4
the manifest carries the five positive and three negative review cases (`extensions.com.openai.review`, taken from
the harness's selection eval), the commerce declaration and the release notes; the items below stay the owner's.

- The category, from the dashboard's list.
- `extensions.com.openai.publication.countries`: a manifest field (uppercase ISO country codes, an allowlist;
  the checker validates the shape when present). The owner selected US, GB, AU and NZ on 5 October;
  omission is allowed by OpenAI and preserves saved portal targeting. A release note for
  the version goes in `publication.release_notes` beside it.
- The reviewer's test account on the populated test workspace (EXT-2) and the video walkthrough, whose URL goes
  into `extensions.com.openai.review.demo_recording_url` (`--submission` on the checker refuses a package without
  it). The eight test cases are in the manifest already and read-only in the dashboard once uploaded.
- The privacy page's content against OpenAI's five topics (categories of personal data, purposes, recipients,
  retention timelines, controls) plus one sentence each on what the host receives, what Lifesight stores and
  what it never receives; the URL exists today, the content is the owner's.
- The domain-verification token into the gateway's `OPENAI_APPS_CHALLENGE_TOKEN` (CG2.2).
- The repo names `Apache-2.0` in three manifests and carries no LICENSE file (pre-existing on the Claude side);
  a licence is a public contract, so adding the file is the owner's.
- A re-upload after any change to metadata or skills needs a new version in both plugin manifests.

## Findings recorded here

- ~~The Claude side (`.mcp.json`, `server.json`) still names `https://mcp.lifesight.io/mcp`~~ **CLOSED,
  verified 2026-10-06:** `.mcp.json`, `mcp.json`, `server.json`'s `remotes` and the README's install
  section all name `https://ask.lifesight.io/mcp`. The old 1.0 host appears nowhere in this repository
  except in this note. `server.json` DOES still say version 0.1.0 while the plugin manifests say 0.2.1
  (the registry entry was published at 0.1.0) — that half of the finding stands, and it is the Claude
  listing build's change, not this one; the checker compares the two plugin manifests only.
- Three skills quote member utterances and argument formats with figures ("Meta says 4x", "what if I cut 10%",
  "+20%"). They are inputs, not platform figures, and they ship to Claude Code already; whether to reword them
  figure-free is a Claude-visible decision for that build.
- Scheduled tasks: the old builder appended an unverified ChatGPT scheduling promise. Version 0.2.1 removes
  it. Scheduling is not advertised until actual execution is verified.
- `claude plugin validate .` validates only `.claude-plugin/marketplace.json`; the plugin manifest and the skills
  are checked by `claude plugin validate --strict .claude-plugin/plugin.json` and `claude plugin validate
  --strict skills`. These Claude-specific validators were not rerun for the public preflight; the original package is preserved.
