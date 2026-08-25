# Static data-atlas apps with API-ready import hooks

Use this pattern when the user wants a complete explorable/searchable database app, but no single reliable public API provides the full domain data and API keys should not block deployment.

## Pattern

1. **Ship a bundled seed atlas first**
   - Build the user-facing product around local JSON/JS seed data so the deployed app works without credentials or third-party uptime.
   - Include enough breadth to make the demo useful immediately: entity profiles, searchable records, categories/tags, filters, and a detail panel.
   - Make the UI honest about the data state: “bundled seed database,” “API-ready enrichers,” or similar, rather than implying live exhaustive coverage.

2. **Prepare enrichers as import-time tools, not runtime dependencies**
   - Add scripts such as `npm run import:<source>` that write reviewed import files under `imports/`.
   - Keep external data out of the critical rendering path until licensing, attribution, quality, and keys are verified.
   - Prefer public/no-key APIs first (MediaWiki/Wikipedia category indexes, Wikidata, Wikimedia Commons metadata), then key-gated sources later (Kaggle, vendor APIs, paid datasets).

3. **Design for rate limits and offline fallback**
   - Do not call many per-record summary/detail endpoints during a build or deploy.
   - If a public endpoint can return `429 Too Many Requests`, catch the error and fall back to a small bundled index so the command remains useful.
   - Record source URL, license/attribution notes, and whether data came from live fetch or fallback.

4. **Validate the data contract**
   - Add lightweight tests for minimum record counts, required fields, search behavior, and profile lookups.
   - Run `npm test`, the import command, and `npm run build` before deploying.
   - If the import command depends on public APIs, assert a minimum count that the fallback can satisfy too.

5. **Deploy and verify like a product, not a shell**
   - Use Vite/React static deployment on Vercel when no backend is needed.
   - Smoke test the live URL in a browser, including at least one search/filter interaction.
   - Update workspace trackers with the production alias, preview/deployment URL, status, and notes about seed coverage and future enrichers.

## Example from CombatAtlas

CombatAtlas shipped as a React/Vite martial arts drill atlas instead of waiting for a perfect martial-arts-drill API:

- 22 martial art profiles
- 882 bundled searchable drill records
- filters for art, category, difficulty, equipment, contact level, and format
- optional import hooks for Wikipedia/MediaWiki, Wikidata, Wikimedia Commons, Kaggle, and `bjjdata`
- Wikipedia import catches live `429` failures and falls back to a bundled 78-technique index

Commands used for validation:

```bash
npm test
npm run import:wikipedia
npm run build
```

Deployment verification included anonymous HTTP `200` checks and browser testing of production search behavior.

## Pitfalls

- Do not block on free-tier account/API key setup if a useful local-first atlas can be shipped now.
- Do not make third-party API calls at runtime unless the app can degrade gracefully when the API is down/rate-limited.
- Do not merge copied text/media from Wikipedia/Wikimedia-style sources into the seed data without checking attribution/license requirements.
- Do not claim “complete exhaustive database” if the data is a broad seed atlas; describe it as bundled coverage plus enrichment hooks.
