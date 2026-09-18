---
name: attribution-reconciliation
description: Why the MMM model, the causal read, the ad platform's own reporting and the last lift test disagree on a channel, and which to plan on. Use for 'these numbers disagree', 'is the platform ROAS real', 'what is the real return of X'.
---
# Attribution reconciliation

## When to use
"Meta says 4x, the model says 2x", "is the platform's ROAS real", "what is the real return of Google".

## How
1. `get_workspace_context` for the promoted plan's model.
2. `compare_channel_measurements` for the channel with that model: the four measurements side by side (the model's contribution, the causal read, the channel's own reporting, the last completed lift test), each with its qualification (uncalibrated, attribution window, confidence interval, significance), the spread between them, which to plan on and what would settle it. This IS the analysis; it is coded, and it never averages. The trust order is fixed: a significant lift test, then the causal read, then the model, then the channel's own reporting. Fewer than three methods is no verdict.
3. `get_attribution_report` with `analyses` `incrementality` and `performance` over the same window if the member wants the campaign level under the channel. Pacing needs CAMPAIGNS or finer; creative ranking needs AD.

## Reading it
- The channel's own reporting counts conversions it may not have caused; the causal read is the platform's incremental view; the model's return is fitted over the whole window unless a test calibrated it.
- A lift test with no return of its own is listed with its lift and p-value but never moves the spread.

## Output
The four figures with their labels and qualifiers exactly as returned, the spread as returned, the read to plan on with its reason, and what would settle the disagreement (a lift test on the channel, a calibration on the test that ran).

## Refuse
Averaging the methods; picking a "true" number; trusting the channel's own reporting over an incremental read; a verdict when the tool raised none.

## Rules that hold for every step

- Start with `get_workspace_context` if you have not this session: it names the workspaces, the champion model, its KPI, currency and data window, the promoted plan, today's date.
- Quote figures exactly as the tool results give them, with their unit and currency. The server computes totals, shares and deltas where they are given; quote those rather than computing your own.
- A `needs_input` warning is a question to put to the member with the options it lists, never a value to guess. A `no_data` warning is a fact to state, never a reason to call again with the same arguments.
- Before you show figures you did not read verbatim, call `check_figures` with your draft and show its `redacted_draft` if any figure is unverified.
- Every result carries `provenance`: which platform read each figure came from. Name the model and the window once, so the member knows what the figures rest on.
