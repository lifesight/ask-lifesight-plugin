---
name: scenario-planning
description: Several budget scenarios side by side on one model and one horizon, with the server's deltas. Use for 'compare three budgets', 'what does +20% versus -20% look like'.
---
# Scenario planning

## When to use
"Compare a 400k, 500k and 600k plan", "show me current versus +20%", "which scenario is the most efficient".

## How
1. `get_workspace_context`; confirm the model and the horizon the member wants.
2. `compare_budget_scenarios` once, with `scenarios` exactly as the member stated them: a `label` and a `total_budget` each (a figure, or an expression on today's spend), the same `constraint_type` and `time_period` for all. It runs the solves itself, aligns them and computes the deltas. Do not also run `start_budget_optimisation` per scenario: that solves everything twice.
3. `get_channel_saturation_curves` for a channel whose allocation swings most across the scenarios, if the member asks why.

## Output
One table, one column per scenario: total spend, the outcome forecast, the return multiple the result carries (ROAS is a multiplier, CPA an amount per unit), and the per-channel split; then one paragraph on where the scenarios differ and what each assumes (the same model, the same window, the same bands).

## Refuse
Adding a scenario the member did not ask for; computing a delta the compare did not return; calling the largest outcome the best without the return multiple beside it.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
