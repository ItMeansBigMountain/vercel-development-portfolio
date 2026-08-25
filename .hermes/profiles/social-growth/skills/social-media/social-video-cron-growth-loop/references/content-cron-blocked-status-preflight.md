# Content cron blocked-status and preflight pattern

Use when a social-video or faceless YouTube cron exits successfully but the business result is blocked: no upload, no metrics, no cleanup, or source/provider failure.

## Durable lesson

For the user's content automation, scheduler success is not the same as product success. A job that returns exit code 0 may still have failed the real objective because auth, source download, provider credentials, channel identity, or asset quality blocked the publish step.

## Required status vocabulary

Prefer structured outcome statuses in scripts and Discord reports:

- `ok_uploaded` — new content was uploaded and verified.
- `ok_rendered_pending_upload` — render succeeded but upload intentionally deferred.
- `ok_noop` — no eligible source/content; nothing was expected to happen.
- `blocked_auth` — Google/YouTube token revoked, expired, missing refresh token, or cannot refresh.
- `blocked_scope` — token valid but lacks required Workspace/YouTube scope.
- `blocked_channel_mismatch` — token resolves to the wrong YouTube channel/brand account.
- `blocked_source` — source video/email/media could not be downloaded, accessed, or restored.
- `blocked_provider` — required provider key/credit/API is missing or exhausted.
- `blocked_quality` — narration/visuals/captions/source grounding failed quality gate.
- `error` — unexpected exception or script failure.

## Preflight sequence

Before spending time on rendering/generation:

1. Verify required Workspace profile token if the job reads Gmail/Drive/Calendar.
2. Verify required YouTube token and channel ID if the job uploads, deletes, or fetches private metrics.
3. Verify provider readiness for ElevenLabs/stock footage/external clipping if those paths are required.
4. Verify source availability or fallback availability before committing to a topic.
5. Only then render, upload, verify URL/channel, and update metrics/learnings.

## Reporting pattern

In Discord, summarize as:

```text
Status: blocked_auth / blocked_source / ok_uploaded
What happened: one sentence
Blocked component: token/source/provider/quality
Next action: exact command/profile/API key/callback needed
Artifacts: path(s) if any
```

Avoid reporting only “cron OK” unless the content objective actually completed.

## Channel/token pitfall

When deleting, uploading, or updating metadata, group work by channel/token. A token for Sosai/Trapiistan cannot delete Classical Echos videos. Always verify `channels().list(mine=True)` before channel-specific operations.
