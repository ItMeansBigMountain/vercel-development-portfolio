# Gmail email audit pattern

Use this when the user asks to audit inboxes, subscriptions, billing notices, newsletters, or junk mail across Gmail/Google Workspace profiles.

## Safety boundary

- Default to **read-only audit**: profile counts, query counts, sender lists, sample subjects, labels, and classification.
- Do **not** delete, trash, spam-report, archive, unsubscribe, send, or modify labels during the audit.
- If cleanup is requested, first present a concrete batch: account/profile, sender, count, action, and examples. Execute only after explicit approval.
- If the user has already declared a sender/category junk, that is enough to propose cleanup, but still show the batch before destructive actions unless the user explicitly says to perform it now.

## Multi-profile OAuth pattern

When tokens are stored under `/opt/data/google_profiles/<profile>/google_token.json`, iterate every profile and build Gmail clients from each token rather than relying on the default single `google_token.json`.

Harmless probes:

- `users.getProfile(userId='me')` for account email and message/thread totals.
- `users.labels.list(userId='me')` to verify labels such as `SPAM` and `TRASH` exist.
- `users.messages.list` + `users.messages.get(format='metadata', metadataHeaders=['From','Subject','Date','List-Unsubscribe'])` for sender audits.

## Useful audit query buckets

Tune these based on user preferences:

- Known junk: declared junk senders/categories, e.g. `newer_than:180d (FoundersCard OR Yieldi OR Crunch OR Higgsfield)`.
- Billing/finance important: `newer_than:90d (invoice OR receipt OR billing OR charge OR payment OR subscription OR renewal OR statement OR Chase OR "Apple Card" OR Robinhood OR Vercel OR Render OR OpenAI OR Anthropic OR AWS OR Azure OR "Google Cloud" OR Stripe)`.
- News source: `newer_than:30d from:tldrnewsletter.com`.
- Review-after-summary: `newer_than:60d (kinobody OR "Daily Stoic")`.
- Consumer marketing junk candidates: `newer_than:90d category:promotions (sale OR discount OR coupon OR offer OR "shop now" OR BOGO OR "limited time")`.
- Subscription review: `newer_than:90d (unsubscribe OR "manage preferences" OR "email preferences")`.

Prefer exact sender queries for high-value categories to avoid false positives from newsletter text:

- Chase: `from:no.reply.alerts@chase.com`
- Apple receipts: `from:no_reply@email.apple.com`
- Robinhood: `from:(noreply@robinhood.com OR hello@snacks.robinhood.com)`
- Landing: `from:(hello@hellolanding.com OR care@hellolanding.com)`

## Classification output

Keep Discord output skimmable:

- Accounts scanned with totals.
- Confirmed important.
- Review-worthy / morning-report useful.
- Known junk found.
- Likely junk / consumer marketing.
- Needs subscription review.
- Recommended next action.

Avoid tables unless the user asks. Use bullets and bold section headers.

## Pitfalls

- Broad terms like `Apple`, `Chase`, `OpenAI`, or `Landing` can match newsletter subjects and produce false positives. Follow up with exact `from:` probes before calling something important.
- Gmail message IDs can appear in multiple query buckets; deduplicate by `(profile, message_id)` or by `(profile, sender)` for sender summaries.
- `List-Unsubscribe` means a message is subscription-like, not necessarily junk. Put unfamiliar senders into review rather than cleanup.
