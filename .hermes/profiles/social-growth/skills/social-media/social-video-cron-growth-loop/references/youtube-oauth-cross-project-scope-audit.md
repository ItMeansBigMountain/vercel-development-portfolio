# Cross-project YouTube OAuth scope audit before reauthorization

Use this procedure whenever a YouTube/social-video account needs reauthorization or the user asks for “all required scopes.” Do not generate URLs first and audit later.

## Procedure

1. Inventory maintained code under active project roots and shared scripts. Search for literal Google scope URIs, `SCOPES`, `scope=`, token paths, API clients, and cron entrypoints. Exclude generated docs, backups, vendored files, and inactive experiments from requirements unless an active workflow calls them.
2. Build a feature-to-scope map. For the current automation class, distinguish:
   - Workspace user OAuth: Gmail read/send/modify/settings, Calendar, Drive, Contacts, Sheets, Docs.
   - YouTube user OAuth: full channel management, upload, force-SSL metadata operations, readonly discovery, Analytics readonly.
   - Cloud service accounts: `cloud-platform`; never merge this into personal-user consent merely because a renderer uses it.
   - Downloader cookies/device login: browser/session auth, not OAuth scopes.
3. Map features per account. Do not grant YouTube scopes to accounts without a YouTube lane, and do not assume `login_hint` locks the browser account.
4. Keep Workspace and YouTube pending state/token files isolated. Generate a separate URL for each credential class. The callback exchange must use the exact scopes saved in that pending record, not whatever constants happen to exist later.
5. In YouTube automation, include the broad `https://www.googleapis.com/auth/youtube` scope when any maintained metadata/channel-management script explicitly requests it, in addition to `youtube.upload`, `youtube.force-ssl`, `youtube.readonly`, and `yt-analytics.readonly`.
6. Regenerate pending OAuth states only after the audit and code/registry updates. Tell the user all older URLs are invalid.
7. Before presenting URLs, read every pending record and assert exact set equality against the audited per-account set (report missing and extra scopes). Compile modified helpers.
8. After callback exchange, verify the actual Workspace email or YouTube channel ID and granted scopes with harmless live probes before installing/replacing production tokens or replaying crons.

## Pitfalls

- A healthy current token may still lack a scope needed by an infrequently run maintenance script; healthchecks must require the audited union, not only upload/read scopes.
- `include_granted_scopes` does not replace explicit scope auditing.
- Broad Workspace Drive access covers file operations, but maintained clients may still request Docs/Sheets scopes explicitly; include the union expected by token-loading code.
- Do not present stale URLs generated before a scope change—their PKCE state and requested scope set no longer represent the audited authorization.
