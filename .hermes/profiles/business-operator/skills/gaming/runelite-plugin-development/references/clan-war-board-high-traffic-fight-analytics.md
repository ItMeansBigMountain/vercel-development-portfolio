# Clan War Board high-traffic fight analytics design

Session lesson from the Clan War Board planning/build work: the product is not just a static leaderboard. Treat it as a RuneLite-first clan competition network with adversarial public traffic.

## Product flow

- Clan leaders post fight availability from the RuneLite plugin: rough time window, target fight size, war type, rules summary.
- Other clan leaders browse availability and apply/mark interest.
- A match is confirmed only when both leaders accept the exact same terms hash.
- Clan members install the plugin; their plugin heartbeats let the service understand plugin-enabled clan membership/readiness.
- During the agreed fight window, participating plugins submit batched observations: participant seen, damage dealt/taken, kills, deaths, returns, world presence, third-party interactions.
- The service aggregates evidence into completed fight stats and winner analysis.
- The RuneLite plugin shows crucial overview metrics; the website shows detailed completed analytics.

## Security stance

Do not claim a public Java RuneLite client can be perfectly proven. Any static embedded plugin secret can be extracted. The practical design is layered:

- website is read-only and uses public/sanitized endpoints or static JSON snapshots,
- write endpoints are plugin-oriented and require install registration/tokens,
- leader endpoints require observed rank/leader eligibility and later verified leader identity,
- event telemetry is append-only evidence, not immediate truth,
- results require multi-client corroboration and anomaly checks,
- rate-limit by install, player, clan, endpoint, IP/network, and fight,
- never expose exact upcoming world/hotspot/rally/fallback info publicly by default.

## RuneLite sidebar UX

Preserve the proven narrow side-panel width. Use vertical views or a compact selector, not wide horizontal tab bars.

Suggested views:

- Board — browse availability and confirmed fights.
- My Clan — plugin member count, active members, leader-eligible count, upcoming/live fights.
- Leader — post availability, view applications, accept/counter/reject; leader-only.
- Live — compact fight overview metrics only.
- Results — recent completed summaries.
- Settings — sync/privacy/service URL/refresh controls.

If a member/non-leader accesses the leader view, show a clear card:

```text
Leader access required
Your current clan rank does not allow fight management.
Ask an Administrator, Deputy Owner, or Owner to manage Clan War Board fights.
```

Substitute the configured minimum rank if stricter.

## Metrics model

Plugin overview should stay compact:

- status/time remaining,
- active plugin-confirmed members per clan,
- kills/deaths observed,
- return counts,
- third-party interference count,
- tentative winner signal,
- confidence score.

Website analytics can show detailed completed data:

- kill/death/return timeline,
- peak active participants,
- unique members by clan,
- damage dealt/taken,
- member return counts,
- third-party damaged/damaging players,
- confidence/anomaly notes,
- winner explanation.

Winner analysis should be weighted and caveated; use `disputed/insufficient confidence` when telemetry is too noisy.