# Stock visuals for faceless newsletter videos

Use this when the faceless newsletter video renderer needs better visuals than text/gradient slides.

## User correction

The user likes the voiceover but does **not** want videos with little happening visually. The video should understand the script and show relevant background pictures/footage: the company being discussed, people working with the topic, office/workflow scenes, security operations, finance/payment rails, fitness/stoic scenes, etc.

## Provider order

1. Pexels video API (`PEXELS_API_KEY`) — preferred stock footage when the key is active.
2. Pixabay video API (`PIXABAY_API_KEY`) — secondary stock footage; good immediate fallback when Pexels is 403/not active.
3. Pexels photo API — acceptable when video is unavailable.
4. Shutterstock preview video (`SHUTTERSTOCK_TOKEN`, plus consumer key/secret for auth maintenance) — useful for topic/company search coverage; treat preview assets/licensing according to the account plan before final public use.
5. Storyblocks (`STORYBLOCKS_PUBLIC_KEY`, `STORYBLOCKS_PRIVATE_KEY`) — keys may require HMAC request signing; wire/test separately before assuming readiness.
6. Reputable no-key image fallback for topic/company images.
7. Dynamic text/shape fallback only for drafts or if the user explicitly accepts it.

## Query generation

Create one visual query per script beat. Use the actual source subject/body and narration, not generic channel keywords.

Examples:

- `Visa and OpenAI partner company office workers technology`
- `Mastercard Agent Pay payment technology office`
- `stablecoin rollout fintech banking app`
- `Ivanti vulnerability cybersecurity operations center`
- `AI infrastructure engineers working data center`
- `stoic discipline morning journaling running alone`
- `gym workout meal prep athletic discipline transformation`

If exact company/topic footage fails, broaden the query semantically instead of falling back immediately: `payment technology office`, `software engineers working startup office`, `cybersecurity server room`, `focused person working laptop city night`.

## Rendering requirements

- Crop/scale to 9:16 vertical.
- Loop stock videos for the scene duration.
- For photos, use a slow zoom/pan (`zoompan`) so they do not feel static.
- Apply a dark overlay/blur if needed so captions stay readable.
- Save `visual_manifest.json` with scene number, caption, query, provider, source URL, and local asset path.
- QA the manifest: if every scene says fallback/dynamic, treat it as draft quality, not final.

## Environment

Set API keys in `/opt/data/.env` and mirror to `/opt/data/HeRmEz/.env` when the project reads both. Keep both files owner-readable/writable only (typically `chmod 600`).

```env
PEXELS_API_KEY=...
PIXABAY_API_KEY=...
STORYBLOCKS_PUBLIC_KEY=...
STORYBLOCKS_PRIVATE_KEY=...
SHUTTERSTOCK_CONSUMER_KEY=...
SHUTTERSTOCK_CONSUMER_SECRET=...
SHUTTERSTOCK_TOKEN=...
```

Operational notes:

- The user may say "Pixels" when they mean **Pixabay**; verify the screenshot/domain before choosing env var names. A key in the `5629...-...` format from `pixabay.com/api/docs` belongs in `PIXABAY_API_KEY`, not `PEXELS_API_KEY` or `PIXELS_API_KEY`.
- Always run a live API probe after adding keys; key presence is not readiness.
- If Pexels returns `403 Forbidden`, comment/disable stale `PEXELS_API_KEY` values in `.env` and route around it to Pixabay/Shutterstock while the user regenerates or activates the Pexels key.
- The renderer/preflight should treat `.env` as source of truth for managed stock keys and override/remove stale inherited process env (`PEXELS_API_KEY`, `PIXELS_API_KEY`, `PIXABAY_API_KEY`, Storyblocks, Shutterstock). Otherwise a revoked Pexels key can keep appearing as present even after `.env` was fixed.
- Pixabay can be validated with `/api/videos/?key=...&q=office%20workers&per_page=3` and should return `hits`.
- Shutterstock video search can be validated with `Authorization: Bearer $SHUTTERSTOCK_TOKEN` against `/v2/videos/search`; preview MP4 URLs appear under `assets.preview_mp4.url`.
- Storyblocks keys are saved as public/private key material but require HMAC signing before the provider should be marked ready.

Pexels or Pixabay alone is enough to activate true stock visuals in the current faceless pipeline. If no backlog emails are present after enabling stock visuals, run the uploader once to verify `processed: 0, uploaded: 0`, then schedule a short-lived watcher (for example hourly for 24 hours) so new newsletters are picked up automatically.