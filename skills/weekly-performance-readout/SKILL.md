---
name: weekly-performance-readout
description: What moved this week across channels in the model's terms, with data caveats stated first. Use for weekly readouts, Monday summaries, 'what happened last week'.
---
# Weekly performance readout

## When to use
"What moved this week", "give me the Monday summary", "how did last week go by channel".

## How
1. `get_workspace_context`: the champion model, its KPI and currency, the data window, the promoted plan. If the data window ends before last week, say so first: the model cannot describe days it has not seen.
2. `get_mmm_report` for the champion with `sections` `contributions`, `incremental_revenue`, `roi_spend_share`, `platform_spend`, twice: `start_date`/`end_date` for the last full week, then the week before (ISO dates from `today` in the context). The two reads are how the compare is grounded; never compute a week-on-week change the results do not carry.
3. `get_data_source_health`: a source that is stale or failing makes its channel's movement a data issue, not a performance change. Say which before reading anything as a trend.
4. `detect_spend_anomalies` with `window_days` 7: an anomaly is a line in the readout, not a conclusion.
5. `get_cue_cards`: what the product already flags. Point to a card; do not repeat it.

## Output
Under **This week**: at most five lines, one per channel that moved, each with the figure, its unit and the window as returned. Under **Watch**: data issues and anomalies. Under **Next**: one action the member could take in the product (a plan, a test, a data fix).

## Refuse
Ranking channels by a figure the report did not carry; calling a one-week change a trend; a figure without its unit and window.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
