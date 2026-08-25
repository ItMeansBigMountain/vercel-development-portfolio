---
name: youtube-automation-with-tts
title: YouTube Automation with ElevenLabs TTS
author: ItMeansBigMountain
description: Automated faceless YouTube video generation with professional voice-overs
version: 1.0
category: social-media
tags: ["youtube", "automation", "tts", "elevenlabs", "faceless-channel"]
---

## Overview
Automated YouTube video creation pipeline with ElevenLabs/Google TTS voice-over integration for faceless channels and viral radar content. Ensures professional-quality narration, truthful metadata, source attribution, durable queue semantics, and verified uploads.

## Viral Clip Radar source acquisition and review

For creator-clip jobs, load `references/source-acquisition-and-manifest-review.md`. It defines queue-vs-never-rendered semantics, the bounded acquisition ladder, zero-byte placeholder protection, exact-source search discipline, and the mandatory review gate for auto-generated windows/titles. In particular, do not retry identical cloud-IP bot-check failures unchanged and do not treat generic auto-spaced manifests as reviewed clips.

When acquisition hits YouTube bot confirmation, HTTP 400/403, login-required, or PO-token failures, also load `references/internet-first-youtube-acquisition-troubleshooting.md`. Research current official docs, issue trackers, and operator reports before retrying; verify that yt-dlp discovers both its PO-token provider and JavaScript challenge runtime. A healthy helper server alone does not prove the downloader environment has the provider plugin wired.

Require script-matched visuals on all faceless/newsletter videos.

**Stock visual reference:** see `references/stock-visual-provider-pattern.md` for the current faceless newsletter visual standard: derive per-beat search queries from the script, prefer Pexels/Pixabay/Shutterstock stock footage/photos, and avoid text-only backgrounds.

For newsletter-driven videos (TLDR, Daily Stoic, Kino Body, Robinhood Snacks, similar), follow `references/faceless-newsletter-quality-gate.md`: **one email = one video**, use the actual email content, require realistic ElevenLabs narration plus relevant Pexels stock footage/images or Hugging Face visuals, and upload public by default unless the user explicitly requests private/unlisted review mode.

For the user's Hermes-level email sorting agent, Gmail source labels/folders, the `EllevenLabsKey` env alias, and the dark monochrome particle-video visual direction from the user's screenshots, follow `references/email-sorting-agent-and-particle-video-style.md`.

For the current faceless newsletter pipeline, use **Pexels stock footage/images first** and **stock/manual fallback clips such as Mixkit-style sources next**. Higgsfield/Sora/text-to-video is not a hard requirement and must not block production when stock visuals are available. Only use Sora/Higgsfield/Hugging Face visuals if explicitly requested or needed for a special video; see `references/google-tts-and-stock-visual-fallbacks-2026-06.md`.

For stock/API visual selection and QA, also follow `references/stock-visuals-for-faceless-newsletters.md`: derive per-scene visual queries from the actual script/email topic, prefer Pexels/Pixabay footage/photos, use Shutterstock previews only according to the account/license state, save `visual_manifest.json`, and treat all-dynamic/text fallback renders as draft quality unless explicitly approved.

For YouTube OAuth, channel-token selection, public/default upload behavior, and account-specific content rules, follow `references/youtube-oauth-metadata-cleanup.md`, `references/content-creation-account-and-upload-rules-2026-06.md`, `references/google-tts-stock-youtube-oauth-fallbacks-2026-06.md`, and `references/google-oauth-project-and-scope-isolation.md`. The last references capture Google TTS fallback, stock-visual gate, OAuth channel-identity verification, Google Cloud project/client mismatch, and why Workspace/Gmail scopes must stay separate from YouTube upload scopes.

For the user's current content-creation system, account mapping, upload visibility, calendar/cron contract, and faceless-vs-Viral-Clip-Radar boundaries, follow `references/content-creation-account-and-upload-rules-2026-06.md`: **Viral Radar is higher priority than faceless YouTube/newsletter videos** when scheduling jobs, retrying queues, or allocating upload/rate-limit capacity. If there is a Viral Radar queue/backlog of videos to clip or queued clips to upload, finish uploading all of them using configured failovers until the queue is empty or a real blocker/rate-limit is reached. Faceless/Daily Stoic videos upload to **A F** using `/opt/data/secrets/youtube-fareed320/youtube_upload_token.json`, expected channel `UCX_nUA3Yr9VR884DNanyMYA`. Viral Radar tries Classical Echos first (`/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json`, channel `UCcIpxiU2CLEsBdHcc7_lcyA`), fails over to Trapiistan/Sosai (`UCsxzQlusqwmMUdjMvKAJDfA`), then A F. Do not trust inherited `YOUTUBE_UPLOAD_TOKEN` values; pass fixed lane tokens and expected channel IDs. Use public uploads by default and do not add stock footage to clipping videos.

For the user's latest faceless-channel script correction, follow `references/faceless-younger-audience-script-style-2026-06.md`: keep critical data, but rewrite it for younger viewers with a fast hook, plain language, relatable stakes, short sentences, and "smart friend" energy instead of expert/professional/technical narration.

For OpenAI Sora as the preferred AI B-roll/video backend, follow `references/openai-sora-video-gen-provider.md`: ChatGPT UI access is not enough for cron automation; configure a Hermes `video_gen` provider (`openai-sora`) with `OPENAI_API_KEY` Videos/Sora API access, and treat Higgsfield/FAL/etc. as fallbacks.

For Google Cloud Text-to-Speech as the production fallback when ElevenLabs credits are low/exhausted, follow `references/google-cloud-tts-fallback.md`: verify the API with a live `text:synthesize` call, use `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_TTS_CREDENTIALS`, default to `en-US-Neural2-J`, and keep local `flite`/edge-style narration review-only unless the user explicitly approves it.

For auditing/rebuilding the user's faceless/newsletter pipeline after quality issues, follow `references/faceless-youtube-audit-lessons-2026-06.md`: key presence is not readiness; provider checks must be live where possible; renderer must actually generate realistic voice + relevant B-roll; otherwise stop at storyboard-only and keep upload crons paused.

For hands-on Classical Echos/newsletter backlog operations, follow `references/newsletter-video-ops-lessons-2026-06.md`: no Markdown tables in Discord reports, target ~2-minute multi-clip videos, separate review fallback renders from final ElevenLabs uploads, search labeled newsletters outside Inbox, use Mixkit-style fallback only with source manifests, and handle YouTube `uploadLimitExceeded` with pending manifests plus resume jobs.

For the current faceless newsletter catch-up lane, follow `references/faceless-newsletter-batch-upload-2026-06.md`: Google TTS is an approved fallback/equivalent when ElevenLabs credits are low, Higgsfield/Sora auth is not required, use Pexels or stock/dynamic visual fallback, upload with the explicit **A F/fareed320** token and expected channel ID, and trash each source email only after a verified YouTube `video_id`.

For the user's corrected script/visual/voice direction, follow `references/faceless-newsletter-avatar-storytelling-and-parrot.md`: scripts must sound like a charismatic avatar naturally sharing a compelling news story (not intro/body/conclusion), videos need broader varied stock footage with reuse avoidance, and Parrot AI is a semi-automated voice experiment path using browser/session export until a stable API/export workflow is proven.

For the user's sharper 2026-06 script-quality correction, follow `references/catchy-natural-newsletter-scripting-2026-06.md`: each newsletter script must be catchy, natural, grounded in actual email facts, and must avoid rigid section labels, generic advice, repeated catchphrases, and spoken captions. For the latest newsletter-specific script correction — catchy, natural monologue, no rigid operator-outline phrases, topic-specific voice packs, and captions separate from TTS — also follow `references/newsletter-natural-script-upgrade-2026-06.md`.

For the successful backlog upload pattern and the latest user correction on natural monologue flow plus semantically aligned multi-asset visuals, follow `references/newsletter-batch-upload-natural-storytelling-and-retry-2026-06.md`: process one email per topic/story, use multiple relevant background assets matched to each beat, retry transient Google TTS 429/5xx with backoff, verify upload IDs before trashing source emails, and re-run discovery until no eligible newsletter emails remain. Additional correction: if a Gmail source is already processed, trash that source email instead of silently skipping it; include topic types for fitness and martial arts; captions are display-only and must never be included in the spoken TTS text; choose an internal famous-actor-style narrator archetype from the email tone/topic, without cloning or claiming celebrity endorsement; require a real stock/API visual per scene and block for review if all providers/fallbacks fail.

For regenerating bad newsletter uploads after narration drift, follow `references/newsletter-grounded-replacement-workflow-2026-06.md`: the script must relay the newsletter's facts in a personified human voice, not insert the assistant's advice/opinion; ban phrases like "build one proof today" and "My read:"; use short proven stock queries instead of long sentence-like API queries; log replacement mappings with `replacement_for`.

For replaying stopped/failed social-video jobs, preventing duplicate newsletter uploads, respecting the user's no-paid-clipping-provider choice, and handling Viral Radar `blocked_source` correctly, follow `references/social-video-recovery-and-source-policy-2026-06.md`.

For the current viral packaging standard, read `/opt/data/HeRmEz/projects/faceless-youtube-channel/VIRAL_YOUTUBE_SYSTEM.md` before rendering or uploading faceless/newsletter videos.

For Stoic/Daily Stoic affiliate offers and existing-video description migrations, follow `references/stoic-affiliate-description-and-metadata-updates.md`: distinguish direct product links from owner-attributed commission links, put a conspicuous disclosure at the top, verify the expected channel, and prove metadata-edit permission with a live `videos.update` plus read-back rather than trusting scopes serialized in the token file.

For Classical Echos newsletter-video rendering after the user's 2-minute quality correction, follow `references/newsletter-video-rendering-provider-fallbacks-2026-06.md`: target ~120 seconds, require multiple relevant visual clips, use Mixkit as a vetted stock fallback when Pexels is blocked, and treat edge-tts as review-only unless explicitly approved.

For Google TTS fallback and the user's corrected stock-visual workflow, follow `references/google-tts-and-stock-visual-fallbacks-2026-06.md`: Pexels/stock fallback is the intended visual path; Higgsfield/Sora auth must not block stock-first newsletter videos, and ElevenLabs should be skipped when low credits would be burned by smoke tests.

For Google Cloud TTS fallback and stock-visual quality-gate rules, follow `references/google-tts-and-stock-visual-fallbacks-2026-06.md`: ElevenLabs is preferred but must be skipped when credits are low, Google TTS is the production fallback, and Higgsfield/Sora/AI-video auth must not block newsletter videos when Pexels or vetted stock fallback visuals are available.

## Triggers
- Manual request: "Generate YouTube video about [topic]"
- Batch processing: "Create 10 videos for my YouTube channel"
- Social media upload: "Upload to YouTube/Instagram/TikTok"

## Configuration Requirements

For scheduled/cron runs, load `social-video-cron-growth-loop` and apply its `references/viral-youtube-system-2026.md` guidance: first 1-3s hook, hook→context→receipts→implication→identity/action close, short captions, visual state changes every 2-4s, and semantic alignment between title/on-screen text/narration/description.

For the user's newsletter-driven faceless channel, also load `references/faceless-newsletter-quality-gate.md`. That reference captures the current bar: one real video per newsletter email, actual TLDR/Daily Stoic/Kino Body content, realistic voiceover, relevant AI B-roll, motivational pacing, and public metadata that does **not** disclose AI/faceless automation.

### Visual provider priority

For this user's newsletter/faceless pipeline, use live-probed stock APIs before any AI-video dependency. Prefer **Pexels** when `PEXELS_API_KEY` is active, but **Pixabay** (`PIXABAY_API_KEY`) is fully approved as the current primary when Pexels is missing/403. Then use Pexels photos, Shutterstock preview/search coverage as license-appropriate, Storyblocks only after HMAC signing is wired, and finally vetted no-key stock/image fallbacks. Do **not** require Higgsfield/Sora/AI-video auth for the normal stock-footage path. Use Hugging Face or other AI visuals only as an optional fallback when stock footage cannot satisfy the quality gate. Sora/text-to-video is not the default because of cost; only use it if explicitly requested for a special video.

```yaml
visuals:
  primary_when_active: pexels
  current_free_stock_primary: pixabay
  photo_fallback: pexels_photos
  preview_search_fallback: shutterstock_preview_video
  needs_hmac_before_ready: storyblocks
  final_fallback: vetted_no_key_stock_or_dynamic_draft
  optional_ai_fallback: huggingface
  avoid_by_default: sora
  not_required_for_standard_path: higgsfield
```

Keep Viral-Clip Radar separate: it clips creator long-form source videos into 9:16 captioned shorts and does **not** need stock footage by default. For YouTube source acquisition failures, follow `references/youtube-source-acquisition-first-aid-2026-06.md`: before paid clipping APIs, update/harden the current downloader, try multiple yt-dlp clients plus bgutil/PO-token support when allowed, accept cookies/proxy env vars, and only then escalate to local/Drive MP4 source or external providers if the user wants that route. If the user explicitly says **not** to use yt-dlp or asks for another Python package, respect that immediately: skip yt-dlp retries and use the Python-only ladder (`pytubefix` clients, then interactive `pytubefix` OAuth device flow, then `pytube`/`innertube` classification) before reporting that the remaining blocker is IP/session-level. If the user says not to use clipping-provider keys, follow `references/social-video-recovery-and-source-policy-2026-06.md`: disable external-provider fallback by default and report `blocked_source` with cookies/proxy/local-source options instead of repeating missing provider-key blockers. Current user-specific update: Opus Clips is explicitly scrapped; prefer the no-Opus ladder of yt-dlp when allowed + pytubefix + plain pytube + official creator repost search before any non-Opus provider. For manual YouTube URL clip/upload requests where a manifest exists but source acquisition is blocked, follow `references/manual-youtube-clip-source-blocker-workflow.md`: verify manifest/source/export/upload-log state, try cookies + Python fallbacks + provider preflight once, then report concrete unblockers (local MP4, fresh cookies, residential proxy, configured non-Opus provider) instead of looping on the same downloader failure.
```yaml
elevenlabs:
  api_key_env: "EllevenLabsKey"  # also accept ELEVENLABS_API_KEY, XI_API_KEY, ELEVEN_API_KEY
  voice_id: "CwhRBWXzGAHq8TQ4Fs17"  # Roger - free-tier friendly fallback
  model: "eleven_flash_v2_5"

google_tts_fallback:
  credentials_env: "GOOGLE_APPLICATION_CREDENTIALS"  # or GOOGLE_TTS_CREDENTIALS
  language: "en-US"
  voice: "en-US-Neural2-J"
  speaking_rate: 1.0
```

Always run live TTS probes before upload; key presence alone is not readiness. For 401/402/auth/scope/voice issues, follow `references/elevenlabs-auth-and-free-tier-probe.md`: use the exact `xi-api-key` header, prefer `EllevenLabsKey` before legacy env aliases, probe `/v1/user` and `/v1/user/subscription`, and fall back to a verified free-tier voice/model before declaring the key broken. If ElevenLabs is exhausted, use the Google Cloud TTS fallback in `references/google-cloud-tts-fallback.md` instead of blocking on ElevenLabs alone.

## Script Templates
```yaml
motivational_script:
  intro_hook: "Montage of {content_type} training..."
  content_bridge: "This is where {various} clips will be..."
  outro_motivator: "Final cinematic shots with {goal}..."

viral_radar_script:
  hook: "Breaking news: {viral_topic}"
  explanation: "What you need to know about {topic}"
  call_to_action: "Subscribe for more viral updates"
```

## Execution Flow
1. **Content Analysis**
   - Parse user request for topic/theme
   - For newsletter/email-driven videos, follow `references/newsletter-email-to-youtube-pipeline.md` and `references/faceless-newsletter-quality-gate.md`: audit source emails, make **one video per email**, use the actual newsletter content, generate relevant B-roll/voiceover, upload only after the quality gate passes, then trash the source email only after YouTube returns a verified `video_id`.
   - For scheduled/cron runs, load `social-video-cron-growth-loop` and run the metrics monitor before choosing the next topic.
   - Identify appropriate B-roll terminology
   - Generate script based on video type

2. **Voice-Over Generation**
   - Prefer ElevenLabs when live subscription/character checks show enough credits.
   - Use the REST header `xi-api-key`, not `Authorization: Bearer`, for ElevenLabs.
   ### Voice-Over Generation
      ```python
      def generate_elevenlabs_tts(script, voice_id="CwhRBWXzGAHq8TQ4Fs17", api_key="YOUR_KEY"):
          # ElevenLabs REST auth uses xi-api-key, not Authorization: Bearer.
          headers = {"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"}
          response = requests.post(
              f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
              headers=headers,
              json={
                  "text": script,
                  "model_id": "eleven_flash_v2_5",
                  "voice_settings": {
                      "stability": 0.42,
                      "similarity_boost": 0.75
                  }
              },
              timeout=60,
          )
          response.raise_for_status()
          return response.content
      ```
      When ElevenLabs credits are low or unavailable, use the Google TTS fallback described in `references/google-tts-stock-youtube-oauth-fallbacks-2026-06.md` before falling back to local review-only voices.
       response.raise_for_status()
       return response.content
   ```

3. **Video Assembly**
   - Generate B-roll using stock footage libraries
   - Apply voice-over to timeline
   - Add transitions and effects
   - Export final video

4. **Upload Pipeline**
   - YouTube API integration
   - Title/description optimization
   - Thumbnail generation
   - Cross-platform posting
   - If editing existing YouTube metadata, first verify the OAuth token owns the target channel; `youtube.upload` alone is insufficient for metadata updates, and wrong-channel tokens return `403 forbidden`.
   - If Google consent shows `deleted_client`, switch to a current OAuth client secret and regenerate the auth URL instead of retrying the stale URL.

## B-Roll Terminology Mapping
- Motivational: "motivational B-roll", "cinematic stock footage"
- Success: "success montage clips", "inspirational stock video"
- Lifestyle: "lifestyle B-roll footage"
- Training: "athlete training", "gym footage"

## Quality Control
- Script review for emotional impact
- Voice-over validation
- Content licensing compliance
- Platform optimization
- For viral Shorts/newsletter videos, enforce a packaging gate before upload: first 1-3 seconds contain a specific curiosity hook, no channel intro, visual state changes every 2-4 seconds, title/on-screen text/description align semantically, and `ffprobe` confirms expected orientation, duration, and audio.
- For the user's faceless newsletter channel, run the `faceless-newsletter-quality-gate` reference before upload: no static text-slide placeholders, no generic filler script, one email per video, relevant AI/stock B-roll, realistic voiceover, and no public disclosure of AI/faceless automation in metadata.
- Narration should feel like one natural charismatic story around the newsletter topic, not a rigid intro/body/conclusion. Use facts as the actual core of the video, not as loose receipts for the assistant's own take. Do not add generic advice, self-improvement morals, or unrelated opinions unless the source newsletter itself says them.
- Retention correction: never stitch newsletter sentences together with repeated synthetic transitions such as “this one lands quietly,” “the reason it works is simple,” “then the email,” “what makes it hit harder,” or “by the end.” Open with a specific character + conflict/reversal in the first sentence, then use hook → concrete scene → escalating proof → reversal → payoff. Create a genuine open loop and close it. Captions must be topic-specific, not generic labels such as “THE SIGNAL” or “THE RECEIPT.” Keep individual spoken beats short enough to sound conversational.
- TTS/render safety: probe every scene’s audio duration against its word count; retry/fallback when a provider returns long silence or corrupt timing. Re-encode concatenated scenes to reset timestamps, and block public upload when final duration/orientation/audio gates fail—never continue after merely logging a warning.
- For the user's faceless YouTube channel, scripts must grab a younger audience first. Avoid sounding like an expert briefing, analyst memo, or professional lecture. Keep the critical data, but translate it into punchy, simple, emotionally clear language: fast hook, short sentences, relatable stakes, light slang when natural, and one idea at a time. If a concept is technical, explain it like a smart friend telling you why it matters, not like a consultant presenting findings.
- Visuals must be semantically aligned with the current spoken beat; use multiple distinct background videos/images and inspect/preserve the visual manifest when QAing. Random generic office/laptop footage is not enough.
- YouTube metadata validation: strip emoji/control-ish Unicode from upload title/description if the API returns `invalidDescription`; keep richer source metadata locally.
- Public metadata should reword the email idea in the user's voice and include configured support URLs. When the user approves affiliate marketing, keep the offer block content-specific, place it at the top with a conspicuous disclosure, and use owner-attributed tracking URLs; direct product links are marketing fallbacks and must not be described as commission-bearing for the user.
- For email/newsletter sources, verify upload with a returned YouTube `video_id` before trashing the Gmail message.
- For the user's faceless newsletter channel, load `references/faceless-newsletter-quality-gate.md` before scripting/rendering/uploading. Key corrections: one email = one video; actual TLDR/Daily Stoic/Kino Body content drives the video; public metadata must hide AI/faceless/automation/source-email details; descriptions include the user's support URLs.

## Example Usage
```bash
# Faceless motivational video
hermes --skill youtube-automation-with-tts --topic "fitness motivation"

# Viral radar clip
hermes --skill youtube-automation-with-tts --type viral-radar --topic "latest tech trends"

# Batch generation
hermes --skill youtube-automation-with-tts --batch --count 10
```

## Output Files
- `[topic]_voiceover.mp3` - Generated audio track
- `[topic]_video.mp4` - Final assembled video
- `[topic]_metadata.json` - YouTube optimization data
- `[topic]_thumbnails/` - Thumbnail variations
- `[topic]_assets/` - License documentation