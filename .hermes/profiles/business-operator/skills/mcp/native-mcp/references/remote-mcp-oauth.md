# Remote MCP OAuth / PKCE in Hermes

Use this reference when connecting a remote HTTP/StreamableHTTP MCP server that requires interactive OAuth, such as Robinhood Agentic Trading.

## Config shape

Prefer Hermes' OAuth mode rather than a static `Authorization` header when the server advertises OAuth:

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

CLI equivalent:

```bash
hermes mcp add robinhood_trading --url https://agent.robinhood.com/mcp/trading --auth oauth
hermes mcp login robinhood_trading
```

## Headless / Discord workflow

Hermes prints an authorization URL and starts a local callback listener on `127.0.0.1:<port>`. In headless gateway sessions, the user's browser is on a different machine, so the final redirect will show a broken localhost page. That is expected.

Tell the user to:

1. Open the exact current authorization URL.
2. Approve in the provider UI.
3. Copy the final browser address bar URL, which must include `code=...` and the same `state=...` value from the current attempt.
4. Paste that whole callback URL back quickly.

The callback URL can be fed to a live PTY process with `process.submit`.

## Pitfalls

- OAuth codes are one-time and tied to the PKCE verifier, callback port, and `state` for that exact attempt. A callback from an earlier timed-out attempt is unusable.
- Always compare the pasted callback URL's `state` and port with the currently waiting auth process before submitting it.
- A URL like `https://robinhood.com/mcp/trading?...` without `code=` is still an authorization/start URL, not the final callback.
- `hermes mcp login <name>` may probe with a short default timeout in some versions. For slow human OAuth over Discord, run a longer probe in a PTY.

## Long-timeout login probe

If the built-in CLI times out before the user can paste the callback, run the probe directly with the Hermes venv Python and a longer timeout:

```bash
cat > /tmp/mcp_login_long.py <<'PY'
from hermes_cli.mcp_config import _get_mcp_servers, _probe_single_server, _oauth_tokens_present
name = 'robinhood_trading'
cfg = _get_mcp_servers()[name]
try:
    tools = _probe_single_server(name, cfg, connect_timeout=300)
    print(f'AUTH_OK tools={len(tools)}')
    for t, d in tools:
        print(t, '-', (d or '')[:160])
    print('tokens_present', _oauth_tokens_present(name))
except Exception as e:
    print('AUTH_FAILED', type(e).__name__, str(e))
PY
PYTHONPATH=/opt/data/hermes-agent /opt/data/hermes-agent/venv/bin/python /tmp/mcp_login_long.py
```

Run it in PTY/background mode so Hermes can later submit the pasted callback URL:

```python
terminal(command="PYTHONPATH=/opt/data/hermes-agent /opt/data/hermes-agent/venv/bin/python /tmp/mcp_login_long.py", pty=True, background=True, notify_on_complete=True)
process.poll(session_id)
process.submit(session_id, pasted_callback_url)
process.wait(session_id, timeout=300)
```

After tokens are saved, restart the gateway/new session so discovered MCP tools appear.