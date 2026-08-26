# Who's Grinding Panel: self row, acronyms, and WOM message states

Session lessons from final screenshot review and OSRS slang reference.

## Current-player row

- Always show the logged-in RuneLite character at the top of the panel on every source tab.
- Purpose: the user wants to see what other people can see about **him** from the same WOM/public data view.
- Row copy should be compact, e.g. `You: <name> what others see`.
- It should expand/collapse just like a normal player row and use the same `Grinding {period}` WOM card.
- If the local player is unavailable, show a short placeholder: `You: log in to show your character`.

## WOM message-state distinction

When screenshots show different messages, distinguish these states:

1. **Transport/API failure** — WOM request failed or could not return usable gained data.
   - UI should not be a long sentence.
   - Use short wrapped lines such as: `Could not load / WOM gains / Tracking was / requested if / possible. Try / refresh or a / longer period.`
2. **No positive gains** — WOM returned data, but selected period has no positive XP/KC/score gains.
   - Use the existing short no-gains fallback: `No recent gains / found. WOM tracking / was started/updated...`.

Both messages should wrap with `<br>` around every 2–4 words in the narrow player card.

## Acronym/slang labels

Use OSRS slang/acronym labels when they improve sidebar fit and are widely understood. Examples:

- `chambers_of_xeric` -> `CoX`
- `chambers_of_xeric_challenge_mode` -> `CM CoX`
- `tombs_of_amascut` -> `ToA`
- `theatre_of_blood` -> `ToB` (not `ToA`)
- `theatre_of_blood_hard_mode` -> `HMT`
- `corrupted_gauntlet` -> `CG`
- `general_graardor` -> `Bandos` (avoid ambiguous `GG` here)
- `grotesque_guardians` -> `GG`
- `last_man_standing` -> `LMS`
- `soul_wars` -> `SW`
- `bounty_hunter_hunter` -> `Bounty Hunter` or `BH` only if space is extremely tight.

See `references/osrs-slang-acronyms.md` for the broader acronym list.

## Verification checklist

- Unit test acronym mapping for at least CoX, ToA, ToB, LMS/SW/Bounty Hunter style activity labels.
- Build with Java 11: `./gradlew clean test assemble --no-daemon --console=plain`.
- Visually verify screenshots: current user row appears above tracked counts/filter and persists across tabs; expanded self card uses the same compact layout as other players.
