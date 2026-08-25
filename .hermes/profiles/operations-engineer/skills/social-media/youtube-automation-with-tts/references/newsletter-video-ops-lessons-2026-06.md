# Newsletter video ops lessons — 2026-06

Use this when operating the user's Classical Echos / faceless newsletter-video backlog pipeline.

## User style and reporting

- In Discord reports, avoid Markdown tables. Use compact bold bullets and short status lists.
- When blocked, state the blocker directly, but first exhaust obvious tool-driven checks.

## Quality gate for Classical Echos newsletter videos

- Target about 2 minutes per newsletter video; use 120 seconds as the render target and reject anything under 110 seconds unless the user explicitly asks for Shorts.
- Use multiple relevant visual segments matched to script beats. Normal 2-minute renders should use at least 6 distinct clips; 8–10 is better.
- Do not upload black/static placeholders, one-clip montages, or generic filler that ignores the newsletter content.
- Distinguish review renders from channel-final renders:
  - Review fallback audio (for example edge-tts) is acceptable only to inspect pacing/visuals.
  - Public channel-final uploads should use ElevenLabs-quality voice unless the user explicitly approves the fallback.

## Source and visual-provider handling

- Newsletter emails may already be labeled outside `INBOX`; search recent all-mail labels for `tldrnewsletter.com`, `dailystoic.com`, `snacks.robinhood.com`, Kino Body, etc., not only `in:inbox`.
- Pexels key presence is not enough. Live-probe Pexels; if it returns 403/quota/auth issues, use an approved fallback or stop before upload.
- Mixkit can serve as a stock-video fallback by scraping direct `.mp4` links from Mixkit pages with a browser User-Agent. Save a manifest of source URLs for each render.

## Upload operations

- Upload public by default for approved automation lanes.
- Verify the active YouTube token owns the target channel before upload/update. Classical Echos uploads use the Classical Echos channel token.
- Use the same Python interpreter for wrapper scripts and nested upload helpers; avoid `python3` if it lacks Google packages. Prefer `sys.executable` in wrapper code.
- YouTube may hard-stop with `uploadLimitExceeded`. Treat this as a channel/day limit: preserve unuploaded workspaces, write a pending manifest, and schedule a one-shot resume job after the expected reset.
- Trash Gmail source messages and delete local workspaces only after a successful YouTube `video_id`, calendar event creation, and upload log entry.
