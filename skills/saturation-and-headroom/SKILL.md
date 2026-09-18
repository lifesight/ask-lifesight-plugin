---
name: saturation-and-headroom
description: How far a channel can scale before returns fall, from its own response curve: headroom, marginal ROI, saturation level. Use for 'can I scale X', 'is Meta saturated'.
---
# Saturation and headroom

## When to use
"How far can I scale Google", "is Meta saturated", "where do returns fall off".

## How
1. `get_workspace_context` for the champion model and the channel's spelling (pass a channel by the names the context lists).
2. `get_channel_saturation_curves` for the channel on that model; pass `target_roas` only if the member named one. The curve is read off the model in the period's spend: no budget, no solve. A cap of N/A comes with a note: relay the note (the return stays above the target up to the last spend on the curve).
3. `get_mmm_report` with `sections` `marginal_roas` for the same model, to place the channel among the others.

## Output
The channel's current spend, its marginal ROI at that point, the headroom and the saturation level exactly as the curve result gives them; where it stands against the other channels' marginal ROAS; the one sentence of advice the figures support.

## Refuse
Reading a point off the curve yourself: what a channel would get under a budget comes from `start_budget_optimisation`, not from the curve. Never turn headroom into a recommended spend figure the result did not carry.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
