---
name: model-health-check
description: Whether the champion MMM model can be trusted for planning: accuracy, backtests, calibration, attribute quality, collinearity, in plain terms. Use for 'can I trust this model', 'is the model any good'.
---
# Model health check

## When to use
"Can I trust the model", "how accurate is it", "which channels does it get wrong", "is it calibrated".

## How
1. `get_workspace_context`, then `list_mmm_models` with `include_challengers` true: which model is the champion, how many challengers exist, the data window.
2. `get_mmm_report` for the champion with `sections` `accuracy`, `backtests`, `calibration`, `attribute_quality`, `input_correlation`. One call fetches them together; a section the platform could not answer comes back as unavailable in its slot: say which, never treat the whole read as failed.
3. `get_geo_experiments` with `status` COMPLETED: which channels have a lift test the model could be calibrated on.

## Reading the sections
- `accuracy` is the fit over the training window; `backtests` the holdout performance, which is the one to plan on.
- `calibration` names the channels anchored by a lift test; an unanchored channel's return is fitted, not measured.
- `attribute_quality` is the model's own flag per channel (why the optimiser is cautious on it); it is not the attribution module.
- `input_correlation`: channels that move together cannot be told apart by the model; say so where it applies.

## Output
A verdict line (fit for planning, use with care, not yet), then one line each for accuracy, holdout backtests, calibration, attribute quality and collinearity with the figure or flag the section carried; then what would raise confidence (a lift test on a named channel, a calibration).

## Refuse
Grading the model on a metric the report did not carry; a verdict that hides an unavailable section.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
