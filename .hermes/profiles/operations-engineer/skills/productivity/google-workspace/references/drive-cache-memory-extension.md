# Google Drive as a Hermes cache / memory extension

Use this pattern when the user wants Google Drive to act as a durable cache for Hermes artifacts, context, or long-form memory.

## Architecture

- Keep compact, high-value facts in Hermes memory / fact store.
- Store bulky or retrievable artifacts in a Drive-backed object cache.
- Save lightweight pointers in memory, e.g. `Drive cache object: namespace=personal-brand key=story-v1`.
- Use a local JSON cache as the source of truth while Drive auth/routing is being finalized.

A practical file layout:

```text
cache/
  index.jsonl
  objects/<namespace>/<key>.json
  blobs/<namespace>/<key>/<attachments>
```

Each JSON object should include namespace, key, title, text, tags, metadata, attachments, created_at, and updated_at.

## Auth decision: OAuth vs service account

For personal Google Drive storage, prefer user OAuth with Drive scope. A Google service account can call Drive APIs, but it does not have normal personal Drive storage quota; uploads to its own Drive space may fail with:

```text
Service Accounts do not have storage quota. Leverage shared drives, or use OAuth delegation instead.
```

Use service accounts only when:

1. The target is a Shared Drive or shared folder the service account can write to, and the code passes `supportsAllDrives=True` / `includeItemsFromAllDrives=True` where needed; or
2. Workspace domain-wide delegation is configured and appropriate; or
3. The operation is read-only against files/folders explicitly shared with the service account.

For the user's Hermes setup, the Hermes base service account is the right default for Hermes-owned automation, but app-specific `GOOGLE_APPLICATION_CREDENTIALS` may point elsewhere. Prefer a tool-specific override such as `HERMES_DRIVE_CACHE_CREDENTIALS` instead of blindly using global ADC.

## Implementation checklist

1. Inspect existing Google credential inventory, but never expose secrets.
2. Choose auth route:
   - personal Drive cache: Google Workspace OAuth token with Drive scope;
   - shared storage: service account + shared folder/Shared Drive folder ID.
3. Build local cache operations first: `put`, `get`, `list`, `search`.
4. Add Drive `probe` before upload: report auth mode, credential/token path, Drive user, folder ID, and parent ID.
5. Add `sync-up` with idempotent folder creation and update-or-create file behavior.
6. If using service accounts with shared drives, include `supportsAllDrives=True` and `includeItemsFromAllDrives=True` on list/create/update calls.
7. Keep local cache payloads out of git via `.gitignore`.
8. Document the next user action clearly: share folder / provide folder ID / complete OAuth.

## Pitfalls

- Do not treat service-account Drive access as equivalent to a user's personal Drive. It may authenticate but still fail to upload due to storage quota.
- Do not use global `GOOGLE_APPLICATION_CREDENTIALS` without checking project purpose; it may be set for an app-specific project rather than Hermes base automation.
- Do not commit cache contents, media, tokens, OAuth JSON, service-account private keys, or generated artifacts.
- `drive-probe` succeeding only proves API/auth reachability; verify write behavior with a tiny test object before promising Drive-backed caching is fully live.
