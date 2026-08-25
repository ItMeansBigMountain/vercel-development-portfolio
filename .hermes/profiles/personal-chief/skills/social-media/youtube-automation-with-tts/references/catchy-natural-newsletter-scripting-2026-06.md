# Catchy natural newsletter script standard — 2026-06

Use this when converting newsletters/emails into faceless videos for the user's Sosai/Trapiistan lane.

## User correction

The user explicitly asked for videos from each newsletter and said: make them sound catchy and natural; write better scripts. Treat this as a script-quality gate, not a cosmetic preference.

## Narration rules

- One newsletter email = one video/story.
- The spoken script should feel like a charismatic host/avatar telling a mini-story, not reading bullet headings.
- Open with the most surprising, high-stakes, or emotionally sticky detail from the newsletter.
- Use actual newsletter facts as the core receipts. Do not invent generic advice, morals, or unrelated opinions.
- Avoid rigid formulas like: `Introduction`, `the signal`, `operator angle`, `move first`, `my read`, `build one proof today`, or stitched-together section labels.
- Captions may be punchy labels, but they are display-only and must not be read aloud by TTS.
- Keep transitions conversational: `here's where it gets interesting`, `the twist is`, `that matters because`, `watch where the money/workflow/behavior moves next`.
- Match tone by topic: AI/tech can be witty and sharp; finance should follow money/cash-flow; security should carry urgency; stoic/self-improvement should feel grounded, not preachy; fitness/martial arts should be vivid and embodied.

## QA before render/upload

Before rendering/uploading, read the script out loud mentally and reject it if it sounds like:

- disconnected lecture cards;
- generic self-help advice not present in the newsletter;
- an assistant's opinion wrapped around a thin source fact;
- repeated old catchphrases;
- captions being spoken as narration.

If the script fails this gate, rewrite it first, then render.

## Implementation note

The project-side script `faceless-youtube-channel/scripts/newsletter_batch_upload.py` was patched in 2026-06 to use tone packs by source type and remove the repeated `BUILD ONE PROOF TODAY` overlay. Preserve this direction when editing the pipeline.
