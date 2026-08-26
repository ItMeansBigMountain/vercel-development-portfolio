# Power-Hour Decision — 2026-08-25

- Timestamp: 2026-08-25 19:30 UTC
- Account: 433711041 / ending 1041 only
- Mode: autonomous policy-gated equities
- Decision: PAUSE / NO NEW ORDERS

## Broker state and kill switches

- Account active and authorized; portfolio value $332.93, above the $10 kill switch.
- Equity value $187.66; broker cash $145.27; authoritative spendable buying power $13.96.
- Unsettled funds: $131.31. No open-ish equity orders found across new, queued, confirmed, unconfirmed, or partially_filled.
- Today’s fills: BAC sold 1.046363 shares at $62.3201; SHOP sold 0.431038 shares at $153.3401, both at 17:36 UTC.
- Material reconciliation blocker: two repeated position queries still show SHOP 0.431037 shares sellable despite the filled sale for 0.431038 shares. Portfolio equity also still includes approximately $66 of SHOP. Broker position/fill state is therefore uncertain under the policy kill switch.
- No order was reviewed or placed; no stop was changed.

## Exposure and liquid-balance math

- Reported equity deployment: $187.66 (56.37% of account value).
- Liquid buying power after pending/open orders: $13.96 (no open-ish orders found).
- 80% deployable target: $11.17; required 20% reserve: $2.79.
- Deployment was intentionally not increased because broker state was uncertain. Cash shown by the broker includes unsettled proceeds and is not fully spendable in this cash account.
- Day P&L was not reported because the portfolio endpoint did not verify it and SHOP reconciliation would make a derived figure unreliable.

## Market regime

Mixed/risk-on rotation. At 19:30 UTC, SPY was +0.23%, QQQ +0.43%, and IWM +0.34% versus prior closes, but daily trend structure was uneven: SPY near SMA20 and above SMA50; QQQ below SMA20/SMA50; IWM below SMA20 but above SMA50. XLF was +0.19% and near its 52-week high, while XLE was -1.01% and XLK +0.62%. Volume was running below recent daily averages for the broad ETFs. This supports selective overnight exposure, not aggressive chasing.

## Position decisions

### MA — HOLD if position is genuine
- Current: $597.70; average cost $572.48; reported value $67.86; unrealized +$2.86.
- Trend: above rising SMA20 $570.66 and SMA50 $539.95; 20-day +8.73%, 60-day +21.49%; strong relative trend versus SPY and XLF.
- Catalyst/quality: Q2 EPS $5.04 beat $4.76 estimate; revenue/cross-border commentary positive; profitable, highly liquid payment network. No imminent verified earnings event (next date tentative 2026-10-29).
- Overnight invalidation: daily close below $582 / loss of recent breakout support; tactical warning below today’s low $595.35. Do not widen.
- Upside reference: $601.62 prior 52-week area, then continuation only on confirmed volume.
- Score: 13/16. Best genuine holding.

### XOM — HOLD/REVIEW, weakest genuine holding
- Current: $161.565; average cost $167.67; reported value $53.80; unrealized -$2.03.
- Trend: above rising SMA20 $158.79 and SMA50 $149.31; 20-day +6.00%, 60-day +11.63%, but today underperformed SPY and XLE and closed near the lower half of its range.
- Fundamentals/event: Q2 EPS $3.52 missed $3.76 estimate, though company reported strong operating/free cash flow; next earnings date tentative 2026-10-30.
- Overnight invalidation: daily close below $158.50/SMA20 zone; hard thesis failure below $156. Do not average down.
- Upside references: $168.64 then $176.41.
- Score: 10/16. Weakest valid holding; candidate for rotation only after broker reconciliation and a materially superior confirmed setup.

### SHOP — STATE UNCERTAIN / DO NOT ACT
- Filled sell: 0.431038 at $153.3401 today.
- Position endpoint still reports 0.431037 sellable at average cost $144.09; this conflicts with the fill and cannot be treated as confirmed overnight exposure.
- Current $153.225; strong 20/60-day momentum but high valuation (PE about 101) and intraday fade from $154.66.
- No duplicate sell or new buy was attempted.

## Fresh candidate review

- V: strongest fresh chart among reviewed alternatives; $382.85 near a new 52-week high, above rising SMA20/SMA50 with 20/60-day momentum. However, entry is at resistance with sub-average volume and no direct fresh catalyst confirmed; watch for breakout-retest rather than chase. Score 12/16.
- XLF: sector strength near 52-week highs, but ETF entry is extended against resistance and lacks a clean retest. Score 11/16.
- SHOP: momentum/catalyst quality is stronger than XOM, but the account-state conflict makes it ineligible and its intraday entry is extended. Score 11/16 for a reduced/watch setup only.

## Action and next check

No trade. Re-query fills, positions, and portfolio at the next market-open check. Resume management only when SHOP’s filled sale and position ledger reconcile. If XOM closes below $158.50 or sector-relative strength continues to deteriorate, review an exit; preserve MA while its $582 support and relative trend hold.
