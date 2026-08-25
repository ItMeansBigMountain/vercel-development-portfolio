# Robinhood Trading MCP with Hermes

Use this reference when connecting Hermes Agent to Robinhood Agentic Trading.

## Robinhood MCP endpoint

Robinhood Trading MCP endpoint:

```text
https://agent.robinhood.com/mcp/trading
```

Hermes native MCP config shape:

```yaml
mcp_servers:
  robinhood_trading:
    url: https://agent.robinhood.com/mcp/trading
    timeout: 180
    connect_timeout: 60
    sampling:
      enabled: false
```

Restart Hermes/gateway after adding the server. MCP tools are discovered at startup.

## Expected pre-auth behavior

A direct Hermes MCP discovery attempt may return `401 Unauthorized` before Robinhood authorization. Treat this as an auth-gating signal, not as evidence the endpoint is wrong.

Robinhood's documented flow for supported clients is interactive:

1. Add the MCP URL to a supported agent/client.
2. Open that client's MCP/auth menu.
3. Select the Robinhood Trading server.
4. Authenticate with Robinhood.
5. Create/fund the dedicated Robinhood Agentic account.

If Hermes does not surface an auth URL automatically, have the user perform the first authorization in a supported client such as ChatGPT Developer Mode, Codex/Claude Code, or Claude Desktop, then inspect whether Robinhood provides a durable token/header/session that can be configured in Hermes.

## Safety policy for this user

Default mode is **read/analyze first**:

- Allowed without trade execution: portfolio/account reads, positions, balances, order history, buying power, risk exposure, diversification, and market/news context.
- Before any order placement: require explicit user approval of ticker, side, quantity/notional amount, order type, time-in-force, account, and max risk.
- Do not create autonomous trading cron jobs without a dedicated funded Agentic account, written strategy, max-position limits, max-loss limits, and kill-switch rules.

Robinhood notes that agents may read all Robinhood accounts after connection, but can only place trades in the dedicated Robinhood Agentic account. The user remains responsible for all trades.
