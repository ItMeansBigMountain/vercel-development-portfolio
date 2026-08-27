# Headless Google OAuth Automation Pitfalls

## Problem

Google Workspace OAuth in headless containers is deliberately blocked by Google's anti-bot measures. Multiple automation attempts failed:

| Attempt | Method | Result |
|---------|--------|--------|
| 1 | Playwright visible-button selectors | Blocked at email page |
| 2 | Playwright accessibility-role `role=button Next` | Blocked at email page |
| 3 | Keyboard `Enter` submission | Blocked at email page |
| 4 | Hybrid keyboard + button fallback | Blocked at email page |

All attempts stopped at the email entry screen with title "Sign in - Google Accounts" at `accounts.google.com`. No password prompt, no CAPTCHA, no 2FA challenge reached.

## Root Cause

Google detects and blocks automated browser sessions before any credential verification. This is intentional Google behavior, not a script bug. The container lacks:
- Real browser fingerprint
- Human interaction patterns
- hCaptcha accessibility cookie (for hCaptcha challenges on other sites, not Google)
- Persistent browser profile with history

## Practical Workaround: Manual OAuth on User Machine

1. **Generate OAuth URLs** using the helper script:
   ```bash
   python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url <profile>
   ```

2. **User opens URLs in their local browser** (has real fingerprint, cookies, history)

3. **User completes Google sign-in + consent**

4. **User copies the `localhost` callback URL** from browser address bar

5. **Exchange callback for tokens**:
   ```bash
   python3 /opt/data/scripts/google_reauth_workflow.py workspace-exchange <profile> '<callback_url>'
   ```

6. **Verify tokens work**:
   ```bash
   python3 /opt/data/scripts/google_reauth_workflow.py verify workspace <profile>
   ```

## When to Use This Pattern

- Any Google Workspace OAuth in headless/CI/container environments
- When automation repeatedly blocks at email/password screens without clear error
- When user has local browser access and can complete OAuth manually

## Do NOT Waste Time On

- Trying different Playwright selectors/waits
- hCaptcha accessibility cookies (Google doesn't use hCaptcha)
- Rotating user agents / browser fingerprints
- Adding delays / human-like typing
- The block is at Google's infrastructure level, not the page level

## Container Environment Constraints

This container has:
- No X11/Wayland display
- No VNC server (no sudo to install)
- No graphical browser
- `cua-driver` not installed
- Python venv without pip

These are environmental limitations, not fixable in-session.