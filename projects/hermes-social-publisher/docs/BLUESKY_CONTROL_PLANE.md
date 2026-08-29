# Bluesky connector pilot implementation

This slice implements the first non-YouTube control-plane flow around Postiz's official Bluesky connector.

Safety behavior:

- Reads the Postiz API key only from a protected file (mode `0600`) or an injected runtime secret; never stores it in the ledger.
- Lists `GET /public/v1/integrations`, requires an enabled `identifier=bluesky` integration, and correlates Postiz's integration ID/name/profile with Bluesky's DID/handle/display name before enabling it.
- Stores non-secret destination identity and publication attempts in SQLite.
- Creates Postiz `draft` records without native publication. Bluesky has no native private post mode, so `now` requires a separate explicit approval flag.
- Uses the caller's idempotency key as a unique ledger key. A retry returns the existing attempt and never resubmits.
- Stores a sanitized copy of the exact Postiz response. Public publication is only `published_verified` when Postiz supplies a control-plane post ID, native platform ID, and URL; missing proof remains `unverified_response` and cannot pass cleanup.
- Sends only sanitized destination/outcome fields to Discord.
- Converts missing human connection/identity steps into structured `AuthorizationRequired` blockers.

Official API surfaces used:

- `GET /public/v1/integrations`: https://docs.postiz.com/public-api/integrations/list
- `POST /public/v1/posts`, including `type=draft`: https://docs.postiz.com/public-api/posts/create
- Bluesky provider settings (`__type=bluesky`): https://docs.postiz.com/public-api/providers/bluesky

Run focused tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Pilot execution remains intentionally blocked until a real public HTTPS Postiz URL, protected narrow API key, connected Bluesky integration, approved expected DID/handle/display name, and (for any public test) explicit public-post consent exist. Do not put credentials in command history, Discord, Kanban, or this repository.
