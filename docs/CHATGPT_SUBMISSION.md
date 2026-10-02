# The ChatGPT submission (WP-CG3.4)

The owner's runbook for submitting Ask Lifesight to the ChatGPT plugin directory: what the package already
carries, what the owner supplies on the day, the dashboard steps as OpenAI documents them (read 2026-10-02 at
`developers.openai.com/plugins/deploy/submission`), what happens after, and the gate. Nothing here concerns
the Claude listing, except one rule: no visible change to the shared server lands while both reviews are open.

Plan: `docs/CHATGPT_DISCOVERY_BUILD_PLAN.md` CG3.4 in the harness repo. Depends on CG3.1 (the package), CG3.2
(the developer-mode proof), CG3.3 (the selection eval, whose cases the review block quotes), EXT-2 (the
populated test workspace). Decision D-26: submit from a global-residency project; Europe verified before
promised.

## 1. What the package carries (built)

| Item | Where | State |
|---|---|---|
| the manifest, listing fields, assets, twelve skills | `plugin.json`, `assets/`, `skills/` (CG3.1) | built |
| five positive review cases: description, prompt, `tools_triggered` (a comma-separated string, as the page documents), `expected_behavior` | `extensions.com.openai.review.test_cases.positive` | built; the prompts are the harness selection eval's indirect prompts for the weekly readout, budget reallocation, saturation and headroom, data health and anomaly triage, verbatim; the tools are every tool the workflow's skill drives, the first after the context named in the behaviour; each behaviour is server-observable (which tools answer, units and currency and provenance on every figure, a no-data result stated) with the data-window caveat conditional. **Rewrite each to what was observed on the test workspace before submitting** (step 5): a champion whose window ends before last week makes the weekly case read differently |
| three negative review cases: description, prompt | `extensions.com.openai.review.test_cases.negative` | built; OpenAI defines a negative as a prompt the plugin should not act on with the expected refusal or safe fallback (its examples are refusals, not off-topic questions), so the three are the plugin's own refusals: a save (the connection reads only, D-20), a promotion (never taken by the plugin; the member approves in Lifesight), a workspace the account does not hold. The off-topic prompts of the selection eval stay in the harness eval, where they measure selection |
| the commerce declaration | `review.commerce: false`, `review.commerce_description` | built: nothing is bought, sold or paid for; plan promotion moves no money |
| release notes for this version | `extensions.com.openai.publication.release_notes` | built |
| the checker's submission mode | `scripts/check_openai_package.py --submission` | built: refuses a package without the demo recording URL or the countries |

## 2. What the owner supplies on the day

| Input | Where it goes | Notes |
|---|---|---|
| the video walkthrough | `review.demo_recording_url` (https, reachable by the reviewer) | the five positive cases in order, on the test workspace; a hosted link (Drive with link access, Loom) |
| the countries | `publication.countries`, uppercase ISO codes | D-26: a global-residency project; the EEA, Switzerland and the UK only once availability there is verified (research note A: no 2026 primary statement lifts the exclusion) |
| the category | the dashboard's list (the manifest's "Productivity" is a placeholder) | pick at upload |
| the reviewer's test account | the dashboard: Metadata & Skills, Review information, Review details (login URL, workspace, sign-in instructions) | EXT-2's test workspace, populated with sample data, not a real customer's; no MFA, no email or SMS code, no magic link, no private network; it must work at once; the admin has turned ChatGPT on in that workspace (the hosts row). Reads only is not a choice here: D-20 never grants a ChatGPT connection the write scopes, which is why two negatives are a save and a promotion refused. Keep the account and its data available for later reviews |
| the domain-verification token | the gateway's `OPENAI_APPS_CHALLENGE_TOKEN` (CG2.2, platform PR #491) | the dashboard shows the token; the gateway serves it as plain text at `https://ask.lifesight.io/.well-known/openai-apps-challenge`; a blank token answers 404 by design (the controller in #491; as of 2026-10-02 the live host answers 404, so either the route is not deployed or the token is blank) |
| the privacy page content | `https://lifesight.io/privacy-policy/` | OpenAI's five topics (categories of personal data, purposes, recipients, retention timelines, controls) plus one sentence each on what the host receives, what Lifesight stores and what it never receives |
| a LICENSE file | the repo root | two manifests (`plugin.json`, `.claude-plugin/plugin.json`) say Apache-2.0; none exists |
| the version | `plugin.json` and `.claude-plugin/plugin.json`, the same number | any metadata or skill change after an upload needs a new version and a complete ZIP; a change to the hosted tools needs no upload |

## 3. The steps

1. Fill §2's manifest fields (the demo URL, the countries), bump the version if anything changed since the
   last upload, then build:

   ```
   uv run --no-project --with jsonschema python -I scripts/check_openai_package.py --submission
   uv run --no-project --with jsonschema python -I scripts/build_openai_zip.py
   ```

   The first refuses a package the dashboard would refuse; the second writes `dist/ask-lifesight-chatgpt.zip`.
2. In the Plugins dashboard: Upload new or existing plugin, Upload plugin, choose the ZIP. Read the automated
   findings under "Metadata & Skills" and "MCPs"; fix and re-upload until clean.
3. Domain verification: the portal shows a challenge token; set it on the gateway (`OPENAI_APPS_CHALLENGE_TOKEN`),
   deploy, and confirm `curl https://ask.lifesight.io/.well-known/openai-apps-challenge` answers the token as
   plain text; then verify in the portal.
4. Pick the category, confirm the listing fields render, attach nothing else (a ZIP with app references or
   lifecycle hooks cannot be submitted; `mcp.json` is the route).
5. Reviewer access: the test account, login URL, workspace and sign-in instructions; run the five positive
   cases yourself on that account first and keep the transcripts.
6. Select the draft, Submit for review, complete the policy attestations. One review is active per plugin at a
   time (the submission page); no expedite requests (the plugin policies page, research note B). A value the
   package carries (the demo URL, the cases) is reapplied on submit over anything edited in the dashboard, so
   change the manifest, not the form.
7. If the Claude listing's review window (EXT-3) is open, land no visible change to the shared server until
   both reviews close (§0.4 of the plan).

## 4. After submission

- Feedback arrives by email. A rejection names the reason; fix, bump the version, re-upload, resubmit. An appeal is
  a reply to the rejection email.
- After publication OpenAI scans the hosted MCP server daily (a scan can be requested right after a deploy): a new
  tool stays unavailable until approved, and a changed tool keeps its previously approved metadata while the update
  is held. A tool rename is therefore a listing event.
- The listing URL goes on the plan's status board and into the console's card
  (`VITE_ASK_LIFESIGHT_CHATGPT_PLUGIN_URL`, CG2.3), which until then says the link follows the listing.
- CG3.6 then watches the by-host measures and searches the directory for the listing's terms.

## 5. The gate

Listed in the directory; the listing URL on the status board and in CG2.3's card; the review cases as run by the
reviewer match what the harness returned on the test workspace.

## 6. Results

| Item | Result | Date |
|---|---|---|
| ZIP uploaded, automated checks clean | | |
| domain verified | | |
| submitted for review | | |
| review outcome | | |
| listing URL | | |
| card variable set and deployed | | |
