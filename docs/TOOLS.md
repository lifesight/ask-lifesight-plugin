# Ask Lifesight MCP: tool reference

Generated from the server's published surface; do not edit by hand. Every result is a `structuredContent` object with `summary`, `workspace`, `data`, `provenance`, `links`, `next` and `warnings` (see the README).

## ask_lifesight

### `get_workspace_context`: Workspace context

Scope `lifesight.read`. read-only, idempotent, open-world.

The starting point for a connection: the workspaces this member holds and the one this connection is on, and for the active workspace the champion MMM models with their KPI, currency and data window, how many challengers exist, the champion's channels, the promoted plan, what this connection may do here, and today's date; figure-free, it orients and does not report. Use this when a conversation starts, when the member asks which workspace or model they are on, or before any tool that needs a model_id or a channel name. Not for figures (that is get_mmm_report and the other reads) or changing the workspace (switch_workspace). active_workspace.source says how the workspace was chosen: argument (this call), record (a switch), default (the sign-in's workspace); id (and data.member.id) is the member's stable id for this connection, never the email. Example: no arguments, or workspace_id="<id>" to orient on another workspace the member holds.

Parameters:

- `workspace_id`, string: Orient on this workspace instead of the active one.

### `switch_workspace`: Switch workspace

Scope `lifesight.read`. destructive, idempotent.

The workspace this connection operates on, changed: every later call runs there until switched again, and the switch is confirmed with the workspace's name. Use this when the member names another workspace of theirs to work in from now on. Not for one call in another workspace (every tool takes workspace_id for that) or for finding out which workspaces the member holds (get_workspace_context). It runs on its own, not beside a query, with a workspace id from get_workspace_context. Example: workspace_id="<id>".

Parameters:

- `workspace_id` (required), string: The workspace to make active.

### `send_feedback`: Send feedback

Scope `lifesight.read`. destructive, idempotent.

The member's verdict on an Ask Lifesight answer, recorded against the thread and turn ids the answer carried: thumbs up or down with an optional note, feeding Lifesight's evaluation set. Use this when the member says an investigation's answer was right, wrong or unhelpful. Not for a problem that needs a human (that is raise_support_ticket) or feedback on a typed tool's result (nothing records that). Example: turn_id="<turn>", verdict="down", note="the Meta figure was last year's".

Parameters:

- `note`, string: What was right or wrong, in the member's words.
- `thread_id`, string: The thread_id the answer carried; the connection's thread otherwise.
- `turn_id` (required), string: The turn_id the answer carried.
- `verdict` (required), string: up when the answer was right and useful, down otherwise. One of: up, down.
- `workspace_id`, string: The workspace of the thread; the active one otherwise.

### `compare_channel_measurements`: Compare a channel's measurements

Scope `lifesight.read`. read-only, idempotent, open-world.

One channel across the four ways Lifesight measures it, side by side: the MMM model's contribution, the platform's causal read, the channel's own reporting and the last completed lift test, each with its qualification (uncalibrated, attribution window, confidence interval, significance), the spread between them, which to plan on (a significant lift test, then the causal read, then the model, then the channel's own reporting) and what would settle the disagreement; coded, never averaged. Use this when the member asks why these numbers disagree, what the real return of a channel is, or whether the platform's ROAS can be trusted. Not for one measurement on its own (that is get_mmm_report, get_attribution_report or get_geo_experiments) or a budget (start_budget_optimisation). The channel goes in the workspace's spelling (get_workspace_context lists them); model_id defaults to the promoted plan's model; the window defaults to the last 90 days. Example: channel="Meta".

Parameters:

- `channel` (required), string: The channel, in the workspace's own spelling, e.g. "Meta" (get_workspace_context lists them).
- `end_date`, string: Causal window end, YYYY-MM-DD, e.g. "2026-08-31".
- `model_id`, string: The MMM model; blank = the promoted plan's model, reported in defaults.
- `start_date`, string: Causal window start, YYYY-MM-DD, e.g. "2026-08-01" (with end_date; default the last 90 days).
- `workspace_id`, string: Run in this workspace for this call only.

### `check_figures`: Check a draft's figures

Scope `lifesight.read`. read-only, idempotent.

Every figure in a draft answer checked against the tool results of this connection's thread, the way Lifesight checks its own assistant: each comes back grounded (a tool result carries it), derived (the sum or difference of one named field across results, marked *), restated (a rounding of a grounded figure), exempt (a year or a small count) or unverified (no result produced it), with a redacted_draft safe to show as is and the grounded_rate; it reads the thread and changes nothing. Use this when a draft answer carries figures. Not for reading a figure (a tool result is the only source of one). Example: draft="Meta drove 1.2M of revenue last quarter at 3.1x ROAS.".

Parameters:

- `draft` (required), string: The answer about to be shown, as text.
- `thread_id`, string: A thread of the member's to check against; the connection's thread in the workspace otherwise.
- `workspace_id`, string: The workspace whose thread to check against; the active one otherwise.

### `start_investigation`: Start an Ask Lifesight investigation

Scope `lifesight.read`. destructive, open-world.

Ask Lifesight, Lifesight's own investigator, started on a thread in the active workspace and returned at once with thread_id, turn_id and the thread's link: it reads the platform with the tools listed on this server, reconciles the figures and drafts the answer with charts over minutes. Use this when the member asks by name for a full investigation or a report with several parts and figures to reconcile, or to continue a thread from the product (thread_id). Not for a single figure, table or curve (that is the typed tools) or reading the answer (get_investigation). One question at a time per thread. Example: question="Why did Meta's return fall in Q3 and what should we change?".

Parameters:

- `question` (required), string: What to investigate, in the member's words.
- `thread_id`, string: Continue this thread of the member's; the connection's thread otherwise.
- `workspace_id`, string: Run in this workspace for this call only.

### `get_investigation`: Read an Ask Lifesight investigation

Scope `lifesight.read`. read-only, idempotent.

An Ask Lifesight thread, read: with a turn_id that turn (running with its progress, which carries poll_after_s, or completed with the answer in summary, the charts as resources and any pending approval); without one the thread's latest completed answer. Use this when an investigation was started and the member is waiting for its answer, or asks what a thread concluded. Not for starting one (that is start_investigation) or a solve's result (get_budget_optimisation). Example: thread_id="<thread>", turn_id="<turn>".

Parameters:

- `thread_id` (required), string: The thread start_investigation returned.
- `turn_id`, string: The turn to read; the latest completed one otherwise.
- `workspace_id`, string: The workspace of the thread; the active one otherwise.

## budget-planning

### `get_budget_optimisation`: Read a budget optimisation

Scope `lifesight.read`. read-only, idempotent.

The result of a start_budget_optimisation or save_budget_plan handle: running (with poll_after_s, the seconds until the next read is due), completed with the allocation and the sections asked for, failed with why, or lost (the solve did not finish; a new start_budget_optimisation call is needed). Use this when a solve answered with a handle and the member is waiting for its result. Not for starting a solve (that is start_budget_optimisation) or a promotion's decision (get_approval_status). A handle is good for a day and only from the connection that started it. Example: handle="<handle>".

Parameters:

- `handle` (required), string: The handle start_budget_optimisation or save_budget_plan returned, e.g. "sol_01J...".
- `response_format`, string: concise: totals and the channel table; detailed: every section in full and the artifact data. One of: concise, detailed.
- `workspace_id`, string: The workspace the solve ran in; the active one otherwise.

### `get_approval_status`: Read an approval's decision

Scope `lifesight.read`. read-only, idempotent.

The member's decision on a plan promotion this connection requested: pending with its expiry (nothing has changed), approved with the outcome (the plan is the workspace's default; no money moved), rejected, or expired; read by approval_id, or by the handle request_plan_promotion returned while its solve ran (preparing until the approval is raised). Use this when the member asks whether the promotion went through or what happened to their request. Not for a solve's result (that is get_budget_optimisation) or raising a request (request_plan_promotion). Only the member's own approvals in workspaces they hold answer. Example: approval_id="<id>".

Parameters:

- `approval_id`, string: The approval_id request_plan_promotion returned.
- `handle`, string: The handle request_plan_promotion returned when its solve ran on.
- `workspace_id`, string: The workspace the request ran in; the active one otherwise.

### `get_current_budget_allocation`: Current budget allocation

Scope `lifesight.read`. read-only, idempotent, open-world.

How the workspace's media budget is split today, per channel, as an MMM model sees it: each channel's current spend and outcome over a one-month baseline, the platform's own totals, and per channel its marginal return, saturation level and headroom ("N/A" when the curve gives no ceiling); no solve runs and nothing changes. Use this when the member asks how spend is allocated now, what each channel returns at today's spend, or as the baseline before any plan. Not for how far one channel could scale (that is get_channel_saturation_curves) or alternatives side by side (compare_budget_scenarios). Spend is per month in the model's currency; the outcome is the model's KPI (revenue, or a count); ROAS is a multiplier on a revenue model, CPA an amount per unit on a count model. Example: model_id from list_mmm_models.

Parameters:

- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `start_budget_optimisation`: Start a budget optimisation

Scope `lifesight.read`. destructive, open-world.

Runs the model's optimiser on a budget and answers within about 20 seconds: the result inline when the solve is quick, else a handle to read with get_budget_optimisation. Use this when the member asks how to split a budget, what to reallocate, or the smallest budget that reaches a target: mode maximise splits total_budget across channels for the best outcome (a figure "500000" or an expression on today's spend "current +10%"; blank reallocates what is spent today); mode target_kpi finds the smallest budget that reaches target_kpi_value. Not for comparing several budgets at once (that is compare_budget_scenarios) or saving a plan (save_budget_plan). constraint_type bounds each channel as a multiple of its historical spend: Current, Conservative, Moderate (the default), Aggressive, or Custom with channel_overrides. time_period is the plan horizon (default a quarter); dates are derived from it, never passed. sections for maximise: allocation (always), forecast, pacing, worksheet, one solve for all. Each call creates a scratch scenario on the platform, not a saved plan. The budget and the constraints are the member's stated values; a needs_input warning names any that is missing. Example: mode="maximise", total_budget="current +10%", model_id from list_mmm_models.

Parameters:

- `channel_overrides`, array: Custom only: per-channel bounds the member named.
- `constraint_type`, string: How far each channel may move from its historical spend; blank = Moderate, reported in defaults. One of: Current, Conservative, Moderate, Aggressive, Custom.
- `mode`, string: maximise the outcome for a budget, or find the budget for a target outcome. One of: maximise, target_kpi.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `sections`, array: maximise only: allocation (always), forecast, pacing, worksheet. One of: allocation, forecast, pacing, worksheet.
- `target_kpi_value`, number: target_kpi only. The outcome to reach, in the model's KPI and currency.
- `time_period`, string: The plan horizon; blank = a quarter, reported in defaults. One of: month, two months, quarter, six months, nine months, twelve months.
- `total_budget`, string: maximise only. A figure as text ("500000") or an expression on today's spend ("current -10%"); blank reallocates today's spend.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `compare_budget_scenarios`: Compare budget scenarios

Scope `lifesight.read`. destructive, open-world.

Up to six budget scenarios optimised on one MMM model and one baseline, side by side: each scenario's outcome, its ROAS (or CPA on a count model) and per-channel allocation with the platform's own deltas against current spend; a solve that takes tens of seconds, creates scratch scenarios and changes no budget. Use this when the member asks what +20% versus -20% looks like, which of several budgets to pick, or how a cut compares with holding. Not for one budget's split (that is start_budget_optimisation) or today's allocation (get_current_budget_allocation). Each scenario is {label, total_budget, constraint_type, description}; total_budget is an amount the member stated or an expression on the current budget ("current", "current -10%", "+20%"). constraint_type: Current, Conservative (default), Moderate, Aggressive or Custom. With one champion and no model_id or time_period the tool plans on it and a quarter and reports the defaults; with several it returns the question to put to the member and nothing runs. A scenario whose bounds cannot place its budget is refused with why. Example: scenarios=[{"label":"Hold","total_budget":"current"},{"label":"Cut","total_budget":"current -10%"}].

Parameters:

- `model_id`, string: The MMM model id from list_mmm_models. Leave out with one champion: the tool plans on it and reports the default.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `scenarios` (required), array: One to six scenarios, each a full optimisation run on the shared baseline.
- `time_period`, string: How long every scenario covers. Leave out unless the member said: a quarter is the reported default. One of: month, two months, quarter, six months, nine months, twelve months.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `get_saved_plans`: Saved budget plans

Scope `lifesight.read`. read-only, idempotent, open-world.

The budget plans saved in the workspace as the console shows them: without plan_id the list (plan id, name, status, model, scenario count, the promoted scenario, when saved); with plan_id that plan, one entry per scenario with its state, plan window, optimised allocation per channel with the platform's totals and deltas, the outcome forecast (monthly) and the weekly pacing schedule. Use this when the member asks what plans exist, what a saved plan proposes, or which scenario is promoted. Not for today's split (that is get_current_budget_allocation) or a new optimisation (start_budget_optimisation); Ask Lifesight's own scratch plans are not listed. Figures are the platform's over the scenario's plan window in the model's currency; ROAS is a multiplier, CPA an amount per unit. Example: no arguments to list, then plan_id="<id>".

Parameters:

- `plan_id`, string: Read this saved plan (a plan_id from the list). Leave out to list.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `save_budget_plan`: Save a budget plan

Scope `lifesight.write`. destructive, open-world.

Optimises a budget with the model and saves the result as a named plan in Lifesight, visible to the member's colleagues in the console (a write; needs write access); it answers within about 20 seconds or hands back a handle for get_budget_optimisation. Use this when the member asks to save, keep or name a plan they can share. Not for a what-if that is not kept (that is start_budget_optimisation) or making a plan the workspace's default: saving does NOT make the plan the workspace's default; that is request_plan_promotion, approved in the product. Give the model, the plan_name and the total_budget the member stated; constraint_type and time_period as start_budget_optimisation. The name, the budget and the constraints are the member's stated values; a needs_input warning names any that is missing. Example: model_id="<id>", plan_name="Q4 moderate", total_budget=500000.

Parameters:

- `channel_overrides`, array: Custom only: per-channel bounds the member named.
- `constraint_type`, string: How far each channel may move from its historical spend; blank = Moderate, reported in defaults. One of: Current, Conservative, Moderate, Aggressive, Custom.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `plan_name` (required), string: The name the plan is saved under, visible to colleagues in the console; as the member stated it.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `time_period`, string: The plan horizon; blank = a quarter, reported in defaults. One of: month, two months, quarter, six months, nine months, twelve months.
- `total_budget` (required), number: The budget to plan, in the model's currency, as the member stated it.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `request_plan_promotion`: Request a plan promotion

Scope `lifesight.decide`. destructive, open-world, needs the member's decision in the product.

Raises a request for an optimised plan to become the workspace's default plan in Lifesight, for the member to approve there (needs decision access); promotion sets the scenario the team plans against and is not a financial transaction: no money moves, no payment runs, no ad-platform spend changes. Use this when the member asks to promote, apply or make a plan the default. Not for saving a plan without promoting it (that is save_budget_plan) or reading a decision (get_approval_status). The tool never performs the promotion: it optimises the budget with the model and pauses for a human decision; on approval the plan is saved under plan_name and promoted, on rejection nothing is saved; the member decides in the Lifesight product, never here. It returns approval_id, the summary and expires_at (or a handle while the solve runs), and the plan counts as promoted only once get_approval_status reports approved. The name, the budget and the constraints are the member's stated values. Example: model_id="<id>", plan_name="Q4 plan", total_budget=500000.

Parameters:

- `constraint_type`, string: How far each channel may move from its historical spend; blank = Moderate, reported in defaults. One of: Current, Conservative, Moderate, Aggressive, Custom.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `plan_name` (required), string: The name the plan is saved under, visible to colleagues in the console; as the member stated it.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `time_period`, string: The plan horizon; blank = a quarter, reported in defaults. One of: month, two months, quarter, six months, nine months, twelve months.
- `total_budget` (required), number: The budget to plan, in the model's currency, as the member stated it.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## ads-data

### `query_ads_data`: Query ads data

Scope `lifesight.read`. read-only, idempotent, open-world.

The ad platforms' own reported figures from the workspace's ads mart in BigQuery (spend, impressions, clicks, conversions, ROAS and CPA by platform, campaign and day), answered in words by Lifesight's data agent for the workspace: one fixed operation, a read of that mart; platform-reported figures, not the model's incremental ones. Use this when the member asks what a platform reported, spend by campaign or week, or clicks and impressions. Not for what a channel drove (that is get_mmm_report) or what was incremental (get_attribution_report). Rows are capped; the question names platforms, metrics and the window. Example: question="Google Ads spend by week last month".

Parameters:

- `question` (required), string: The question, in words, naming platforms, metrics and the window.
- `workspace_id`, string: Run in this workspace for this call only.

## core

### `list_mmm_models`: List MMM models

Scope `lifesight.read`. read-only, idempotent, open-world.

The workspace's marketing mix models: the champions (signed off, the ones to report and plan on), newest first, with model id, display name, outcome KPI, currency and data window; challengers (under review) are counted, listed only with include_challengers=true, and never planned on. Use this when the member asks which models exist, which model a report or plan should run on, or when any other MMM tool needs a model_id. Not for what a model says (that is get_mmm_report) or today's spend split (get_current_budget_allocation). outcome_kpi filters by the model's KPI (revenue, conversions, installs), matched exactly, case-insensitively; several champions for one KPI have no tie-break, they are shown for the member to choose. data.sections_available lists what get_mmm_report can read per model. Example: outcome_kpi="revenue".

Parameters:

- `include_challengers`, boolean: Also list models under review. Only when the member asks to see them.
- `outcome_kpi`, string: Only models whose outcome KPI matches (exact, case-insensitive), e.g. revenue.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## model-insights

### `get_mmm_report`: MMM report

Scope `lifesight.read`. read-only, idempotent, open-world.

What a marketing mix model says, by section, in one call: contributions (what each channel drove), contribution_trends, accuracy (fit), causal_structure, incremental_revenue, roi_spend_share, platform_spend, platform_engagement, input_correlation, immediate_vs_carryover, marginal_roas, sem_effects (direct, indirect and halo), decomposition (the series split into drivers), response_curves, and the diagnostics backtests, calibration and attribute_quality. Use this when the member asks what drove revenue, how a channel performed last quarter, whether the model is accurate, what the marginal return is, or what carried over. Not for how far one channel can scale (that is get_channel_saturation_curves), a budget (start_budget_optimisation) or incremental ad performance over a window (get_attribution_report). Default sections: contributions, accuracy, causal_structure; every section the question needs goes in one call; a section the model cannot produce is reported unavailable and the others still answer. Dates blank = the model's own data window; dates outside it return no data. Figures are in the model's currency and KPI (units in provenance); ROAS is a multiplier; an index is not an amount. Example: model_id from list_mmm_models, sections=["contributions","marginal_roas"].

Parameters:

- `end_date`, string: Window end, YYYY-MM-DD; blank uses the model's own window.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `sections`, array: The sections to read; default contributions, accuracy, causal_structure. One of: accuracy, attribute_quality, backtests, calibration, causal_structure, contribution_trends, contributions, decomposition, immediate_vs_carryover, incremental_revenue, input_correlation, marginal_roas, platform_engagement, platform_filters, platform_spend, response_curves, roi_spend_share, sem_effects.
- `start_date`, string: Window start, YYYY-MM-DD; blank uses the model's own window.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `get_channel_saturation_curves`: Channel saturation curve

Scope `lifesight.read`. read-only, idempotent, open-world.

How far ONE channel can scale before the next unit of spend stops paying for itself, read off the model's response curve: the saturation cap at a target return (null with a note when the return stays above the target to the curve's end), the operating point at the end of the curve period with its marginal ROAS (marginal CPA on a count model), the model's own optimised point, the inflection point (past it is diminishing returns, not saturation), where the sample ends, and on detailed the Hill parameters, time to conversion, curve points and adstock; no solve, no budget. Use this when the member asks whether a channel is saturated, how much more it can take, or what the headroom is. Not for a plan's allocation (that is start_budget_optimisation) or every channel at once (get_current_budget_allocation gives each channel's headroom in one read). One channel per call, named as the model does (google_spend) or as the console labels it (Google Ads); spend figures cover the whole curve period, not a week, in the model's currency. Example: channel="Google Ads", model_id from list_mmm_models.

Parameters:

- `channel` (required), string: The channel, as the model names it or as the console labels it.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `target_roas`, number: The return the next unit of spend must still earn; 1.0 means it pays for itself.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## causal-attribution

### `get_attribution_report`: Causal attribution report

Scope `lifesight.read`. read-only, idempotent, open-world.

Incremental ad performance over a window from the causal attribution read, by analysis: performance (spend, platform-reported and incremental revenue, iROAS, mROAS per row), pacing (what is under or over its daily plan), creatives (the best ads by an incremental metric), incrementality (how much of the platform's claimed revenue is real), saturation (channels at or past their efficient point at target_roas) and budget_allocation (a linear split of target_budget, only when the member gives a budget). Use this when the member asks what was really incremental last month, whether the platform's ROAS is real, what is off pace, or which ads earned their spend. Not for what the MMM says a channel drove (that is get_mmm_report) or a lift test (get_geo_experiments). start_date and end_date are required: without a window the read is a nightly snapshot that answers nothing. level: ACCOUNT, CAMPAIGNS (default; pacing needs this or finer), ADSET or AD. Default analyses: every one but budget_allocation. The result names the model the calibration uses and the promoted plan. Spend and revenue are in the workspace's currency; a ROAS is a multiplier; an incremental factor is a fraction of platform-reported revenue. Example: start_date="2026-08-01", end_date="2026-08-31", analyses=["incrementality","pacing"].

Parameters:

- `analyses`, array: The analyses to derive from the one read; default every one but budget_allocation. One of: performance, pacing, creatives, incrementality, saturation, budget_allocation.
- `end_date` (required), string: Window end, YYYY-MM-DD. Required.
- `level`, string: Granularity of the breakdown; pacing needs CAMPAIGNS or finer. One of: ACCOUNT, CAMPAIGNS, ADSET, AD.
- `metric`, string: For creatives: the incremental metric to rank ads by. One of: iRoas, iRevenue, iFactor, platformVsIncrementalRevenue, pRoas, pRevenue, spend.
- `min_share_floor`, number: For budget_allocation: the smallest share any channel may keep (a fraction).
- `min_spend`, number: For creatives: ignore ads below this spend so tiny-sample winners do not top the list.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `start_date` (required), string: Window start, YYYY-MM-DD. Required.
- `target_budget`, number: For budget_allocation: the budget to split, as the member stated it.
- `target_roas`, number: For saturation: the return a channel must still earn to count as unsaturated.
- `top_n`, integer: For creatives: how many ads to rank.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## experiments

### `get_geo_experiments`: Geo experiments

Scope `lifesight.read`. read-only, idempotent, open-world.

The workspace's geo and time incrementality experiments: without experiment_id the list, newest first (id, kind, name, status, outcome KPI, treatment dates, channels, cells), filtered by status (the platform's values), kind (GEO, TIME, EXTERNAL), channel or a name fragment; with experiment_id that experiment's report by section: results (lift and significance per cell, test vs control), recommendations (the market designs to run next), lift_over_time, power_curve, pre_period_fit, control_markets, progress (a live experiment's stage and day) and secondary_fit. Use this when the member asks what a test showed, whether the lift was significant, which experiments ran, or what to test next. Not for modelled channel effects (that is get_mmm_report) or incremental ad performance over a window (get_attribution_report). Default sections: results, recommendations, lift_over_time, progress. Lift is a percent, iROAS a multiplier, weights fractions. Example: status=["COMPLETED"] to find one, then experiment_id="<id>", sections=["results"].

Parameters:

- `channel`, string: Listing: only experiments on this channel, as the platform names it (case and spaces ignored).
- `experiment_id`, string: Read this experiment's report (an id from the list). Leave out to list.
- `kind`, string: Listing: only experiments of this kind. One of: GEO, TIME, EXTERNAL.
- `name`, string: Listing: only experiments whose name contains this text.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `sections`, array: With experiment_id: the sections to read; default results, recommendations, lift_over_time, progress. One of: results, recommendations, lift_over_time, power_curve, pre_period_fit, control_markets, progress, secondary_fit.
- `status`, array: Listing: only experiments in these statuses. Archived ones show only when ARCHIVED is asked for. One of: DRAFT, UPLOADING, DESIGNING, DESIGN_READY, FINDING_MARKETS, MARKETS_READY, SCHEDULED, RUNNING, STOPPED, AWAITING_DATA_TO_MEASURE_LIFT, AWAITING_LIFT_CONFIRMATION, MEASURING_LIFT, COMPLETED, AWAITING_POST_TREATMENT_DATA, AWAITING_POST_TREATMENT_CONFIRMATION, POST_TREATMENT_MEASURING_LIFT, POST_TREATMENT_COMPLETED, FAILED, POST_TREATMENT_FAILED, ARCHIVED.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## creative-intelligence

### `get_creative_performance`: Creative and tactic performance

Scope `lifesight.read`. read-only, idempotent, open-world.

Which creative tactics an MMM model measures (prospecting, retargeting, and so on) and the reported paid spend behind them, two reads in one call: the model's tactic list (has_tactics false when the model has no tactic breakdown and the list is its channels) and the workspace's resolved spend by tactic (source_table says whether the taxonomy or the raw ads mart answered). Use this when the member asks what tactics the model knows, what was spent by tactic, or wants spend beside an incrementality read. Not for what a tactic or channel drove (that is get_mmm_report) or the best ads by incremental return (get_attribution_report with analyses=["creatives"]). This is reported spend in the workspace's currency, not a modelled contribution. Example: model_id from list_mmm_models; include_spend=false for the tactic list alone.

Parameters:

- `include_spend`, boolean: Also read the workspace's resolved paid spend by tactic (default true).
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## data-pipeline

### `get_data_source_health`: Data source health

Scope `lifesight.read`. read-only, idempotent, open-world.

The workspace's connected data sources (ad platforms, conversion sources, uploads) and whether data is flowing: without integration every source with its health, live (data flowing), attention (a member must act: auth error, failed sync, transformation error), setup (authorised, not yet flowing) or paused; with integration that source's recent sync runs, newest first, with when the last sync succeeded or failed, rows ingested per run and error codes. Use this when the member asks whether the data is fresh, whether anything is broken, when Meta last synced, or why fewer rows landed. Not for spend that stopped or spiked (that is detect_spend_anomalies: a stale source is a pipeline matter, not a campaign anomaly). An integration that is a UUID is read directly; a name ("Meta", "Google Ads") is resolved from the list in the same call and the summary gives the id. Rows are the platform's own counts; times are the platform's timestamps. Example: no arguments, then integration="<uuid>".

Parameters:

- `integration`, string: One source: its integration id (a UUID, read directly) or its name (resolved from the list; the summary then gives the id). Leave out to list every source.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## anomaly-detection

### `detect_spend_anomalies`: Spend anomalies

Scope `lifesight.read`. read-only, idempotent, open-world.

What looks off in the workspace's paid media over the last days: spend that spiked, dropped or stopped, ROAS or CTR that moved sharply, revenue off its recent run rate, per ad platform (source) and per campaign, each compared over its last window_days against the days before and anchored on that source's own latest day; findings worst first with the detector's window and baseline values, their basis (daily mean, window total vs run rate, or ratio), the change in percent and, for spend, a z-score, with the rules that judged them; stale sources named apart. Use this when the member asks what is this spike, whether anything stopped spending, why ROAS dropped on Meta, or whether anything looks odd this week. Not for a broken connector (that is get_data_source_health) or whether the spend was incremental (get_attribution_report). window_days 1 to 30, default 7; source is the mart's key (facebook_ads, google_ads) or blank for every source. Spend is in the workspace's currency. Example: window_days=7, source="facebook_ads".

Parameters:

- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `source`, string: One ad platform by the mart's source key (facebook_ads, google_ads, rtb_house); leave out to scan every source.
- `window_days`, integer: The comparison window in days; the baseline is the 28 days before it, or four windows when longer.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## knowledge

### `search_lifesight_docs`: Search Lifesight docs

Scope `lifesight.read`. read-only, idempotent, open-world.

The Lifesight product documentation, searched: what a term or methodology means (adstock, saturation, MMM calibration, geo lift), how a feature works, how to do something in the product; the same answer for every customer, never the member's data. Use this when the member asks what a term means, how a method works, or how to do something in Lifesight. Not for the member's own figures (those come from the model, attribution and planning tools). Returns the matching chunks as text, each headed by its document title and section, best first. mode semantic (default) fuses meaning and keyword hits and re-ranks, up to 15 chunks; keyword is the exact-term fallback ("MROAS", "MROAS OR adstock"), up to 10, for when semantic found nothing or the query is an identifier. section narrows to one documentation section; list_sections=true returns the section names instead. Concise returns the first three chunks when many matched; detailed every chunk. Example: query="what is adstock decay", or query="MROAS", mode="keyword".

Parameters:

- `list_sections`, boolean: Return the documentation's section names instead of searching.
- `mode`, string: semantic fuses meaning and keyword hits; keyword is the exact-term fallback. One of: semantic, keyword.
- `query`, string: What to look for: a question or topic in semantic mode, the exact term(s) or a boolean expression in keyword mode. Required unless list_sections is true.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `section`, string: Only this documentation section (a name from list_sections). Blank searches everything. One of: INTRODUCTION, GETTING STARTED, PLATFORM, METHODOLOGIES, HOW TO'S, COMPARISONS & USE CASES, LEARN, MCP Server, PARTNERS, SECURITY & COMPLIANCE, SUPPORT, WEB DOCS.
- `top_k`, integer: Chunks to return: up to 15 in semantic mode, 10 in keyword mode; the larger end for lists and comparisons.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## collaboration

### `raise_support_ticket`: Raise a support ticket

Scope `lifesight.write`. destructive, open-world.

A ticket with Lifesight support in the member's name, raised or checked (needs write access): to raise one, summary (one line, the title), description (the member's own words) and category (technical_error, data_issue, customer_disagreement, agent_misbehavior, user_escalation or feature_request) with priority low, medium (default), high or critical; to check one, ticket_key only. Use this when the member asks for support or a human, disputes figures, hits an error a retry will not fix, or finds data missing or wrong. Not for a question the documentation answers (that is search_lifesight_docs). Returns the key and its link, or the ticket's state, assignee and last update; a ticket is visible to Lifesight staff and is raised at the member's request. Example: summary="Meta spend missing since Monday", description="<the member's words>", category="data_issue".

Parameters:

- `category`, string: What kind of issue (to raise). One of: technical_error, data_issue, customer_disagreement, agent_misbehavior, user_escalation, feature_request.
- `description`, string: The member's own words about the problem (to raise).
- `priority`, string: How urgent. One of: low, medium, high, critical.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `summary`, string: One line, the ticket's title (to raise).
- `ticket_key`, string: A ticket raised before (its key, e.g. ABC-123), to check its state; leave out to raise one.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## cue-cards

### `get_cue_cards`: Cue cards

Scope `lifesight.read`. read-only, idempotent, open-world.

What needs the member's attention today: the top cue cards their workspace agents raised (anomalies, broken data sources, plans to review, questions waiting on them), scored and ranked for this member, filtered to what they may see, each with a deep link into the product; the cards are delivered beside the result, not inside data. Use this when the member asks what to look at, what is waiting on them, or for their top five things. Not for the figures behind a card (that is the tool it names: detect_spend_anomalies, get_data_source_health, get_saved_plans). limit is 1 to 20, default 5, given only when the member names a number; card actions (dismiss, snooze, take it, approve) stay in the product through the card's link. Example: no arguments, or limit=3.

Parameters:

- `limit`, integer: How many cards, 1 to 20; 5 unless the member names a number.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## Server instructions

What a client reads before the first call:

```
Lifesight marketing measurement for this member's workspaces: marketing mix models (MMM), causal attribution, geo-lift experiments, budget optimisation and saved plans, data-source health, spend anomalies, creative performance, the member's cue cards, and the product docs.
get_workspace_context, a connection's first call, gives the workspaces the member holds and the active one, the champion models with KPI, currency and data window, the promoted plan, today's date, and three questions the workspace can answer today.
Every result is a structuredContent object: the answer in `summary`, the payload in `data`, the workspace, `provenance` (which platform read each figure came from, its unit and currency), console `links`, `warnings` (no_data, defaults taken, inputs still needed, reconciliation findings). Figures come only from tool results; the server computes compares, shares and totals, which the payload carries; check_figures reports which figures in a draft the thread's results ground. A needs_input warning carries the questions the member has still to answer.
switch_workspace changes the active workspace for this connection; every tool also takes workspace_id for one call.
Long work never holds a call: start_budget_optimisation answers inline when quick, else with a handle for get_budget_optimisation; start_investigation runs Ask Lifesight on a thread (a compound investigation asked for by name, or to continue a product thread) and get_investigation reads it, progress carrying poll_after_s. compare_channel_measurements puts a channel's four measurements side by side and says which to plan on. query_ads_data answers in words over the ad platforms' own figures. The prompts are the workflows members run most.
save_budget_plan (write access) saves a plan by name; request_plan_promotion (decision access) never promotes: the member approves in the product and get_approval_status reads the decision; promotion moves no money. Access the connection lacks is refused with a sentence naming where the member enables it.
```
