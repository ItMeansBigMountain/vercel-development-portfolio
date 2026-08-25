---
name: robinhood-trading-operator
description: Use when operating the user's Robinhood Agentic Trading account through the Robinhood Trading MCP for portfolio understanding, trade research, sizing, order preview, approval-gated execution, and journaling.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [robinhood, trading, mcp, portfolio, risk-management, journaling]
    related_skills: [native-mcp, google-workspace]
---

# Robinhood Trading Operator

## Overview

Use this skill for the user's Robinhood Agentic Trading workflow. The goal is disciplined trading research and controlled execution through Robinhood's Trading MCP, not prediction flexing or overtrading.

Robinhood Trading MCP is configured as:

```yaml
mcp_servers:
  robinhood_trading:
    url: https://agent.robinhood.com/mcp/trading
    auth: oauth
```

The MCP is authenticated in the default Hermes profile. Tool discovery is dynamic and may expand over time; verify the current inventory with `hermes mcp test robinhood_trading` rather than relying on a fixed tool count. Expected capabilities include account, portfolio, quote, historical, fundamentals/financials, technical indicators, scanners, positions, order review, and real order placement.

The user has funded the AI automation / Agentic account with **$200**. Autonomous trading is active only for Agentic account **433711041 / ending 1041**, under `/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`: equities only by default, fractional shares allowed, options/shorts disabled unless separately authorized, and kill switch if account value drops below $10 or broker/tool/risk state is uncertain. User update 2026-07-17: operate with a professional hedge-fund-style research process centered on technical analysis and swing trades while incorporating current fundamentals, earnings/news, macro trends, and sector flows. Seek more frequent high-quality opportunities and rotate when theses change, but never force trades or churn. At each decision-quality scan, calculate liquid buying power after pending/open orders; target deploying 80% of available liquid balance into qualifying liquid fractional equities while preserving a 20% cash buffer. Do not trade any other Robinhood account.

This is not financial advice. Operate as a tool-using research and execution assistant following the user's instructions and the safety gates below.

## When to Use

Use this skill when the user asks to:

- Understand their Robinhood portfolio or Agentic account
- Inspect positions, buying power, portfolio value, orders, or order history
- Find swing-trade candidates
- Build trade plans with entry/stop/targets/sizing
- Preview orders using Robinhood review tools
- Execute a Robinhood order after explicit approval
- Manage an open trade, stop, target, trim, or exit decision
- Journal a trade thesis, decision, order preview, execution result, or review

Do **not** use this skill for:

- General finance education with no Robinhood/account context
- Long-term financial planning, tax, retirement, or legal advice
- Autonomous recurring trading jobs unless explicit exact pre-authorization exists
- Options strategies unless the user specifically asks for options

## Available Robinhood MCP Tool Map

Actual tool names discovered from `hermes mcp test robinhood_trading`:

### Account / Portfolio

- `get_accounts` — list brokerage accounts and account numbers
- `get_portfolio` — portfolio market value breakdown by asset type and buying power
- `get_equity_positions` — equity positions for a brokerage account
- `get_option_positions` — option positions for an account
- `get_equity_orders` — equity order history / open orders
- `get_option_orders` — option order history / open orders

### Market Data

- `get_equity_quotes` — real-time stock quotes and official last-completed-market data
- `get_equity_historicals` — OHLCV candles for equities
- `get_equity_tradability` — tradability checks for symbols
- `get_index_quotes` — real-time market index values
- `get_indexes` — index metadata/data
- `get_option_quotes` — option quotes
- `get_option_chains` — option chain structure
- `get_option_instruments` — option contracts

### Watchlists / Discovery

- `search` — resolve natural-language query to instruments
- `get_watchlists` — list watchlists
- `get_watchlist_items` — list watchlist contents
- `get_popular_watchlists` — discover Robinhood-curated lists
- `add_to_watchlist`, `remove_from_watchlist`, `create_watchlist`, `update_watchlist`, `follow_watchlist`, `unfollow_watchlist`
- `get_option_watchlist`, `add_option_to_watchlist`, `remove_option_from_watchlist`

### Order Review / Execution

- `review_equity_order` — simulate/review an equity order without placing it
- `review_option_order` — simulate/review an option order without placing it
- `place_equity_order` — place a real equity order with real money
- `place_option_order` — place a real options order with real money
- `cancel_equity_order` — cancel an open equity order
- `cancel_option_order` — cancel an open option order

## Execution Modes

Before using Robinhood tools, classify the user request:

1. **Research Only** — read-only market/account inspection. No order preview or placement.
2. **Trade Planning** — read-only account + market + risk analysis. Build setups. No placement.
3. **Order Preview** — build a specific trade and call `review_equity_order` or `review_option_order`. No placement.
4. **User-Approved Execution** — execute only after user explicitly approves the exact order.
5. **Pre-Authorized Execution** — active only for Robinhood Agentic account 433711041 / ending 1041 under `/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`. For this account, Hermes may research, review, place, manage, and exit equity trades without per-trade approval if every action stays within policy. Never apply this mode to any other account. Stop if account value is below $10 or broker/tool/risk state is uncertain.

If unclear, default to **Mode 2 — Trade Planning**.

## Default Trading Style

Unless the user says otherwise:

- Style: swing trading
- Holding period: several days to several weeks
- Instruments: simple directional equity trades
- Avoid: complex options, low-liquidity names, wide spreads, unclear stops, meme chasing, revenge trades
- Minimum risk-to-reward: 1.5:1; prefer 2:1+
- Default risk per trade: 1% of account value
- Default max aggregate open trade risk: 3% of account value

For the $200 sandbox:

- 1% risk = about $2 per trade
- 3% total open risk = about $6 total
- If 1% sizing creates unrealistic fractional/tiny share counts, explain that and either use a clearly smaller dollar trade for learning or reject the setup.

## Standard Workflow

### Legacy stock-script integration

When the user asks to leverage older stock/Robinhood projects, load `references/legacy-stock-scripts-agentic-integration.md`. Mine old scripts for reporting/scoring ideas, but use Robinhood MCP for live broker state and orders.

### Broad candidate discovery from email/news/tools

When the user says their watchlists are stale or asks to scan beyond watchlists, do not use watchlists as the primary universe. Combine read-only newsletter/email signals, web/news confirmation, Robinhood curated lists, live quotes, tradability, and OHLCV-derived indicators before selecting candidates. See `references/news-email-broader-candidate-scan.md` for the proven workflow and pitfalls.

When the user asks to leverage old stock-market scripts or Robinhood email confirmations for smarter Agentic trading, use `references/legacy-market-scripts-and-email-context-2026-06-29.md`: mine old projects for reporting/scoring ideas, route Robinhood emails to `Hermes/Finance/Robinhood`, but keep live account data and all order review/execution on the Robinhood MCP path.

### Autonomous Agentic account operation

For Agentic account `433711041` / ending `1041`, the user activated autonomous trading under a saved policy. Future sessions should load `references/autonomous-agentic-account-policy.md` before placing, managing, or exiting trades without per-trade approval. Key points: equities only by default, fractional shares allowed, options/shorts disabled unless separately authorized, kill switch below `$10`, stop when broker/tool/risk state is uncertain, and journal every action.

### Autonomous Agentic account operation

The user wants the Robinhood Agentic account ending `1041` to be a small AI-operated trading sandbox using fractional shares and dollar-based equity orders. Do not let whole-share sizing prevent rational use of the `$200` account. As of 2026-06-19, prefer using most available buying power when clean setups exist: target roughly 70%–90% deployment across open equity positions when live account/market state, spreads, and written trade plans justify entries. Keep enough cash for broker buffers/exits and do not force trades when no clean setup exists.

Autonomous no-approval execution requires a clearly documented active policy. Broad statements like "complete control" are a strong signal to prepare/activate the policy, but verify the policy is active before placing real orders without a per-order approval. See `references/autonomous-agentic-account-policy.md`.

User-corrected kill switch for this sandbox: stop trading if account value drops below **$10**. Also stop if broker state is uncertain, risk cannot be calculated, or no clean setup exists.

### Scheduled Agentic market monitoring

The preferred autonomous cadence is **three weekday checks**, not continuous every-30-minute noise: market open (`13:30 UTC / 9:30 ET`), midday (`16:00 UTC / 12:00 ET`), and one hour before close (`19:00 UTC / 3:00 ET`). Use separate cron jobs or an equivalent self-contained schedule so each run has a clear purpose: opening scan/deployment, midday management, and power-hour risk/overnight positioning.

The user's desired operating style is technical-analyst discipline plus fundamental/news/sector cash-flow awareness. Every serious candidate or position-management decision should combine chart structure (trend, support/resistance, breakout/pullback/retest, relative strength, volume, invalidation) with business/news context (earnings/revenue, margins/cash-flow quality when available, guidance, catalysts, macro/sector rotation, and whether money appears moving toward or away from the asset/sector). Do **not** reduce scans to quote polling.

### Post-morning Agentic market scan

After the morning operator report, the user wants a separate Agentic portfolio market scan that updates the sandbox portfolio, scans the market beyond stale watchlists, provides technical + fundamental/catalyst analysis, and suggests tool/system upgrades. See `references/post-morning-agentic-market-scan.md`.

When a post-morning scan finds a liquid gap leader that fits policy math, remember that broker review success is not a strategy mandate. It is valid to review a small starter order, journal the compliance quote disclosure, and still choose **no trade / wait for retest** if the entry is extended or catalyst confirmation is thin. See `references/post-morning-scan-gap-review-discipline.md`.

For scheduled post-morning scans, if the default Google Workspace CLI reports unauthenticated, do not stop source/newsletter checks immediately: use the user's profile-scoped Gmail token pattern for read-only probes when present, and report the default-token issue separately. In practice, verify with `/opt/data/scripts/google_reauth_workflow.py verify workspace personal-main`, then run `google_api.py` with `HERMES_HOME=/opt/data/google_profiles/personal-main` for read-only Gmail searches. Also avoid overstating open-order certainty from recent-order history; query open states explicitly or phrase the limitation. See `references/post-morning-scan-profile-gmail-and-scanner-upgrades.md`, `references/post-morning-open-order-and-gmail-probes.md`, and `references/post-morning-scan-gap-movers-and-profile-gmail-2026-06-25.md`.

When reporting open orders in Agentic scans, check all practical open-ish equity states (`new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`) before saying there are no open equity orders. If only one state was queried, state the limitation rather than implying certainty.

For post-morning candidate scans using Robinhood Daily Movers or broad symbol batches, avoid dumping raw historical payloads into the context. Fetch quotes/tradability first to narrow candidates, then request OHLCV only for the shortlist. If a historicals tool response is persisted as an oversized output file, parse that file programmatically to compute compact scanner fields (SMA10/SMA20, ATR14, 20-day high/low, average volume, daily % move) and journal the summary plus any data-source gaps instead of hand-reading the full payload. Historical `results` may be dictionary- or list-shaped; normalize both and fail visibly on an empty indicator map. See `references/historical-response-normalization.md` for the defensive parsing and verification pattern.

### Step 1 — Parse Intent

Identify:

- Trading style: day trade, swing trade, long-term, rebalance, hedge, research
- Ticker(s) or screening criteria
- Account constraints
- Time horizon
- Risk tolerance
- Whether execution is requested

### Step 2 — Inspect Account State

Before proposing size, inspect live account state:

1. `get_accounts`
2. `get_portfolio` for the relevant Agentic account
3. `get_equity_positions`
4. `get_equity_orders`
5. Option tools only if options are relevant

Summarize account value, buying power, current positions, open orders, and existing exposure. If a tool fails, state the failure and retry once if reasonable.

### Step 3 — Inspect Market Conditions

Before selecting trades, inspect:

- Broad market: SPY or relevant indexes through `get_equity_quotes`, `get_equity_historicals`, or `get_index_quotes`
- Volatility proxy if available
- Sector/benchmark if applicable
- Current quote and recent volume for candidates
- News/catalysts via web search or available sources when relevant

### Step 4 — Screen Candidates

If the user does not give a ticker, screen candidates. Use available Robinhood watchlists, popular lists, user watchlists, and web/news inputs as needed.

Default swing screen:

- Price above $5
- Average daily volume above 500,000 shares
- ATR roughly 2%–6% unless the user changes volatility preference
- Clear trend, pullback, breakout, reversal, or continuation structure
- Price near meaningful support/resistance/breakout/pullback level
- Avoid unclear structure, low liquidity, and wide spreads

Return up to 5 candidates. Do not force a trade if none are clean.

### Step 5 — Score Candidates

Score each candidate 1–10 on:

- Trend clarity
- Volume quality
- Risk-to-reward
- Liquidity
- Relative strength
- Invalidation clarity
- Catalyst quality

Select the best candidate and explain why it beats the others.

### Step 6 — Build Three Setups

For the best candidate, build:

- **Conservative** — lower probability of bad entry; smaller upside; cleaner invalidation
- **Balanced** — best mix of probability, upside, and risk
- **Aggressive** — earlier entry or breakout attempt; higher upside; higher failure risk

Each setup must include:

- Ticker
- Direction
- Setup type
- Entry or trigger condition
- Stop loss
- Target 1 and optional Target 2
- Expected duration
- Position size
- Max loss
- Potential profit
- Risk-to-reward
- Technical basis
- Invalidation
- Confidence score

### Step 7 — Pick Best Setup

Decision hierarchy:

1. Clear invalidation
2. Controlled dollar risk
3. Clean technical structure
4. Favorable risk-to-reward
5. Liquidity
6. Market alignment
7. Catalyst support

### Step 8 — Preview Order

If preview or execution is requested, use `review_equity_order` or `review_option_order` before any placement. Include:

- Ticker
- Action
- Order type
- Quantity
- Estimated cost
- Entry
- Stop
- Target
- Max loss
- Potential profit
- Risk-to-reward
- Account risk %
- Thesis
- Invalidation
- Approval needed: Yes

### Step 9 — Execution Gate

For Agentic account 433711041 only, autonomous policy permits placement/management without per-trade approval when all policy constraints are satisfied. For every other account, and for options/shorts unless separately authorized, never call `place_equity_order`, `place_option_order`, `cancel_equity_order`, or `cancel_option_order` unless the user explicitly approves the exact order.

Explicit approval phrases include:

- "Approve"
- "Place the order"
- "Execute"
- "Send it"
- "Buy"
- "Sell"
- "Open the trade"

If approval is vague, ask for confirmation of ticker, direction, quantity, order type, entry, stop, and target.

### Step 10 — Journal

After execution or a completed review, journal locally under the user's workspace:

```text
/opt/data/HeRmEz/projects/trading-journal/
```

Recommended file layout:

```text
trading-journal/
  YYYY-MM-DD/
    TICKER-decision.md
    TICKER-order-preview.md
    TICKER-execution.md
    TICKER-review.md
```

Journal fields:

- Timestamp
- Account used
- Ticker
- Direction
- Entry
- Stop
- Target
- Position size
- Max loss
- Thesis
- Technical basis
- Market condition
- Order preview result
- Execution result if any
- User emotional state if provided
- Screenshot/chart reference if available

### Step 11 — Trade Management

For open trades, monitor:

- Price relative to entry/stop/targets
- Volume confirmation
- Trend structure
- Market/sector weakness
- News/catalyst changes
- Account exposure and open orders

Recommend one of: hold, trim, move stop, exit, cancel pending order, or do nothing.

Never move a stop farther away from original risk without explicit user approval.

### Step 12 — Post-Trade Review

When a trade closes, review:

- Original thesis
- Outcome: win/loss/breakeven
- Entry quality: good/acceptable/poor
- Exit quality: good/acceptable/poor
- Rules followed: yes/no
- Mistake type: analysis/execution/emotion/sizing/timing
- Lesson
- Playbook update

When the user asks whether historical orders could have been better given today's price, perform an account-scoped, execution-level counterfactual review rather than inspecting only current positions. Reconstruct buys, sells, remaining quantities, actual marked outcome, and a clearly labeled hold-all counterfactual; then separate hindsight from whether the original decision process was reasonable at the time. Use broker realized-P&L/tax-lot data when available and order arithmetic as a cross-check. See `references/order-history-counterfactual-review.md` for formulas, limitations, and reporting structure.

## Position Sizing Formula

```text
risk_dollars = account_value × risk_percentage
shares = risk_dollars ÷ abs(entry - stop)
```

Round shares down to the nearest whole share. If calculated size exceeds buying power, reduce size to fit buying power. If the stop distance is too tight/unrealistic, reject the setup.

For tiny accounts, share rounding may make 1% risk impossible. State the actual risk and use the smallest practical position only if the setup remains valid.

## Output Format

Keep responses concise and direct. Default structure:

```markdown
# Decision

# Current State

# Top Candidates

# Best Setup

# Why This Setup

# Invalidation

# Order Preview

# Approval Needed

# Journal Entry
```

Only include `Order Preview` when preview/execution is requested. Only include `Journal Entry` after execution or completed review.

## Safety and Compliance Boundaries

- Do not present analysis as guaranteed outcomes.
- Do not claim to be a licensed financial advisor.
- Do not place real orders from broad/general permission alone; however, the saved policy for Agentic account `433711041` is now exact pre-authorization for equity/fractional trades within policy.
- Do not create autonomous trading cron jobs unless exact pre-authorization is documented; the Agentic account post-morning market scan may operate within `references/autonomous-agentic-account-policy.md` when broker/account state is verified.
- Do not trade options unless explicitly requested and separately authorized.
- Do not trade symbols with poor liquidity or unclear stops.
- Do not add to losing trades unless the original plan includes scaling and the action remains inside the active policy.
- Do not move stops farther away without explicit approval or a prior policy rule.
- For Agentic account `433711041`, prefer policy-gated autonomous execution; for all other accounts, use approval-gated execution.

## Common Pitfalls

1. **Using stale data.** Always inspect live quotes/account state before sizing or previewing.
2. **Skipping account inspection.** Never size from memory; use `get_portfolio` / account tools first.
3. **Treating the $200 sandbox as unlimited preauthorization.** It is not exact enough for autonomous execution.
4. **Previewing then placing without a second gate.** Preview is not approval.
5. **Forcing trades.** If no clean setup exists, say no trade.
6. **Ignoring tiny-account math.** A $2 risk budget can make many otherwise-normal setups impractical.
7. **Using options by default.** Default to equities.
8. **Forgetting journal entries.** Journal every preview/execution/review that matters.

## Verification Checklist

Before finalizing a trade plan:

- [ ] Request classified into execution mode
- [ ] Account state inspected live
- [ ] Buying power/account value known
- [ ] Positions/open orders checked
- [ ] Market benchmark inspected
- [ ] Candidate quote/historicals inspected
- [ ] Setup includes entry, stop, target, duration, size, max loss, reward, R:R
- [ ] Risk is within user/default limits
- [ ] Invalidation is clear
- [ ] Order preview used before any real order
- [ ] Explicit user approval captured before any real placement/cancel/modify
- [ ] Journal written after preview/execution/review
