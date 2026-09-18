# Lifesight MIA MCP: tool reference

Generated from the server's published surface; do not edit by hand. Every result is a `structuredContent` object with `summary`, `workspace`, `data`, `provenance`, `links`, `next` and `warnings` (see the README).

## mia

### `get_workspace_context`: Workspace context

Scope `mia.read`. read-only, idempotent, open-world.

Call this first. The workspaces this member holds and the one this connection is on; for the active workspace: the champion MMM models with their KPI, currency and data window, how many challengers exist, the champion's channels, the promoted plan, and today's date. Figure-free: it orients, it does not report. active_workspace.source says how the workspace was chosen: argument (this call), record (a switch), default (the sign-in's workspace).

Parameters:

- `workspace_id`, string: Orient on this workspace instead of the active one.

### `switch_workspace`: Switch workspace

Scope `mia.read`. idempotent.

Change the workspace this connection operates on; every later call runs there until switched again. Call it on its own, not beside a query. Takes a workspace id from get_workspace_context and confirms the switch with the workspace's name.

Parameters:

- `workspace_id` (required), string: The workspace to make active.

### `send_feedback`: Send feedback

Scope `mia.read`. idempotent.

Record the member's verdict on a Mia answer (ask_mia or get_mia_investigation): thumbs up or down with an optional note, against the thread and turn ids the answer carried. Feeds Lifesight's evaluation set.

Parameters:

- `note`, string: What was right or wrong, in the member's words.
- `thread_id`, string: The thread_id the answer carried; the connection's thread otherwise.
- `turn_id` (required), string: The turn_id the answer carried.
- `verdict` (required), string: up when the answer was right and useful, down otherwise. One of: up, down.
- `workspace_id`, string: The workspace of the thread; the active one otherwise.

### `compare_channel_measurements`: Compare a channel's measurements

Scope `mia.read`. read-only, idempotent, open-world.

One channel across the four ways Lifesight measures it: the MMM model's contribution, the platform's causal read, the channel's own reporting, and the last completed lift test, side by side with each read's qualification (uncalibrated, attribution window, confidence interval, significance), the spread between them, which to plan on (a significant lift test, then the causal read, then the model, then the channel's own reporting) and what would settle the disagreement. Coded, never averaged. Pass the channel in the workspace's spelling (get_workspace_context lists them); model_id defaults to the promoted plan's model. The window defaults to the last 90 days (the cue card judges the promoted plan's elapsed window). Use it for 'why do these numbers disagree', 'what is the real return of X', 'can I trust the platform's ROAS'.

Parameters:

- `channel` (required), string: The channel, in the workspace's own spelling.
- `end_date`, string: Causal window end, YYYY-MM-DD.
- `model_id`, string: The MMM model; blank = the promoted plan's model, reported in defaults.
- `start_date`, string: Causal window start, YYYY-MM-DD (with end_date).
- `workspace_id`, string: Run in this workspace for this call only.

### `check_figures`: Check a draft's figures

Scope `mia.read`. read-only, idempotent.

Before you show figures, submit the draft: every figure in it is checked against the tool results of this connection's thread, the way Lifesight checks its own assistant. Each comes back grounded (a tool result carries it), derived (the sum or difference of one named field across results, marked *), restated (a rounding of a grounded figure), exempt (a year or a small count) or unverified (no result produced it), with a redacted_draft you can show as is and the grounded_rate. Reads the thread, changes nothing. Call it once per answer that carries figures; if a figure is unverified, read it with a tool or drop it.

Parameters:

- `draft` (required), string: The answer you are about to show, as text.
- `thread_id`, string: A thread of yours to check against; the connection's thread in the workspace otherwise.
- `workspace_id`, string: The workspace whose thread to check against; the active one otherwise.

### `start_mia_investigation`: Start a Mia investigation

Scope `mia.read`. open-world.

Start Lifesight's own investigator, Mia, on a thread in the active workspace and return at once: for a compound investigation the member asks for by name (several parts, figures to reconcile, a report with charts), or to continue a thread from the product (thread_id). She reads the platform, reconciles figures and drafts the answer; it takes minutes. Read it with get_mia_investigation(thread_id, turn_id). For a single figure, table or curve use the typed tools instead. One question at a time per thread.

Parameters:

- `question` (required), string: What to investigate, in the member's words.
- `thread_id`, string: Continue this thread of the member's; the connection's thread otherwise.
- `workspace_id`, string: Run in this workspace for this call only.

### `get_mia_investigation`: Read a Mia investigation

Scope `mia.read`. read-only, idempotent.

Read a Mia thread: with a turn_id, that turn (running with its progress, or completed with the answer, the charts and any pending approval); without one, the thread's latest completed answer. The answer is in summary; the artifacts ride along as resources.

Parameters:

- `thread_id` (required), string: The thread start_mia_investigation returned.
- `turn_id`, string: The turn to read; the latest completed one otherwise.
- `workspace_id`, string: The workspace of the thread; the active one otherwise.

### `ask_mia`: Ask Mia (investigation thread)

Scope `mia.read`. open-world.

Run Lifesight's own investigator, Mia, on a thread in the active workspace: for a compound investigation the member asks for by name, or to continue a thread from the product. She reads the platform, reconciles figures and drafts a report with charts. Slow: minutes. If the answer is not ready within one call the result says status=running; ask again with the same thread_id to read it. For a single figure or table, use the typed tools instead.

Parameters:

- `question`, string: What to ask Mia (not needed with read_latest).
- `read_latest`, boolean: Do not ask anything: return the thread's latest completed answer (how to read a turn that was still running).
- `thread_id`, : Continue a thread of yours (also how to read a turn that was still running); the connection's thread in the active workspace otherwise.
- `workspace_id`, : Run in this workspace for this call only.

## budget-planning

### `get_budget_optimisation`: Read a budget optimisation

Scope `mia.read`. read-only, idempotent.

Read the result of a start_budget_optimisation handle: status running (ask again after poll_after_s), completed with the allocation and the sections asked for, or lost (the solve did not finish; start it again). A handle is yours for a day and only from the connection that started it.

Parameters:

- `handle` (required), string: The handle start_budget_optimisation returned.
- `response_format`, string: concise: totals and the channel table; detailed: every section in full and the artifact data. One of: concise, detailed.
- `workspace_id`, string: The workspace the solve ran in; the active one otherwise.

### `get_approval_status`: Read an approval's decision

Scope `mia.read`. read-only, idempotent.

The member's decision on a plan promotion this connection requested (request_plan_promotion): pending with its expiry (nothing has changed), approved with the outcome (the plan is the workspace's default; no money moved), rejected, or expired. By approval_id, or by the handle request_plan_promotion returned while its solve ran (preparing until the approval is raised). Only the member's own approvals in workspaces they hold.

Parameters:

- `approval_id`, string: The approval_id request_plan_promotion returned.
- `handle`, string: The handle request_plan_promotion returned when its solve ran on.
- `workspace_id`, string: The workspace the request ran in; the active one otherwise.

### `get_current_budget_allocation`: Current budget allocation

Scope `mia.read`. read-only, idempotent, open-world.

How the workspace's media budget is allocated today, per channel, as an MMM model sees it: each channel's current spend and outcome over a one-month baseline, the platform's own totals, and per channel its marginal return, saturation level and headroom ("N/A" when the curve gives no ceiling). Use it as the baseline before any plan, or when the member asks how spend is split now. No solve runs and nothing changes. Spend is per month in the model's currency; the outcome is the model's KPI (revenue, or a count); ROAS is a multiplier on a revenue model, CPA an amount per unit on a count model. Example: model_id from list_mmm_models. For what a channel could scale to use get_channel_saturation_curves; for alternatives side by side use compare_budget_scenarios.

Parameters:

- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `start_budget_optimisation`: Start a budget optimisation

Scope `mia.read`. open-world.

Run the model's optimiser (a solve takes seconds to minutes); answers within about 20 seconds with the result when the solve is quick, else with a handle: mode maximise splits a budget across channels for the best outcome (total_budget as text: a figure "500000" or an expression on today's spend "current +10%"; blank reallocates what is spent today), mode target_kpi finds the smallest budget that reaches target_kpi_value. constraint_type bounds each channel as a multiple of its historical spend: Current, Conservative, Moderate (the default), Aggressive, or Custom with channel_overrides. time_period is the plan horizon (default a quarter); dates are derived from it, never passed. sections for maximise: allocation (always), forecast, pacing, worksheet, one solve for all. A short solve returns the result inline; otherwise read it with get_budget_optimisation(handle). Each call creates a scratch scenario on the platform (not a saved plan). Never invent a budget or a constraint the member did not state; a needs_input warning lists what to ask them.

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

Scope `mia.read`. open-world.

Optimise up to six budget scenarios on one MMM model and one baseline and compare them side by side: each scenario's outcome, its ROAS (or CPA on a count model) and per-channel allocation with the platform's own deltas against current spend. Each scenario is {label, total_budget, constraint_type, description}; total_budget is an amount the member stated or an expression on the current budget ("current", "current -10%", "+20%"); never invent a budget. constraint_type: Current, Conservative, Moderate, Aggressive or Custom (default Conservative). model_id and time_period may be left out: with one champion the tool plans on it and a quarter and reports the defaults; with several it returns the question to put to the member (nothing ran). This is a SOLVE: it creates scratch scenarios on the platform and takes tens of seconds; it changes no budget. A scenario whose bounds cannot place its budget is refused with why. Example: scenarios=[{"label":"Hold","total_budget":"current"},{"label":"Cut","total_budget":"current -10%"}]. For today's split alone use get_current_budget_allocation.

Parameters:

- `model_id`, string: The MMM model id from list_mmm_models. Leave out with one champion: the tool plans on it and reports the default.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `scenarios` (required), array: One to six scenarios, each a full optimisation run on the shared baseline.
- `time_period`, string: How long every scenario covers. Leave out unless the member said: a quarter is the reported default. One of: month, two months, quarter, six months, nine months, twelve months.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `get_saved_plans`: Saved budget plans

Scope `mia.read`. read-only, idempotent, open-world.

The budget plans saved in the workspace, as the console shows them. Without plan_id it lists them: plan id, name, status, model, scenario count, the promoted scenario and when it was saved. With plan_id it reads that plan: one entry per scenario with its state, plan window, the optimised allocation per channel with the platform's totals and deltas, the outcome forecast (monthly rollup) and the weekly pacing schedule. Use it when the member asks what plans exist, what a saved plan proposes, or which scenario is promoted; MIA's own scratch plans are not listed. Figures are the platform's, over the scenario's plan window, in the model's currency; ROAS is a multiplier, CPA an amount per unit. Example: no arguments to list, then plan_id="<id>". For today's split use get_current_budget_allocation.

Parameters:

- `plan_id`, string: Read this saved plan (a plan_id from the list). Leave out to list.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `save_budget_plan`: Save a budget plan

Scope `mia.write`. open-world.

Optimise a budget with the model and save the result as a named plan in Lifesight, visible to the member's colleagues in the console (a write; needs the mia.write scope). Give the model, the name and the total budget the member stated; constraint_type and time_period as start_budget_optimisation. Answers within about 20 seconds when the solve is quick, else with a handle to read with get_budget_optimisation. Saving does NOT make the plan the workspace's default plan; that is request_plan_promotion, which the member approves in the product. Never invent a name, a budget or a constraint; a needs_input warning lists what to ask. Example: model_id="<id>", plan_name="Q4 moderate", total_budget=500000.

Parameters:

- `channel_overrides`, array: Custom only: per-channel bounds the member named.
- `constraint_type`, string: How far each channel may move from its historical spend; blank = Moderate, reported in defaults. One of: Current, Conservative, Moderate, Aggressive, Custom.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `plan_name` (required), string: The name the plan is saved under, visible to colleagues in the console; as the member stated it, never invented.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `time_period`, string: The plan horizon; blank = a quarter, reported in defaults. One of: month, two months, quarter, six months, nine months, twelve months.
- `total_budget` (required), number: The budget to plan, in the model's currency, as the member stated it.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `request_plan_promotion`: Request a plan promotion

Scope `mia.decide`. destructive, open-world, needs the member's decision in the product.

Ask the member to make an optimised plan the workspace's default plan in Lifesight (needs the mia.decide scope). Promotion sets the default scenario the team plans against; it is NOT a financial transaction: no money moves, no payment runs, no ad-platform spend changes. This tool never performs the promotion: it optimises the budget with the model and PAUSES for a human decision; on approval the plan is saved under plan_name and promoted (so mia.decide covers that save); on rejection nothing is saved. The member approves or rejects it in the Lifesight product, never here. It returns approval_id, the summary and expires_at (or a handle when the solve is slow: read it with get_approval_status). Then read the decision with get_approval_status. Never invent a name, a budget or a constraint; never tell the member the plan was promoted until get_approval_status says approved. Example: model_id="<id>", plan_name="Q4 plan", total_budget=500000.

Parameters:

- `constraint_type`, string: How far each channel may move from its historical spend; blank = Moderate, reported in defaults. One of: Current, Conservative, Moderate, Aggressive, Custom.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `plan_name` (required), string: The name the plan is saved under, visible to colleagues in the console; as the member stated it, never invented.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `time_period`, string: The plan horizon; blank = a quarter, reported in defaults. One of: month, two months, quarter, six months, nine months, twelve months.
- `total_budget` (required), number: The budget to plan, in the model's currency, as the member stated it.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## ads-data

### `query_ads_data`: Query ads data

Scope `mia.read`. read-only, idempotent, open-world.

Ask a natural-language question of the workspace's ads mart in BigQuery (the ad platforms' own reported spend, impressions, clicks, conversions, ROAS and CPA by platform, campaign and day), through Lifesight's data agent for the workspace: e.g. "Google Ads spend by week last month". Platform-REPORTED figures, not the model's incremental ones: for what a channel drove use get_mmm_report. Rows are capped; narrow by platform, campaign or window.

Parameters:

- `question` (required), string: The question, in words, naming platforms, metrics and the window.
- `workspace_id`, string: Run in this workspace for this call only.

## core

### `list_mmm_models`: List MMM models

Scope `mia.read`. read-only, idempotent, open-world.

The workspace's marketing mix models: the champions (signed off, the ones to report and plan on), newest first, with model id, display name, outcome KPI, currency and data window. Use it to pick the model_id every other MMM tool takes, or when the member asks which models exist. Challengers (models under review) are counted but not listed unless include_challengers is true; do not plan on one. outcome_kpi filters by the model's KPI, matched exactly and case-insensitively (revenue, conversions, installs). Example: outcome_kpi="revenue". A workspace with several champions for one KPI has no tie-break rule: show them and let the member choose. data.sections_available lists what get_mmm_report can read for a model.

Parameters:

- `include_challengers`, boolean: Also list models under review. Only when the member asks to see them.
- `outcome_kpi`, string: Only models whose outcome KPI matches (exact, case-insensitive), e.g. revenue.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## model-insights

### `get_mmm_report`: MMM report

Scope `mia.read`. read-only, idempotent, open-world.

What a marketing mix model says, by section, in one call: contributions (what each channel drove), contribution_trends, accuracy (fit), causal_structure, incremental_revenue, roi_spend_share, platform_spend, platform_engagement, input_correlation, immediate_vs_carryover, marginal_roas, sem_effects (direct vs indirect effects and halo), decomposition (the series split into drivers), response_curves; and the diagnostics backtests, calibration, attribute_quality. Default sections: contributions, accuracy, causal_structure. Ask for every section the question needs at once; a section the model cannot produce is reported as unavailable, the others still answer. Dates blank = the model's own data window; dates outside it return no data rather than a guess. Figures are in the model's currency and KPI (units in provenance); ROAS is a multiplier, an index is not an amount. Example: model_id from list_mmm_models, sections=["contributions","marginal_roas"]. For one channel's headroom use get_channel_saturation_curves; for a plan use the budget tools.

Parameters:

- `end_date`, string: Window end, YYYY-MM-DD; blank uses the model's own window.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `sections`, array: The sections to read; default contributions, accuracy, causal_structure. One of: accuracy, attribute_quality, backtests, calibration, causal_structure, contribution_trends, contributions, decomposition, immediate_vs_carryover, incremental_revenue, input_correlation, marginal_roas, platform_engagement, platform_filters, platform_spend, response_curves, roi_spend_share, sem_effects.
- `start_date`, string: Window start, YYYY-MM-DD; blank uses the model's own window.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

### `get_channel_saturation_curves`: Channel saturation curve

Scope `mia.read`. read-only, idempotent, open-world.

How far ONE channel can scale before the next unit of spend stops paying for itself, read off the model's response curve: the saturation cap at a target return (null with a note when the return stays above the target to the curve's end), the operating point at the end of the curve period with its marginal ROAS (marginal CPA on a count model), the model's own optimised point on the same curve, the inflection point (past it is diminishing returns, not saturation), and where the sample ends; on detailed also the Hill parameters, time to conversion, curve points and adstock. No new solve, no budget. One channel per call; name it as the model does (google_spend) or as the console labels it (Google Ads). Spend figures cover the whole curve period, not a week, in the model's currency. Example: channel="Google Ads", model_id from list_mmm_models. For a plan's allocation use the budget tools.

Parameters:

- `channel` (required), string: The channel, as the model names it or as the console labels it.
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `target_roas`, number: The return the next unit of spend must still earn; 1.0 means it pays for itself.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## causal-attribution

### `get_attribution_report`: Causal attribution report

Scope `mia.read`. read-only, idempotent, open-world.

Incremental ad performance over a window, from the causal attribution read, by analysis: performance (the incremental breakdown: spend, platform-reported and incremental revenue, iROAS, mROAS per row), pacing (what is under or over its daily plan), creatives (the best ads by an incremental metric), incrementality (how much of the platform's claimed revenue is real), saturation (channels at or past their efficient point at target_roas) and budget_allocation (a linear split of target_budget; only when the member gives a budget). Default: every analysis but budget_allocation. start_date and end_date are REQUIRED: without a window the read is a nightly snapshot that answers nothing. level: ACCOUNT, CAMPAIGNS (default; pacing needs this or finer), ADSET or AD. The result names the model the calibration uses and the promoted plan. Spend and revenue are in the workspace's currency; a ROAS is a multiplier; an incremental factor is a fraction of platform-reported revenue. Example: start_date="2026-08-01", end_date="2026-08-31", analyses=["incrementality","pacing"]. For what the MMM says a channel drove use get_mmm_report; for a lift test use get_geo_experiments.

Parameters:

- `analyses`, array: The analyses to derive from the one read; default every one but budget_allocation. One of: performance, pacing, creatives, incrementality, saturation, budget_allocation.
- `end_date` (required), string: Window end, YYYY-MM-DD. Required.
- `level`, string: Granularity of the breakdown; pacing needs CAMPAIGNS or finer. One of: ACCOUNT, CAMPAIGNS, ADSET, AD.
- `metric`, string: For creatives: the incremental metric to rank ads by. One of: iRoas, iRevenue, iFactor, platformVsIncrementalRevenue, pRoas, pRevenue, spend.
- `min_share_floor`, number: For budget_allocation: the smallest share any channel may keep (a fraction).
- `min_spend`, number: For creatives: ignore ads below this spend so tiny-sample winners do not top the list.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `start_date` (required), string: Window start, YYYY-MM-DD. Required.
- `target_budget`, number: For budget_allocation: the budget to split, as the member stated it. Never invent one.
- `target_roas`, number: For saturation: the return a channel must still earn to count as unsaturated.
- `top_n`, integer: For creatives: how many ads to rank.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## experiments

### `get_geo_experiments`: Geo experiments

Scope `mia.read`. read-only, idempotent, open-world.

The workspace's geo and time incrementality experiments. Without experiment_id it lists them, newest first, with id, kind, name, status, outcome KPI, treatment dates, channels and cells; filter by status (the platform's values), kind (GEO, TIME, EXTERNAL), channel or a name fragment. With experiment_id it reads that experiment's report by section: results (lift and significance per cell, test vs control), recommendations (the market designs to run next), lift_over_time (treatment vs counterfactual series), power_curve, pre_period_fit, control_markets (test markets and control weights), progress (a live experiment's stage and day) and secondary_fit. Default sections: results, recommendations, lift_over_time, progress. Lift is a percent, iROAS a multiplier, weights fractions. Example: status=["COMPLETED"] to find one, then experiment_id="<id>", sections=["results"]. For modelled channel effects use get_mmm_report; for incremental ad performance over a window use get_attribution_report.

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

Scope `mia.read`. read-only, idempotent, open-world.

Which creative tactics an MMM model measures (prospecting, retargeting, and so on) and the reported paid spend behind them. Two reads in one call: the model's tactic list (with has_tactics false when the model has no tactic breakdown and the list is its CHANNELS; say so) and the workspace's resolved spend by tactic where the taxonomy resolved one (source_table says whether the taxonomy or the raw ads mart answered). Use it for "what tactics does this model know", "what did we spend by tactic", or to put spend beside an incrementality read. This is REPORTED spend in the workspace's currency, not a modelled contribution: for what a tactic or channel DROVE use get_mmm_report; for the best ads by incremental return use get_attribution_report with analyses=["creatives"]. Example: model_id from list_mmm_models; include_spend=false for the tactic list alone.

Parameters:

- `include_spend`, boolean: Also read the workspace's resolved paid spend by tactic (default true).
- `model_id` (required), string: The MMM model id from list_mmm_models.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## data-pipeline

### `get_data_source_health`: Data source health

Scope `mia.read`. read-only, idempotent, open-world.

The workspace's connected data sources (ad platforms, conversion sources, uploads) and whether data is flowing. Without integration it lists every source with its health: live (data flowing), attention (a member must act: auth error, failed sync, transformation error), setup (authorised, not yet flowing) or paused. With integration it adds that source's recent sync runs (newest first): when the last sync succeeded or failed, rows ingested per run, error codes. The rule: an integration that is a UUID is read directly; a name ("Meta", "Google Ads") is resolved from the list in the same call and the summary gives the id to call again with. Use it for "is anything broken", "when did Meta last sync", "did fewer rows land yesterday". Rows are the platform's own counts; times are the platform's timestamps. Example: no arguments, then integration="<uuid>". For spend that stopped or spiked use detect_spend_anomalies; a stale source is a pipeline matter, not a campaign anomaly.

Parameters:

- `integration`, string: One source: its integration id (a UUID, read directly) or its name (resolved from the list; the summary then gives the id). Leave out to list every source.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## anomaly-detection

### `detect_spend_anomalies`: Spend anomalies

Scope `mia.read`. read-only, idempotent, open-world.

What looks off in the workspace's paid media over the last days: spend that spiked, dropped or stopped, ROAS or CTR that moved sharply, revenue off its recent run rate, per ad platform (source) and per campaign, each compared over its last window_days against the days before and anchored on that source's own latest day. Findings come worst first with the detector's own window and baseline values, their basis (daily mean, window total vs run rate, or ratio), the change in percent and, for spend, a z-score; the rules that judged them ride along. Stale sources are named apart: a source days behind is a pipeline matter, not a campaign anomaly. Use it for "any anomalies this week", "did anything stop spending", "why did ROAS drop on Meta". window_days 1 to 30, default 7; source is the mart's key (facebook_ads, google_ads) or blank for every source. Spend is in the workspace's currency. Example: window_days=7, source="facebook_ads". For a broken connector use get_data_source_health; for whether the spend was incremental use get_attribution_report.

Parameters:

- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `source`, string: One ad platform by the mart's source key (facebook_ads, google_ads, rtb_house); leave out to scan every source.
- `window_days`, integer: The comparison window in days; the baseline is the 28 days before it, or four windows when longer.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## knowledge

### `search_lifesight_docs`: Search Lifesight docs

Scope `mia.read`. read-only, idempotent, open-world.

Search the Lifesight product documentation: what a term or methodology means (adstock, saturation, MMM calibration, geo lift), how a feature works, how to do something in the product. The same answer for every customer; it never reads the member's data. Returns the matching chunks as text, each headed by its document title and section, best first; answer from them and cite the section. mode semantic (default) fuses meaning and keyword hits and re-ranks, up to 15 chunks; keyword is the exact-term fallback ("MROAS", "MROAS OR adstock"), up to 10, for when semantic found nothing or the query is an identifier. section narrows to one documentation section; list_sections=true returns the section names instead of searching. Concise returns the first three chunks when many matched; detailed returns every chunk. Example: query="what is adstock decay", or query="MROAS", mode="keyword". For the member's own figures use the model, attribution and planning tools, never the docs.

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

Scope `mia.write`. open-world.

Raise a ticket with Lifesight support in the member's name, or check one raised before (needs the mia.write scope). Use it when the member asks for support or a human, disputes figures, hits an error that a retry will not fix, or finds data missing or wrong. To raise one give summary (one line, the ticket's title), description (the member's own words, never paraphrased away) and category: technical_error, data_issue, customer_disagreement, agent_misbehavior, user_escalation or feature_request; priority low, medium (default), high or critical. To check one give ticket_key only (the key returned when it was raised, never invented). Returns the key and its link, or the ticket's state, assignee and last update. A ticket is visible to Lifesight staff: raise one only when the member asked.

Parameters:

- `category`, string: What kind of issue (to raise). One of: technical_error, data_issue, customer_disagreement, agent_misbehavior, user_escalation, feature_request.
- `description`, string: The member's own words about the problem (to raise).
- `priority`, string: How urgent. One of: low, medium, high, critical.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `summary`, string: One line, the ticket's title (to raise).
- `ticket_key`, string: A ticket raised before (its key, e.g. MIA-123), to check its state; leave out to raise one.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## cue-cards

### `get_cue_cards`: Cue cards

Scope `mia.read`. read-only, idempotent, open-world.

What needs the member's attention today: the top cue cards their workspace agents raised (anomalies, broken data sources, plans to review, questions waiting on them), scored and ranked for this member, filtered to what they may see, each with a deep link into the product. Use it for "what should I look at", "what is waiting on me", "my top five things". The cards are delivered BESIDE the result, not inside data: read them from the accompanying content. limit is 1 to 20, default 5; give a number only when the member names one. Card actions (dismiss, snooze, take it, approve) stay in the product through the card's link. Example: no arguments, or limit=3. For the figures behind a card use the tool it names (detect_spend_anomalies, get_data_source_health, get_saved_plans).

Parameters:

- `limit`, integer: How many cards, 1 to 20; 5 unless the member names a number.
- `response_format`, string: concise: the summary, headline figures and links (default unless the tool says otherwise). detailed: the full payload and, where the tool draws, the artifact data. One of: concise, detailed.
- `workspace_id`, string: Run in this workspace for this call only (a workspace id from get_workspace_context). Leave out to use the active workspace.

## Server instructions

What a client reads before the first call:

```
Lifesight marketing measurement for this member's workspaces: marketing mix models (MMM), causal attribution, geo-lift experiments, budget optimisation and saved plans, data-source health, spend anomalies, creative performance, the member's cue cards, and the product docs.
Start with get_workspace_context: the workspaces the member holds and the active one, the champion models with KPI, currency and data window, the promoted plan, today's date.
Every result is a structuredContent object: the answer in `summary`, the payload in `data`, the workspace, `provenance` (which platform read each figure came from, its unit and currency), console `links`, `warnings` (no_data, defaults taken, inputs still needed, reconciliation findings). Figures come only from tool results; the server computes compares, shares and totals, so quote them rather than recomputing; check_figures tells you which figures in a draft the thread's results ground before you show them. A needs_input warning lists the questions to put to the member.
switch_workspace changes the active workspace for this connection; every tool also takes workspace_id for one call.
Long work never holds a call: start_budget_optimisation answers inline when quick, else with a handle for get_budget_optimisation; start_mia_investigation runs Lifesight's own investigator, Mia, on a thread (a compound investigation asked for by name, or to continue a product thread) and get_mia_investigation reads it; poll every poll_after_s seconds. compare_channel_measurements puts a channel's four measurements side by side and says which to plan on. query_ads_data answers in words over the ad platforms' own figures. The prompts are the workflows members run most.
save_budget_plan (mia.write) saves a plan by name; request_plan_promotion (mia.decide) never promotes: the member approves in the product and get_approval_status reads the decision; promotion moves no money. A scope the connection does not hold is refused; say so and point to the product.
```
