# Personal Gmail cleanup and routing rules (2026-06)

Use when auditing, cleaning, sorting, or routing the user's personal Gmail accounts.

## Account permission policy

The user explicitly granted full Workspace read/write access for both personal accounts:

- `personal-main` / `affan.fareed@gmail.com`
- `personal-secondary` / `fareed320@gmail.com`

Full access includes Gmail read/modify/send/settings and full Calendar, Drive, Docs, Sheets, and Contacts scopes. Do not treat `personal-main` as Gmail-read-only anymore.

## Cleanup boundaries

The user allows known junk/spam/promo cleanup without per-item review, but continue guarding security, finance, billing, login, verification, receipts, appointments, and source/newsletter workflows unless the user explicitly categorizes them.

User-categorized junk/promo examples from this session:

- myQ / Chamberlain sale promos
- YEEZY promos
- Discord Nitro promos
- Starbucks Rewards promos
- Unity Asset Store notifications
- Caleb Hammer promos
- Skool / Mojo Dojo weekly digests and community promos
- Chase Freedom DashPass/referral/cashback promos
- Expedia rewards/terms promo updates
- Ollama promotional/update emails
- Robinhood staking/rewards promo-ish emails, when explicitly classified as junk by the user
- Chess.com streak reminders
- O'Reilly Auto promos
- Best Buy reward/promo emails
- Therabody Prime Day promos
- Wade / Hyperplexed feedback emails
- Cooldown event invites
- Completed-event Ticketmaster emails when the user states the event is done

User-approved deletes from this session:

- RuneScape finale info
- LaserAway appointment details
- Landing Orlando waitlist
- npm 2FA reminder in `fareed320@gmail.com` after user said delete it
- PayPal SoundCloud payment/receipt in `fareed320@gmail.com` after user said delete it

## Keep / route / special handling

- Grammarly Insights is personal information. Do not use it as content-source material and do not clean it as junk unless the user explicitly says so.
- Zoom meeting-assets emails should be routed to `Hermes/Archive/Zoom Meeting Assets` and removed from Inbox. The user holds classes and wants this as an archive for meeting summaries.
- Robinhood trade confirmations, order executions, and account notices should be routed to `Hermes/Finance/Robinhood` and removed from Inbox. These can be useful context for the Agentic Robinhood MCP trading project.

## Newsletter duplicate policy across personal accounts

`affan.fareed@gmail.com` may have duplicate newsletter subscriptions also present in `fareed320@gmail.com`.

When handling TLDR / Kinobody / Greg / similar source newsletters:

1. Check both personal accounts.
2. If a source sender exists in `fareed320@gmail.com`, treat the copy in `affan.fareed@gmail.com` as duplicate: trash it from affan and attempt standards-based one-click unsubscribe when available.
3. If the source exists only in `affan.fareed@gmail.com`, feed it into the faceless YouTube newsletter pipeline, then remove it only after verified upload/video_id according to the standard source-email protocol.
4. Keep `fareed320@gmail.com` as the preferred newsletter/source account where possible.

## Verification pattern

For destructive or routing actions:

- After trashing, re-fetch metadata and verify `TRASH` is present.
- After routing/archiving, verify the target label is present and `INBOX` is removed.
- Save a non-secret local JSON audit under `/opt/data/HeRmEz/projects/_ops/` when doing multi-message cleanup.
