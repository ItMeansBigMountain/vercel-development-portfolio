# CombatAtlas lawful data expansion plan

Generated: 2026-08-25 UTC

## Question

How can CombatAtlas expand beyond the current generated 22-art / 882-drill seed dataset using authoritative APIs, open datasets, public-domain or permissively licensed sources, and scrapeable pages without copying copyrighted instructional text?

## Current dataset audit

The live bundled dataset contains 22 martial arts, 10 drill categories, and 882 drills. A direct Node import check found 0 duplicate drill IDs/slugs, but all 882 drills are `verified: false`, all 882 lack `sourceUrl`, and the only drill `sourceType` is `CombatAtlas seed`. This means the dataset is broad but provenance-light; expansion should first add evidence and provenance rather than more generated prose.

Category distribution is balanced enough for product UX: grappling 94, striking 91, traditional/self-defense/sparring 89 each, defense/footwork/conditioning/beginner foundations 88 each, weapons 78. Art distribution is also roughly even at 39-42 drills per art.

## What I collected in this run

- Re-fetched Wikipedia `Category:Martial arts techniques` through the official MediaWiki Action API with a named User-Agent and wrote 88 category-member records to `imports/research/wikipedia-martial-arts-techniques.json`. Wikipedia/Wikimedia APIs explicitly provide open access to Wikimedia project knowledge, while Wikimedia terms allow reuse under free/open licenses and the API etiquette requires meaningful User-Agent, serial/grouped requests, caching, and backoff/rate-limit care.[1][2][5]
- Fetched the bjjdata public JSON endpoint and wrote its 25 BJJ competition-submission clip entries to `imports/research/bjjdata-sample.json`. The site advertises a JSON file for embedding, and the repository README says the data is MIT licensed while clarifying that the value is timestamped YouTube links and metadata, not copied video media.[11][12]
- Probed Wiktenauer's MediaWiki API for HEMA pages/categories and preserved API/robots results in `imports/research/probe-results.json`. Wiktenauer is a HEMA primary-source library, and its copyright policy says default original content is CC BY-SA 4.0, but per-item source tables can include public domain, CC BY, CC BY-SA, CC BY-NC-SA, orphan, uncertain, and mixed-license content, so it must be imported only after page-level license filtering.[6][7]
- Checked robots/terms signals for Wikimedia, Wiktenauer, GitHub Pages, Project Gutenberg, Library of Congress, Kaggle, and ViCoS; the machine-readable decisions are in `imports/research/source-inventory.json`.

## Source decisions

### Ready now: import safely with provenance

1. bjjdata (`ubershmekel/bjjdata`)
   - Use for BJJ submission technique tags, clip timestamps, event/title metadata, and source links.
   - License: MIT per repo README/LICENSE; do not copy YouTube media or YouTube descriptions.[11][12]
   - Required fields: `source`, `sourceUrl`, `repositoryUrl`, `license`, `entryId`, `retrievedAtUtc`.
   - Next implementation: normalize each clip tag into technique facets (`armbar`, `triangle`, `collar-choke`, etc.) and attach links as evidence/reference media, not hosted content.

2. Wikipedia MediaWiki category index
   - Use for technique names, page IDs, canonical URLs, and optional summaries only if attribution/share-alike obligations are satisfied.[1][2][5]
   - License: article text under Wikimedia free licenses, commonly CC BY-SA; names and factual identifiers are safer than copied prose.[2]
   - Required fields: `source`, `sourceUrl`, `pageid`, `license`, `retrievedAtUtc`, `attribution`.
   - Next implementation: merge category-member names against existing `skillsTrained` and create `technique_evidence` records. Do not paste article extracts into drill instructions unless the app has a visible attribution/share-alike strategy.

3. Wikidata
   - Use for QIDs, aliases, identifiers, country/origin/family facts, and multilingual labels. Wikidata structured data in main/property/lexeme namespaces is CC0; text in other namespaces may be CC BY-SA 4.0.[3]
   - Required fields: `source`, `sourceUrl`, `qid`, `license`, `retrievedAtUtc`.
   - Next implementation: query/search only the current technique/art names first; cache results and avoid broad SPARQL hammering.

### Ready with per-record review

4. Wikimedia Commons
   - Use for images/video thumbnails/media only after checking each file's exact license metadata. Commons reuse guidance is explicitly license-specific and requires correct attribution details.[4]
   - Required fields: `filePageUrl`, `author`, `license`, `licenseUrl`, `source image/media URL`, `retrievedAtUtc`.
   - Do not ship a Commons asset if license, author, or source URL is missing or if the file appears to be a non-free derivative work.

5. Wiktenauer
   - Use for HEMA source/treatise/technique metadata and public-domain/CC BY/CC BY-SA text only after checking source tables. Wiktenauer says default original content is CC BY-SA 4.0, but it also hosts non-commercial, orphan, uncertain, and mixed-license material.[7]
   - Robots: general crawl/API probing was allowed in this run; robots content signal permits search/reference use and reserves `ai-train=no`, so use as a cited source/reference corpus, not an AI-training corpus.
   - Required fields: `pageid`, `lastrevid`, `licenseTag`, `sourceTableUrl`, `sourceUrl`, `retrievedAtUtc`.
   - Exclude CC BY-NC-SA, orphan, uncertain, and mixed-license sections from any default commercial/product seed.

6. Library of Congress
   - Use item-level public-domain/no-known-restrictions materials, IIIF manifests, metadata, and public-domain images/text. LOC guidance says online availability does not itself grant reuse rights; item-level `Rights and Access` / `Rights Advisory` is the controlling field, and public-domain/no-known-restrictions items may be freely used.[10]
   - Robots: `loc.gov` disallows `/search` and sets `Crawl-Delay: 5`, so use item JSON/IIIF endpoints and cache.
   - Candidate: `Combat Manual of 1467` for HEMA/combat-manual source metadata.[17]

7. Project Gutenberg
   - Use specific public-domain eBook landing pages and offline catalogs/feeds, not live bulk search scraping. Project Gutenberg says most eBooks are public domain in the US and may be used commercially/derivatively, but terms warn the site is intended for human users, bulk automation should use mirrors/offline catalogs/feeds, OPDS requests need proper User-Agent/contact, and non-US users must check local copyright.[8][9]
   - Candidate items found: `Practical Training for Running, Walking, Rowing, Wrestling, Boxing, Jumping, and All Kinds of Athletic Feats` and `Secrets of the Sword`.[15][16]
   - Canonical source should be eBook landing page, not a deep file URL.

### Blocked or excluded

8. Kaggle Grappling Techniques
   - Search result reports Apache 2.0 and useful fields, but the Kaggle page failed to fetch unauthenticated here; do not scrape behind login.[13]
   - Import only after a Kaggle token is provided and the official Kaggle API confirms dataset license/version.

9. ViCoS Brazilian Jiu-Jitsu Positions Dataset
   - Good academic reference, but license is CC BY-NC-SA 4.0, which is not safe for a commercial/default product seed. It also contains images/annotations, not drill instructions.[14]
   - Use as citation/reference or non-commercial experiment only; exclude from default data expansion.

## Recommended expansion architecture

1. Add a separate `techniqueEvidence`/`sourceRecords` layer rather than overwriting `drills` directly. This lets the UI show “verified by source” badges without claiming that generated drill instructions came from a source.
2. Keep generated coaching text and sourced facts separate. Safe fields from external sources are technique names, aliases, source URLs, page IDs/QIDs, license metadata, position/type tags, and bibliographic metadata.
3. Only copy prose when the source license and product obligations are clear. For CC BY-SA sources, either avoid copied text or implement visible attribution and share-alike compliance before release.
4. Deduplicate with normalized keys: lowercase ASCII slug, alias map from Wikidata, and source-specific IDs (`pageid`, `qid`, repo entry ID). Store duplicates as additional evidence, not duplicate drills.
5. Validate every imported record before merge:
   - Has `sourceUrl`, `license`, `retrievedAtUtc`, `sourceRecordId`.
   - License is one of allowed product values: `MIT`, `CC0`, `public domain`, `CC BY 4.0`, `CC BY-SA 4.0 with attribution/share-alike plan`.
   - `NC`, `orphan`, `uncertain`, `all rights reserved`, failed fetch, and login-only records stay out of product seed.
   - Media has author + license URL + file page URL.

## Implementation plan

P0 importer work:
- Build `scripts/import_bjjdata.mjs` to ingest `https://ubershmekel.github.io/bjjdata/data.json`, output normalized records under `imports/bjjdata-normalized.json`, and never download YouTube media.
- Extend `scripts/import_wikipedia_techniques.mjs` to add `retrievedAtUtc`, `pageid`, and `license` fields; preserve the current slow/no-key behavior.
- Add a schema test that fails any imported record missing provenance fields.

P1 importer work:
- Build a Wikidata alias/QID enrichment script for existing martial arts and imported technique names.
- Build a Commons media candidate script that collects only file metadata first; require manual license review before UI use.
- Build a Wiktenauer HEMA script that imports page metadata and source-table license tags only; skip text until a license whitelist is implemented.
- Build LOC/Gutenberg public-domain bibliographic importers for old manuals, using item/landing pages and offline catalogs, not search-page scraping.

## Machine-readable deliverables

- `imports/research/source-inventory.json` — source-by-source legal/robots/license/action inventory.
- `imports/research/wikipedia-martial-arts-techniques.json` — 88 current MediaWiki category-member records collected through the official API.
- `imports/research/bjjdata-sample.json` — 25 bjjdata entries collected from the public JSON endpoint.
- `imports/research/probe-results.json` — robots/API probe outputs for auditability.

## Confidence, uncertainty, contradictions

Confidence is high for Wikimedia/Wikidata/Commons because those decisions are grounded in official Wikimedia API, terms, data-license, and Commons reuse pages.[1][2][3]
Confidence is high for bjjdata because the public project page and GitHub README were accessible and consistent.[11][12]
Confidence is high for Project Gutenberg policy, LOC item-level caution, and ViCoS exclusion because those were read from their official/project pages.[8][9][10]
Confidence is medium for Kaggle because only search metadata was reachable in this environment; the official dataset page fetch failed, so treat Apache 2.0 as unverified until checked through the Kaggle API.[13]
The main contradiction is Wiktenauer: it is highly relevant and partly open, but its own policy mixes permissive, non-commercial, orphan, uncertain, and public-domain material, so broad scraping would be unsafe even though robots allows crawling.[6][7]

## Sources

[1] https://www.mediawiki.org/wiki/Wikimedia_APIs
[2] https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
[3] https://www.wikidata.org/wiki/Wikidata:Licensing
[4] https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia
[5] https://www.mediawiki.org/wiki/API:Etiquette
[6] https://wiktenauer.com/wiki/Main_Page
[7] https://wiktenauer.com/wiki/Wiktenauer:Copyrights
[8] https://www.gutenberg.org/policy/permission.html
[9] https://www.gutenberg.org/policy/terms_of_use.html
[10] https://www.loc.gov/legal/security-copyright-and-privacy/understanding-copyright
[11] https://ubershmekel.github.io/bjjdata
[12] https://github.com/ubershmekel/bjjdata
[13] https://www.kaggle.com/datasets/liiucbs/grappling-techniques/versions/1
[14] https://vicos.si/resources/jiujitsu
[15] https://www.gutenberg.org/ebooks/56398
[16] https://www.gutenberg.org/ebooks/46093
[17] https://www.loc.gov/item/2021667792
