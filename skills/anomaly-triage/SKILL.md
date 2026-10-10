---
name: anomaly-triage
description: Triage recent spend anomalies using source health and the returned measurements, distinguishing data gaps from observed changes without inventing a cause. Use for 'what is this spike', 'anything odd in spend'.
---
# Anomaly triage

## When to use
"Anything odd in spend this week", "why did TikTok spike", "is this a data problem".

## How
1. `detect_spend_anomalies` with `window_days` as the member said (blank = the tool's default).
2. `get_data_source_health`: report stale or failing sources as data-quality caveats before interpreting their anomalies. Source health alone does not establish an anomaly's cause or prove that a change is real.
3. State each anomaly's source, comparison window and figures as returned. If there are no anomalies, say so; do not search for a change the result did not show.
4. If the question needs corroboration and the anomaly supplies concrete matching dates, use `get_attribution_report` with that `start_date` and `end_date` for the relevant performance or pacing read. Distinguish incremental measurements from platform-reported figures. Missing coverage is a limit, not corroboration; do not substitute a model's different window or guess missing dates.
5. Raw ad/campaign drill-down and a backend investigation are unavailable through this connection. If the bounded reads cannot explain the change, say what remains unknown and suggest the specific source or campaign to inspect in the Lifesight console. Do not invent a replacement tool or retry a no-data request unchanged.

## Output
Two lists when applicable. **Data issues or gaps**: the source, since when if returned, and what the health read establishes. **Observed changes**: the source, figure and window from the anomaly result, any matching corroboration, and what remains unexplained. Then one concrete next check per observed change. If all sources are healthy or no anomaly is detected, state that result directly.

## Refuse
Explaining an anomaly's cause beyond what a read showed; calling a data issue a performance change; calling a platform-reported change incremental.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
