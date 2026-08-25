# YouTube transcript ingestion into Viral Radar / faceless workflows

Session learning: when the user wants to use a YouTube video transcript, do not make them paste large transcript chunks into Discord by default. Use a reusable ingestion wrapper first.

## Durable wrapper

```bash
python3 /opt/data/scripts/youtube_transcript_ingest.py "YOUTUBE_URL" --creator "Creator Name" --title "Short title"
```

The wrapper:

- Calls the skill's `scripts/fetch_transcript.py` helper.
- Falls back to `yt-dlp --skip-download --write-subs --write-auto-subs` when `youtube-transcript-api` is blocked by cloud/VPS IP rules.
- Writes review artifacts under `/opt/data/HeRmEz/projects/viral-clip-radar/CLIP_PLANS/`.
- Mirrors source metadata under `/opt/data/HeRmEz/projects/faceless-youtube-channel/STATE/source_transcripts/`.
- Extracts candidate moments using self-improvement keywords such as one-second rule, worst days, gratitude, meditation, exercise, learning, social/flirting, discipline, dopamine, relapse, and momentum.

## Bot-block handling

If both transcript API and yt-dlp are blocked with YouTube's “Sign in to confirm you’re not a bot” message:

1. Report the block plainly.
2. Ask for the video URL plus either browser cookies, a local media/transcript file, or pasted chunks as fallback.
3. Do not claim transcript ingestion succeeded unless artifacts were actually written.

## Content safety

For creator sources like Hamza and Andrew Huberman, preserve attribution and require transformative use: hook, captions, context/analysis, and no raw reuploading.
