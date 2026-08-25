# Automatic media cleanup for social-video pipelines

Use this pattern when the user expects clipping/render jobs to clean themselves up continuously, not only during a manual disk-pressure intervention.

## Required design

1. **Install a dedicated deterministic cleanup job** rather than relying only on prose inside generation/upload cron prompts.
2. Schedule it independently so cleanup still runs when discovery, rendering, upload, OAuth, or model-driven jobs fail.
3. Keep cleanup silent when no files are removed; report file count and reclaimed bytes only when work occurs.
4. Use allowlisted media roots and extensions. Never recursively purge an entire project root.
5. Protect active retry and hold queues unconditionally.
6. Preserve code, manifests, subtitles, source metadata, upload logs/ledgers, analytics, research briefs, and performance notes.
7. Delete temporary source media immediately after successful renders when the source is no longer needed. Keep rendered clips when upload is blocked by moving them into the protected retry queue with complete upload metadata.
8. Apply retention windows to stale generated media and unqueued source/render/temp media. Keep queue media until confirmed upload or an explicit user-approved discard.
9. Verify after every cleanup: targeted remaining-file count, queue integrity, and filesystem free space.

## Workflow correction

When the user says they want automatic cleanup, completing one manual cleanup is not sufficient. In the same task, verify an existing cleanup schedule or create one, execute a dry run, execute/verify the script, and report the schedule/job ID.

## Clip-run ordering

1. Scout and select an approved source.
2. Acquire the source with the configured fallback ladder.
3. Render and validate vertical clips.
4. Attempt upload.
5. If upload succeeds, preserve the returned video ID/URL and delete generated media according to policy.
6. If upload fails, queue the exact rendered clip plus title, description, attribution, source URL, and blocker details.
7. Delete only source/temp media that is no longer needed for retry.
8. Run the deterministic cleanup and verify protected queue files remain.

## Pitfalls

- Do not claim automation exists merely because a generation cron prompt says “clean up safely.”
- Do not delete a rendered clip after an upload/auth/quota failure unless it has first been copied or moved into a protected retry queue with metadata.
- Do not let age-based cleanup touch `UPLOAD_QUEUE`, `UPLOAD_QUEUE_HOLD`, or equivalent retry roots.
- Do not use unrelated filler simply because an approved creator source is blocked. Continue through approved source-ready fallbacks or report the blocker; when the user separately authorizes broader scouting, label the source and lane honestly.
