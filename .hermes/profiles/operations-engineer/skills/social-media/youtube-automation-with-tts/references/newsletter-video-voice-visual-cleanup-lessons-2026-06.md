# Newsletter video voice, visual, and cleanup lessons — 2026-06

Session learning from the user's newsletter-to-YouTube pipeline corrections.

## Narration and captions

- Captions/headers are **display-only**. Do not include overlay captions such as `YOU MISSED THIS`, `THE RECEIPT`, or `YOUR MOVE` in the TTS text.
- The spoken script should be a natural charismatic monologue, not a rigid intro/body/conclusion outline.
- Use the original email tone/topic to pick an internal narrator archetype inspired by familiar movie-actor energy:
  - AI/tech: fast, witty inventor energy.
  - Security: heist-briefing / no-nonsense urgency.
  - Finance/crypto: smooth strategic confidence.
  - Stoic: calm wise narrator.
  - Fitness/martial arts: intense mentor / training-montage energy.
- Do not clone, impersonate, or publicly claim celebrity endorsement. Keep actor references internal as writing direction only.

## Topic classification

Add/maintain explicit classes for:

- `fitness` — Kino Body, workout, gym, physique, nutrition, training discipline.
- `martial_arts` — karate, boxing, MMA, UFC, BJJ, Muay Thai, sparring, dojo, warrior/training-standard content.

## Visuals

- Each scene must have its own relevant stock/API asset.
- Derive one concrete keyword from the spoken beat, then combine it with topic + mood for a short search query.
- Keep stock search queries short. Long sentence-like queries caused provider failures; target ~75 chars or less and trim at word boundaries.
- If Pexels/Pixabay/Shutterstock/Wikimedia or approved stock fallbacks fail for a scene, block for review instead of rendering black/random/generic filler.
- Preserve `visual_manifest.json` with scene, caption, keyword, query, selected asset, and provider metadata.

## Voice provider order

- Prefer ElevenLabs when a live generation succeeds.
- Use Google Cloud TTS as production fallback.
- Parrot AI remains a browser/manual experiment path until export/download is proven reliable end-to-end.

## Upload and Gmail cleanup

- One email = one video.
- Upload first; require a returned YouTube `video_id`.
- Append the source-message idempotency marker immediately after verified upload, **before** Gmail cleanup. This prevents duplicate uploads if Gmail trash fails.
- Then try to trash the source email.
- If the source account has read-only Gmail scope, record `trashed_source_email=false` / cleanup error, but do not mark the render/upload as failed.
- For `personal-main / affan.fareed@gmail.com`, Gmail may intentionally be read-only; avoid requiring Gmail modify scope unless the user explicitly changes that policy.
