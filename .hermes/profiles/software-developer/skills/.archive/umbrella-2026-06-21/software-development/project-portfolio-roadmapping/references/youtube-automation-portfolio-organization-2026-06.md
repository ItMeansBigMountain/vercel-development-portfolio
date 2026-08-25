# YouTube Automation Portfolio Organization (2026-06)

Session learning: when the user has multiple YouTube automation projects, organize them by **project lane** and centralize shared upload infrastructure instead of leaving each project with its own ad hoc uploader.

## Workspace docs created

```text
/opt/data/HeRmEz/projects/YOUTUBE_AUTOMATION_PORTFOLIO.md
/opt/data/HeRmEz/projects/_ops/youtube-automation/YOUTUBE_UPLOAD_METHOD.md
```

## Portfolio lane pattern

Use clear ownership boundaries:

```text
faceless-youtube-channel = original faceless videos generated from trends
viral-clip-radar         = transformative short clips from existing long-form content
youtube-high-ticket-*    = personal story / authority / future offer channel
tweet_video_generator    = legacy/archive, not active upload source
```

## Operating rules

- One shared YouTube OAuth/upload method in `_ops/youtube-automation/`.
- Per-project render pipelines are allowed, but upload goes through the shared method.
- Add `UPLOADS/youtube_uploads.jsonl` to each active YouTube project.
- First uploads are private until user approval.
- Legacy deleted-client tokens should be documented as archive/source material, not revived as canonical credentials.

## Next-step queue shape

After organizing the portfolio, make the next queue concrete:

1. Replace old per-project upload scripts with shared uploader calls.
2. Build a one-command pipeline for the highest-priority active project.
3. Record uploads in JSONL.
4. Build a simple report/dashboard showing latest MP4, YouTube ID, privacy, upload date, and next action.
