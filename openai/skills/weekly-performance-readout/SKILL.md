---
name: weekly-performance-readout
description: Compare complete weeks covered by the model across channels and lead with data caveats. Use for weekly readouts, Monday summaries and questions about what moved.
---
# Weekly performance readout

## When to use
"What moved this week", "give me the Monday summary", "how did last week go by channel".

## How
1. `get_workspace_context`: identify the champion model, KPI, currency and data window. Check whether the requested weeks are fully covered. If they are outside the window, state the coverage gap first and offer the two most recent consecutive complete Monday-to-Sunday weeks the model does cover. For a general weekly readout, use those latest covered weeks and state their dates. If there are fewer than two complete weeks, report available coverage without a week-to-week comparison.
2. `get_mmm_report` for the champion with `sections` `contributions`, `incremental_revenue`, `roi_spend_share`, `platform_spend`, twice: pass explicit `start_date` and `end_date` for each covered week. Use the same model and sections for both reads. Report a change figure only when the tools return it.
3. `get_data_source_health`: flag stale or failing sources before interpreting channel movement. Freshness gaps limit the interpretation. Compare source coverage and the model window before attributing a cause.
4. Use `detect_spend_anomalies` for recent spend signals when its reporting window is relevant. Match the dates and seek corroborating source or platform data before interpreting the cause. Keep later anomalies separate from the covered weeks.
5. `get_cue_cards`: what the product already flags. Point to a card; do not repeat it.

## Output
Under **Covered weeks**: at most five lines, one per channel that moved, each with the figure, its unit and the window as returned. Under **Watch**: data issues and anomalies. Under **Next**: one action the member could take in the product (a plan, a test, a data fix).

## Refuse
Ranking channels by a figure the report did not carry; calling a one-week change a trend; a figure without its unit and window.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
