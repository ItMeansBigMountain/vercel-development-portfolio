# Manual Callback OAuth Workflow (Container-Safe)

## Problem
Headless browser automation for Google OAuth fails in containers due to:
- No display server (X11/Wayland)
- No VNC server installable without sudo
- Google bot detection blocking headless Chromium
- `computer_use` tool requires GUI desktop session

## Solution: Manual Callback Workflow

### Step 1: Generate Auth URL (Agent)
```python
from google_profile_oauth import auth_url
auth_url("personal-main")  # prints URL to stdout
```

### Step 2: User Opens URL in Their Browser
- Opens on their local machine (has display, cookies, 2FA, passkeys)
- Signs in with credentials
- Approves all requested scopes
- Google redirects to `http://localhost:1/?code=XXXX&state=YYYY`

### Step 3: User Copies Full Callback URL
- Page shows "This site can't be reached" — **expected**
- Copy entire URL from address bar: `http://localhost:1/?code=...&state=...&scope=...`

### Step 4: Agent Exchanges Code for Token
```python
from google_profile_oauth import auth_code
auth_code("personal-main", "http://localhost:1/?code=...&state=...&scope=...")
```

### Step 5: Agent Verifies Token
```python
from google_reauth_workflow import verify_workspace
verify_workspace("personal-main")
```

## Cron Job Pattern
```
# Auth URL generation (manual trigger)
0 2 * * 0 /opt/hermes/.venv/bin/python3 /opt/data/scripts/google_profile_oauth.py auth-url personal-main > /opt/data/cache/oauth-urls/personal-main.txt
0 2 * * 0 /opt/hermes/.venv/bin/python3 /opt/data/scripts/google_profile_oauth.py auth-url personal-secondary > /opt/data/cache/oauth-urls/personal-secondary.txt
# ... etc

# Verification (automatic, every 30 min)
*/30 * * * * /opt/hermes/.venv/bin/python3 /opt/data/scripts/google_reauth_workflow.py verify workspace personal-main
*/30 * * * * /opt/hermes/.venv/bin/python3 /opt/data/scripts/google_reauth_workflow.py verify workspace personal-secondary
# ... etc
```

## Why This Works
| Factor | Manual Callback | Headless Automation |
|--------|-----------------|---------------------|
| Display needed | No (user's browser) | Yes (container needs X11) |
| 2FA/Passkey | User handles | Blocked |
| Bot detection | User is human | Headless flagged |
| VNC/sudo | Not needed | Required |
| Token result | Identical | Identical |

## Credential Safety
- Passwords **never** leave Hostinger `.env`
- Agent only sees auth URL + callback URL (no passwords)
- Tokens stored in `/opt/data/google_profiles/<profile>/google_token.json` (600)
- Refresh tokens enable automatic renewal for months

## When to Use
- Primary: Container environments without GUI
- Fallback: When automated browser auth fails
- Proactive: Quarterly re-auth to keep refresh tokens alive