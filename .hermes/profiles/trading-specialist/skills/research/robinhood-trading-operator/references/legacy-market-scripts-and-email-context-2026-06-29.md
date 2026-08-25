# Legacy market scripts + Robinhood email context (2026-06-29)

Use this when improving the user's Agentic Robinhood trading system from existing workspace code and email data.

## What to mine from old projects

The workspace contains older market/trading projects whose ideas are useful, but their direct execution/auth paths should not replace Robinhood MCP:

- `robinhood-daily-portfolio-report`: clean Python report formatter. Reusable for journal/report output: positions -> market value, daily change, total P/L, text report. Tests passed with `python3 -m unittest discover -s tests -v`.
- `Fintech`: older `robin_stocks` scripts (`robinAPI.py`, `daytrade.py`, `STOCKS.txt`). Mine ideas only: sort holdings by P/L, PE ratio, dividends, sector/industry, earnings/news. Do not use legacy credential/login/order execution.
- `Financial.Market.ML`: research/ML/RL market experiments. Treat as research material, not production signal until isolated and verified.
- `stockNews` and `portfolio-sentiment-subscription-app`: useful dashboard/news/sentiment/watchlist concepts for candidate scoring inputs.

## Preferred integration pattern

Build a research adapter around the Robinhood MCP rather than resurrecting old trading-login code:

1. Pull live account state from MCP: portfolio, positions, open-ish orders, quotes/historicals.
2. Pull Robinhood trade/order/account emails from Gmail label `Hermes/Finance/Robinhood` for execution/account context.
3. Apply old-script analytics as pure functions: P/L ranking, daily/total change, sector grouping, PE/dividend/news scoring when data is available.
4. Output a concise candidate/risk report and write a journal entry under `/opt/data/HeRmEz/projects/trading-journal/`.
5. Use MCP order review/placement only under the Agentic account policy; never use `robin_stocks` execution paths.

## Email context rule

Robinhood trade confirmations, order executions, and account notices should be routed into `Hermes/Finance/Robinhood`. They can inform the Agentic trading project but are not themselves a mandate to trade.
