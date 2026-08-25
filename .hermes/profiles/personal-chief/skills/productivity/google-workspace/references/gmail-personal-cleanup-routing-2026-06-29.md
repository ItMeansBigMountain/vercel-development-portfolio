# Gmail personal cleanup/routing policy update (2026-06-29)

Use this when auditing or cleaning the user's personal Gmail profiles.

## Personal account permissions

The user explicitly granted full read/write Workspace access for both personal profiles:

- `personal-main` / `affan.fareed@gmail.com`
- `personal-secondary` / `fareed320@gmail.com`

For both, Workspace automation may use Gmail read/modify/send/settings plus Calendar, Drive, Docs, Sheets, and Contacts scopes. Destructive Gmail cleanup still follows the user's cleanup policy boundaries.

## Durable routing rules discovered in cleanup

- **Robinhood trade/order/account notices**: route to `Hermes/Finance/Robinhood`, remove from Inbox, and treat as useful context for the Agentic Robinhood MCP trading project.
- **Zoom meeting-assets emails**: route to `Hermes/Archive/Zoom Meeting Assets`, remove from Inbox. The user teaches/holds classes and wants these as a class/meeting-summary archive.
- **Grammarly Insights**: personal information. Do not treat as junk, newsletter-source material, or content-pipeline input unless explicitly instructed.
- **Known junk confirmed by user**: myQ/Chamberlain promos, YEEZY, Discord Nitro promos, Starbucks Rewards promos, Unity Asset Store notifications, Caleb Hammer promo, Skool/Mojo Dojo digests/promos, Chase Freedom DashPass/referral/cashback promos, Expedia rewards terms update, Ollama promos/updates, Robinhood staking/rewards promo, Chess.com streak reminders, O'Reilly Auto promos, Best Buy promos/rewards, Therabody promos, Wade/Hyperplexed feedback, Cooldown event invites, completed Ticketmaster event emails, npm 2FA reminder when user marks it done, PayPal SoundCloud/payment receipts when user marks them junk.

## Newsletter duplicate rule

For `affan.fareed@gmail.com`, duplicate newsletter subscriptions may overlap with `fareed320@gmail.com`.

1. Check both personal accounts when handling newsletter/source emails for the faceless YouTube pipeline.
2. If the same sender/source exists in `fareed320@gmail.com`, delete/trash the duplicate from `affan.fareed@gmail.com` and unsubscribe from the affan copy when safe one-click List-Unsubscribe is available.
3. If a newsletter/source email exists only in `affan.fareed@gmail.com`, use it in the faceless channel pipeline first, then trash it only after the standard verified-upload protocol returns a YouTube `video_id`.
4. Do not route Grammarly Insights into this source workflow; it is personal information.

## Implementation notes from this session

- `email_sorting_agent.py` was updated to include `personal-main` and to route Robinhood, Zoom meeting assets, and Grammarly appropriately.
- `newsletter_batch_upload.py` was updated so the default profile selection checks both `personal-secondary` and `personal-main` (`all-personal`) and includes `support@kinobody.com` / `dan@tldrnewsletter.com` queries.
