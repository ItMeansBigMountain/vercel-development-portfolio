# OSRS Clan Competition Service Pattern

Use when building a RuneLite-adjacent public service/site for Old School RuneScape clans.

## Product/data rules learned

- Do not ship faux clans, fake scheduled fights, or fake battle results once the site is public. Use real public source data where possible and show empty states until real RuneLite submissions/telemetry exist.
- Real clan source for initial public data: Wise Old Man Groups API.
  - `GET https://api.wiseoldman.net/v2/groups?limit=<n>` returns real public groups with name, clan chat, description, homeworld, images, verified/patron flags, score, and memberCount.
  - `GET https://api.wiseoldman.net/v2/groups/{id}` returns group detail and `memberships`, including public player fields such as displayName, role, type, build, status, country, EHP/EHB, and timestamps.
- Use group detail membership builds to infer clan type where possible:
  - pure-heavy -> Pure Clan
  - zerker/berserker-heavy -> Zerker Clan
  - main-heavy -> Main Clan
  - otherwise keyword fallback from group name/chat/description: pvp, pk, wild, iron, pvm, social.
- Scheduled fights should remain empty until authenticated RuneLite leader write endpoints exist.
- Completed battle analytics should remain empty until real post-fight telemetry exists.

## OSRS visual direction

Use OSRS/Wiki-inspired design instead of generic SaaS styling:

- Parchment panels, brown/gold borders, dark beveled buttons, old-brick red labels.
- Serif headings, RuneScape-like panel boxes, textured brown background.
- OSRS Wiki theme colors are useful anchors:
  - parchment/body main `#e2dbc8`
  - body mid `#d0bd97`
  - body border `#94866d`
  - button dark `#18140c`
  - osrs brown `#605443`
  - link brown `#936039`
  - old brick `#9f261e`
  - gold/supernova `#f9d000`
- Use public OSRS Wiki MediaWiki API for thematic images:

```text
https://oldschool.runescape.wiki/api.php?action=query&format=json&prop=pageimages&piprop=thumbnail|original&pithumbsize=1000&titles=Wilderness&origin=*
```

Useful pages:

```text
Wilderness
Clan Wars
Revenant Caves
```

Always include attribution in data/docs/UI when using Wiki imagery.

## Website/API shape

Useful public endpoints:

```text
GET /api/clans                 # live WOM group list
GET /api/clans?q=<query>       # search/filter live WOM groups
GET /api/clans/{womGroupId}    # real WOM group detail + members/builds
GET /api/theme/assets          # OSRS Wiki image/theme assets
GET /api/public/availability   # empty until real leader posts exist
GET /api/public/battles        # empty until real telemetry exists
GET /api/fight-setup/schema    # required match agreement fields
```

Fight setup schema should require:

```text
opponent clan
location
world
scheduled start time
combat level range
fight length / duration
fight type
rules / returns / caps
```

World/location/rally details are operational PvP intel: keep exact accepted details private until both leaders agree and only show sanitized public summaries.

## Verification checklist

- Unit tests mock external APIs for deterministic CI.
- Smoke test real WOM and OSRS Wiki APIs locally before deploying.
- Verify live endpoints after app deploy.
- Browser/visual check the live site after front-end changes.
- Confirm public availability/results show empty states rather than fake data before RuneLite writes exist.
