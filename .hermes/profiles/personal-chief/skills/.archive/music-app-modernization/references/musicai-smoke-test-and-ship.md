# MusicAI smoke-test and ship checklist

Use this when shipping a MusicAI/music-app modernization slice, especially when OAuth, durable storage, or provider status changed.

## Local smoke test shape

Add a small Playwright suite rather than relying only on Flask test-client requests:

- Homepage renders the intended provider strategy, e.g. YouTube-first and Spotify/SoundCloud as roadmap when blocked by paid/API access.
- `/healthz` reports durable encrypted storage for production-like envs: `backend: postgres`, `durable: true`, `encrypted: true`, `ready: true`.
- `/api/analyze-text` returns a real Watson result (`source: watson_nlu`) when Watson credentials are configured, and fallback behavior remains transparent when credentials fail.
- `/analyze-text` validates empty input and renders an analysis for pasted lyrics/song text.
- Provider connect routes return a 302 with the expected OAuth URL, callback, and scopes. For Google/YouTube, inspect the redirect `Location` header instead of navigating all the way to Google to avoid external OAuth page flakiness.

## Playwright-on-server notes

If the default Playwright browser cache is not writable, set a project-local cache path and ignore it:

```json
{
  "scripts": {
    "test:smoke": "PLAYWRIGHT_BROWSERS_PATH=.cache/ms-playwright playwright test"
  }
}
```

Ignore:

```gitignore
node_modules/
.cache/
test-results/
playwright-report/
```

Install once locally:

```bash
npm install
PLAYWRIGHT_BROWSERS_PATH=.cache/ms-playwright npx playwright install chromium
npm run test:smoke
```

## Production verification after deploy

After Vercel deploy, verify from the live URL:

- `/healthz` reports Postgres/durable/encrypted token storage.
- `POST /api/analyze-text` with a short upbeat text returns `ok=true`, `source=watson_nlu`, and no warning if Watson is expected to work.
- `/providers/youtube_music/connect` returns a 302 to Google OAuth with `youtube.readonly`, `youtube.force-ssl`, and the production callback URL.

## Git hygiene

Before pushing, ensure large Playwright browser binaries and Hermes cache/state files are not in the commit range. If the repo has unrelated dirty state, stage only MusicAI files, and if a push is rejected due to unrelated historical large files, rebase the feature commit directly onto current `origin/main` rather than pushing stale backup commits.