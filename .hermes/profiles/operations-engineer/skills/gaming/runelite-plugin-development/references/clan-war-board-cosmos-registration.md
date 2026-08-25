# Clan War Board durable plugin registration

Use this when moving Clan War Board from truthful zero-state/ephemeral telemetry to real plugin-only clan registration.

## Client contract

- Generate one UUIDv4 installation ID and persist it through RuneLite `ConfigManager`; do not regenerate it on every startup.
- Register only when a real clan is detected.
- Send the real player name, clan name, observed clan-rank value, plugin version, and public-stat preference.
- Never include the development role override in registration or authorization payloads. Pretend-leader/pretend-member remains local UI state only.
- Keep public player statistics opt-in; world reporting remains public.

## Service contract

- Validate UUIDv4 and a non-empty normalized clan name.
- Hash the installation ID before persistence; never return that hash in public API responses.
- Make registration idempotent per installation and clan.
- A clan is created only by real plugin activity, never by WOM/external directory imports or fixtures.
- Public member responses should expose only privacy-safe fields such as display name when opted in, public/private state, and last-seen time.

## Production storage boundary

- Keep in-memory storage only for tests/local runs.
- Production must explicitly select Cosmos and fail loudly if endpoint/key settings are missing.
- Health should expose the real backend plus a production-readiness boolean; gate deployment on `storage=cosmos` and readiness true.
- Fetch Cosmos credentials through Azure OIDC at deploy time and write them to Static Web Apps backend settings. Do not store Cosmos keys in GitHub variables, the plugin, or frontend assets.
- Verify real Cosmos connectivity against an empty container without inserting fake clans.

## Verification sequence

1. Unit-test invalid registration, privacy default, idempotency, and public-response hash removal.
2. Run the full Java 11 RuneLite build.
3. Exercise real Cosmos read connectivity without creating fabricated records.
4. Deploy through GitHub Actions.
5. Verify live health says Cosmos/readiness true.
6. Verify invalid registration returns HTTP 400 and `/api/clans` remains empty until a real plugin client registers.
