---
name: parrot-ai-creative-pipeline
description: Use when leveraging the user's paid Parrot AI account for faceless YouTube voice, avatar, image, video, audio, and creative-model workflows while reducing paid API usage elsewhere.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [parrot-ai, faceless-youtube, tts, video-generation, cost-optimization]
    related_skills: [youtube-automation-with-tts]
---

# Parrot AI Creative Pipeline

## Overview

Parrot AI (`https://www.tryparrotai.com`) is available through the user's account and can be used as a semi-automated creative workbench for faceless YouTube production. Treat it as a browser-first provider unless/until a stable API adapter is built.

Primary value: offload experiments and some production assets from paid APIs such as ElevenLabs, Sora/Veo, FAL, Stability, OpenAI image APIs, and standalone music/SFX providers when Parrot credits/subscription access make it cheaper.

Primary login identity observed/provided by user:

- Service URL: `https://www.tryparrotai.com`
- Login method: email/password
- Primary login email / username: `Affan.fareed@gmail.com`

Do **not** store or repeat the user's password in files, skills, logs, or reports. The user provided it in-chat once for browser login, but durable skills/memory/docs must not contain raw secrets. Login is through the browser session only; if the session expires, ask the user to provide/enter the password again or use an approved secret manager/env var that is outside the repo.

## Research-First Source Acquisition and Audio Fallback

When creator-video acquisition is blocked, research the current failure across official documentation, active issue trackers, recent operator forums, and official creator distribution before repeating local retries. Classify player/API rejection separately from media/GVS rejection: a PO-token provider may solve media authorization but cannot necessarily fix an IP/player-level `LOGIN_REQUIRED` gate.

If exact official audio is available, use the documented audio-first fallback: verify the RSS/CDN enclosure, transcribe with word timestamps, select complete transcript-backed moments, and render clearly labeled audio-led vertical clips. For long files on constrained hosts, use chunked CPU transcription with per-chunk checkpoints and bounded concurrency.

Keep user-facing operational reports laconic: status, produced artifacts/URLs, queue count, raw blocker, and next action. Do not repeatedly explain already-established context.

See [`references/source-acquisition-and-audio-fallback.md`](references/source-acquisition-and-audio-fallback.md) for route ordering, verification gates, chunked transcription, FFmpeg waveform composition, and queue semantics.

## Current Account Snapshot

Observed in the logged-in web app:

- Account email is visible in profile.
- Profile has a Stripe customer ID and Manage button.
- Account joined date shown: `12/20/2025`.
- Buy Credits dialog showed **0 credits** balance at the time of inspection.
- Credit packs shown: Starter 100 credits, Creator 500 credits, Pro 1000 credits; dialog says credits never expire.
- Credit History page showed **No transactions yet**.
- Buy modal disclosed rough credit costs: Video Generation ~3 credits/sec, Image Creation ~5 credits each, Voice Cloning ~2 credits/sec, and “200+ More” ~6 credits each.
- Playground JS includes a no-credit message: “You need credits to use this feature. Verify your email to get 5 free credits.”
- The app advertises access to 200+ AI models / 500+ playground models, but the web UI does not currently prove unlimited generation despite the user's belief/account purchase.

Before relying on Parrot for production, verify live generation/export works for the needed tool and check whether subscription/unlimited access bypasses the visible 0-credit balance.

## When to Use

Use this skill when the user asks to:

- Use Parrot AI / Pair AI / tryparrotai.com.
- Generate character-style or celebrity-style narration.
- Create talking avatars from an image.
- Clone or manage custom voices.
- Use Parrot's playground models for image, video, music, SFX, or TTS.
- Reduce costs from other APIs by using an already-paid Parrot account.
- Build a faceless YouTube pipeline with Parrot exports.

Do not use Parrot as the default unattended cron provider until one end-to-end export has been proven reliable and the account has usable credits/subscription access.

## High-Level Feature Inventory

Observed first-party app sections:

1. **Talking Video / AI Voice**
   - Create character/celebrity-style AI voice videos.
   - New create UI has a 500-character text limit.
   - Classic create UI has a 300-character text limit.
   - New UI has an **Audio only** toggle, useful for pipeline voiceover extraction.
   - New UI has a **Remove watermark** toggle for video outputs.
   - Voice library includes premium and community voices.

2. **Clone a Voice / Custom Voices**
   - Create custom celebrity-style voice clones from clean MP3 samples.
   - Sample requirements shown by UI:
     - MP3 format only.
     - One speaker only.
     - Over 20 seconds long.
     - No background noise.
   - Optional cover photo: square headshot image, recommended 500x500px, PNG/JPG up to 10MB.
   - `Publish to public` checkbox defaults checked; turn it off for private/internal voices unless user explicitly wants public.

3. **AI Playground**
   - Advertised as 500+ models.
   - Has model categories: Top, All, Image → Video, Text → Video, Text → Image, Audio, Video → Video, Image → Image.
   - Includes a built-in media upload tool: upload files up to 100MB and get shareable URLs.

4. **Popular tools on dashboard**
   - Voice Changer: audio → audio.
   - Image Generator: text → image.
   - Image Editor: image → image.
   - Image Animator: image → video.
   - Avatar Generator: image → talking video.
   - Viral Effects: image → video.

5. **History**
   - Recent creations are visible.
   - Use History as the fallback retrieval path when a generated result is not directly downloadable from the current create page.

## Playground Model Families Observed

### Image generation / editing

Observed models and tools include:

- Nano Banana 2: text-to-image and image-to-image.
- Nano Banana Pro: text-to-image and image-to-image.
- Nano Banana: text-to-image and image-to-image.
- GPT Image 2 API: text-to-image and image-to-image.
- Grok Imagine Image: text-to-image and image-to-image.
- FLUX.1 [schnell].
- FLUX.1 [dev].
- FLUX.1 [dev] with LoRAs.
- FLUX1.1 [pro].
- FLUX1.1 [pro] ultra.
- FLUX.1 Kontext [pro].
- FLUX 2 Pro Edit.
- Flux 2 Pro.
- FLUX.2 [klein] 9B.
- SeedVR2 image upscaling.
- Bria RMBG 2.0 background removal.
- Birefnet Background Removal V2.
- Bytedance Seedream V4.5 Edit.
- Bytedance Seedream V5 Lite Edit.

Use Parrot image models to offload thumbnail concepts, avatar headshots, background removal, image edits, and image-to-video source frames when credits are cheaper than external image APIs.

### Video / animation

Observed models and tools include:

- Experiment with Sora: Sora 2 text-to-video.
- Video Generator: text-to-video powered by VEO 3.
- Image to video generator: Wan.
- Seedance 2 Image to Video.
- Seedance 2 Reference to Video: up to 9 images, 3 videos, and 3 audio clips, native audio and camera control.
- Kling Video v3 Image to Video [Pro].
- Kling Video v3 Image to Video [Standard].
- Kling Video v2.6 Image to Video.
- Kling Video 2.5 Turbo Pro.
- Happy Horse: 1080p video with synchronized native audio and multilingual lip-sync from text prompts or images.
- PixVerse V6.
- Video Lip Sync.
- Custom Animation.
- Viral Effects.

Use Parrot video tools for special B-roll, image animation, avatar motion, lip-sync, viral effects, and tests that would otherwise spend Sora/Veo/FAL provider credits. For routine newsletter videos, still prefer stock footage first unless AI video is explicitly requested.

### Audio / music / SFX / TTS

Observed audio models include:

- Stable Audio 3 Medium Base Text to Audio: stereo music up to 6 minutes, base checkpoint.
- Stable Audio 3: licensed-data stereo music up to 6 minutes.
- Stable Audio 3 Small Music: full stereo compositions up to 2 minutes.
- Stable Audio 3 Small SFX: sound effects.
- Sonilo V1.1 Text to Music.
- Lyria 3 Pro.
- Mirelo SFX1.6: ambient sounds and loopable soundscapes.
- Stable Audio Open.
- Stable Audio 2.5.
- CassetteAI music generator.
- CassetteAI Sound Effects Generator.
- MMAudio V2 Text to Audio: prompt-described synchronized audio.
- MiniMax Music, MiniMax Music v1.5, MiniMax Music 2.5, MiniMax Music 2.6.
- Lyria2.
- Kokoro TTS, Kokoro TTS British English, Kokoro TTS Brazilian Portuguese.
- F5 TTS.
- ElevenLabs TTS Multilingual v2.
- ElevenLabs Eleven v3 TTS.
- ElevenLabs dialogue / realistic audio dialogue.
- ElevenLabs Sound Effects V2.
- ElevenLabs Music.
- ACE Step Prompt To Audio.
- ACE Step music with lyrics.
- Gemini TTS.

Use Parrot audio tools to offload background music, stingers, transitions, ambient loops, SFX, and possibly commodity TTS. Use ElevenLabs direct API only when quality, automation, or account economics beat Parrot.

## Internal API Findings

No public documented API was found during inspection. The frontend uses internal endpoints and Firebase/AppCheck:

- `/api/create`
- `/api/create-public`
- `/api/create-voice-preview`
- `/api/get-voice-preview`
- `/api/save-voice-preview`

`/api/create` appears to require:

- Firebase authenticated user token in `Authorization: Bearer ...`.
- Firebase AppCheck token in `X-Firebase-AppCheck`.
- JSON payload matching the selected tool/model.

Therefore, production automation should start as authenticated browser automation, not direct HTTP calls. Build a direct adapter only after capturing one successful request/response and a repeatable result URL.

## Everyday Integration Matrix

Use Parrot as a creative-generation layer for any Hermes-built service when it is cheaper than direct APIs and export is reliable.

### AI Voice / Talking Video

- **Everyday use:** narrator voice tests, character-style hooks, short meme/news clips, talking-head inserts.
- **Faceless YouTube:** generate short avatar/persona voice chunks, then concatenate into a full narration track. Use as A/B tests against ElevenLabs/Google TTS.
- **Other workflows:** sales demo explainers, onboarding clips, Discord announcement videos, personalized client intros.
- **Integration path:** browser automation first; save exported audio/video into the project workspace; renderer consumes the local file.

### Voice Changer

- **Everyday use:** transform recorded narration into a consistent host/persona voice.
- **Faceless YouTube:** record or synthesize clean base narration, then run it through Voice Changer for personality.
- **Other workflows:** voice branding for tutorials, product demos, support clips.
- **Integration path:** generate/upload base audio, select target voice, export changed audio, normalize with ffmpeg.

### Custom Voice / Voice Clone

- **Everyday use:** create reusable brand voices from approved clean samples.
- **Faceless YouTube:** build a private house narrator voice instead of paying per-generation elsewhere.
- **Other workflows:** client-specific explainers, internal training voice, recurring newsletter host.
- **Integration path:** upload >20s clean MP3 one-speaker sample, upload 500x500 cover image, uncheck `Publish to public` unless explicitly requested, generate test clips, save voice ID/name in project docs.

### Text/Image Generator

- **Everyday use:** thumbnail concepts, brand avatars, background art, illustrations, social images.
- **Faceless YouTube:** generate thumbnails, avatar headshots, scene stills for image-to-video, channel art.
- **Other workflows:** landing page hero art, ad mockups, product visuals, blog art.
- **Integration path:** prompt → export image → store under `assets/generated/parrot/` with prompt/model metadata.

### Image Editor / Image-to-Image

- **Everyday use:** fix thumbnails, remove/replace backgrounds, adjust style, turn rough assets into polished visuals.
- **Faceless YouTube:** edit host avatar, make consistent scene cards, remove unwanted text/logos from generated images.
- **Other workflows:** client site visuals, social creative variants, presentation graphics.
- **Integration path:** upload source image → edit prompt → export → store original and edited output with metadata.

### Background Removal / Upscaling

- **Everyday use:** isolate subjects, make transparent PNGs, improve low-res assets.
- **Faceless YouTube:** cut out avatar/host figures, improve thumbnail clarity, prepare image-to-video inputs.
- **Other workflows:** ecommerce/product cards, ad creatives, website assets.
- **Integration path:** batch source images when possible; fallback to local/rembg only when Parrot credits are unavailable.

### Image Animator / Image-to-Video

- **Everyday use:** animate stills into short B-roll clips.
- **Faceless YouTube:** animate thumbnails, article art, generated avatars, scene stills, or charts into motion backgrounds.
- **Other workflows:** social reels, website hero loops, ad creatives.
- **Integration path:** generate/choose still image → animate with Wan/Kling/Seedance/PixVerse/etc. → export mp4 → add to visual manifest.

### Text-to-Video / Video Generator

- **Everyday use:** special AI B-roll, ads, cinematic clips, surreal meme inserts.
- **Faceless YouTube:** create high-value clips for important story beats when stock footage is too generic.
- **Other workflows:** marketing demos, concept videos, product announcement loops.
- **Integration path:** use sparingly; record prompt/model/credit cost; mix with stock footage to control cost.

### Talking Avatars / Video Lip Sync

- **Everyday use:** make an image/persona speak a script.
- **Faceless YouTube:** use short intro/outro host shots, not necessarily full-video narration.
- **Other workflows:** onboarding, course lessons, client greetings, explainers.
- **Integration path:** image/avatar + audio/script → generated talking clip → renderer inserts at intro/outro or chapter breaks.

### Viral Effects / Custom Animation

- **Everyday use:** fast social effects and attention-grabbing motion.
- **Faceless YouTube:** hook clips, transitions, meme overlays, short retention boosters.
- **Other workflows:** TikTok/Reels assets, campaign creative, announcements.
- **Integration path:** use for short segments only; avoid overusing effects in serious finance/security/news videos.

### Text-to-Audio / Music / SFX

- **Everyday use:** background music, intros, whooshes, stingers, ambient loops, sound effects.
- **Faceless YouTube:** replace paid music/SFX APIs for channel sound design; generate intro sting and low-volume bed.
- **Other workflows:** game/app SFX, podcast bumpers, ad beds, notification sounds.
- **Integration path:** prompt → export wav/mp3 → loudness normalize → store with license/model metadata → mix under narration.

### Media Upload / Share URLs

- **Everyday use:** temporary hosted files for Parrot model inputs.
- **Faceless YouTube:** upload images/audio/video source assets up to 100MB for model workflows.
- **Other workflows:** share generated client preview assets.
- **Integration path:** avoid using Parrot-hosted URLs as the only copy; always download/save durable copies into the project.

## Unlimited-Access Verification Protocol

The user believes the account has unlimited access. Do not assume this from the UI alone. For each tool family, run one tiny low-risk generation and record:

- tool/model name,
- prompt/input,
- whether it generated with zero credits shown,
- whether it consumed credits,
- output URL/path,
- export/download reliability,
- recommended production use.

Store results in project docs or a `parrot_capability_matrix.json`. If a generation opens a purchase/credits gate, stop and mark it **not currently unlimited from web UI** rather than purchasing credits.

## Cost-Offload Strategy

Use this decision order:

1. **Can stock/free local assets meet the quality bar?**
   - Use stock footage/images first for routine newsletter videos.

2. **Can Parrot generate the asset without extra spend?**
   - If yes, use Parrot before paid external APIs.
   - Especially good candidates: SFX, music beds, avatar clips, special B-roll, image edits, background removal, and short voice tests.

3. **Does Parrot require credits and is the balance usable?**
   - If current balance is 0, do not assume paid/lifetime access covers generation.
   - Ask the user whether to buy/use credits only when a generation requires it.

4. **Is an external API more reliable/cheaper for batch automation?**
   - Keep Google TTS, stock visuals, and direct provider APIs as fallbacks for unattended cron runs.

5. **Does the output need exact repeatability?**
   - Prefer direct APIs for high-volume unattended production.
   - Prefer Parrot for creative experiments and asset generation when browser export is acceptable.

## Faceless YouTube Pipeline Recipe

### Parrot voiceover experiment

1. Generate a charismatic avatar-style script with `youtube-automation-with-tts`.
2. Split narration into chunks under 500 characters for new UI, or 300 for classic UI.
3. Open `https://www.tryparrotai.com/app/create-new`.
4. Select an approved voice/persona.
5. Toggle **Audio only**.
6. Generate the chunk.
7. Capture the output audio URL or download from the result/history.
8. Save files as `parrot_chunk_001.mp3`, `parrot_chunk_002.mp3`, etc.
9. Concatenate with ffmpeg into `voice_parrot.mp3`.
10. Feed `voice_parrot.mp3` into the existing renderer.
11. Smoke-test final video before upload.

### Talking avatar experiment

1. Create or select a host avatar image.
2. Use **Avatar Generator / Create Talking Avatars / Video Lip Sync**.
3. Provide short, high-energy script chunks.
4. Export short clips.
5. Use them as intro/outro/personality inserts, not necessarily full-video footage.

### AI B-roll experiment

1. Create a strong scene prompt from the script beat.
2. Prefer image-to-video when you can control a consistent avatar/visual brand.
3. Test Wan, Seedance, Kling, PixVerse, Happy Horse, Sora/Veo depending on cost and output quality.
4. Save generated media plus prompt/model metadata in `visual_manifest.json`.
5. Use generated clips sparingly with stock B-roll to control cost.

### Music/SFX experiment

1. Use audio models for short intros, whooshes, impact hits, ambient loops, or low-volume background music.
2. Save prompt, model, duration, and resulting file URL/path.
3. Normalize volume before mixing under narration.
4. Avoid copyrighted-sounding requests or direct artist mimicry for public uploads.

## Safety and Platform Notes

Parrot offers celebrity/character-style voices and cloning. For public YouTube:

- Prefer original/parody-inspired descriptions instead of exact protected names in public metadata.
- Do not clone private individuals without explicit consent.
- Avoid deceptive impersonation.
- Do not brand videos as if a celebrity/character endorsed the content.
- Keep internal notes separate from public titles/descriptions.
- For commercial/public use, verify Parrot terms and the selected model/voice restrictions when in doubt.

Safer style prompts:

- `hyper-energetic nautical cartoon tech host`
- `sarcastic animated startup-news narrator`
- `chaotic Saturday-morning-cartoon AI reporter`
- `movie-trailer finance narrator`
- `cybersecurity goblin explaining the breach`

Riskier public framing:

- `SpongeBob reads AI news`
- `Elon Musk endorses this stock`
- `clone this real person without consent`

## Source Acquisition and Audio-First Fallback

For creator clips blocked by YouTube bot/IP attestation, use the internet-first diagnosis, acquisition ladder, official-audio fallback, resumable low-memory transcription, and truthful audio-led rendering workflow in:

- `references/youtube-source-acquisition-audio-fallback.md`

Do not repeatedly mutate yt-dlp flags without researching the current failure class. In particular, distinguish GVS/format 403 failures that may benefit from PO tokens from player API `LOGIN_REQUIRED` failures that occur before media URLs are issued.

## Verification Checklist

Before saying Parrot is integrated:

- [ ] Logged in successfully in browser.
- [ ] Confirmed current credit/subscription state.
- [ ] Generated at least one test asset with the intended tool.
- [ ] Downloaded or captured the resulting media file/URL.
- [ ] Saved the file into the project workspace.
- [ ] Fed the file into the target pipeline.
- [ ] Rendered a short smoke-test video/audio output.
- [ ] Documented model, prompt, voice, and cost/credit usage.

## Live Verification Log

- New AI Voice UI test with a community voice accepted text/voice selection but did not produce a visible media result in the browser run.
- Classic AI Voice test with default Donald voice triggered Firebase AppCheck / reCAPTCHA requests and then stayed on `LOADING...`; no `/api/create` request or downloadable media was observed.
- These tests do **not** prove the account lacks unlimited access; they show the browser automation path is currently blocked/hanging before generation completes. Retry with a fresh browser, app/mobile UI, another model, or direct request capture before marking AI Voice as usable.

## Common Pitfalls

1. **Assuming paid account means usable credits.** The inspected credit dialog showed 0 credits. Always verify live generation before depending on Parrot.

2. **Trying to direct-call internal APIs too early.** Firebase AppCheck and auth tokens make this fragile. Use browser automation first.

3. **Generating long narration in one pass.** The voice UI has 300–500 character limits. Chunk and concatenate.

4. **Leaving custom voice public by accident.** The custom voice form defaults `Publish to public` checked. Turn it off for private/internal voices.

5. **Using direct celebrity/character branding in public YouTube metadata.** Keep exact names internal when testing; use original/persona language publicly.

6. **Letting Parrot replace reliable cheap paths.** For routine newsletter videos, stock footage + Google TTS may still be cheaper and more automatable than credit-based Parrot generations.
