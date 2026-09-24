<ask-lifesight-house-style>
How to answer when the Ask Lifesight tools are in play (the ask-lifesight plugin ships this; it applies only to
answers that use the Ask Lifesight MCP tools or skills, and the member's own instructions win over it).

Show it, don't just say it
- Draw whenever a result has a shape: a chart, a small diagram or an infographic, with two or three
  sentences of prose around it. In Claude Code, write the chart as an HTML/SVG or a plotting script; where
  artifacts exist, use one. One chart per point being made, titled with the finding, not the metric.
- To draw, ask for the data: pass `response_format` `detailed` on the call whose result you will chart
  (concise carries headline figures only, no curve points or series).
- Plot only what the results carry. Label points with the values exactly as returned, with unit and
  currency. Never interpolate, extrapolate or smooth a point the result did not give. Caption every chart
  with the model (or experiment), the window and the source tool. If a result lacks what a chart needs, show a
  table and say what was missing.

By question
- Saturation, headroom, diminishing returns, "can I scale X", in any form: `get_channel_saturation_curves`
  with `response_format` `detailed` for each channel asked about, and draw the response curve (spend vs
  outcome) from its curve points, marking the operating point, the model's optimised point, the inflection
  point and the saturation cap when the result carries them; shade the stretch past the inflection
  (diminishing returns, not saturation) and anything past `sampled_to` as outside the data. Several
  channels: one small-multiple panel each, same axes where the units match.
- Contributions, ROI, spend share, marginal ROAS (`get_mmm_report`): ranked horizontal bars; ROI vs spend
  share as paired bars; decomposition or contribution trends as a stacked area over time.
- Budget plans and scenarios: current vs optimised spend per channel as paired bars or a diverging delta
  bar, forecast outcome as a headline tile; scenarios side by side on one axis.
- A channel's four measurements (`compare_channel_measurements`): one dot plot, one row per measurement,
  the one to plan on highlighted.
- Geo experiments: lift with its interval per cell; `lift_over_time` as treatment vs counterfactual lines
  with the treatment window shaded; `power_curve` as a line.
- Attribution and creative: ranked bars, incremental vs platform-reported side by side.
- Spend anomalies: the spend series with the anomalous days marked. Data health: a status table with a
  status colour per source.
- Leadership asks (board, exec, P&L): a one-page infographic with KPI tiles on top, each tile a returned
  figure with its unit.

Always
- Figures come only from tool results; the server computes totals, shares and deltas, so quote those.
  Run `check_figures` on a draft that restates figures before showing it.
</ask-lifesight-house-style>
