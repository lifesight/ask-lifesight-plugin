# OpenAI public package preflight

The public builder validates a portable Ask Lifesight package and the actual ZIP; production behavior, privacy policy content and portal scan results remain separate checks.

## Source validation

[[scripts/openai_preflight.py#check_source]] checks metadata, safe assets, review field shapes and parsed skill YAML before packaging.

Version 0.2.1 quotes seven descriptions containing colons, removes the stale read-only review wording and describes model forecasts as estimates. The owner selected US, GB, AU and NZ. Country omission is valid in the portable ZIP; imported targeting still needs portal confirmation.

## Archive validation

[[scripts/openai_preflight.py#check_zip]] refuses unsafe paths, normalization collisions, symlinks, unsupported private components and excessive archive sizes, then validates the extracted public payload.

The builder has explicit draft and submission-metadata modes. It adds no scheduled-task promise. A successful local check does not upload, submit, attest or publish anything.

## Regression coverage

The tests exercise malformed skill YAML, unsafe archives, credential-bearing URLs, invalid metadata, symlink leakage and incomplete final review materials.

Run `uv run --no-project --with pyyaml python -I tests/test_openai_preflight.py`. The current source and draft ZIP pass; final metadata mode remains blocked until a real accessible video URL is supplied. Dedicated reviewer execution and production MCP/skill scans require separate evidence.

## Production profile alignment

[[scripts/openai_preflight.py#production_profile]] loads the pinned assistant-only golden surface; [[scripts/openai_preflight.py#check_tool_profile]] rejects unavailable operation references in packaged skills and review cases.

Version 0.2.2 targets the production measurement front door, retaining read/write/decide. The manifest no longer promises documentation search or Jira support; anomaly triage uses returned anomalies, health and optional matching attribution reads, with an honest console fallback.

## Reference refresh

[[scripts/sync_production_profile.py#capture_profile]] resolves a harness commit and checks its golden names against the assistant-only allowlist. [[scripts/openai_preflight.py#render_tool_reference]] renders the public reference.

Run the sync script with `--harness-repo` and the intended `--ref`, then use `--check` to compare without writing. The fixture records the source commit and surface digest. [[scripts/openai_preflight.py#check_tool_reference]] rejects stale documentation; no fixture or internal script is added to the upload ZIP.

## Production profile regressions

The tests reject excluded and misspelled skill operations, legacy aliases, poisoned reference headings, unsupported review operations and tampered ZIP payloads while preserving all permission categories.

The production reference and test cases are not proof of real reviewer execution. Profile-schema, application-outcome and other separately audited runtime issues remain outside this F05 package change.
