# Faceless newsletter batch upload workflow — 2026-06

Use this when catching up newsletter emails into public faceless YouTube uploads.

## User corrections captured

- The current faceless Daily Stoic lane uploads to **A F** using the explicit fareed320 token. It processes Daily Stoic emails only; other newsletter types stay out of this lane.
- The user corrected the visual-provider requirement: **do not require Higgsfield/Sora** for this lane. Use **Pexels** when `PEXELS_API_KEY` exists; otherwise use the stock/manual/Mixkit-style fallback or dynamic cinematic visuals. Higgsfield auth failure is not a blocker for this workflow.
- Google Cloud TTS is approved as the fallback/equivalent voice path when ElevenLabs credits are low or unavailable. Do not burn the last ElevenLabs free-tier credits on batch catch-up.
- Every newsletter email still needs a solid attention-grabbing/operator-style summary; do not upload generic scripts that ignore the email body.

## Current working script

Batch renderer/uploader:

```bash
cd /opt/data/HeRmEz/projects/faceless-youtube-channel
/opt/hermes/.venv/bin/python scripts/newsletter_batch_upload.py --limit 10
```

Useful flags:

```bash
# Render without upload/trash for QA
/opt/hermes/.venv/bin/python scripts/newsletter_batch_upload.py --limit 1 --no-upload

# Process a specific Gmail message id from personal-secondary
/opt/hermes/.venv/bin/python scripts/newsletter_batch_upload.py --message MESSAGE_ID
```

The script:

1. Discovers source emails in `personal-secondary` from TLDR/Daily Stoic/Kino-style sources, excluding Trash.
2. Builds one video per email.
3. Uses the actual email subject/body/snippet to generate a hook, signal, operator angle, proof, and CTA.
4. Synthesizes voice with Google Cloud TTS (`GOOGLE_APPLICATION_CREDENTIALS` / `GOOGLE_TTS_CREDENTIALS`, default `en-US-Neural2-J`).
5. Renders a 9:16 multi-scene MP4 with audio and attention-grabbing captions.
6. Uploads public through `/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py` using the explicit Trapiistan/Sosai Oyama token `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json`. The legacy `/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json` currently resolves to the same Sosai Oyama channel, but new scripts/docs should prefer the explicit Trapiistan path so account intent is unambiguous.
7. Appends upload/source markers to `UPLOADS/newsletter_youtube_uploads.jsonl`.
8. Trashes the Gmail source only after YouTube returns a verified `video_id`.

## Script-flow correction

The user liked the direction of the uploaded faceless newsletter videos but corrected the script style: scripts must **flow naturally** like one short-form story, not sound like disconnected lecture cards or rigid headings. Keep punchy caption labels if useful, but voiceover needs conversational transitions and a clear narrative arc.

Use this voiceover pattern:

1. Hook immediately with the strongest/strangest part of the newsletter.
2. Continue with natural transitions that sound spoken, not templated: “That’s where it gets interesting…”, “The part people miss is…”, “Then the receipts start stacking up…”.
3. Add humor only when appropriate for the topic.
4. Match the newsletter tone/category rather than forcing the same generic operator voice.
5. Use actual newsletter facts as receipts and strip citation artifacts (`[4]`, “HEADLINES & TRENDS”, emoji boxes, source mechanics) from narration.
6. Avoid formulaic spoken labels such as “the signal,” “operator angle,” “move first,” “intro/body/conclusion,” or generic morals like “build one proof today” unless the source itself says them.
7. If the generated narration sounds like headings stitched together, rewrite before rendering/uploading.
8. Before a batch upload after script changes, run at least one `--no-upload` smoke render to catch Gmail auth, TTS, script, or visual issues before public publishing.

Project detail/reference doc: `/opt/data/HeRmEz/projects/faceless-youtube-channel/docs/newsletter-script-style-guide.md`.

## OAuth/channel notes

Reauth callbacks are exchanged with:

```bash
export OAUTHLIB_INSECURE_TRANSPORT=1
/opt/hermes/.venv/bin/python /opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py \
  --client-secret /opt/data/secrets/faceless-youtube-channel/youtube_client_secret.json \
  --token /opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json \
  --pending /opt/data/secrets/faceless-youtube-channel/youtube_oauth_pending.json \
  exchange 'http://localhost:5000/?state=...&code=...&scope=...'
```

Verify identity after exchange with `channels().list(mine=true)`. Current accepted result for the faceless lane is **Sosai Oyama** (`UCsxzQlusqwmMUdjMvKAJDfA`).

Required YouTube scopes for this lane:

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

## Pitfalls

- Run the batch script with `/opt/hermes/.venv/bin/python`; system `python3` may not have Google libraries.
- Do not use the shared uploader default token for faceless uploads. Pass the faceless token explicitly or use the patched faceless scripts.
- Do not treat missing Higgsfield auth as a blocker for this workflow.
- Do not trash source emails until upload succeeds and a `video_id` exists.
- If YouTube quota/upload limits appear, stop the batch and resume after reset rather than trashing pending source emails.
