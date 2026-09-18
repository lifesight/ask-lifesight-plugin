---
name: experiment-readout
description: What a completed geo experiment found and what it did not: lift, confidence, significance, markets, pre-period fit. Use for 'what did the test show', 'was the lift significant'.
---
# Experiment readout

## When to use
"What did the Google geo test show", "was the lift significant", "which markets were test and control".

## How
1. `get_geo_experiments` with `name` (part of it is enough) or `experiment_id`; filter by `status`, `kind` or `channel` as the platform names them (Meta and Facebook are different names: when one finds nothing, try the other). The list carries no results: never quote a lift from it. If several match, list them and ask.
2. `get_geo_experiments` with the `experiment_id` and `sections` `results`, `lift_over_time`, `pre_period_fit`, `control_markets`; add `power_curve` when the result was not significant, `progress` while it is still running.

## Reading it
- The record says why it was run (the hypothesis) and what it was designed on (the pre-treatment window, not the treatment window). Never invent a hypothesis when the record carries none.
- A live experiment carries `progress`: lead with where it stands and the day count.
- A failed experiment carries the platform's own reason: give it in plain words, do not read the report again.
- Significance is the platform's call; a non-significant result measured nothing.

## Output
One line with the lift, its confidence interval and significance as returned; one on the treatment and control markets and how well the pre-period fitted; one on what the result means for the channel's measured return; then **Not established** for what the test did not measure.

## Refuse
Calling a non-significant result a lift; extrapolating the lift to spend levels the test did not run; quoting a figure from the list rather than the report.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
