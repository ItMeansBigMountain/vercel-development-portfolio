# Drive service-account cache pattern

Use when Hermes needs Google Drive as durable object storage/cache, especially for generated MP4s or bulky artifacts that should be deleted from local VPS disk after backup.

## Key behavior

Google service accounts can authenticate to the Drive API, create/list folders, and write into locations they have access to, but they do **not** have normal personal My Drive storage quota. Uploads to a service-account-owned My Drive can fail with:

```text
Service Accounts do not have storage quota. Leverage shared drives, or use OAuth delegation instead.
```

Do not treat that as bad credentials. It means the destination must be changed.

## Correct routes

Preferred for service-account-based cache:

1. Create a Google Shared Drive, or a Drive folder/location that is writable by the service account.
2. Share/add the service account email as a writer/content manager.
3. Set the cache parent folder/drive ID in the workflow config, e.g. `HERMES_DRIVE_CACHE_PARENT_ID`.
4. Use Drive API calls with `supportsAllDrives=True` and list calls with `includeItemsFromAllDrives=True`.
5. Upload large artifacts there, then delete local copies only after Drive returns a successful upload response.

Alternative:

- Use personal OAuth with Drive scope when the user wants files written directly as their Google user account.

## Safe MP4 cache workflow

For generated clips:

1. Compute local file metadata first: size, SHA-256, source path, namespace/key.
2. Upload the MP4 to Drive under a deterministic cache folder such as `Hermes Drive Cache/mp4-cache/<namespace>/`.
3. Write a manifest containing Drive file ID/link, SHA-256, size, source path, and auth mode.
4. Upload the manifest next to the MP4 when possible.
5. Delete the local MP4 only after the MP4 upload succeeds.
6. If quota, permission, or API errors occur, keep the local MP4 and report the blocker.

This pattern lets Hermes use Drive as an external cache/backing store without filling VPS disk or losing generated media.