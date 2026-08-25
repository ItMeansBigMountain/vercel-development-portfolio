# Post-morning scan: open-order certainty and profile Gmail probes

Use this reference for scheduled Agentic post-morning scans when no user is present.

## Open-order certainty

Do not infer "no open orders" from recent order history or a single `state=new` query alone.

For equity orders, explicitly check the open-ish states supported by the Robinhood MCP before reporting certainty:

- `new`
- `queued`
- `confirmed`
- `unconfirmed`
- `partially_filled`

If time/tool budget prevents checking all states, phrase the report as limited, for example: "no `new` equity orders found; other open states were not exhaustively queried." Prefer exhaustive checks for autonomous scans because pending orders change risk and buying power.

## Gmail/news source probes in cron

For scheduled post-morning scans, default Google Workspace auth may not be the same as the user's profile-scoped Gmail tokens. If the default CLI is unavailable or a secondary profile is revoked, do not stop the market scan. Use the best authenticated profile-scoped read-only token available, report failed profiles separately, and continue with Robinhood + web/news research.

A safe pattern is:

1. Verify likely profiles with `/opt/data/scripts/google_reauth_workflow.py verify workspace <profile>`.
2. Use only read-only Gmail metadata/search probes for source discovery.
3. Search recent market-relevant sources such as TLDR, Robinhood Snacks, and other routed newsletter labels/senders.
4. Treat brokerage execution confirmations as account-state corroboration, not trade signals.
5. Report expired/revoked profiles as a Tool Upgrade item, not as a blocker when other sources are available.

## Candidate discipline

When Robinhood Daily Movers or news scans show large gap leaders, classify the gap before considering a trade:

- Strong catalyst but extended location: watch for retest, do not chase.
- Binary biotech/drug data: usually avoid for the small Agentic sandbox unless risk is unusually clear.
- Meme/turnaround spike: require confirmation/retest; avoid fresh chase entries.
- Earnings/investor-update catalyst: avoid fresh buys immediately before/into binary earnings unless explicitly planned.

Broker review success is not a mandate to trade. If entry location is extended or catalyst confirmation is thin, choose no trade and journal the reason.
