# Faceless newsletter video quality gate

Use this reference when turning TLDR, Daily Stoic, Kino Body, or similar Gmail newsletters into videos for the user's faceless YouTube channel.

## Corrections captured from user feedback

The user rejected generic static/text-slide uploads and metadata that exposes the production method. The channel standard is:

- **One email = one video.** Do not combine newsletters and do not make a generic trend clip from several signals.
- **Use the actual newsletter content.** Subject, body, and core points must drive the script, b-roll prompts, captions, and public description.
- **Motivational-video vibe.** Cinematic pacing, emotional narration, relevant high-contrast b-roll, punchy captions, and a clear personal/operator takeaway.
- **Realistic voice required.** Prefer ElevenLabs when credits are healthy; Google Cloud TTS (`en-US-Neural2-J` default) is approved as equivalent/fallback for the current faceless newsletter catch-up lane. Do not upload robotic/flite fallback audio as final channel content.
- **Relevant visuals required.** Prefer Pexels stock clips/images; use the approved stock/manual/Mixkit-style or dynamic cinematic visual fallback when Pexels is unavailable. Higgsfield/Sora auth failure is not a blocker for the current faceless newsletter catch-up lane.
- **Public metadata must hide production details.** Titles/descriptions/tags must not say AI-generated, automation, faceless, ElevenLabs, source email/profile, pipeline, or similar behind-the-scenes wording.
- **Descriptions should sound like the user.** Reword the email's idea naturally and opinionatedly; do not disclose the newsletter source mechanics.
- **Support links belong in descriptions.** Include the user's configured public URLs: Linktree, Buy Me a Coffee, Cash App, Venmo. Affiliate links come later only after the user approves video quality.

## Visual quality correction: stock footage over abstract slides

The user explicitly corrected that faceless newsletter videos should not rely on Higgsfield-only, black/static, or mostly abstract text visuals. Keep the voiceover, but make the video visually informative: understand the script, then show relevant background footage/photos of the company, product category, people working with the topic, security/finance/AI/fitness context, or other stock assets that reinforce the narration.

Implementation standard:

- Generate per-scene visual queries from the actual newsletter subject/body and script beats.
- Prefer real stock footage APIs: Pexels video first, Pixabay video second, Pexels photos third, Shutterstock preview/licensed video if configured, then other safe image fallback.
- Use topic/company phrases where useful, but fall back to broad semantic queries (`engineers working on AI`, `payment technology office`, `cybersecurity operations center`, `gym discipline`, `morning journaling`) when exact company footage is unavailable.
- Treat `PIXABAY_API_KEY` as the Pixabay env var. Do not confuse Pixabay with Pexels/Pixels: a key shaped like `56299266-...` from `pixabay.com/api/docs` belongs in `PIXABAY_API_KEY`, not `PEXELS_API_KEY`. If a stale `PEXELS_API_KEY` returns 403, disable it and let the renderer fall through to Pixabay.
- Render stock videos looped/cropped to 9:16; render photos with slow zoom/pan and dark overlays for legible captions.
- Save a `visual_manifest.json` recording scene, query, provider, source URL, and asset path for QA.
- Do not call the video ready if the manifest shows only fallback_dynamic unless the user explicitly accepts a draft.

## Script style correction — viral story, not lecture

The user liked the video direction but corrected the scripts twice: fixed beats still sound too structured. Scripts must feel like a charismatic avatar/personality sharing news as a compelling mini-story, not an intro/body/conclusion outline.

Use these principles:

- Start with the strongest hook immediately, like “wait, did you see this?”
- Keep one clear core message per email/video.
- Build a natural story arc with stakes, curiosity, twist, receipts, and a practical takeaway, but do **not** make the spoken narration sound sectioned.
- Match tone by source/topic: AI/tech can be witty and curious, security should be urgent/practical, finance should follow the money, Stoic/fitness should feel motivational but grounded.
- Use humor only when appropriate and never trivialize real harm/security incidents.
- Avoid robotic narration headings such as “the signal,” “operator angle,” “move first,” or “in conclusion.” Captions can be punchy, but voiceover must sound like one continuous human monologue.
- Use actual newsletter body facts as receipts, not generic filler.
- Increase visual variety: use 8–10 distinct scenes when possible, derive varied queries from company/category/mood, mix stock footage/photos, and avoid reusing the same generic office/laptop clips. Keep a visual URL history.
- Parrot AI may be explored for voice experiments if it has an API/export path, but public content should use original/parody-inspired personas rather than exact impersonations of celebrities or protected entertainment characters.

Project doc: `/opt/data/HeRmEz/projects/faceless-youtube-channel/docs/newsletter-script-style-guide.md`.

## Public metadata pattern

```text
<Reworded idea from the email in the user's voice.>

My read: <strong opinion / practical takeaway>. Build one proof today.

More from me: https://linktr.ee/sosai.oyama
Support the channel: https://buymeacoffee.com/affanfareev
Cash App: https://cash.app/$sosaioyama
Venmo: https://venmo.com/u/SosaiOyama

#Shorts
```

Avoid:

- "AI-generated"
- "faceless automation"
- "ElevenLabs"
- "generated from newsletter"
- "source profile" / "source email"
- "pipeline" / bot wording

## Implementation pitfall

Do not confuse a gate with a working renderer. It is not enough for code to check that provider keys exist and then proceed to render text slides or flite audio. The upload path must actually produce and use realistic voiceover plus relevant B-roll clips. If either generation step fails, the correct output is a storyboard package only, with no upload and no source-email trash.

## Quality gate before upload

A final video may be uploaded only if all are true:

1. The video is based on exactly one source email.
2. The actual email content is visible in the hook, narration, captions, and b-roll prompts.
3. Voiceover is realistic ElevenLabs or equivalent quality.
4. B-roll is relevant to the email's topic and not a static text placeholder.
5. **Classical Echos faceless newsletter videos should be about 2 minutes long** (target ~120 seconds, minimum 110 seconds) unless the user explicitly requests a shorter Short.
6. **Use multiple relevant stock clips/images matched to script beats**; do not upload a one-clip video, black/static fallback, or decorative text-only background. For newsletter videos, derive visual search queries from the actual script/email topic (company names, products, security issue, finance/payment rail, Stoic/fitness theme) and fetch assets through stock APIs when available: Pexels video → Pixabay video → Pexels photo → reputable no-key image fallback → dynamic text fallback only as a last resort. A normal render should use distinct relevant visual segments per beat and preserve a `visual_manifest.json` with provider/query/asset metadata.
7. Metadata hides production details and includes the user's support links.
8. The final MP4 is 9:16, plays with audio, and passes a quick local probe.
9. Source Gmail message is trashed only after YouTube returns a verified `video_id`.
