# Hermes ↔ Amazon Affiliate MCP

## Intent
When the user asks for Amazon affiliate integration “with chat,” treat the deliverable as first-class MCP tools available in Hermes/Discord—not merely a skill, CLI, dashboard, database, or example API client.

## Architecture
- MCP server: `/opt/data/HeRmEz/projects/affiliate-ops/mcp_server.py`
- Hermes server name: `amazon_affiliate`
- Registry: `/opt/data/HeRmEz/projects/affiliate-ops/data/affiliate_ops.db`
- Dedicated secret file: `/opt/data/secrets/affiliate-ops/creators.env` (`0600`)
- Tools appear after session/gateway restart as `mcp_amazon_affiliate_*`.

## Authentication layers
Keep these distinct:
1. **Associates Central login:** browser session, password/MFA, contracts, tax interview, banking, and reports. Human completion is required for MFA, attestations, tax certification, and bank verification.
2. **Partner Tag / Tracking ID:** public attribution identifier used in Special Links; it is not a secret or API credential. Current user-confirmed ID: `masub-20`.
3. **Creators API:** OAuth 2.0 client-credentials authentication using Credential ID, Credential Secret, credential version, marketplace, and Partner Tag. Never request the secret in Discord; load it from the protected file.
4. **Hermes MCP:** local stdio connection exposing bounded operations to chat. MCP connectivity does not prove Amazon API authorization; test both discovery and a real authenticated Amazon call.

## Required credential file
```dotenv
AMAZON_CREATORS_CREDENTIAL_ID=
AMAZON_CREATORS_CREDENTIAL_SECRET=
AMAZON_CREATORS_CREDENTIAL_VERSION=3.1
AMAZON_PARTNER_TAG=masub-20
AMAZON_MARKETPLACE=www.amazon.com
```

## Verification sequence
1. Confirm `creators.env` exists and mode is `0600` without printing values.
2. Test MCP discovery: `hermes mcp test amazon_affiliate`.
3. Restart/new session so tools are injected; a gateway cannot restart itself from inside its own process.
4. Call `mcp_amazon_affiliate_creators_api_status`; require credential ID, secret, and Partner Tag presence.
5. Make a small real `amazon_get_items` call for a known ASIN.
6. Verify the returned URL is Amazon-vended and contains the correct attribution before registering or publishing it.
7. Read back the registered link and, after publication, the destination description.

## Operational boundary
Creators API supports authenticated catalog/product-link operations. Do not claim it can change tax answers, bank details, contracts, MFA, or general Associates settings. Track only non-sensitive readiness metadata for those areas.

## Onboarding delays
Amazon may delay application/credential availability after onboarding. Record a bounded follow-up reminder with the official onboarding URL rather than polling aggressively or claiming access exists. Once credentials appear, place them in the protected file and perform the verification sequence above.

## Publishing gate
Do not integrate Amazon links into creator descriptions merely because a Partner Tag is known. Require either:
- an Amazon-vended link from authenticated Creators API, or
- a user-generated/verified SiteStripe Special Link.

Then verify attribution, disclosure placement, channel/campaign registration, and published-description readback.