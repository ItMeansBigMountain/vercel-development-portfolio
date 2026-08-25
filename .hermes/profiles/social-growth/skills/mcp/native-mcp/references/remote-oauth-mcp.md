# Remote OAuth MCP Authentication Pattern

Use this when configuring a remote HTTP/StreamableHTTP MCP server that requires OAuth 2.1/PKCE, especially from a headless Discord/gateway session.

## Hermes CLI flow

Prefer configuring OAuth explicitly instead of static headers:

```bash
hermes mcp add <name> --url <mcp-url> --auth oauth
hermes mcp login <name>
hermes mcp test <name>
```

For an already-manually-added server, ensure the config includes:

```yaml
mcp_servers:
  <name>:
    url: https://example.com/mcp
    auth: oauth
    enabled: true
```

OAuth tokens are stored under `$HERMES_HOME/mcp-tokens/` and reused by future sessions/gateway restarts.

## Headless callback handling

Hermes prints an authorization URL and starts a localhost callback listener such as:

```text
http://127.0.0.1:<port>/callback
```

In a headless/remote environment, the user's browser may fail after approval because `127.0.0.1` is the user's local machine, not the server. This is expected. Ask the user to copy the final broken callback URL from the address bar and paste it back. The URL/query must include both `code=...` and the matching `state=...` from the currently running attempt.

## Timeout workaround

`hermes mcp login` may time out quickly during the initial tool-discovery probe. If the user needs more time, run the lower-level probe with a larger timeout in a PTY/background process and submit the pasted callback URL to that process:

```bash
PYTHONPATH=/opt/data/hermes-agent /opt/data/hermes-agent/venv/bin/python - <<'PY'
from hermes_cli.mcp_config import _get_mcp_servers, _probe_single_server, _oauth_tokens_present
name = '<name>'
cfg = _get_mcp_servers()[name]
tools = _probe_single_server(name, cfg, connect_timeout=300)
print(f'AUTH_OK tools={len(tools)}')
print('tokens_present', _oauth_tokens_present(name))
PY
```

Run with `pty=true` so pasted callback input can be delivered with `process.submit(...)`.

## Robinhood Trading MCP notes

Robinhood's Trading MCP endpoint is:

```text
https://agent.robinhood.com/mcp/trading
```

Configure it as OAuth, not a bearer-token header:

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

Safety default for financial/trading MCPs: start read/analyze-only. Do not place trades unless the user explicitly approves the exact order/action in the current conversation.
