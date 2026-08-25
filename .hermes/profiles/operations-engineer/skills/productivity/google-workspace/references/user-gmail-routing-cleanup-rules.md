# User Gmail Routing and Cleanup Rules

Use when sorting or cleaning the user's Gmail profiles.

## Durable account policy

Both personal accounts now have user-approved full Workspace/Gmail read-write scopes:
- `personal-main` / `affan.fareed@gmail.com`
- `personal-secondary` / `fareed320@gmail.com`

## Cleanup rules

- Known junk/spam/promotional senders may be trashed without per-item review when clearly low risk.
- Preserve finance/security/billing/account emails unless the user explicitly marks a sender/category as junk.
- Newsletter/source emails are normally deleted only after verified YouTube upload, except duplicate subscriptions on `affan.fareed@gmail.com` as below.

## Specific routing preferences

- Grammarly Insights is personal information. Do not treat it as junk or content-source material without explicit instruction.
- Robinhood trade confirmations, order executions, account notices, and relevant finance notices should route to `Hermes/Finance/Robinhood` and can support the Agentic Robinhood MCP project.
- Zoom meeting-assets emails should route to `Hermes/Archive/Zoom Meeting Assets` for class/meeting summary archives.

## Newsletter duplicate rule

The preferred newsletter/source account is `fareed320@gmail.com` / `personal-secondary`.

For `affan.fareed@gmail.com` / `personal-main`:
1. If the sender also exists in `fareed320@gmail.com`, treat the affan copy as duplicate; trash it and unsubscribe from affan when a safe one-click List-Unsubscribe endpoint exists.
2. If only affan has the sender/email, keep it available to the faceless YouTube newsletter pipeline.
3. After a video upload returns a verified YouTube `video_id`, trash the source email per standard protocol.

YouTube newsletter scripts should check both personal accounts, with `personal-secondary` first and `personal-main` second.