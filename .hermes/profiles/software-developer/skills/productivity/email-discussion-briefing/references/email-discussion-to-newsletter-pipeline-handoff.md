# Email discussion to action handoff — newsletter pipeline cleanup

When the user reviews an email discussion brief and says they agree with the proposed prioritization, treat that as approval to proceed with the named next actions from the brief, but keep destructive-scope boundaries intact.

## Pattern

1. Discuss/read email read-only first.
2. If user agrees to run newsletter/video cleanup pipelines:
   - Process only the newsletter/source categories that were discussed or are governed by the newsletter pipeline.
   - Generate/upload video first.
   - Require YouTube `video_id` before any source-email cleanup.
   - For already-processed newsletter emails, cleanup/trash may proceed only where the Gmail token has modify scope or the source pipeline rule permits it.
3. For accounts intentionally configured read-only, such as `personal-main / affan.fareed@gmail.com`, do not request or assume Gmail modify scope just to clean up. Report that cleanup could not physically trash messages and mark them processed/idempotent where the video upload succeeded.
4. Do not generalize approval to unrelated email deletion, unsubscribe, archiving, or replies.

## Reporting

- Say which profiles were scanned.
- Say how many eligible newsletter items remained.
- List uploaded URLs.
- Separately state cleanup status:
  - source email trashed,
  - source email marked processed but not trashed due to read-only scope,
  - blocked pending review.
