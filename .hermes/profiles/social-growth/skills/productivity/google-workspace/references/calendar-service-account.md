# Google Calendar with a Service Account

Use this when the user provides a Google Cloud service-account JSON and wants durable Calendar automation without a personal OAuth browser flow.

## What service accounts can and cannot do

- A service account is its own Google principal, not the user's Google identity.
- It can access calendars only when the target calendar is explicitly shared with the service-account email, unless the user is on Google Workspace and configures domain-wide delegation.
- API keys are not enough for private personal calendars or event creation. Use OAuth or a service account.

## Setup pattern

1. Save the service-account JSON outside the git-backed project tree, e.g.:

   ```bash
   /opt/data/google_service_account.json
   chmod 600 /opt/data/google_service_account.json
   ```

2. Add the credential path to the Hermes env file:

   ```env
   GOOGLE_APPLICATION_CREDENTIALS=/opt/data/google_service_account.json
   ```

3. Ask the user to share the desired calendar with the service-account email from the JSON (`client_email`).
   - Read-only: **See all event details**
   - Write access: **Make changes to events**

4. Verify service-account auth and Calendar API access:

   ```bash
   /opt/hermes/.venv/bin/python - <<'PY'
   import json, urllib.request, urllib.error
   from google.oauth2 import service_account
   from google.auth.transport.requests import Request

   path = '/opt/data/google_service_account.json'
   scopes = ['https://www.googleapis.com/auth/calendar.readonly']
   creds = service_account.Credentials.from_service_account_file(path, scopes=scopes)
   creds.refresh(Request())

   req = urllib.request.Request(
       'https://www.googleapis.com/calendar/v3/users/me/calendarList?maxResults=10',
       headers={'Authorization': 'Bearer ' + creds.token},
   )
   try:
       with urllib.request.urlopen(req, timeout=20) as r:
           data = json.load(r)
       print(json.dumps({
           'ok': True,
           'calendar_count': len(data.get('items', [])),
           'summaries': [i.get('summary') for i in data.get('items', [])[:5]],
       }, indent=2))
   except urllib.error.HTTPError as e:
       print(json.dumps({'ok': False, 'status': e.code, 'body': e.read().decode(errors='replace')[:1000]}, indent=2))
   PY
   ```

## Common outcomes

- `calendar_count: 0` with `ok: true`: auth works, but no calendars are shared yet.
- `403 accessNotConfigured`: enable the Google Calendar API in the service account's project.
- `404 Not Found` or empty list when targeting a personal calendar: the calendar has not been shared with the service account, or the wrong calendar ID is being used.

## Safety

Never print the private key or full service-account JSON in replies or logs. Confirm before creating, updating, deleting, or inviting attendees to events.
