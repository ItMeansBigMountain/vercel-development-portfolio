# Google OAuth project/client and scope isolation lessons (2026-07)

Use this when adding YouTube upload failovers or troubleshooting Google OAuth login errors.

## Project/client mismatch pitfall

Google OAuth test users are attached to the Google Cloud project/OAuth app that owns the client ID in the auth URL. If the user adds a test user in one project but the auth URL uses another project's client ID, login can fail with:

```text
Access blocked
Error 403: access_denied
```

Do not assume the visible Google Cloud project in the user's screenshot is the project used by the current URL. Inspect the client secret file and auth URL client ID.

Useful inspection:

```bash
python3 - <<'PY'
import json
from pathlib import Path
for p in [
 '/opt/data/secrets/youtube-fareed320/youtube_client_secret.json',
 '/opt/data/google_profiles/personal-secondary/google_client_secret.json',
]:
    data=json.loads(Path(p).read_text())
    obj=data.get('installed') or data.get('web') or {}
    print(p)
    print('project_id:', obj.get('project_id'))
    print('client_id:', obj.get('client_id'))
    print('redirect_uris:', obj.get('redirect_uris'))
PY
```

## Keep Workspace and YouTube OAuth separate

For fareed320 and similar accounts, keep two separate OAuth tokens/flows:

- Workspace/Gmail/Calendar/Drive/Docs/Sheets/Contacts token for Hermes email/workspace automation.
- YouTube upload/read/analytics token for video upload failover.

Do not merge these into one confusing flow. Generate both links if the user wants to preserve the account's old Workspace permissions and add YouTube upload.

Workspace scopes include Gmail/calendar/drive/docs/sheets/contacts. YouTube scopes include:

```text
https://www.googleapis.com/auth/youtube.upload
https://www.googleapis.com/auth/youtube.force-ssl
https://www.googleapis.com/auth/youtube.readonly
https://www.googleapis.com/auth/yt-analytics.readonly
```

## Hermes project standardization

If the user wants OAuth to show/use the Hermes Google project, replace the YouTube client secret files with the Hermes OAuth client JSON, then regenerate auth URLs. Existing tokens may continue to work until reauth, but new auth URLs should come from the Hermes client.

Files that may need replacement/verification:

```text
/opt/data/secrets/youtube-classicalechos/youtube_client_secret.json
/opt/data/secrets/youtube-fareed320/youtube_client_secret.json
/opt/data/secrets/youtube-main/youtube_client_secret.json
/opt/data/secrets/youtube-trapiistan/youtube_client_secret.json
/opt/data/secrets/google/youtube/youtube-main-client-secret.json
/opt/data/secrets/google/youtube/faceless-youtube-channel-client-secret.json
```

Back up old client secrets before overwriting them under:

```text
/opt/data/HeRmEz/projects/_backups/
```

## Verification after callback exchange

Exchange the callback with the existing reauth workflow, then verify. The command's `youtube-exchange` verifies by default; there is no `--verify` flag, only `--no-verify` to skip verification.

```bash
python3 /opt/data/scripts/google_reauth_workflow.py youtube-exchange fareed320 '<full localhost callback URL>'
python3 /opt/data/scripts/youtube_auth_healthcheck.py --verbose
```

If the YouTube profile's channel ID is pending, verification should discover `channels().list(mine=True)` and write the actual channel ID/title back into the registry.

## Reporting

When guiding the user, state clearly:

- which OAuth URL is Workspace vs YouTube
- which localhost callback shape to send back
- which project/client ID the URL is using
- that a pending failover is not active until token exchange and channel verification complete