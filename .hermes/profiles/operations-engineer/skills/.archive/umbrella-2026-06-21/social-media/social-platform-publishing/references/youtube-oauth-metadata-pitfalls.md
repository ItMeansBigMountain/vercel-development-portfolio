# YouTube OAuth client and metadata update pitfalls

Use this when YouTube upload or metadata-edit OAuth fails during social publishing automation.

## `Error 401: deleted_client`

Google's OAuth page may show:

```text
Access blocked: Authorization Error
Error 401: deleted_client
The OAuth client was deleted.
```

This means the OAuth client ID embedded in the auth URL no longer exists. Do not retry the same URL. Inventory available Google OAuth client-secret JSON files and regenerate the auth URL using a live client for the relevant project.

Safe inventory pattern:

- Search known secrets/project folders for JSON files.
- Parse only safe metadata: path, `installed` vs `web`, `project_id`, redacted client ID prefix, redirect URIs.
- Do not print client secrets or token contents.
- Update the OAuth helper's default client path to the current live client.
- Generate a fresh auth URL and have the user paste back the full localhost redirect.

## Upload scope is not enough for description/title cleanup

`https://www.googleapis.com/auth/youtube.upload` can upload videos but may not allow editing existing video snippets. If `videos.update(part='snippet')` returns insufficient permission, reauth with broader YouTube scope such as:

```text
https://www.googleapis.com/auth/youtube.upload
https://www.googleapis.com/auth/youtube
```

Then retry metadata cleanup.

## Wrong-channel tokens return forbidden

If `videos.update(part='snippet')` returns `403 forbidden` after scope reauth, verify the token owns the channel that owns the target video. Multi-channel users may authorize a different YouTube identity than the one that uploaded the older video. Always run `channels().list(part='snippet,contentDetails', mine=True)` and compare it with the target video's `snippet.channelId` / `channelTitle` before claiming cleanup is impossible.

Use separate token paths for separate channels/projects when needed, and name them by channel purpose rather than reusing one ambiguous `youtube_upload_token.json`.

## Metadata safety for faceless/newsletter projects

Public YouTube titles/descriptions/tags should not expose production mechanics such as AI-generated, faceless automation, ElevenLabs, source email, source profile, or pipeline wording. Keep this operational detail in local manifests only.

For the user's newsletter/faceless channel, descriptions should include the configured public support/social URLs when available: Linktree, Buy Me a Coffee, Cash App, and Venmo. After editing, read the snippet back and verify both: (1) banned production terms are absent, and (2) required support URLs are present.
