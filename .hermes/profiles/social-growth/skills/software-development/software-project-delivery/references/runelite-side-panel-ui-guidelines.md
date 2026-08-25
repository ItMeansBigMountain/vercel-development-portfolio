# RuneLite side-panel UI guidelines

Use this when building or reviewing OSRS/RuneLite plugin side panels.

## Default-width rule

RuneLite side panels must fit the default RuneLite sidebar width without asking players to resize the client. Treat horizontal overflow as a product bug.

Practical layout targets:

- Keep outer panel padding small: about 4px, not 8px+.
- Disable horizontal scrolling on the panel scroll pane.
- Wrap summary text at a conservative width (roughly 150-160px depending on button/sidebar content).
- Use compact fonts for tabs and dense metadata (around 9-10pt), while keeping headings readable.
- Use compact row controls: prefer icon/`×` buttons with tooltips over wide text buttons like `Remove`.
- Keep member row copy short; put detail in tooltips or follow-up views when needed.
- Heatmaps/grids should use small cells and 1-2px gaps so 24-hour grids fit in 4x6 layouts.

## Social-tracker side panels

For plugins that track friends list, clan chat, or friends chat:

- Start empty by default. Do not seed fake/default people just to make the UI look populated.
- Show clear empty/status states until real source scanners populate members.
- If multiple social sources exist, prefer top tabs for the primary views (e.g. `Friends Chat`, `Clan Chat`, `Friends List`) instead of a wider dropdown.
- Keep sources distinct even when the same player appears in multiple places; merge internally but show source tags compactly.
- Rescan on login and expose a manual `Rescan` button.
- Add an integer refresh interval config in minutes, defaulting to 60, for automatic rescans while logged in.
- Let users remove/untrack individual members and persist an ignored/removed set so rescans do not immediately re-add them.

## Verification

- Run `./gradlew clean test assemble --no-daemon` after UI changes.
- Manually launch with `./gradlew run --no-daemon` or Windows `.gradlew.bat run --no-daemon` and inspect at default RuneLite side-panel width.
- Look specifically for clipped tab labels, horizontal scrollbars, oversized buttons, heatmap overflow, and long empty-state messages.