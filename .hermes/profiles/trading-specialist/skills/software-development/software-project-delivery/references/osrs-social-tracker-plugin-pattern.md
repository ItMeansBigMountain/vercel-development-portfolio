# OSRS/RuneLite social tracker plugin pattern

Use this when turning an OSRS plugin idea from a placeholder panel into a usable local tracking product for friends, clan members, or friends-chat participants.

## Product shape

A strong first slice is a local social tracker, not external XP/KC enrichment:

- Configurable source toggles: friends list, clan members, friends chat.
- Normalize player names and merge the same player across multiple sources.
- Track compact member records: display name, source tags, status, first seen, last seen, last status change, optional world, optional activity summary.
- Let the user remove/untrack individual members.
- Persist removed/ignored names compactly so rescans do not immediately re-add them.
- Cap tracked members with a config value to control memory/API usage.
- Render source filters in the panel: All, Friends, Clan, Friends Chat.

## Implementation sequence

1. Write/refresh `PRODUCT_DIRECTION.md` so the user's current vision is durable before coding.
2. Replace hardcoded sample rows with state classes first:
   - `TrackedMember`
   - `TrackedMemberSource`
   - `TrackedMemberStatus`
   - `SocialTrackerState`
   - source/filter enum(s)
3. Add a service boundary before live RuneLite API integration:
   - owns a `Map<normalizedName, TrackedMember>`
   - loads/saves ignored names
   - merges duplicate observations across sources
   - rejects ignored names
   - enforces max tracked members
   - exposes immutable snapshots for Swing rendering
4. Update the Swing panel to render state:
   - tracked/ignored counts
   - last scan timestamp
   - source filter dropdown
   - rescan button
   - per-member remove button
   - empty/loading/unsupported/stale messages
5. Wire plugin startup/login/config-change events to rescan and refresh the panel.
6. Add tests for merge-across-sources, remove/ignore, cap behavior, existing formatting, and heatmap bucketing.
7. Run Java 11 verification: `./gradlew clean test assemble --no-daemon --console=plain`.

## Live-source integration boundary

If live RuneLite social APIs are uncertain or require GUI/client verification, do not block the whole architecture. Use seeded/local `SocialSourceSnapshot` inputs behind the same service boundary, then replace them later with source scanners:

- `FriendsListScanner`
- `ClanMemberScanner`
- `FriendsChatScanner`

Each scanner should fail gracefully when logged out, no clan/friends chat is active, or the API is unavailable. Keep network/API calls off the client thread.

## Persistence guidance

Use hidden config for compact ignored-name persistence when possible. Do not persist large histories in RuneLite config. External WOM/TempleOSRS enrichment should refresh only currently tracked/non-ignored members, with batching/debounce and stale/failure UI states.

## Pitfalls

- Do not keep hardcoded sample rows once the user asks for the real tracker loop.
- Do not wire WOM/TempleOSRS first; local discovery/tracking/removal is the product foundation.
- Do not let the tracking list grow forever; always include cap + one-by-one removal.
- Do not conflate friends chat with clan membership; preserve separate source tags even when the same name appears in both.
- Build success is not full RuneLite readiness; still call out the need for manual `./gradlew run --no-daemon` client smoke testing when live UI/API behavior matters.
