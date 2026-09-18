---
name: pnl-translation
description: The promoted plan in finance terms: spend, forecast outcome, return per unit of spend, current versus plan. Use for 'explain this to the CFO', 'what does the plan mean for the P&L'.
---
# P&L translation

## When to use
"Put the plan in finance terms", "what does this mean for the P&L", "the CFO wants the numbers".

## How
1. `get_workspace_context`, then `get_saved_plans` to find the promoted plan's id, then `get_saved_plans` with that `plan_id`: the optimised spend per channel, the totals and the forecast as the platform gives them, one entry per scenario with the promoted one marked.
2. `get_current_budget_allocation` for the current split beside it.

## Output
A table with total spend, forecast outcome and the return multiple (ROAS is a multiplier, CPA an amount per unit; use the ones the result carries), current versus plan, and the delta the result gives; then three sentences a finance reader can act on. State the plan window and the currency once.

## Refuse
Converting currencies; annualising; computing a margin or a payback the platform did not return; treating a forecast as a commitment.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
