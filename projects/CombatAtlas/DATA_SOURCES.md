# CombatAtlas Data Integration Notes

The app is designed so external data sources are import-time enrichers, not runtime blockers.

For the full 2026-08-25 legal/source audit, expansion plan, and machine-readable inventory, see:

- `DATA_EXPANSION_PLAN.md`
- `imports/research/source-inventory.json`
- `imports/research/probe-results.json`
- `imports/research/wikipedia-martial-arts-techniques.json`
- `imports/research/bjjdata-sample.json`

## Ready without keys

### Wikipedia / MediaWiki

Technique category endpoint:

```text
https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Martial_arts_techniques&cmlimit=500&format=json
```

Useful for technique names and summaries. Requires CC BY-SA attribution if text is copied into the app.

### Wikidata

```text
https://www.wikidata.org/w/api.php?action=wbsearchentities&search=armbar&language=en&format=json
```

Useful for aliases, entity IDs, cross-language links, and structured metadata.

### Wikimedia Commons

```text
https://commons.wikimedia.org/w/api.php
```

Useful for licensed images/media. Store author/license/source URL per asset.

### GitHub bjjdata

```text
https://github.com/ubershmekel/bjjdata
```

MIT-licensed BJJ clip/tag metadata. Good for optional BJJ enrichment.

## Key-ready later

### Kaggle Grappling Techniques

```text
https://www.kaggle.com/datasets/liiucbs/grappling-techniques
```

Requires free Kaggle account/token. When available, add env vars only locally/Vercel, never commit keys:

```text
KAGGLE_USERNAME=...
KAGGLE_KEY=...
```

## Runtime principle

The production app should remain usable with the local bundled database even if every external source is unavailable. API imports should write/cache normalized seed files before deployment.
