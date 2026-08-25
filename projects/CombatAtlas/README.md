# CombatAtlas — Martial Arts Drill Database

CombatAtlas is now a Vercel-ready React/Vite app with a bundled local martial arts drill atlas.

An Expo universal iPhone/web shell is available in `mobile/`. It preserves the same 22-art/882-drill atlas and adds consent-first test ads plus a receipt-verifying remove-ads boundary. See `mobile/README.md` for Expo Go and verification commands.

CI/CD, environment separation, release, and rollback procedures are documented in `RELEASE.md`. The canonical Vercel alias is `https://combatatlas-flame.vercel.app`; its current deployment-protection blocker is recorded there rather than hidden.

## Current shipped state

- 22 martial arts profiles across striking, grappling, weapons, traditional practice, self-defense, hybrid MMA, and movement arts.
- Minimal customer-facing homepage: universal search bar plus a clean martial arts grid.
- 882 searchable drills with short instructions, coaching cues, difficulty, contact level, and YouTube demonstration search links.
- Search finds both martial arts and drills from one field.
- Each martial art and drill resolves to a visual illustration, so the product no longer depends on broken external image providers.
- Developer/source panels were removed from the public webpage.

## Why the database is bundled first

No single free public API appears to provide “every martial art drill.” CombatAtlas works now with a broad seed atlas and can later enrich from APIs/datasets without making the live app depend on credentials or third-party uptime.

## Optional future data/API enrichers

- Wikipedia MediaWiki category members for martial arts technique summaries — no key, CC BY-SA attribution required.
- Wikidata aliases/entity IDs — no key.
- Wikimedia Commons images/media — no key, license attribution required.
- Kaggle Grappling Techniques — free Kaggle username/key required.
- `ubershmekel/bjjdata` GitHub repo — no key, MIT clip/tag metadata.

## Commands

```bash
npm install
npm test
npm run build
npm run dev
npm run import:wikipedia
```

`npm run import:wikipedia` fetches no-key Wikipedia/MediaWiki technique records into `imports/wikipedia-techniques.json` for review/attribution before merging into the bundled seed database.

## Legacy backend

The original Django REST backend remains under `combatAtlas_Backend/` as legacy source. The live Vercel product currently uses the static React/Vite frontend for fast public review without requiring a database or server credentials.
