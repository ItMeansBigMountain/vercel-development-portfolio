# Service Account + Domain-Wide Delegation Setup

## Goal
Create a Google Cloud Service Account with Domain-Wide Delegation to impersonate any Workspace user — **zero OAuth prompts, ever**.

## Prerequisites
- **Google Workspace Admin** access (super admin)
- Existing Google Cloud project: `airy-sled-497503-r8` (Hermes project)

---

## Step 1: Create Service Account (in Google Cloud Console)

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=airy-sled-497503-r8
2. Click **CREATE SERVICE ACCOUNT**
   - Name: `hermes-workspace-automation`
   - Description: `Zero-touch Workspace API access via Domain-Wide Delegation`
   - Click **CREATE AND CONTINUE**
3. **Grant roles** (optional but recommended):
   - `Service Account User` (allows impersonation)
   - No IAM roles needed for DWD itself
4. Click **DONE**

---

## Step 2: Enable Domain-Wide Delegation

1. In service account details, copy **Unique ID** (numeric, e.g., `123456789012345678901`)
2. Go to: https://admin.google.com/ac/owl/domainwidedelegation
3. Click **ADD NEW**
   - Client ID: paste the Unique ID
   - OAuth Scopes: comma-separated list:
     ```
     https://www.googleapis.com/auth/gmail.readonly,
     https://www.googleapis.com/auth/gmail.send,
     https://www.googleapis.com/auth/gmail.modify,
     https://www.googleapis.com/auth/gmail.settings.basic,
     https://www.googleapis.com/auth/calendar,
     https://www.googleapis.com/auth/drive,
     https://www.googleapis.com/auth/contacts,
     https://www.googleapis.com/auth/spreadsheets,
     https://www.googleapis.com/auth/documents
     ```
4. Click **AUTHORIZE**

---

## Step 3: Create & Download Service Account Key

1. In service account details → **KEYS** tab → **ADD KEY** → **Create new key** → **JSON**
2. Save as `/opt/data/secrets/hermes-workspace-automation-sa.json`
3. `chmod 600 /opt/data/secrets/hermes-workspace-automation-sa.json`

---

## Step 4: Python Usage (Impersonation)

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA_FILE = "/opt/data/secrets/hermes-workspace-automation-sa.json"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
]

def get_service(user_email: str, service: str, version: str):
    """Get an authenticated service impersonating user_email."""
    creds = service_account.Credentials.from_service_account_file(
        SA_FILE, scopes=SCOPES
    ).with_subject(user_email)
    return build(service, version, credentials=creds, cache_discovery=False)

# Usage examples:
gmail = get_service("affan.fareed@gmail.com", "gmail", "v1")
calendar = get_service("trapiistan@gmail.com", "calendar", "v3")
drive = get_service("fareed320@gmail.com", "drive", "v3")
```

---

## Step 5: Replace OAuth Verification with DWD Verification

Create a verification script that uses the service account instead of OAuth tokens:

```python
# verify_workspace_dwd.py
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA_FILE = "/opt/data/secrets/hermes-workspace-automation-sa.json"
SCOPES = [...]  # same as above

PROFILES = {
    "personal-main": "affan.fareed@gmail.com",
    "personal-secondary": "fareed320@gmail.com",
    "trapiistan": "trapiistan@gmail.com",
    "classicalechos": "classicalechos@gmail.com",
    "burner": "laflametoast@gmail.com",
}

creds = service_account.Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)

for profile, email in PROFILES.items():
    user_creds = creds.with_subject(email)
    results = {}
    for svc, ver, call in [
        ("gmail", "v1", lambda s: s.users().getProfile(userId="me").execute()),
        ("calendar", "v3", lambda s: s.calendarList().list(maxResults=1).execute()),
        ("drive", "v3", lambda s: s.files().list(pageSize=1).execute()),
        ("people", "v1", lambda s: s.people().connections().list(resourceName="people/me", pageSize=1).execute()),
    ]:
        try:
            call(build(svc, ver, credentials=user_creds, cache_discovery=False))
            results[svc] = {"ok": True}
        except Exception as e:
            results[svc] = {"ok": False, "error": str(e)[:200]}
    print(json.dumps({"profile": profile, "email": email, "probes": results}, indent=2))
```

---

## Cron Job for DWD Verification

```bash
# Runs every 30 min, verifies all 5 accounts via Service Account
*/30 * * * * /opt/hermes/.venv/bin/python3 /opt/data/scripts/verify_workspace_dwd.py
```

---

## Security Notes

- Service account key is **high-value** — store only in `/opt/data/secrets/` (excluded from backups)
- Domain-Wide Delegation grants **broad access** — limit scopes to minimum needed
- Monitor [Admin Console > Security > API Controls](https://admin.google.com/ac/owl/domainwidedelegation) for unauthorized clients
- Rotate service account key annually: `gcloud iam service-accounts keys rotate --iam-account=hermes-workspace-automation@airy-sled-497503-r8.iam.gserviceaccount.com`

---

## Next Steps

1. **You**: Run Steps 1-3 in Google Cloud Console + Admin Console
2. **Me**: Deploy the verification script + cron job
3. **Result**: Zero-touch Workspace API access for all 5 accounts, forever