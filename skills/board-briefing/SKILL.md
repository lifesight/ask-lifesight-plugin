---
name: board-briefing
description: Marketing effectiveness for a leadership audience: five statements, each backed by one read, no jargon. Use for 'board summary', 'exec update', 'one page for leadership'.
---
# Board briefing

## When to use
"A page for the board", "the exec update on marketing", "what do I tell leadership".

## How
1. `get_workspace_context`.
2. `get_mmm_report` for the champion with `sections` `contributions`, `incremental_revenue`, `roi_spend_share` over the last quarter (`start_date`/`end_date` from `today`).
3. `get_saved_plans`: which plan is promoted and what it proposes.
4. `get_geo_experiments` with `status` COMPLETED: one proof point from a test, if there is one.

## Output
At most five statements, one sentence each, each with one figure as returned and its unit, in this order: what marketing drove; where the return is highest; where spend and return diverge; what the plan in force changes; what was proven by test. End with **Caveats**: the model's window and any unavailable section.

## Refuse
Jargon (say "incremental revenue", not iROAS, and explain it once); a figure without its unit; a forecast; a comparison the reads did not carry.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
