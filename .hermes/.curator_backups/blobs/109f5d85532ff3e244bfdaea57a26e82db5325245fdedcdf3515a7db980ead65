# Viral YouTube system notes — 2026-06

Use for faceless/newsletter YouTube Shorts and similar social-video generation.

## Research-backed operating principles

- YouTube's own guidance treats thumbnail/title as the video billboard: packaging must earn the click, but retention must deliver the promise. Strong CTR with weak retention means the title/thumbnail overpromised or the first section underdelivered.
- Creator Analytics growth loop: watch CTR, audience retention, returning viewers, and traffic source behavior. Retention graph drop-offs should directly shape the next script/opening.
- Shorts growth consensus: first 1-3 seconds decide the swipe; cold seed distribution expands when viewers watch instead of swiping; completion, replay, and average watch time per impression matter more than volume alone.
- Timing studies are cohorts, not rules. For this user's US/Texas audience, test Tue/Wed 12-6 PM CT, weekday lunch 12-3 PM CT, evening 7-9 PM CT, plus weekend YouTube windows. Let Studio analytics override defaults.

## Script formula

1. Cold open in under 12 words. Examples:
   - `Nobody is talking about the real problem with X.`
   - `This looks like X. It is really Y.`
   - `If you only saw the headline, you missed the money.`
2. Promise the viewer a specific insight immediately.
3. No intro/welcome/source disclosure in public copy.
4. One core emotion per video: fear, ambition, status, relief, anger, curiosity, or identity.
5. Beat structure:
   - 0-3s: hook + visual motion/change.
   - 3-10s: context fast.
   - 10-35s: 2-3 receipts/proofs/examples.
   - 35-55s: reversal/implication.
   - Final 3-5s: identity/action close that can loop back to the hook.
6. Prefer identity CTAs over generic CTAs: `Build one proof today`, `Save the signal`, `Move before it becomes obvious`.

## Visual formula

- Change visual state every 2-4 seconds: cut, zoom, caption emphasis, progress bar, or color accent.
- First frame needs readable high-contrast text and relevant human/tech/market imagery.
- Use stock footage first: Pexels/Pixabay video, then photos, then vetted fallback. Text-only/dynamic renders are draft quality unless explicitly approved.
- On-screen headline should be 5-7 words max; body captions should support the narration rather than duplicate every word.
- Title, on-screen text, narration, visual queries, and description should align semantically.

## Packaging rules

- Titles: ~58-70 characters; one curiosity gap; no emoji/control characters.
- Use concrete nouns and stakes: `AI`, `money`, `skills`, `security`, `jobs`, `discipline`, `proof`.
- Description: one-line premise, one-line takeaway, support links, #Shorts. No AI/faceless/newsletter disclosure in public metadata.
- Tags are secondary; keep them aligned to topic intent.

## Quality gate additions

- Scripts compile.
- TTS provider is live: ElevenLabs or Google TTS; local/flite is review-only.
- At least most scenes use external stock/photo/video assets or an approved semantic fallback.
- `ffprobe` confirms vertical 1080x1920 for Shorts/newsletter lane, nonzero audio, and a reasonable duration.
- Upload helper returns dry-run JSON or real `video_id`; source email is trashed only after verified `video_id`.
