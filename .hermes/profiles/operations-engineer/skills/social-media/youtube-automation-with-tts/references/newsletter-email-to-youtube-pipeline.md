# Newsletter email → faceless YouTube pipeline

Use when the user asks to turn Gmail newsletters (TLDR, Daily Stoic, Kino Body, similar source emails) into faceless YouTube videos and then clean up the source emails.

For the current channel quality bar, also load `references/faceless-newsletter-quality-gate.md`. The key correction is: **one email = one video**, actual newsletter content must drive the video, and uploadable outputs require realistic voiceover plus relevant stock/API visuals. Prefer per-beat stock footage/photos over AI-video-only gating: Pexels/Pixabay/Shutterstock-backed visuals are acceptable when matched to the script topic.

## Proven workflow

1. **Audit source emails first**
   - Use profile-scoped Google tokens under `/opt/data/google_profiles/<profile>/google_token.json` when available.
   - Treat TLDR from `personal-secondary` / `fareed320@gmail.com` as the preferred TLDR source.
   - Treat Daily Stoic and Kino Body as source-worthy: summarize/use before deleting.
   - Keep priority/security/billing messages out of bulk cleanup.
   - When the user names a specific newsletter class (for example, “make a Daily Stoic video”), do **source-specific discovery first** rather than running the mixed newsletter batch queue. Search the approved Gmail profiles for that sender, select the newest eligible unprocessed message, inspect its subject/date, and pass its explicit Gmail message ID to the renderer. This prevents an earlier TLDR/Kino result from taking precedence merely because of batch query ordering.
   - For Daily Stoic, search `from:info@dailystoic.com -in:trash` across `personal-secondary` first and then `personal-main`; prefer the newest eligible message unless the user identifies a particular issue. Render with an explicit command such as `newsletter_batch_upload.py --profile personal-secondary --message <gmail_id>`.

2. **Generate one real video per email — quality bar**
   - Each source email gets its **own** video. Do not combine multiple newsletters into one generic upload.
   - Use the actual email content from TLDR, Daily Stoic, Kino Body, etc.; do not replace it with a generic trend/self-improvement script.
   - Store artifacts under `/opt/data/HeRmEz/projects/faceless-youtube-channel/videos/<timestamp-slug>/`.
   - Preserve non-secret source metadata in `source_email.json` or equivalent: profile, message id, sender, subject, date, excerpt.
   - Required style: motivational faceless-video vibe — cinematic, emotionally paced, high-contrast, relevant B-roll, punchy captions, realistic ElevenLabs narration.
   - Required assets: realistic voiceover (ElevenLabs preferred when credits are healthy; Google Cloud TTS approved for the current faceless catch-up lane) plus relevant visuals for the email's specific topic. Prefer real stock footage/photos from APIs over abstract slides: derive per-beat visual queries from the source subject/body/script, fetch Pexels/Pixabay assets when keys are configured, and save a `visual_manifest.json` for QA. Static text-slide videos are not acceptable for the faceless channel.
   - Public YouTube metadata must hide production details: never mention AI-generated, faceless automation, ElevenLabs, source email/profile, pipeline, or similar behind-the-scenes wording.
   - Reword the email idea in the user's voice for title/description. Include the configured public support links (Linktree, Buy Me a Coffee, Cash App, Venmo); add affiliate links later only after the user likes the videos.
   - If no AI video/B-roll provider is configured, create a script/storyboard only and do **not** upload a low-quality placeholder.

3. **Upload with the shared uploader**
   - Use `/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py`.
   - Log uploads to a JSONL file under the project, e.g. `UPLOADS/newsletter_youtube_uploads.jsonl`.
   - Capture the returned `video_id` and URL; this is the verification handle.

4. **Delete/trash source emails only after verified upload**
   - Only trash newsletter/source email after YouTube returns a `video_id`.
   - Verify Gmail labels show `TRASH` if reporting deletion/trash completion.
   - If upload fails, leave the source email untouched.

## YouTube metadata pitfall

YouTube can reject descriptions containing emoji/control-ish Unicode with `invalidDescription`. Sanitize titles/descriptions to printable ASCII or a conservative safe character set before upload, while keeping full source metadata locally.

## User-specific policy

- Known junk/spam cleanup may run without per-item review.
- Newsletter/source emails are different: delete only after the newsletter was used and the upload was verified.
- Use concise Discord reporting: bullets with uploaded URLs, source profile/message id, and trash verification.
