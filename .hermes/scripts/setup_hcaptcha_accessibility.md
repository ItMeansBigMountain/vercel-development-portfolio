# hCaptcha Accessibility Cookie Setup

## Goal
Obtain a persistent accessibility cookie from hCaptcha that allows automated browsers to bypass CAPTCHA challenges on sites that use hCaptcha (not Google's own reCAPTCHA).

---

## Step 1: Register for hCaptcha Accessibility

1. Go to: https://dashboard.hcaptcha.com/welcome_accessibility
2. **Sign up** with an email you control
3. Complete the accessibility verification (they may ask for a brief explanation)
4. Once approved, you'll get access to the accessibility cookie

---

## Step 2: Get the Accessibility Cookie

### Option A: Dashboard Method (Recommended)
1. Log into https://dashboard.hcaptcha.com
2. Go to **Settings** → **Accessibility**
3. Copy the **Accessibility Cookie** value (long base64 string)

### Option B: Browser Extension Method
1. Install hCaptcha Accessibility browser extension
2. Visit any site with hCaptcha
3. Complete the accessibility challenge once
4. The cookie is stored in your browser profile

---

## Step 3: Apply Cookie to Automated Browser

### For Playwright (current automation):
```python
# In google_workspace_browser_reauth.py, add to browser context:
context = browser.new_context(
    # ... existing options ...
)
# Add hCaptcha accessibility cookie
context.add_cookies([{
    "name": "hcaptcha_accessibility",
    "value": "YOUR_ACCESSIBILITY_COOKIE_VALUE",
    "domain": ".hcaptcha.com",
    "path": "/",
    "secure": True,
    "httpOnly": False,
    "sameSite": "None"
}])
```

### For persistent Chrome profile:
```python
# Launch with user data dir that has the cookie
context = browser.new_context(
    user_data_dir="/opt/data/browser-profiles/hcaptcha-accessible",
    # ... other options ...
)
```

---

## Step 4: Store Cookie Securely

Add to Hostinger `.env` (or your secret manager):
```
HCAPTCHA_ACCESSIBILITY_COOKIE="your-long-base64-cookie-string"
```

Then in automation:
```python
import os
cookie = os.environ.get("HCAPTCHA_ACCESSIBILITY_COOKIE")
if cookie:
    context.add_cookies([{"name": "hcaptcha_accessibility", "value": cookie, ...}])
```

---

## Important Limitations

| Limitation | Impact |
|------------|--------|
| **Only works on hCaptcha sites** | Google uses reCAPTCHA — this won't help with Google sign-in |
| **Cookie expires** | Typically 30-90 days; must renew |
| **Per-browser-profile** | Cookie tied to browser profile; headless needs explicit injection |
| **Not a silver bullet** | Some sites use additional bot detection beyond CAPTCHA |

---

## For Google OAuth Specifically

**This does NOT bypass Google's own bot detection** on accounts.google.com. Google uses:
- reCAPTCHA (not hCaptcha)
- Behavioral analysis
- Device fingerprinting
- IP reputation

The real solution for Google OAuth automation is:
1. **Refresh tokens** (already deployed via cron) — primary
2. **Service Account + DWD** (guide created) — long-term zero-touch
3. **Persistent Chrome profile** with real cookies — fallback for interactive flows

---

## Next Steps

1. **You**: Complete hCaptcha accessibility signup at https://dashboard.hcaptcha.com/welcome_accessibility
2. **Me**: Add cookie injection to browser automation scripts
3. **Result**: Automated flows on hCaptcha-protected sites (Discord, some SaaS, etc.) work unattended