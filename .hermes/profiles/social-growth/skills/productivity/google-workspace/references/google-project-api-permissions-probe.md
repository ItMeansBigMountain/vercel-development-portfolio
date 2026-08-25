# Google Project API and Permission Probe Pattern

Use this when the user asks for a table of Google projects, enabled APIs, and what permissions/access are working.

## Safety rules

- Never print or copy `private_key`, `client_secret`, access tokens, refresh tokens, or full API keys.
- Report only safe metadata: project ID, service-account email, redacted OAuth client ID, credential path, file mode, enabled API names, endpoint status, and high-level error class.
- Use read-only scopes and harmless probes. Do not create, modify, share, send, upload, or delete anything during inventory.

## Credential classes

- **Service account JSON** can mint access tokens and probe many project/API endpoints.
- **OAuth client JSON** cannot by itself reveal enabled APIs or user permissions. It needs a user OAuth token or separate Cloud IAM access; document this limitation rather than reading or exposing the client secret.
- **API keys** can probe public endpoints, but should be redacted and not copied into docs.

## Useful probes

For each service-account JSON:

1. Parse safe fields from JSON:
   - `project_id`
   - `client_email`
   - file mode
2. Mint scoped access tokens with `google-auth`; use one scope per API family when practical.
3. Try Cloud/project management endpoints:
   - Service Usage list enabled APIs:
     `GET https://serviceusage.googleapis.com/v1/projects/{project_id}/services?filter=state:ENABLED&pageSize=200`
   - Cloud Resource Manager project metadata:
     `GET https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}`
   - IAM policy, read-only:
     `POST https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}:getIamPolicy` with `{}`
4. Try harmless product API probes:
   - Calendar: `GET https://www.googleapis.com/calendar/v3/users/me/calendarList`
   - Drive: `GET https://www.googleapis.com/drive/v3/about?fields=user,storageQuota`
   - Gmail: `GET https://gmail.googleapis.com/gmail/v1/users/me/profile`
   - Sheets: `GET https://sheets.googleapis.com/v4/spreadsheets/not-a-real-id`
   - Docs: `GET https://docs.googleapis.com/v1/documents/not-a-real-id`
   - YouTube: `GET https://www.googleapis.com/youtube/v3/videos?part=id&chart=mostPopular&regionCode=US&maxResults=1`

## Interpreting probe results

- `200 OK`: API and credentials worked for that read.
- `404 not_found` on an intentionally fake Docs/Sheets ID: API is reachable; the test resource is fake. Treat this as "API reachable," not a failure.
- `SERVICE_DISABLED`, `accessNotConfigured`, or "has not been used": API is disabled for that project or not propagated yet.
- `403 permission_denied`: API may be enabled, but the principal lacks permission, target resource is not shared, or domain-wide delegation/user impersonation is missing.
- Calendar `calendarList` returning OK for a service account may still show zero calendars until the target calendar is shared with the service-account email.
- Cloud Resource Manager disabled can prevent project display-name/IAM-role lookup even when product APIs like Calendar, Drive, or YouTube work.

## YouTube-specific lesson

Service-account credentials can read public YouTube Data API endpoints such as `videos?chart=mostPopular` when `youtube.googleapis.com` is enabled for the project. This is suitable for public trend metadata in tools like `viral-clip-radar`. YouTube channel uploads, private channel reads, channel management, and analytics commonly still require user OAuth.

## Output shape

If the user explicitly asks for a table, provide a compact Markdown table even if the default Discord style usually avoids tables. Include:

- project/credential label
- project ID
- principal/client
- canonical path
- IAM permissions/roles visible
- enabled APIs visible
- API probes/status

Also save the full safe inventory to a workspace `_ops` document when working in the HeRmEz repo.
