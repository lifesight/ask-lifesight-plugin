# F05 — Production package alignment

Prepared 10 October 2026 on `codex/f05-production-profile`, based on public-plugin main `e30678c13d3becb0472e0d5202ae9151538f31ad`. Source remediation is complete; merge, package upload and the final portal scan remain release actions.

## Package changes

Version 0.2.2 removes unavailable product-documentation search and support-ticket promises from the listing. The shared README now describes the production assistant-only front door rather than the broader development catalog. Both plugin manifests use the same version; the endpoint, countries, starter prompts and authentication configuration are preserved.

Anomaly triage uses `detect_spend_anomalies`, `get_data_source_health` and, only when concrete matching dates/coverage are available, `get_attribution_report`. It distinguishes data-quality caveats from observed changes, accepts no-anomaly/no-data results and states when raw campaign investigation requires a console check. Healthy data alone does not prove an anomaly's cause.

Read, write and decide remain available: 20 read-scope tools, `save_budget_plan` with write, and `request_plan_promotion` with decide and the human gate. No production tool or permission was removed or added.

## Source of truth and prevention

The fixture `tests/fixtures/production-mcp-surface.json` pins the assistant-only golden surface from harness commit `2fecca00d2eac65391c17cf9d14e5e79e8eb1fa8`. Its canonical surface SHA-256 is `85fe4355ff66ad512468184d0aa53812e8100d7047d801dab7c3499fbda1f34e`.

`scripts/sync_production_profile.py` reads the exact resolved Git commit, checks the golden names against its production allowlist, and generates `docs/TOOLS.md`. It does not import/run the harness or fetch a remote. `--check` compares the fixture and reference without writing.

The package validator uses that fixture, not headings in a development tool reference, for skill and review-case availability. It rejects unavailable or misspelled operation references, including legacy ads aliases, while distinguishing schema/result fields from operations. Review case operation lists allow only actual tool names. The ZIP's extracted payload is checked against the same contract; the fixture and reference are not included in the public ZIP.

These checks establish syntactic tool availability, not semantic correctness of every possible natural-language claim. The changed listing and anomaly instructions were also reviewed directly.

## Verification

The local package checker and draft ZIP build pass. The profile/reference matches the fetched harness `origin/main`; the generated reference contains exactly 22 tools. The regression suite passes 29 tests, including rejection of poisoned references, excluded skills, legacy aliases, invalid review operations, a tampered fixture and unavailable operations inside the actual ZIP. Scoped Python lint and `lat check` pass.

The upload remains a 16-file public ZIP: manifests, twelve skills and two SVGs. The final-submission mode still requires the actual recording URL; this F05 change does not bypass that separate material check or claim all other audit findings are closed. No authenticated ChatGPT rehearsal or model-driven evaluation was performed for the rewritten skill in this remediation.

## Release and targeted rehearsal

Anil should review and commit the changes in this public-plugin worktree, push the branch and merge through the normal repository process. Rebuild the draft ZIP from the merged release source and upload the intended candidate after the other necessary fixes. This package-only remediation does not require a gateway/frontend/harness deployment.

With the ready sample accounts, ask about a spend spike and a no-anomaly window. Confirm that only available tools are selected, dates are not guessed, stale sources are disclosed, and an unestablished cause is stated as unknown. Keep the console escalation as a manual next check, without an unavailable tool call. Confirm the final portal skill/tool scan sees the matching production profile.

A later harness/profile change requires a fresh sync and regression run. Do not label F05 fully released from a source commit alone: the uploaded package and scanned MCP surface must agree.
