# ChatGPT submission runbook — updated 5 October 2026

The public package is prepared as version `0.2.1`. Draft setup, review submission and publication are
separate milestones. Local checks cannot prove portal scan outcomes, reviewer access or production health.

## What is prepared

The package contains a production MCP endpoint, twelve workflow skills, branding, listing metadata,
five positive and three negative case definitions, commerce disclosure and release notes. It preserves
read, write and decide. The owner selected United States, UK, Australia and New Zealand: `US`, `GB`, `AU`, `NZ`.

Seven previously malformed YAML descriptions are quoted correctly. The optimisation case no longer calls
the entire connection read-only. Model forecasts are described as estimates. The public builder no longer
adds an unverified ChatGPT scheduled-task instruction. Existing private hooks/bindings remain in the
original source; the public ZIP excludes them.

## Build a draft ZIP

Draft mode checks package structure and present metadata while allowing unfinished review materials.

```bash
uv run --no-project --with jsonschema --with pyyaml python -I scripts/check_openai_package.py
uv run --no-project --with jsonschema --with pyyaml python -I scripts/build_openai_zip.py --draft
```

The builder checks the actual ZIP, including its manifests, skill YAML, paths and assets. It includes only
`plugin.json`, `mcp.json`, `skills/` and `assets/`. Record the SHA-256 of the exact artifact uploaded. Draft
validation is not a successful final review or tool scan.

## Portal draft and domain setup

Use the intended verified publisher and project when creating the draft and connecting the actual server.

1. Confirm verified business identity and submission permission for the organization/project. The package
   cannot prove either. Follow the current portal's project eligibility checks.
2. Upload the valid ZIP with its MCP server included; resolve upload validation errors before proceeding.
3. Open MCPs, Connect. Confirm `https://ask.lifesight.io/mcp` and OAuth. Obtain the portal's exact challenge
   URL and token. The owner selected `https://ask.lifesight.io`; a token has not been issued yet.
4. Deploy the prepared gateway configuration with that token, check public HTTP 200 and exact `text/plain`
   body, then verify in the portal. G01's deployment worktree is `ls4x/k8s-wt-g01-domain`. Keep the token
   out of chat and audit reports.
5. Connect and authenticate, wait for the tool scan, inspect all discovered tools and any findings. After
   server fixes use Reconnect or Rescan as appropriate. Do not scan staging and call it production proof.

## Required closeout before review

Review the saved draft and exercised production experience before submitting for human review.

- Resolve required setup/validation errors and inspect all skill safety/security scan results. Our target is
  zero unresolved findings; OpenAI permits some nonblocking findings to be sent for review.
- Correct the published privacy policy to reflect actual AI processing, recipients, retention and controls.
  A reachable URL alone is insufficient. Review terms/support coverage and test the public contact route.
- Close the access-control and scope gaps in the MIA audit, particularly support-ticket ownership,
  persistent file imports, bounded investigation reach and approval targets. Review actual tool annotations.
- Run the five positives on a dedicated sample-data reviewer account with read, write and decide access.
  Compare actual tool calls and outputs against the definitions; keep the three negative outcomes too.
  Definitions in the manifest do not claim execution. Promotion requires the human gate in Lifesight.
- Record and host a walkthrough of actual interactions. Verify playback without requesting private access,
  then set `review.demo_recording_url` to its real HTTPS URL. Do not substitute a script or placeholder URL.
- Enter reviewer credentials, login URL, workspace and sign-in instructions only through secure portal
  fields. Test immediate login without MFA approval, codes, magic links or private-network dependencies.
- Confirm the imported publisher, cases, release notes and countries. Test availability for the chosen
  regions, including the UK. Confirm commerce=false accurately describes the submitted tools.
- Inspect the uploaded metadata version and the current production tool snapshot together. Reupload replaces
  package contents; omitted fields can preserve earlier saved values. Do not assume a new ZIP clears them.

## Local final-metadata checks

Final-metadata mode demands the actual demo URL and complete review definitions. Online checks remain separate.

```bash
uv run --no-project --with jsonschema --with pyyaml python -I scripts/check_openai_package.py --submission
uv run --no-project --with jsonschema --with pyyaml python -I scripts/build_openai_zip.py --submission
uv run --no-project --with pyyaml python -I tests/test_openai_preflight.py
```

Country declarations are optional in the ZIP. Omitting them preserves portal targeting; an explicit empty
list removes restrictions. This package explicitly uses the owner's four selected codes. Final imported
targeting still needs confirmation in the portal. Optional dark assets and screenshots are not required;
screenshots are appropriate only if the tool scan reports a UI output template. This package has none.

## Review and publication

The authorized publisher completes attestations and controls when the reviewed package becomes public.

Once closeout is complete, select Submit for review and complete the real policy attestations. Do not attest
that unresolved privacy, access or reviewer-flow issues are fixed. When approved, select the approved version
and Publish plugin. Verify the listing URL and directory search, then run a post-publication connection smoke.
An approved version is not publicly listed until published. Metadata/skill changes need the package workflow;
hosted tool changes use deployment and rescanning. Keep the live tool contract compatible during review.

## Official sources and a documentation conflict

The current portal and official documentation define submission behavior; our checker covers local package rules.

[Submission](https://developers.openai.com/plugins/deploy/submission),
[validation errors](https://developers.openai.com/plugins/deploy/submission-errors),
[plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines),
[MCP review](https://developers.openai.com/plugins/deploy/app-review).

The guidelines explicitly say annotation justifications are no longer required, while the error reference
still lists `justification_required`. We preserve explicit accurate boolean annotations and do not invent
an undocumented wire field. If the portal reports that error, retain the exact finding and resolve the
conflict with OpenAI. Portal scan results remain unverified until actually observed.
