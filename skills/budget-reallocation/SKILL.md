---
name: budget-reallocation
description: Reallocate a stated budget across channels with the MMM optimiser and explain the moves from the response curves. Use for 'how should I split', 'reallocate', 'optimise my budget'.
---
# Budget reallocation

## When to use
"How should I split X across channels", "reallocate my budget to maximise return", "what if I cut 10%".

## How
1. `get_workspace_context`, then `get_current_budget_allocation` for today's split: every constraint band is a multiple of what a channel spends today, so the current split is the anchor of everything that follows.
2. `start_budget_optimisation` with `mode` `maximise`. `total_budget` exactly as the member stated it, as text: a figure ("500000") or an expression on today's spend ("current -10%"); blank reallocates what they spend today (say so). `time_period` as stated (blank = a quarter, disclosed). `constraint_type` as stated (blank = Moderate, disclosed): Current keeps channels where they are, Conservative, Moderate and Aggressive widen the bands, Custom takes `channel_overrides` the member named. `sections` `allocation` and `forecast`. Never pass dates: the plan window is derived from the horizon and the model's own data.
3. If the result is a handle (`data.status` `running`), read `get_budget_optimisation` every `poll_after_s` seconds until `completed`. One solve runs at a time on a connection.
4. `get_channel_saturation_curves` for the two channels the plan moves most: headroom and marginal ROI explain the move.

## What-ifs
"What if I increase Google by 20%" is an ordinary optimisation with one channel pinned: `constraint_type` `Custom` and `channel_overrides` with `min_spend` and `max_spend` both at the target figure. Take the channel's current spend from `get_current_budget_allocation` and pass the figure the member wants; never do the percentage yourself. A floor with no ceiling is not a pin.

## Output
A table of channels with current spend, optimised spend and the delta as the result gives them; the forecast outcome; two sentences on why the top moves make sense from the curves. Say what was held and what moved. The scratch scenario is not a saved plan: offer `save_budget_plan` under a name the member gives (needs the `mia.write` scope).

## Refuse
Inventing a budget, a horizon or a constraint the member did not state; promising an outcome the forecast section did not carry; a budget far from today's spend without saying first that the bands may not place it.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
