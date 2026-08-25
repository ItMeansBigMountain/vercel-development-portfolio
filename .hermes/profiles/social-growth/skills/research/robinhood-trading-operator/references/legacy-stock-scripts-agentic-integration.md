# Legacy Stock Scripts → Agentic Robinhood Integration

Use when the user asks to leverage older stock-market scripts/projects for the Agentic Robinhood MCP trading workflow.

## User intent

The user wants older Robinhood/stock/news scripts mined for useful analysis ideas, then folded into the current MCP + cron + trading journal system. Do not run legacy broker-login/order code directly if the MCP provides safer authenticated tools.

## Projects to inspect first

- `/opt/data/HeRmEz/projects/robinhood-daily-portfolio-report`
  - Clean Python reporting module.
  - Useful: position rows, market value, daily change, total P/L, text report format.
  - Test command: `python3 -m unittest discover -s tests -v`.

- `/opt/data/HeRmEz/projects/Fintech`
  - Older `robin_stocks` scripts such as `robinAPI.py`, `daytrade.py`, `STOCKS.txt`.
  - Useful ideas: P/L sorting, PE ratio sorting, dividend view, sector/industry sort, earnings/news checks.
  - Avoid direct credential/login/order execution from these scripts.

- `/opt/data/HeRmEz/projects/Financial.Market.ML`
  - Older market ML/RL experiments.
  - Useful as research/reference, not production trade execution.

- `/opt/data/HeRmEz/projects/stockNews`
  - Retired standalone app/backend.
  - Useful idea: portfolio dashboard + news/catalyst layer + sentiment/candidate scoring.

## Integration shape

Build or update cron/reporting around:

1. Live MCP account state: account value, buying power, positions, open-ish orders.
2. Position quote/P&L snapshot using MCP quotes and average cost.
3. Robinhood Gmail confirmations/account notices routed to `Hermes/Finance/Robinhood`.
4. News/catalyst layer from web/email/news sources.
5. Candidate scoring: technical structure, relative strength, volume/liquidity, catalyst quality, risk/reward, invalidation clarity.
6. Policy gate: equities-only by default, no forced trades, journal all reviews/executions.

## Reporting expectation

The user expects scripts to be understood by their outputs. When importing an old script idea, state:
- what input it expects,
- what output it creates,
- whether it was tested,
- whether it is safe to use live or only as reference.