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

`scanner/catalyst_feed.py` is a strict discovery-only normalizer. It accepts a
row only when the requested ticker is explicit in structured metadata or appears
as a standalone ticker mention in its text. It canonicalizes URLs, conservatively
deduplicates normalized titles, preserves multiple catalyst tags, and emits
keyword evidence for materiality separately from directional word count. A
publication time more than five minutes in the future is invalid. Invalid,
undated, or stale rows have `is_scoreable=false` and `catalyst_score=null`.

Publisher and domain fields are provenance hints only. `source_quality` remains
`unverified` and `corroboration_count` remains zero unless a future verification
system supplies real evidence; the aggregator is recorded separately. No source
authority, corroboration, confidence, or company-name entity resolution is
inferred. Empty, malformed, or irrelevant inputs produce no fallback signals.

Consumer contract: records are unverified research leads, never recommendations
or order triggers. Consumers must require `research_only=true`,
`is_scoreable=true`, explicit `relevance_evidence`, and independent source/entity
verification. Broad-market regime (including SPY/QQQ/IWM), sector and relative
strength/flows, technicals, fundamentals, volume, liquidity, risk/invalidation,
reward/risk, and live broker/account checks remain external and mandatory. Those
policy gates must run before candidate scoring, preview, or execution. This
module has no brokerage, order, preview, or execution integration.

Local-only usage (requires outbound access to Yahoo Finance):

    python3 -m scanner.catalyst_feed AAPL --limit 5

Offline verification (no third-party packages or credentials required):

    python3 -m unittest tests.test_catalyst_feed -v
