# Stock visual provider pattern for faceless newsletter videos

Use this when the user wants better visuals for the faceless YouTube newsletter pipeline.

## Durable user correction

The user likes the voiceover but rejected videos that are mostly text/abstract backgrounds. They want the renderer to understand the script and use visuals behind the captions: company/topic pictures, people working on the topic, office/engineering/security/finance/fitness/stoic footage, and any usable stock footage API assets.

## Provider order

For each script beat, derive a visual search query from the source email subject/body and the generated narration beat. Use this order:

1. Pexels video (`PEXELS_API_KEY`)
2. Pixabay video (`PIXABAY_API_KEY`)
3. Pexels photo (`PEXELS_API_KEY`)
4. Shutterstock preview/licensed video (`SHUTTERSTOCK_TOKEN`; consumer key/secret may be present too)
5. Safe no-key image fallback, e.g. Wikimedia topic images when appropriate
6. Dynamic text/background fallback only as the last resort

Persist a `visual_manifest.json` containing scene number, caption, search query, selected provider, asset path, and provider URL/id. This makes later QA/debugging possible.

## Env var pitfall

Do not confuse Pixabay with Pexels/Pixels.

- Pixabay keys often look like `56299266-...` and come from `pixabay.com/api/docs`; store as `PIXABAY_API_KEY`.
- Pexels keys come from `pexels.com/api`; store as `PEXELS_API_KEY`.
- If `PEXELS_API_KEY` returns HTTP 403, disable/comment it instead of repeatedly trying it; let the pipeline fall through to Pixabay.

When loading `.env`, stock-provider keys should override stale inherited process env values so revoked keys do not delay or poison renders.

## Query construction

Prefer exact subject chunks first, but widen quickly when exact company footage is unavailable:

- `Visa and OpenAI partner company office workers technology`
- `Mastercard launches Agent Pay fintech payment technology office`
- `cybersecurity operations center server room`
- `artificial intelligence engineers working laptop startup office`
- `focused person working laptop city night motivation`
- `morning journaling stoic discipline`
- `gym workout meal prep athletic discipline`

Company-name queries are useful for images, but broad semantic queries often produce better video footage.

## Rendering pattern

- Use a full-frame 9:16 background from the selected visual asset.
- For stock video, loop and crop to 1080x1920.
- For photos, use slow zoom/pan so the scene feels alive.
- Add dark overlay boxes so captions remain readable.
- Keep the user-facing title/description free of production details: never mention API, Pexels, Pixabay, AI-generated, pipeline, source email, or automation.

## Upload rule

Newsletter/source emails are trashed only after YouTube returns a verified `video_id`. If render or upload fails, leave the source email untouched.
