# Ask Lifesight for Claude

Lifesight's marketing measurement inside Claude: marketing mix models (MMM), causal attribution,
geo-lift experiments, budget optimisation and saved plans, data-source health, spend anomalies,
creative performance, the member's cue cards and the product docs, over the Ask Lifesight MCP
server, plus the workflows members run most as skills.

Every figure comes from the Lifesight platform, with its unit, currency, model and window
stated beside it. The server computes the compares, shares and totals; the client quotes them.
No figure is ever estimated.

## Install

In Claude Code:

```
/plugin marketplace add lifesight/ask-lifesight-plugin
/plugin install ask-lifesight@lifesight
```

The first call opens the Lifesight console login page in your browser; sign in as usual (SSO and
MFA as in the product) and you come back connected, with every workspace you hold attached. No
key to handle. In claude.ai and Claude Desktop, add the connector `https://mcp.lifesight.io/mcp`
from the directory; the skills below are Claude Code's, the workflows are also served as MCP
prompts so every client gets them.

For headless use (CI, the Agent SDK), mint a personal access token in the console (Settings,
MCP) and send it as `Authorization: Bearer pat_...`; tokens last 90 days and are revoked from
the same page.

## Try it

Three prompts that use the connector end to end, each answered from your own workspace's data
with the platform read it came from named beside every figure:

| Ask | What happens |
|---|---|
| "Which channels are saturating and where is the headroom?" | `get_workspace_context`, then `get_channel_saturation` on the champion model: marginal ROI, saturation level and headroom per channel |
| "Optimise my Q4 budget at 5M and compare it with what is promoted" | `start_budget_optimisation` (inline or a handle you read back), then `compare_budget_scenarios` against the promoted plan |
| "Are my geo experiments agreeing with the model for paid social?" | `compare_channel_measurements`: the model's return, the causal read's, the ad platform's own and the last lift test's, side by side |

## What it can do

Start every session with `get_workspace_context`: the workspaces you hold and the active one,
the champion models with their KPI, currency and data window, the promoted plan, today's date.
`switch_workspace` moves the connection; every tool also takes `workspace_id` for one call.

| You ask | Tool |
|---|---|
| What drives revenue, how each channel contributed, ROI and spend share, marginal ROAS, accuracy, backtests, calibration | `get_mmm_report` |
| How far a channel can scale before returns fall | `get_channel_saturation_curves` |
| What is running now, measured incrementally: pacing, top creatives, incrementality against platform-reported figures | `get_attribution_report` |
| Why the model, the causal read, the platform and the last lift test disagree on a channel | `compare_channel_measurements` |
| What a geo experiment found | `get_geo_experiments` |
| How to split a budget, what a scenario would return | `start_budget_optimisation`, `get_budget_optimisation`, `compare_budget_scenarios` |
| What plans exist and what the promoted one proposes | `get_saved_plans`, `get_current_budget_allocation` |
| Save a plan by name (scope `mia.write`) | `save_budget_plan` |
| Make a plan the workspace's default, with your approval in the product (scope `mia.decide`) | `request_plan_promotion`, `get_approval_status` |
| Is the data fresh, what looks odd in spend | `get_data_source_health`, `detect_spend_anomalies` |
| What the ad platforms report, in words | `query_ads_data` |
| Which figures in a draft the tool results actually produced | `check_figures` |
| Raise a ticket with Lifesight support, or check one (scope `mia.write`) | `raise_support_ticket` |
| A compound investigation by Lifesight's own investigator, Mia, on a thread you can open in the product | `start_mia_investigation`, `get_mia_investigation` |

The full reference, generated from the server's published surface: [docs/TOOLS.md](docs/TOOLS.md).

## Skills

Twelve workflows, one skill each, loaded when the question matches: weekly performance
readout, budget reallocation, scenario planning, model health check, saturation and headroom,
attribution reconciliation, experiment readout, experiment roadmap, anomaly triage, board
briefing, P&L translation, data health. Each names the tools in order, the output shape and what
Claude refuses to do (invent a budget, average two measurements, call a one-week change a trend).

## What a write does, and does not do

- `save_budget_plan` saves an optimised plan under a name you give; it appears in the console
  under your name. It does not change what the workspace plans against.
- `request_plan_promotion` never promotes. It optimises, then pauses; you approve or reject it
  in the Lifesight product (the request shows in your Mia conversation list as "Claude
  connection"), and `get_approval_status` reads the decision. Promotion sets the workspace's
  default plan, the one the team plans against. It is not a financial transaction: no money
  moves, no payment runs, no ad-platform spend changes.
- A connection holds `mia.read` unless a workspace admin grants `mia.write` or `mia.decide` to
  it. A scope the connection does not hold is refused, and Claude says so.

## Limits

- One optimisation at a time per connection; a solve answers inline within about 20 seconds,
  otherwise you get a handle to read (`get_budget_optimisation`). An investigation by Mia is
  read the same way (`get_mia_investigation`).
- A result is cut to fit the transport (about 40,000 characters of payload); the `warnings`
  say what was cut and how to narrow (a section, a window, a filter, `response_format`
  `concise`). The product shows all of it.
- `check_figures` checks up to 300 figures against the last 20 successful results of the
  connection's thread.
- Rate limits, enforced by the Lifesight gateway (token buckets; a request over the limit is
  `429` and Claude retries after a moment):
  - tool calls: 10 per second, bursts of 20, per member in a workspace (each connection has its
    own bucket, separate from the product's);
  - before a call is authenticated: 5 per second, bursts of 20, per source address;
  - the sign-in and token endpoints (connect, refresh): 5 per second, bursts of 10, per source
    address.
- A connection stays signed in while you use it: its token lives 1 hour and refreshes itself,
  and the connection lapses only after 30 days without use (then Claude asks you to sign in
  again). It keeps the workspace you switched to and its conversation threads for the same
  time. A personal access token lives 90 days. Disconnecting a client in Lifesight (Settings,
  Claude & MCP) takes effect within a minute.

## Privacy

Every call runs as you, in a workspace you hold, and lands on your own conversation thread in
Lifesight with the same audit trail as the product. The server never forwards your token to the
platform; it uses its own short-lived credential for your identity. Lifesight's privacy policy:
https://lifesight.io/privacy-policy/.

## Changelog

- 0.1.0 (2026-09-18): first release for the parallel window: 28 tools, 12 skills and prompts,
  OAuth through the console login, personal access tokens.
