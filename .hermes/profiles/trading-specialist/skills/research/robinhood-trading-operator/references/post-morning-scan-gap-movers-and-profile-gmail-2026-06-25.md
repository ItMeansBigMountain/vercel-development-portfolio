# Post-morning scan: gap movers + profile-scoped Gmail token (2026-06-25)

Use this reference when a scheduled post-morning Agentic scan needs broader candidate discovery beyond stale watchlists and the default Google Workspace CLI token is not authenticated.

## What worked

- Verify the profile-scoped Workspace token first with the user's helper:
  - `python3 /opt/data/scripts/google_reauth_workflow.py verify workspace personal-main`
- If default `google_api.py` says `Not authenticated`, run it with the profile-specific Hermes home instead of stopping newsletter/source checks:
  - `HERMES_HOME=/opt/data/google_profiles/personal-main python /opt/data/hermes-agent/skills/productivity/google-workspace/scripts/google_api.py gmail search '<query>' --max 20`
- Keep the Google action read-only for market-source scans.
- Treat broad newsletter keyword searches as source discovery, not a trade signal. In this run, broad TLDR/Robinhood/Snacks search mostly returned TLDR InfoSec, which is usually not a direct equity catalyst.

## Candidate workflow pattern

1. Verify Agentic account, portfolio, positions, option positions, recent orders, and all open-ish equity states: `new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`.
2. Pull SPY/QQQ/IWM quotes and daily bars for regime.
3. Use Robinhood `Daily movers` as a fresh universe when watchlists are stale.
4. Quote and chart the Daily Movers subset plus current holdings.
5. For gap leaders, separate broker/tradability success from strategy quality:
   - strong catalyst + big gap is not automatically a buy;
   - wait for retest if price is far above prior close/support;
   - document the no-chase decision when R:R cannot be calculated cleanly at current price.
6. Journal even no-trade decisions with exact account state, candidates, trigger levels, and tool limitations.

## Useful Gmail search patterns

- Broad but noisy: `("Robinhood Snacks" OR from:snacks@robinhood.com OR from:news@robinhood.com OR subject:Snacks OR from:tldrnewsletter.com) newer_than:7d`
- If broad search only finds TLDR InfoSec, report that source limitation and do not overstate it as market confirmation.

## Pitfalls

- Do not say there are no open equity orders after checking only one state; query all practical open-ish states.
- Do not force deployment toward the 70%–90% policy target when candidates are extended gaps or current positions are already under pressure.
- Do not add to losing NVDA/SOFI just to use buying power; first require reclaim/stabilization and a fresh risk plan.
