# News + Email + Robinhood MCP Candidate Scan Pattern

Use this when the user asks to scan beyond their watchlists, says watchlists are stale, or wants candidates sourced from newsletters/news/tools.

## Durable workflow

1. **Mode defaults to Trade Planning** unless the user explicitly requests order preview/execution.
2. **Inspect account first** with Robinhood MCP: accounts, portfolio, positions, open/recent orders. Use the Agentic account only when `agentic_allowed=true` and the account is clearly identified.
3. **Do not depend on user watchlists** when they are stale. Treat watchlists as optional context, not the candidate universe.
4. **Newsletter source pass**:
   - Robinhood Snacks = financial markets newsletter/source, not account mail.
   - TLDR AI / InfoSec / Founders = catalyst/theme source; extract public tickers and theme-adjacent public companies.
   - Email scans should be read-only unless the task is specifically email sorting/cleanup.
5. **News/web pass**: confirm newsletter themes with current web/news searches before ranking candidates.
6. **Robinhood market pass**:
   - Pull live quotes for broad-market proxies: `SPY`, `QQQ`, `IWM`.
   - Pull live quotes and tradability for candidate tickers.
   - Pull daily OHLCV bars for roughly 2–4 months and compute simple indicators: 10/20/50-day moving averages, 14-day ATR %, 20-day return, recent volume ratio, 20-day high/low.
7. **Small-account filter** for the user's $200 Agentic account:
   - Prefer fractional tradable, liquid equities.
   - Default risk is about $2/trade and $6 total open risk.
   - High-priced equities can still be candidates only via dollar/fractional sizing; whole-share sizing will usually be impossible.
   - Reject or demote very high ATR names unless position size is tiny and stop is logical.
8. **Rank candidates** by trend clarity, volume quality, liquidity, catalyst/theme support, invalidation clarity, and risk-to-reward.
9. **Save a dated journal note** under `/opt/data/HeRmEz/projects/trading-journal/YYYY-MM-DD/` with sources used, candidates screened, rejection reasons, best setup, and whether an order preview was run.

## Session-proven candidate sourcing example

A useful broad scan combined:

- Robinhood Snacks email: Amazon less-than-truckload freight expansion → `AMZN`, `XPO`, `ODFL`, `SAIA`, `FDX`, `UPS`.
- TLDR AI email: OpenAI/Ona, cloud execution, AI agents → AI infra/software watchlist.
- TLDR InfoSec email: Oracle PeopleSoft / ServiceNow / GitHub/npm security themes → `ORCL`, `NOW`, `CRWD`, `MSFT`.
- Web/news confirmation: AI/chip/infrastructure momentum → `NVDA`, `AMD`, `AVGO`, `MU`, `IREN`, `ORCL`, `HOOD`, `RKLB`.
- Robinhood quotes/historicals/tradability then selected `HOOD` as the cleanest setup because it had strong 20-day trend, live relative strength, volume confirmation, clean fractional sizing, and better $200-account fit than higher-priced names.

## Pitfalls

- Do not confuse Robinhood Snacks with Robinhood account/transaction emails.
- Do not force a trade when the scan only produces watchlist candidates.
- Do not treat raw capital-efficient fractional affordability as a complete risk plan; still compute stop distance, max loss, target, and R:R.
- Do not run `place_*` tools from a scan. Use `review_*` only when the user asks for preview, and `place_*` only after exact order approval.
