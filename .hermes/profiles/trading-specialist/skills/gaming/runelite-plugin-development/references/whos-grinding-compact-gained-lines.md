# Who's Grinding Panel: compact gained-line formatting

Session lessons from iterative user review of the expanded player card.

## Formatting rules

- Keep the expanded player card focused on `Grinding {period}` only; no data links/source/debug rows.
- Size the card to its content, not to remaining panel height.
- Use the user-approved sidebar width: content aligned to the top dropdown/title width with only a tiny right pad (~3 px).
- Use multiple left-aligned `JLabel` rows instead of one giant HTML blob when rendering complex card content.
- Every stat item gets its own row:
  - each skill XP gain,
  - each boss KC gain,
  - each activity/minigame score gain.
- Gained values (`xp`, `kc`, `score`) should be bolded.
- Use readable card text around 12f and a 13f title unless it clips.

Example:

```html
<b>Skills</b>:<br>
▴ Ranged: <b>+379,085 xp</b> (XP)<br>
▴ Hitpoints: <b>+248,500 xp</b> (XP)<br>
<b>Bosses</b>:<br>
⚔ Phantom Muspah: <b>+37 kc</b> (KC)<br>
⚔ Scurrius: <b>+19 kc</b> (KC)<br>
<b>Activities</b>:<br>
★ PvP Arena: <b>+132 score</b> (Score)<br>
★ LMS: <b>+34 score</b> (Score)
```

## Label cleanups

Map WOM activity keys to player-facing labels before rendering:

- `last_man_standing` -> `LMS`
- `bounty_hunter_hunter` -> `Bounty Hunter`
- `bounty_hunter_rogue` -> `Bounty Hunter Rogue`

Fallback remains title-casing underscore-separated WOM metric keys.

## No-data wrapping

If WOM has no positive gains after start/update + retry, display a concise explanation manually wrapped into short chunks (~3 words per line), not a long one-line sentence.

## Verification expectation

For layout complaints, build success is not enough. Use representative data such as `oyama` and verify all of the following before reporting done:

1. WOM gained endpoint returns real skills/bosses/activities for the chosen period.
2. The summary string contains line breaks for skills, bosses, and activities.
3. `./gradlew clean test assemble --no-daemon --console=plain` succeeds.
4. Generate or inspect a sidebar-width render/screenshot and confirm no trailing text, no large left/right margin, no blank filler height, and bold gained values are legible.
5. Remove temporary render/probe files before final repo status unless the user asked to keep them.
