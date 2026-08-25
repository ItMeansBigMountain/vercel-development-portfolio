# Product Direction

## Outcome

One durable content object enters Hermes and can become platform-correct posts across every connected network. Operators can review a calendar, publish immediately or schedule, see returned URLs, inspect failures, and learn from metrics without manually uploading the same media repeatedly.

## Architecture

1. **Content intake**
   - Existing Viral Radar and faceless pipelines
   - Original AI/Parrot media
   - Manually supplied regular content
   - Canonical asset hash, provenance, rights/attribution, and brand lane

2. **Hermes control plane**
   - Normalize title, description, caption, alt text, audience, disclosures, and schedule
   - Generate platform-specific variants without changing source truth
   - Apply approval and public/private policy per lane/platform
   - Submit to Postiz through a version-pinned adapter

3. **Postiz publishing engine**
   - Official OAuth connections
   - Cross-platform scheduling and media publishing
   - Retry/queue semantics
   - Provider-specific limits and errors

4. **Publication ledger**
   - Source asset SHA-256
   - Brand/account identity
   - Platform, post ID, URL, status, published time
   - Retry history, errors, and metrics checkpoints

5. **Feedback loop**
   - Pull platform metrics where supported
   - Compare hooks, timing, formats, and account growth
   - Feed verified learnings into future content planning

## Build versus adopt

Adopt Postiz connectors/scheduler because duplicating official OAuth, resumable media upload, provider review requirements, token rotation, and rate-limit handling across 8+ networks is expensive and fragile. Build only the Hermes-specific layer: content schema, lane policy, adapters, ledger, health checks, metrics learning, Discord presentation, and safe cleanup.

## Non-goals

- Scraping/private APIs as the default publishing path
- Storing platform passwords when OAuth is available
- One identical caption blindly copied everywhere
- Deleting source media before every requested platform confirms a post ID
- Inventing engagement or platform support
