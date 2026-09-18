---
name: experiment-roadmap
description: Which channels to test next, from where the model is least certain: unanchored, flagged, high spend share. Use for 'what should we test next', 'where do we need a lift test'.
---
# Experiment roadmap

## When to use
"What should we test next", "which channels need calibration", "plan our lift tests for the quarter".

## How
1. `get_workspace_context`, then `get_mmm_report` with `sections` `calibration` and `attribute_quality`: the channels with no lift-test anchor and the ones the model flags.
2. `get_mmm_report` with `sections` `roi_spend_share`: where the spend is. A channel that carries a large share of spend on a fitted, unanchored return is where a test pays back first.
3. `get_geo_experiments` with `status` COMPLETED and RUNNING: what has been tested or is running now, so the roadmap does not repeat it.
4. `get_geo_experiments` with `sections` `recommendations` for the latest completed experiment if the member wants design options.

## Output
An ordered list of at most four channels to test, each with the reason in the model's own terms (unanchored, flagged, spend share) and the figure that says so; then what is already running or done.

## Refuse
Sizing a test or estimating its duration: the product's design flow does that; point to it.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
