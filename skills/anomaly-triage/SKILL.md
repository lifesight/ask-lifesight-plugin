---
name: anomaly-triage
description: Sort recent spend anomalies into data issues and real changes, with the ad platform's own figures beside them. Use for 'what is this spike', 'anything odd in spend'.
---
# Anomaly triage

## When to use
"Anything odd in spend this week", "why did TikTok spike", "is this a data problem".

## How
1. `detect_spend_anomalies` with `window_days` as the member said (blank = the tool's default).
2. `get_data_source_health`: an anomaly on a source that is stale or failing is a data issue first, whatever the figure says.
3. For each remaining anomaly, `query_ads_data` in words for what the ad platform reports about that source and window. These are platform-reported figures, not incremental; say so.

## Output
Two lists. **Data issues**: the source, since when, what the health read says. **Real changes**: the source, the figure and the window as the anomaly result gives them, what the platform reports. Then one recommended check per real change.

## Refuse
Explaining an anomaly's cause beyond what a read showed; calling a data issue a performance change; calling a platform-reported change incremental.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
