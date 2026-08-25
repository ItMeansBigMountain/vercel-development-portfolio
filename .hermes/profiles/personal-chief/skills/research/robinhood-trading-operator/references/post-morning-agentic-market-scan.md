# Post-Morning Agentic Market Scan

Session learning: after the user's normal morning operator report, they want a separate Agentic portfolio scan focused on the Robinhood sandbox account.

## Timing

- Run after the morning report, not inside the main morning report.
- Current scheduled example: weekdays around `13:50 UTC` / about `8:50 AM Central`.

## Required scan contents

1. **Agentic portfolio update**
   - Account value
   - Buying power/cash
   - Positions
   - Open orders
   - Recent order/fill status when relevant

2. **Market scan**
   - SPY, QQQ, IWM or relevant broad benchmarks
   - Bullish/bearish/neutral one-line read
   - Key thing to watch today

3. **Candidate discovery beyond stale watchlists**
   - Do not rely primarily on user watchlists when they are stale.
   - Use news, source emails/newsletters, Robinhood curated lists/daily movers, web search, live quotes, tradability, and OHLCV.

4. **Technical analysis**
   - Trend vs recent moving averages when available
   - Support/resistance/invalidation
   - Volume/ATR or volatility context when available
   - Setup type and quality

5. **Fundamental/catalyst analysis**
   - What changed
   - Why it matters
   - What would disconfirm the thesis

6. **Tool/system upgrade notes**
   - Data gaps found during scan
   - Better scanners/scripts to build
   - MCP/tool improvements
   - Watchlist refresh suggestions

7. **Journal update**
   - Write `/opt/data/HeRmEz/projects/trading-journal/YYYY-MM-DD/post-morning-market-scan.md`.

## Compact direct-MCP collection pattern

When `hermes mcp test robinhood_trading` connects and discovers tools but first-class MCP calls are not exposed to the cron agent, use an in-process collector rather than incorrectly reporting Robinhood as unavailable:

1. Import `register_mcp_servers`, `_load_mcp_config`, and the Hermes tool `registry` from the local Hermes source tree.
2. Register only `robinhood_trading`, then invoke `mcp_robinhood_trading_<tool>` handlers through the registry.
3. Decode both MCP response shapes: `structuredContent.data` and JSON nested under `result`.
4. Collect portfolio, equity positions, option positions, recent equity orders, and every open-ish equity order state (`new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`) before assessing risk.
5. Batch quotes/fundamentals/tradability first, then request daily historicals only for benchmarks, holdings, and the narrowed candidate set.
6. Compute a compact artifact with live price, daily move, SMA10/20/50, ATR14, 20-day high/low, average volume, position value/P&L, and deployment percentage. Persist raw/compact JSON under `/tmp` when useful for audit/debugging, but journal only the decision-quality summary.
7. Robinhood quote payloads may omit current-session volume even when fundamentals contain it. Prefer the same-day `get_equity_fundamentals.volume` field and label the gap rather than reporting zero volume.
8. Treat successful connectivity/discovery as a prerequisite check, not proof that account/order calls succeeded; broker certainty requires successful live account, position, order, and quote responses.

This fallback is a collection path only. It does not relax policy, account, review, execution, or journaling gates.

## Portfolio-management decision rule

Before seeking a new entry, calculate current equity deployment and live P/L per position. If deployment is already inside the policy target (currently roughly 70%–90%), prefer managing existing invalidation levels and preserving the remaining cash over forcing another candidate. Report concrete review zones for every open holding, especially the technically weakest position.

## Safety

- Only use the Agentic account ending `1041` / account number `433711041`.
- Do not trade other accounts.
- Do not trade options by default.
- Stop all trading consideration if account value is below `$10`, broker state is uncertain, or risk cannot be calculated.
- If no clean setup exists, say no trade instead of forcing one.

## Output style

Concise Discord bullets. No Markdown tables unless the user specifically asks.

Recommended sections:

- Decision
- Agentic Portfolio
- Market Read
- Top Candidates
- Best Setup
- Risk / Invalidation
- Tool Upgrades
- Journal
