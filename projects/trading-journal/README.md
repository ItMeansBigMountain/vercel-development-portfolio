# Trading Journal

Hermes Robinhood Agentic Trading journal.

Default account: Robinhood Agentic sandbox (masked in chat as ••••1041)
Default mode: swing-trading research, order preview, approval-gated execution.
Default risk: 1% per trade, 3% aggregate open risk, minimum 1.5:1 R:R.

Folders:
- `YYYY-MM-DD/` — trade decisions, previews, executions, reviews
- `playbook/` — durable rules, watchlists, lessons, setup templates
- `scanner/` — research-only market/catalyst normalization helpers

## Catalyst feed

`scanner/catalyst_feed.py` migrates the useful no-credential Yahoo Finance RSS
parsing and deterministic sentiment idea from the retired `stockNews` backend.
It normalizes timestamps and ticker identity, removes duplicates, marks stale or
undated stories, and labels catalyst type/direction. Its score is a headline
heuristic for candidate research only; it neither recommends nor places trades.
It intentionally returns no synthetic fallback articles when a source is empty
or malformed.

Local-only usage (requires outbound access to Yahoo Finance):

    python3 -m scanner.catalyst_feed AAPL --limit 5

Offline verification (no third-party packages or credentials required):

    python3 -m unittest tests.test_catalyst_feed -v
