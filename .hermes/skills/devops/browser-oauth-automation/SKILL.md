---
name: browser-oauth-automation
description: "Automate browser OAuth reauth with Playwright."
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [oauth, browser, playwright, google, automation, security]
    related_skills: [google-workspace, hermes-agent-operations, social-video-cron-growth-loop]
---

# Browser OAuth Automation

Use when automated browser reauthentication is needed for OAuth providers where refresh tokens have been revoked/expired and normal OAuth exchange fails.

## Prerequisites

- Hostinger project `.env` contains email/password variables for each profile
- Container has been recreated (not just restarted) after `.env` changes
- Playwright + Chromium installed in isolated venv: `/opt/data/.venvs/google-oauth-browser`
- Provider API dependencies available in Hermes runtime

## Core Pattern

```python
# 1. Generate auth URL via provider helper (PKCE, offline access, consent prompt)
# 2. Launch headless Chromium via Playwright
# 3. Navigate to auth URL
# 4. Fill email → press Enter → fallback click role=button "Next"
# 5. Wait for visible password field
# 6. Fill password → press Enter → fallback click role=button "Next"
# 7. Handle consent/continue buttons by accessibility role
# 8. Capture localhost callback (http://localhost:PORT/?code=...&state=...)
# 9. Exchange via helper with scope verification
# 10. Verify token with live probes
```

## Google Workspace Profile Map

| Profile | Email Var | Password Var | Expected Email |
|---------|-----------|--------------|----------------|
| personal-main | GOOGLE_PERSONAL_MAIN_EMAIL | GOOGLE_PERSONAL_MAIN_PASSWORD | affan.fareed@gmail.com |
| personal-secondary | GOOGLE_PERSONAL_SECONDARY_EMAIL | GOOGLE_PERSONAL_SECONDARY_PASSWORD | fareed320@gmail.com |
| trapiistan | GOOGLE_TRAPIISTAN_EMAIL | GOOGLE_TRAPIISTAN_PASSWORD | trapiistan@gmail.com |
| classicalechos | GOOGLE_CLASSICALECHOS_EMAIL | GOOGLE_CLASSICALECHOS_PASSWORD | classicalechos@gmail.com |
| burner | GOOGLE_BURNER_EMAIL | GOOGLE_BURNER_PASSWORD | laflametoast@gmail.com |

## YouTube Channel Profiles

| Profile | Expected Channel | Token Path |
|---------|------------------|------------|
| fareed320 | A F (UCX_nUA3Yr9VR884DNanyMYA) | /opt/data/secrets/youtube-fareed320/youtube_upload_token.json |
| trapiistan | Sosai Oyama (UCsxzQlusqwmMUdjMvKAJDfA) | /opt/data/secrets/youtube-trapiistan/youtube_upload_token.json |
| classicalechos | Classical Echos (UCcIpxiU2CLEsBdHcc7_lcyA) | /opt/data/secrets/youtube-classicalechos/youtube_upload_token.json |

## Critical Fixes Discovered

| Issue | Fix |
|-------|-----|
| Hidden `Next` button wrapper intercepted click | Use `page.get_by_role("button", name="Next", exact=True)` + keyboard `Enter` fallback |
| Password field not visible after email submit | Explicit `wait_for(state="visible", timeout=15000)` on `input[name="Passwd"]` |
| Playwright exceptions serialize form values | Catch all exceptions, emit only generic `FAILED stage=browser_automation reason=redacted_exception` |
| Credentials exposed in cron logs | Use `no_agent=true` cron with sanitized script; delete failure outputs immediately |
| Headless Google OAuth blocks on bot detection | Manual callback workflow: generate auth URL → user opens in browser → paste `localhost` callback → exchange via helper |
| Container lacks display/VNC for `computer_use` | Don't attempt GUI automation in headless containers; use manual callback or Service Account DWD |
| Refresh tokens eventually revoked | Proactive `*/30 * * * *` cron jobs that verify + refresh; alert only on revocation |

## Credential Safety Rules

- **Never** write passwords to files, logs, or Discord
- Read only from `os.environ` at runtime
- Exception handler must redact Playwright call logs
- Screenshots saved to `/opt/data/cache/oauth-debug/` with 0600 permissions
- Delete cron output directories containing failures immediately

## Verification Pattern

After exchange, run harmless probes specific to the provider:
- Google Workspace: Gmail `users.getProfile` + `labels.list`, Calendar `calendarList.list`, Drive `files.list`, People `connections.list`
- YouTube: `channels.list(part="id,snippet", mine=True)` with expected channel ID match

Token is healthy only if all probes succeed AND identity matches expected.

## Related Files

See `references/headless-oauth-automation-pitfalls.md` for why headless Google OAuth fails in containers and the manual-callback workaround.

See `references/service-account-domain-wide-delegation.md` for zero-touch Service Account + Domain-Wide Delegation setup.

See `references/hcaptcha-accessibility-cookie.md` for hCaptcha accessibility cookie setup and injection.

See `references/manual-callback-workflow.md` for container-safe manual callback pattern.