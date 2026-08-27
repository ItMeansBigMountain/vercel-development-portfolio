# Agentic OPEN Scan — 2026-08-26

- Evidence timestamp: 2026-08-26T13:42:51Z (quotes primarily 13:39–13:40Z)
- Account: Robinhood Agentic ending 1041 only
- Mode: autonomous policy-gated equities
- Decision: **PAUSE / NO ORDERS**

## Live broker state

- Account active, cash account, and accessible to this agent.
- Account value: **$331.96**; equity value: **$186.69**; broker cash/buying power: **$145.27**; unsettled funds: **$0.00**.
- Open-ish equity orders: new 0, queued 0, confirmed 0, unconfirmed 0, partially_filled 0.
- Recent verified fills (2026-08-25): BAC sell 1.046363 @ $62.3201; SHOP sell 0.431038 @ $153.3401.
- Position endpoint still reports SHOP 0.431037 shares sellable at $144.09 average cost, matching yesterday's unresolved conflict almost exactly. Because the filled sell and position ledger remain unreconciled, broker position/risk state is uncertain. Policy therefore prohibits review or placement.
- Account value is above the $10 kill switch. Drawdown from the latest observed $332.93 value is approximately **-0.29%**, below the 10% recent-high pause and 5% daily pause thresholds.

## Liquid-balance math

- Pending/open-order commitments: $0 verified.
- Liquid buying power after pending orders: **$145.27**.
- Exact 80% deployable target: **$116.22**.
- Required 20% reserve: **$29.05**.
- Reported existing equity exposure: **56.24%** of account value. No deployment was attempted because uncertain broker inventory is a binding kill switch.

## Market regime

**Mixed/rotation; price discovery incomplete at 09:40 ET.** SPY -0.05% and slightly above SMA20/SMA50; QQQ -0.15% and below SMA20/SMA50; IWM -0.04% near SMA20 and above SMA50. XLK +0.08% but below SMA20; SMH -0.20% and below SMA20/SMA50; XLF +0.07% above both averages; XLE -0.15% above rising averages; XLI led at +0.80% but remained below SMA20. Early volume confirmation was not mature. This is not a broad risk-on breakout tape.

## Holding decisions

1. **MA — HOLD, strongest (13/16).** $600.03, +0.11% today, +4.81% from $572.48 cost; above SMA20 $572.49 and SMA50 $542.14, +6.62%/21.47% over 20/60 days, testing $601.23 resistance. Do not add at resistance. Invalidation remains a daily close below $582; warning on loss of the $598 opening range.
2. **SHOP — STATE UNCERTAIN / DO NOT ACT.** Broker reports 0.431037 shares worth about $65.36 and +5.23% from cost despite yesterday's verified sale of 0.431038. Technically $151.63 remains above SMA20 $143.25 and SMA50 $128.28 with strong 20/60-day relative momentum, but it is fading -1.46% at the open. No duplicate sell or buy.
3. **XOM — HOLD/EXIT REVIEW, weakest genuine holding (9/16).** $159.44, -0.75% today and -4.91% from $167.67 cost; just above SMA20 $159.17 and above SMA50 $149.59, but opening relative weakness and prior Q2 EPS miss reduce quality. Daily close below $158.50 triggers exit review; hard thesis failure below $156. Never average down.

## Fresh candidate scorecard

Each score is 0–2 for regime, sector-relative strength, 20/60-day momentum, catalyst/revisions, quality/cash flow, volume/entry confirmation, invalidation clarity, and R:R.

- **UBER — 11/16 (1/2/2/1/2/1/1/1): WATCH.** $81.28, +1.16%, above SMA20 $74.88/SMA50 $73.34, +14.90%/+15.45% over 20/60 days and above prior $80.43 resistance. Opening breakout lacks mature volume/retest confirmation; wait for a hold/retest near $80.40 rather than chase.
- **MSFT — 11/16 (1/2/2/1/2/1/1/1): WATCH.** $493.82, +0.43%, above SMA20 $482.92/SMA50 $423.80 with exceptional 20-day relative strength. Entry is extended from support and below $513.73 resistance; no confirmed opening retest.
- **PLTR — 10/16 (1/2/2/1/1/1/1/1): WATCH/REDUCED ONLY.** $171.73, -0.58%, above SMA20 $161.95/SMA50 $140.72 with +39.02% 20-day momentum, but high volatility (ATR14 $7.44), crowding/extension, and no mature volume confirmation make opening entry unattractive.
- **NVDA — 9/16 (1/1/1/2/2/0/1/1): NO TRADE.** $211.66, -0.65%, below SMA20 $214.58 but above SMA50 $207.81; 60-day momentum is nearly flat and semiconductor ETF trend is weak. Earnings-event risk and lack of entry confirmation dominate.
- **AVGO — 7/16 (1/0/0/2/2/0/1/1): NO TRADE.** $357.16 near $355.31 support but below SMA20/SMA50 with negative 20/60-day momentum and weak semiconductor-sector trend despite verified prior EPS beats.

No fresh candidate reached the 13/16 full-policy threshold. No 10–12 candidate justified a reduced starter before an opening retest, especially with uncertain broker inventory.

## Fundamentals, earnings, and source limitations

Robinhood live fundamentals and earnings endpoints were checked for MA, XOM, SHOP, AVGO, NVDA, MSFT, GOOGL, AMZN, META, and PLTR. Verified earnings history supported MA quality and AVGO's recent EPS beats; the broad calendar confirmed an active earnings tape. Current external-news reconnaissance was handed to a researcher, but the delegated result failed to return usable citations. That limitation was not filled with guesses and reinforces the no-trade decision.

## Tool/failure record

- The trading-specialist profile lacked a cached Robinhood OAuth token; the configured default Hermes home connected successfully and supplied live broker data.
- Direct legacy `rh_call.py` failed because its MCP import name is stale; the current `streamable_http_client` path succeeded.
- `get_equity_tradability` raised an exception in the market batch, so fractional tradability of fresh candidates was not independently confirmed. This alone bars placement.
- MCP session shutdown emitted HTTP 400 after successful payload return; returned account/market payloads were complete.
- Research delegation returned no usable source brief.

## Action, risk, and next check

No order reviewed, placed, canceled, or modified. No fill occurred during this scan. Re-query SHOP position/fill reconciliation, all five open-order states, and tradability at the midday check. If reconciliation is still unresolved, remain paused. If it clears, preserve MA above $582, review XOM on a close below $158.50, and consider only confirmed retests scoring at least 10/16; full-size deployment requires 13/16 and exact policy risk math.
