# Expected Environment Variables for OAuth Providers

## Overview

When auditing or rebuilding OAuth automation, consult `config.yaml` and MCP server definitions for the expected variable names per provider. Below is the consolidated map derived from `/opt/data/config.yaml`.

## Google Workspace Profiles

| Profile | Email Variable | Password Variable | Expected Email | Token Path |
|---------|---------------|-------------------|----------------|------------|
| personal-main | `GOOGLE_PERSONAL_MAIN_EMAIL` | `GOOGLE_PERSONAL_MAIN_PASSWORD` | affan.fareed@gmail.com | — |
| personal-secondary | `GOOGLE_PERSONAL_SECONDARY_EMAIL` | `GOOGLE_PERSONAL_SECONDARY_PASSWORD` | fareed320@gmail.com | — |
| trapiistan | `GOOGLE_TRAPIISTAN_EMAIL` | `GOOGLE_TRAPIISTAN_PASSWORD` | trapiistan@gmail.com | — |
| classicalechos | `GOOGLE_CLASSICALECHOS_EMAIL` | `GOOGLE_CLASSICALECHOS_PASSWORD` | classicalechos@gmail.com | — |
| burner | `GOOGLE_BURNER_EMAIL` | `GOOGLE_BURNER_PASSWORD` | laflametoast@gmail.com | — |

### YouTube Channel Profiles (subsets of Google Workspace)

| Profile | Expected Channel | Token Path |
|---------|------------------|------------|
| fareed320 | A F (UCX_nUA3Yr9VR884DNanyMYA) | `/opt/data/secrets/youtube-fareed320/youtube_upload_token.json` |
| trapiistan | Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) | `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json` |
| classicalechos | Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) | `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json` |

## Cloudflare Workers Accounts

| Account | Variable | Notes |
|---------|----------|-------|
| Primary | `CLOUDFLARE_API_TOKEN` | — |
| Blog | `CLOUDFLARE_BLOG_API_TOKEN` | — |

## Third-Party MCP Server OAuth

| Service | MCP Config (config.yaml) | Auth Mode | Env Var |
|---------|--------------------------|-----------|---------|
| Vercel | `mcp_servers.vercel` | OAuth | `VERCEL_API_TOKEN` (CLI; MCP OAuth is separate, via `hermes mcp login vercel`) |
| Amazon Affiliate | `mcp_servers.amazon_affiliate` | Script-based | `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` |
| PayPal | `mcp_servers.paypal` | OAuth | — (MCP handles token exchange) |
| Stripe | `mcp_servers.stripe` | OAuth | — (MCP handles token exchange) |
| Square | `mcp_servers.square` | OAuth | — (MCP handles token exchange) |
| Unreal Engine | `mcp_servers.unreal-engine` | None | — |

## Parrot AI

| Variable | Notes |
|----------|-------|
| `PARROTAI_API_KEY` or `PARROTAI_OAUTH` | **Not found in config.yaml** — verify it exists in the Hostinger `.env` or MCP server config |

## Verification

For each provider, verify token health by running a harmless probe:
- **Google Workspace**: Gmail `users.getProfile`, Calendar `calendarList.list`, Drive `files.list`
- **Vercel**: `vercel projects ls` against the account
- **YouTube**: `channels.list(part="id,snippet", mine=True)` with expected channel ID match

## Missing Variables to Check

- `PARROTAI_OAUTH` / `PARROTAI_API_KEY` — referenced by user but not found in config
- `GOOGLE_WORKSPACE_OAUTH` — Google OAuth flows referenced in scripts but no single env var in config; credentials are read from Hostinger `.env` at runtime for each profile