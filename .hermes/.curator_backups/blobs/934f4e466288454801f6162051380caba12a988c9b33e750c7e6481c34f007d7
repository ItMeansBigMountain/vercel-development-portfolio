# Clan War Board secure match workflow

## RuneLite production boundary

Use current official RuneLite and accepted Plugin Hub patterns before implementing networked clan features:

- Read rank from `Client.getClanChannel()`, `ClanChannel.findMember(...)`, `ClanChannelMember.getRank()`, and `ClanRank.getRank()`.
- Official rank values are `ADMINISTRATOR=100`, `DEPUTY_OWNER=125`, `OWNER=126`, `JMOD=127`, and `GUEST=-1`.
- Inject RuneLite's shared `OkHttpClient` and `ScheduledExecutorService`; do not construct a per-plugin HTTP client, block the game thread, use the common `CompletableFuture` pool, or call `Thread.currentThread().interrupt()` in Plugin Hub code.
- Marshal Swing changes through the EDT and guard callbacks after shutdown.
- Persist only a non-secret UUIDv4 installation ID in `ConfigManager`. Keep bearer session tokens memory-only because RuneLite config is plaintext.
- Pin the production HTTPS API URL in code. Expose no endpoint override, pretend role, developer mode, mock mode, or experimental network option.
- Show leader controls only when both observed RuneLite rank and the server-issued `leader:write` capability agree.

## Authority limitation

A persistent installation UUID is continuity, not identity. A public RuneLite plugin can be modified, so client-observed clan rank is not Jagex-attested. Label the trust level honestly (for example, `runelite_client_observed_rank`) and do not describe it as cryptographic leader verification. Truly high-impact administration needs an external verification/approval mechanism.

## Session and write-proof contract

Registration returns an opaque short-lived token. Store only `SHA-256(token)` with installation hash, clan ID, observed rank, capabilities, issue/expiry times, nonce history, and rate-window timestamps.

Every write requires:

```text
Authorization: Bearer <token>
X-CWB-Timestamp: <epoch seconds>
X-CWB-Nonce: <UUID>
```

Enforce expiration, capability, five-minute freshness, unique nonce, per-session sliding rate limit, and token rotation/revocation. In Cosmos, use ETag-conditional session replacement; persistence without optimistic concurrency still allows two scale-out workers to accept the same nonce. Map failures explicitly: 401 auth/proof, 403 capability/participant, 404 missing resource, 409 ETag race, 429 rate limit.

Registration is the bootstrap trust boundary. Do not pretend a token makes a spoofable rank claim authoritative. Rate-limit bootstrap and plan external leader verification before exposing irreversible/high-impact operations.

## Cosmos document model

Reuse containers only when their partition keys fit:

- `clans` partition `/normalizedName`: clan docs and hashed session docs with distinct `docType` values.
- `wars` partition `/clanPairKey`: availability and challenge docs.

All public queries must filter `docType`. Strip Cosmos `_etag`, `_rid`, `_self`, `_attachments`, `_ts`, partition metadata, installation hashes, and session data from responses.

## Canonical match terms

Validate and normalize before adding routes:

- opponent clan ID
- location
- public OSRS world
- timezone-aware ISO-8601 start time normalized to UTC
- combat range 3–126 with min <= max
- bounded duration
- bounded rules text

Serialize sorted compact JSON and SHA-256 it. Acceptance is tied to `termsHash`, never only a mutable challenge ID.

```text
proposed -> creator accepted
opponent accepts same hash -> confirmed
any terms change -> reconfirm_required
both participants accept new hash -> confirmed
opponent -> reject
creator -> cancel
counter -> replace terms/hash; clear old acceptance except countering clan
```

Derive actor clan from the authenticated session, never request JSON. Only creator/opponent may read or act on a challenge; outsiders cannot become the second acceptance.

## Availability and telemetry

Leader availability writes require `leader:write`, bounded UTC time/duration/combat fields, Cosmos persistence, and a sanitized public projection.

Telemetry is also a write: require `telemetry:write`, bind event clan to session clan, cap batches, preserve private-by-default player names, and reject unauthenticated submissions. The complete telemetry milestone must additionally gate collection to confirmed fight world/time/location windows, include war ID + terms hash + sequence/idempotency fingerprint, persist/dedupe events, and use bounded retry/backoff.

## TDD and verification

Write failing tests first for:

1. Token issuance and hash-only storage.
2. Member denial of leader writes.
3. Expiry, stale timestamp, replayed nonce, and rate limiting.
4. Rotation revoking the old token.
5. Canonical terms hash and reconfirmation.
6. Outsider challenge rejection and participant inbox filtering.
7. Cosmos/public projection privacy.
8. Telemetry authentication and clan binding.
9. RuneLite config reflection proving no dev/endpoint methods.
10. Unique client nonce headers and session parsing.

Run Java 11 `./gradlew clean test assemble --no-daemon --console=plain`, Python tests/compile, and a source scan for dev overrides, `java.net.http`, common-pool futures, and thread interruption. Do not claim deployment until child repos are committed/pushed, Azure deployment completes, authenticated live register/rotate/availability/challenge/replay smoke tests pass, and parent gitlinks match exact remote SHAs.
