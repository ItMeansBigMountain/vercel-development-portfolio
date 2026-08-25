# Post-Morning Scan: Profile Gmail + Scanner Upgrade Notes

Use for scheduled post-morning Agentic portfolio market scans when the normal Google Workspace CLI path is not using the user's profile-scoped OAuth tokens.

## Durable workflow lesson

- If `google_api.py` reports `Not authenticated` during a cron scan, do **not** conclude Gmail is unavailable. This user's Workspace setup may use profile-scoped tokens under `/opt/data/google_profiles/<profile>/google_token.json`.
- For read-only newsletter/source probes, verify and use the profile-scoped token directly when available, especially `personal-main` for the user's main Gmail lane.
- A harmless probe pattern is:
  - load `/opt/data/google_profiles/personal-main/google_token.json`
  - build Gmail API service from `google.oauth2.credentials.Credentials`
  - run `users.messages.list` with a narrow query and `maxResults`
  - read only metadata headers/snippets unless full body is needed
- Keep output concise: report whether market-relevant source emails were found, not raw credential/token details.

## Candidate scan upgrade pattern

For future post-morning scans, prefer a deterministic scanner script that combines:

- Robinhood Daily Movers / curated list symbols
- live quote and daily % move
- bid/ask spread %
- 20d average volume
- ATR % from recent historicals
- price vs 10d/20d moving averages
- recent high/low support and resistance
- fractional tradability for account 433711041
- catalyst/news note and disconfirmation condition

Rank candidates, but keep the final trading decision policy-gated: broker review success is not a mandate to trade; no trade is correct when the market tape is risk-off, setup confirmation is missing, or existing deployment is already near target.

## Open-order check pitfall

Recent order history is not the same as an open-order query. In scan reports, either query open states explicitly or phrase as "no open order surfaced in recent order query" instead of claiming certainty from a broad recent-order pull.
