# Boss Search Comparative Audit and Upgrade Pattern

Use this reference when a competing RuneLite plugin has a target/monster search worth studying or when a boss selector's autocomplete and final resolution disagree.

## First distinguish the two meanings of “search”

A plugin may use the word for:

1. **Target discovery** — finding/selecting a monster or boss by name.
2. **Loadout optimization** — searching combinations of owned gear for the highest-DPS setup.

Audit both before deciding what the user wants improved. Do not mistake a sophisticated gear hill-climb for a better text box, or vice versa.

## Exact pinned-source comparison

At `Diogo-G-Dias/bis-gear-plugin` revision `2aa61a455c7656313caf8ca189f001c8a621663e`, target discovery had these useful patterns:

- approximately 2,850 monsters rather than a boss-only catalog;
- `IconTextField` plus a focus-bound result list;
- combat level, HP, and asynchronously cached thumbnails in result rows;
- immediate substring filtering with prefix-first sorting;
- at most 40 visible matches;
- thumbnail fetching debounced after typing and kept out of the Swing renderer/EDT.

Its owned-gear search was a separate hill-climb seeded by strong weapons and complete sets, followed by pair-slot improvement and prayer-fill passes. Treat that as optimization-engine evidence, not target-search UX evidence.

## Durable BIS Loadouts search pattern

For a boss-focused advisor, prefer confidence and practical lookup quality over inflating the catalog with ordinary monsters:

1. Use one pure matcher shared by autocomplete and final target resolution. A panel-side substring filter plus service-side fuzzy resolver creates inconsistent behavior.
2. Rank in this order:
   - exact canonical name;
   - exact base name (for leading articles/forms);
   - prefix;
   - word start;
   - all query tokens, regardless of token order;
   - loose substring;
   - bounded Levenshtein typo match.
3. Normalize case, punctuation, repeated whitespace, and combining marks.
4. Expand a small explicit alias table for common unambiguous boss shorthand (`KBD`, `Jad`, `Zuk`, `Cerb`, `Huey`, etc.). Keep aliases in search logic; do not replace canonical display names with ambiguous acronyms.
5. Reject irrelevant distant matches instead of filling the popup with nonsense.
6. Cap actual-query suggestions to roughly 12 in the narrow RuneLite sidebar. Preserve curated insertion order for an empty query so “best overall” and familiar targets remain stable.
7. If duplicate names exist, add a data-quality weight so a detailed GearScape-backed profile wins over a Wiki-only generic entry without overriding exact-name relevance.
8. Keep free-form input available for fallback resolution, but do not let the typed row displace a canonical exact match.
9. Make the action discoverable with direct copy such as **Search boss** and a compact tooltip listing representative shorthand.

## Strict TDD sequence

Write and observe RED tests before production edits:

- typo: `vorkth` → `Vorkath`;
- shorthand: `kbd` → `King Black Dragon`;
- token order: `dragon black king` → `King Black Dragon`;
- exact name before longer form: `Brutus` before `Demonic Brutus`;
- nonsense returns no suggestions;
- empty query preserves original order and respects the limit;
- a real EDT Swing test types into the editable combo/text field, drains `invokeLater`, and checks the model contains the canonical match and stays within the compact limit;
- customer-facing label visibly says `Search boss`.

Then run focused matcher/panel/data-service tests, followed by `clean test assemble` under Java 11 and the official Plugin Hub marker build.

## README and support-copy safety for OSRS plugins

When adding a humorous support ask to an OSRS plugin README:

- discover and verify the creator's exact public support URL instead of inventing a handle;
- keep real-money support and voluntary in-game tips explicitly separate;
- state that there is no GP-for-cash exchange so the copy cannot be read as real-world trading;
- keep the joke appropriate and brief, then return to product documentation;
- verify the live GitHub link after publishing.

## Safe adaptation boundaries

- Reimplement interaction ideas; do not copy competitor code.
- Do not broaden from bosses to every monster unless the product requirement changes and full stat/form data can be maintained at equivalent quality.
- Thumbnails are valuable only if fetched asynchronously, cached, and never downloaded from a cell renderer.
- Keep target forms/NPC IDs and elemental/attribute mechanics distinct; smarter string matching must not collapse combat profiles.
