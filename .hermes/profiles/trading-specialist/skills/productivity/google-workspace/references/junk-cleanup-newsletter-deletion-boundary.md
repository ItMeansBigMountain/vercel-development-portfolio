# Junk cleanup approval + newsletter deletion boundary

Session update: the user approved cleanup of known junk/spam emails without requiring a per-item review each time. This changes the previous default for junk only; it does **not** make all Gmail deletion broadly approved.

## Apply this boundary

Allowed without per-item review when sender/category is clearly known junk/spam or marketing from the user's approved junk list:
- Trash/delete obvious promo/junk messages.
- Keep conservative guards for login/security/password/verification/receipt/charge/billing terms unless the user explicitly classifies a sender/message type as junk.
- Report concise counts and examples afterward.

The user has explicitly classified these as junk/promo examples: myQ/Chamberlain sale promos, YEEZY, Discord Nitro promos, Starbucks Rewards promos, Unity Asset Store notifications, Caleb Hammer promos, Skool/Mojo Dojo digests/promos, Chase Freedom DashPass/referral/cashback promos, Expedia rewards/terms promo updates, Ollama promos/updates, Chess.com streak reminders, O'Reilly Auto promos, Best Buy reward/promos, Therabody Prime Day promos, Wade/Hyperplexed feedback, Cooldown event invites, and completed-event Ticketmaster emails when the user says the event is done.

Still require care/verification:
- Newsletter/source emails (TLDR, Daily Stoic, Kino Body): summarize or use as content first. If creating YouTube videos, trash only after upload returns a verified YouTube `video_id`.
- For `affan.fareed@gmail.com`, duplicate newsletter/source senders that also exist in `fareed320@gmail.com` may be trashed/unsubscribed from affan; affan-only source emails should feed the faceless channel before cleanup.
- Grammarly Insights is personal information; do not treat it as junk or content-source material without explicit instruction.
- Priority/admin/security/billing/finance/calendar/Drive actions still require explicit approval unless the user gave an exact scoped instruction.
- Robinhood trade/order/account emails should generally route to `Hermes/Finance/Robinhood` for the Agentic trading project rather than be deleted, except specific promo-ish messages the user calls junk.
- Zoom meeting-assets emails should route to `Hermes/Archive/Zoom Meeting Assets`, not junk.

## Verification pattern

After Gmail trash/delete actions, re-fetch the message metadata and confirm `labelIds` contains `TRASH` before reporting the item as cleaned up.
