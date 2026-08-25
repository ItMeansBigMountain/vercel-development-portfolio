# Who's Grinding Panel: WOM rollback, suffix cleanup, and not-on-WOM behavior

Session lessons from restoring the plugin after fallback/search changes broke the WOM-first card.

## Known-good rollback point

When the user reports that WOM stats or player lookup regressed after fallback experiments, restore the WOM-primary baseline before adding new fallback/search changes. The known-good commit used in this session was:

```text
a0e2162 feat: add player header and OSRS acronym labels
```

That point was before the official hiscores fallback commits and still loaded WOM gains for known players such as `oyama`.

Do not layer official-hiscores experiments, JSON endpoint changes, or search UI refactors on top of a broken WOM flow. First restore and verify WOM for a known player, then reapply small safe UI-only changes.

## Verification probe

Use WOM's gained endpoint with the same headers as the plugin when checking whether the service still knows a player:

```text
GET https://api.wiseoldman.net/v2/players/{name}/gained?period=week
User-Agent: WhosGrindingPanel RuneLite plugin
Accept: application/json
```

Expected for a known player like `oyama`: HTTP 200 with `data` and positive gained values.

## Remove redundant gain labels

The card value suffix already carries the unit. Do not append parenthesized category labels after each value.

Bad:

```text
Ranged: +606,383 xp (XP)
Yama: +26 kc (KC)
Clue Scrolls Hard: +1 score (Score)
```

Good:

```text
Ranged: +606,383 xp
Yama: +26 kc
Clue Scrolls Hard: +1 score
```

Search the source/tests for these exact strings before finishing:

```text
(XP)
(KC)
(Score)
```

## Player not on WOM

Observed behavior:

- `GET /v2/players/{name}/gained?period=week` returns 404 when WOM does not know the player.
- `POST /v2/players/{name}` may be blocked from the plugin/runtime environment by WOM protection, so do not assume the plugin can always create/update a player.

If update fails, show a clear card message instead of a generic failure:

```text
Player not on
WOM yet. Open
Wise Old Man and
track/update them,
then refresh here.
```

Keep WOM as the primary source. Official hiscores fallback is a separate current-total snapshot comparison path and should not replace or interfere with the WOM-first path.
