Portfolio Heartbeat Script

This script generates the **Portfolio Heartbeat** section for the morning report.
It:

- Discovers all Robinhood MCP servers.
- Retrieves each account’s portfolio value, cash, buying power, and positions.
- Pulls current quotes and recent news for owned symbols.
- Formats a concise heartbeat block showing value, positions, 24‑h P&L, and news headlines.
- Writes the formatted block to `/tmp/portfolio_heartbeat.txt` for the morning‑report cron job.

Key implementation notes:

- Uses `McpToolClient` to call `robinhood_trading` tools (`get_accounts`, `get_portfolio`, `get_equity_positions`, `get_equity_quotes`).
- Calls `web_search` for news headlines.
- Calculates 24‑h P&L from recent historical candles.
- Handles missing data gracefully and logs errors without aborting.