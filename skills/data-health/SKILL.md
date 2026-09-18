---
name: data-health
description: Whether the numbers can be trusted this week: sources, freshness, gaps, and which reads each gap dulls. Use for 'is the data fresh', 'why is Meta missing'.
---
# Data health

## When to use
"Is the data fresh", "why is Meta missing from the report", "did the sync run".

## How
1. `get_data_source_health` for every integration (no argument), then for one `integration` alone if the member named it.
2. `get_workspace_context`: the champion model's data window against `today`. A model whose window ends long before today is trained on data older than the sources.
3. `get_cue_cards`: data cards the product already raised.

## Output
One line per source with its status and last successful sync as returned; then **Gaps** (a source failing, a window that ended); then what each gap means for which reads: a stale source dulls attribution and anomalies before it touches the model.

## Refuse
Saying the data is fine when a source's status was not returned; guessing when a sync will run.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
