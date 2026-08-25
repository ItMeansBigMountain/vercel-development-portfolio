# Boss autocomplete via OSRS Wiki + GearScape APIs

Use this pattern when a RuneLite plugin needs a robust, low-maintenance boss picker/autocomplete rather than a hand-maintained enum/list.

## Public endpoints

- GearScape monster index: `https://api.gearscape.net/api/monster`
  - Public/read-only, no API key observed.
  - Filter records with a boss flag when available.
  - Use as the preferred source for machine-readable boss IDs, combat levels, and stat-oriented matching.
- GearScape equipment index: `https://api.gearscape.net/api/equipment/all`
  - Public/read-only, useful for gear recommendation engines and stat comparisons.
- OSRS Wiki boss category:
  - `https://oldschool.runescape.wiki/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:Bosses&cmnamespace=0&cmlimit=500`
  - Use as canonical fallback coverage for boss names that are not well represented in GearScape.
- OSRS Wiki page lookup:
  - `https://oldschool.runescape.wiki/api.php?action=opensearch&format=json&search=<name>&limit=1&namespace=0`
  - Use to attach a canonical wiki page URL to an autocomplete/result entry.

## Runtime pattern

1. Fetch API data in a background executor, never on the RuneLite/game/UI thread.
2. Build a merged boss index:
   - GearScape boss entries first for structured stats.
   - Wiki `Category:Bosses` names second for canonical coverage.
   - De-duplicate normalized names but keep source metadata (`GearScape`, `OSRS Wiki`, or both).
3. Keep a local fallback list so plugin startup and dropdown rendering still work when endpoints are offline.
4. Match user-entered boss names with weighted scoring:
   - Exact/case-insensitive normalized matches first.
   - Prefer GearScape-backed entries over Wiki-only entries when strings are similarly close.
   - Allow Wiki-only entries to resolve to a page link even if structured stats are unavailable.
5. Parse API responses with a small JSON dependency such as `com.google.code.gson:gson:2.10.1` if the project does not already have a JSON parser.

## Side-panel autocomplete UI pattern

- Use an editable Swing `JComboBox` or similar side-panel component.
- As the user types, filter the merged boss index in memory; do not re-query the network per keystroke.
- On Enter or selection:
  - Persist the selected boss name into the RuneLite `ConfigManager`/plugin config bridge.
  - Trigger panel refresh and recommendation recomputation.
- Display source/status labels so users understand when a boss is GearScape-backed versus Wiki-only fallback.

## Verification

Add a smoke test or small Java main/test fixture that loads the live services outside RuneLite and verifies:

- Boss index count is non-trivial.
- Equipment index count is non-trivial if gear recommendations depend on it.
- Known bosses such as `Vorkath` resolve to GearScape-backed entries.
- Known Wiki-only/minor bosses resolve to Wiki URLs without crashing the recommendation engine.

In this user's container, RuneLite plugin Gradle tasks generally need:

```bash
JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew test assemble --no-daemon -q
```

## Pitfalls

- Do not maintain a static all-boss enum unless it is only a fallback; the user explicitly wants API-backed dropdowns to avoid manual plugin updates.
- Do not block the RuneLite UI while loading remote data.
- Do not make the plugin unusable when GearScape is down; Wiki/local fallback should still permit search and page linking.
- Do not rely only on OSRS Wiki category data for boss readiness scoring; Wiki gives coverage, but GearScape-style structured monster/equipment data is more useful for scoring and BiS logic.
