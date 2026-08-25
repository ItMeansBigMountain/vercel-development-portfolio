# Remote OAuth MCP: Robinhood Trading pattern

Use this when connecting Hermes to a remote HTTP MCP server that requires OAuth 2.1 / PKCE, especially Robinhood Trading MCP.

## Robinhood Trading MCP

Endpoint:

```text
https://agent.robinhood.com/mcp/trading
```

Preferred Hermes setup:

```bash
hermes mcp add robinhood_trading --url https://agent.robinhood.com/mcp/trading --auth oauth
```

If operating in Discord/headless SSH, the CLI prints an authorization URL and waits for a callback. The user must:

1. Open the printed Robinhood OAuth URL in their own browser.
2. Authenticate and approve.
3. Expect the final redirect to a `http://127.0.0.1:<port>/callback?...` page to fail locally if no tunnel is set up.
4. Copy the full final redirect URL from the browser address bar.
5. Paste it back into the waiting `hermes mcp login <name>` process.

Hermes' OAuth paste fallback accepts the full redirect URL, just `?code=...&state=...`, or `code=...&state=...`.

## Useful commands

```bash
hermes mcp list
hermes mcp test robinhood_trading
hermes mcp login robinhood_trading
```

If a server was initially configured without OAuth and returns `401 Unauthorized`, remove and re-add it with `--auth oauth`:

```bash
hermes mcp remove robinhood_trading
hermes mcp add robinhood_trading --url https://agent.robinhood.com/mcp/trading --auth oauth
```

If non-interactive setup times out before config is saved, ensure the config has:

```yaml
mcp_servers:
  robinhood_trading:
    url: https://agent.robinhood.com/mcp/trading
    auth: oauth
    timeout: 180
    connect_timeout: 60
    sampling:
      enabled: false
    enabled: true
```

Then start an interactive or PTY-backed login:

```bash
hermes mcp login robinhood_trading
```

## Safety boundary for trading MCPs

Treat trading MCPs as high-risk even when the user is enthusiastic. Default to read/analyze mode: portfolio value, buying power, positions, balances, order history, risk exposure, diversification, and market/news context. Do not place trades unless the user explicitly approves the specific order details in the current session. Avoid autonomous trading cron jobs until there is a dedicated funded Agentic account, written strategy, max-position/max-loss limits, and a kill switch.
