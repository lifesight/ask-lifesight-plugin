# Ask Lifesight for Claude and ChatGPT

Lifesight's marketing measurement inside Claude: marketing mix models (MMM), causal attribution,
geo-lift experiments, budget optimisation and saved plans, data-source health, spend anomalies,
creative performance and the member's cue cards, over the Ask Lifesight MCP
server, plus the workflows members run most as skills.

Every figure comes from the Lifesight platform, with its unit, currency, model and window
stated beside it. The server computes the compares, shares and totals; the client quotes them.
Figures are sourced from tool results; model forecasts and optimisation results are estimates, not guaranteed outcomes.

## ChatGPT

The same package is a ChatGPT plugin: `plugin.json` (the open agent-plugins manifest with OpenAI's
`extensions.com.openai.interface` block), `mcp.json` (the server at `https://ask.lifesight.io/mcp`), the
twelve skills and the brand assets. `uv run --no-project --with jsonschema --with pyyaml python -I scripts/build_openai_zip.py --draft`
runs local package and ZIP checks and writes `dist/ask-lifesight-chatgpt.zip` for the Plugins dashboard;
Publisher listing notes and submission procedures are maintained internally.

## Install

In Claude Code:

```
/plugin marketplace add lifesight/ask-lifesight-plugin
/plugin install ask-lifesight@lifesight
```

The first call opens the Lifesight console login page in your browser; sign in as usual (SSO and
MFA as in the product) and you come back connected, with every workspace you hold attached. No
key to handle.

In chat (claude.ai and Claude Desktop) and in Cowork, add the plugin, then connect the server
`https://ask.lifesight.io/mcp` from the plugin's Connectors tab. The skills below work in chat,
Cowork and Claude Code alike. The connector also serves eleven of these workflows as MCP
prompts. Anomaly triage is available as a plugin skill; it is not currently exposed as an MCP
prompt in this restricted profile.

| | Skills | House-style hook | Connector |
|---|---|---|---|
| Chat (claude.ai, Claude Desktop) | Yes | Ignored | Plugin's Connectors tab |
| Cowork | Yes | Yes | Plugin's Connectors tab |
| Claude Code | Yes | Yes | Connects on first call |

For headless use (CI, the Agent SDK), mint a personal access token in the console (Settings,
MCP) and send it as `Authorization: Bearer pat_...`; tokens last 90 days and are revoked from
the same page.

## Try it

Three prompts that use the connector end to end, each answered from your own workspace's data
with the platform read it came from named beside every figure:

| Ask | What happens |
|---|---|
| "Which channels are saturating and where is the headroom?" | `get_workspace_context`, then `get_channel_saturation_curves` on the champion model: marginal ROI, saturation level and headroom per channel |
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
| Save a plan by name (scope `lifesight.write`) | `save_budget_plan` |
| Make a plan the workspace's default, with your approval in the product (scope `lifesight.decide`) | `request_plan_promotion`, `get_approval_status` |
| Is the data fresh, what looks odd in spend | `get_data_source_health`, `detect_spend_anomalies` |
| Which MMM models are available | `list_mmm_models` |
| Which creative tactics a model measures and the creative data returned for it | `get_creative_performance` |
| What needs attention in the workspace | `get_cue_cards` |
| Record feedback on an existing product answer you own | `send_feedback` |
| Which figures in a draft the tool results actually produced | `check_figures` |

The connector exposes 22 tools. The profile-scoped reference is [docs/TOOLS.md](docs/TOOLS.md);
accepted arguments come from the connected server's advertised schema. Backend investigations,
model-backed ads queries, semantic product-documentation search and Jira support operations
are not available through this connection. For help, use [Lifesight support](https://support.lifesight.io/en/).

## Skills

Twelve workflows, one skill each, loaded when the question matches: weekly performance
readout, budget reallocation, scenario planning, model health check, saturation and headroom,
attribution reconciliation, experiment readout, experiment roadmap, anomaly triage, board
briefing, P&L translation, data health. Each names the tools in order, the output shape and what
Claude refuses to do (invent a budget, average two measurements, call a one-week change a trend).

## House style

The plugin loads a short house style into every Claude Code and Cowork session
([guidance/house-style.md](guidance/house-style.md), through a `SessionStart` hook): draw a chart
wherever a result has a shape, ask the tools for `detailed` results so there is something to draw,
and the chart each kind of question gets (saturation questions always get the response curve with
its inflection point, operating point and cap marked). Charts plot only what the results carry,
labelled with the values as returned. It applies only to answers that use Ask Lifesight, and your
own instructions win over it.

In chat (claude.ai and Claude Desktop) plugin hooks are ignored, so the house style does not
load there; the skills still do. To get the house style in chat, paste the same file into a
Project's instructions or your profile preferences.

## Scopes and changes in Lifesight

Six tools can change state. The scope name is not a promise that a call has no side effects:

| Tool | Required scope | Effect |
|---|---|---|
| `switch_workspace` | `lifesight.read` | Changes the connection's active workspace |
| `send_feedback` | `lifesight.read` | Stores feedback on an existing product answer you own |
| `start_budget_optimisation` | `lifesight.read` | Creates scratch scenarios and can retire superseded scratch rows |
| `compare_budget_scenarios` | `lifesight.read` | Runs scenario work with scratch-state changes |
| `save_budget_plan` | `lifesight.write` | Saves a plan under the supplied name |
| `request_plan_promotion` | `lifesight.decide` | Requests a workspace-default change that needs human approval in Lifesight |

- `save_budget_plan` saves an optimised plan under a name you give; it appears in the console
  under your name. It does not change what the workspace plans against.
- `request_plan_promotion` never promotes. It optimises, then pauses; you approve or reject it
  in the Lifesight product (the request shows in your Mia conversation list as "Claude
  connection"), and `get_approval_status` reads the decision. Promotion sets the workspace's
  default plan, the one the team plans against. It is not a financial transaction: no money
  moves, no payment runs, no ad-platform spend changes.
- A connection holds `lifesight.read` unless a workspace admin grants `lifesight.write` or `lifesight.decide` to
  it. A scope the connection does not hold is refused, and Claude says so.

## Limits

- One optimisation at a time per connection; a solve answers inline within about 20 seconds,
  otherwise you get a handle to read (`get_budget_optimisation`).
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
  again). It keeps the workspace you switched to for as long as it stays connected. A personal
  access token lives 90 days. Disconnecting a client in Lifesight (Settings, Claude & MCP)
  revokes its access within a minute. These sign-in rules are separate from how long records
  are kept (see Privacy).

## Privacy

Calls run as you in a workspace you hold. Tool execution can record inputs and results on your
Lifesight thread; some operations use existing records without adding their full inputs/results.
Feedback is stored against the relevant answer. Draft text sent for figure checking is processed
against recorded results without being added to the thread by that operation. The audit record
uses an input digest rather than the raw inputs. The server uses a short-lived platform credential
for your identity rather than forwarding your connector token.

Connector threads and audit records are retained for two years. Disconnecting revokes the
connection's access but does not delete existing Lifesight records, or anything Claude has
already received. For access or deletion requests, write to privacy@lifesight.io. Lifesight's
privacy policy: https://lifesight.io/privacy-policy/.

## Disable, uninstall and disconnect

Disable or remove the plugin through your client's plugin controls. In Claude Code, use
`claude plugin disable ask-lifesight@lifesight` or
`claude plugin uninstall ask-lifesight@lifesight`.
Disabling or removing the plugin does not revoke a separately connected assistant's access.
To revoke that access, disconnect the client in Lifesight Settings, Claude & MCP.
Disconnecting does not delete historical records or information already received by the assistant.

## Changelog

- 0.2.2 (unreleased): align public capability claims and the reference with the restricted
  22-tool profile; distinguish twelve plugin skills from eleven remote prompts; disclose all
  six state-changing tools; clarify storage and disconnect behavior; correct the
  Claude terms link to the confirmed service-terms URL; keep publisher listing notes and submission procedures out of the public package.
  Tool parameter blocks are retained from the previous public reference;
  no connector runtime, endpoint, OAuth, skill or hook changes are included.
- 0.2.1: README platform/retention clarification, directory metadata and experiment-readout
  uncertainty wording present in the 24 October public source.
- 0.2.0 (earlier development): the house style, loaded at session start; the saturation skill draws the
  response curve from `detailed` results; the earlier development catalogue.
- 0.1.0 (2026-09-18): initial development package for the parallel window,
  OAuth through the console login, personal access tokens.
