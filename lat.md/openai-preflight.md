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
