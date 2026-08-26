# tweetBetweenTheLines

> **Free the minds of the consumer with data.**

A privacy-first personal data liberation platform. Users connect supported accounts through official OAuth or import official account archives, choose what may be analyzed, and receive an explainable personal profile covering interests, language, attention, behavior, personality reflection, and non-diagnostic wellbeing signals.

## Current state

Historical prior art exists in `ItMeansBigMountain/tweetBetweenTheLines`; the modern production rebuild is now active as a TypeScript/Expo universal product. See:

- [`PRODUCT_DIRECTION.md`](PRODUCT_DIRECTION.md)
- [`PRODUCT_ARCHITECTURE.md`](PRODUCT_ARCHITECTURE.md)
- [`PRIVACY_SAFETY_ARCHITECTURE.md`](PRIVACY_SAFETY_ARCHITECTURE.md) — production threat/privacy model, consent and deletion lineage, archive sandbox, explainability, bias evaluation, and clinical-safety gates
- [`PLATFORM_OAUTH_ARCHIVE_MATRIX.md`](PLATFORM_OAUTH_ARCHIVE_MATRIX.md) — official-source OAuth/API and archive-import coverage decisions for the connector registry
- [`ARCHIVE_SCHEMA_AND_FIXTURE_PLAN.md`](ARCHIVE_SCHEMA_AND_FIXTURE_PLAN.md) — deterministic user-archive parser map, upload limits, field-level category coverage, synthetic fixture policy, and provenance/versioning strategy
- [`USER_OWNED_SOCIAL_ARCHIVE_RESEARCH.md`](USER_OWNED_SOCIAL_ARCHIVE_RESEARCH.md) — cited official-source research on 20-year social archive portability, consumer archive products, local insight packs, and safety boundaries
- [`SOCIAL_LIFE_BLUEPRINT.md`](SOCIAL_LIFE_BLUEPRINT.md) — buildable product/UX/data/safety specification for the user-owned unified life timeline, themes, relationships, chapters, achievements, adventures, persuasion transparency, optional AI storylines, and personalized-video consent gates
- [`IMPLEMENTATION_BACKLOG.md`](IMPLEMENTATION_BACKLOG.md) — downstream implementation backlog for the Social Life Blueprint MVP, review gates, and specialist handoffs
- [`OPERATIONS_RUNBOOK.md`](OPERATIONS_RUNBOOK.md) — observability, backups/restore, incident response, cost controls, privacy requests, and closed-beta operations gates
- [`CLOSED_BETA_DEPLOYMENT_PLAN.md`](CLOSED_BETA_DEPLOYMENT_PLAN.md) — Git-based deployment flow, consented/synthetic E2E fixture policy, and per-platform release evidence ledger
- [`MOBILE_RELEASE_MATRIX.md`](MOBILE_RELEASE_MATRIX.md) — verified Android installable-preview URL/checksum, iOS installable-web path, native export evidence, and exact store-signing gates
- [`DURABLE_BACKEND_RUNBOOK.md`](DURABLE_BACKEND_RUNBOOK.md) — local durable adapter, PostgreSQL/queue/KMS/sandbox bindings, migrations, and recovery commands
- [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md) — production dependency-audit triage and accepted-risk boundary

## Current implementation slice

- `packages/domain` contains the tested, UI-independent personal-event normalization and profile snapshot domain.
- `packages/domain/src/safetyPolicy.ts` provides executable fail-closed contracts for consent receipts, separated processing planes, deletion lineage, insight-release gates, model provenance, and multilingual cohort readiness.
- `packages/domain/src/personalityWellbeing.ts` keeps licensed, reviewed self-report trait scoring separate from observational language reflections; unsupported locales abstain and all wellbeing output remains explicitly non-diagnostic with professional and emergency-help guidance.
- `packages/domain/src/operations.ts` provides executable production readiness, closed-beta participant, and cost-control gates that fail closed when deployment/operations evidence is missing.
- `archive_schema_registry.json` and `fixtures/archive-synthetic/social_archive_synthetic_fixtures.json` provide machine-readable parser targets and synthetic/redacted-sample fixture gates for official user archives.
- `apps/api` is a runnable local TypeScript HTTP service and injectable backend contract. Its first-party authentication boundary keeps Google/Apple account login separate from consented social linking, uses purpose/redirect/subject-bound one-time PKCE state, returns opaque app sessions, records per-source consent, and preserves linked metadata when provider revocation fails. Provider status is explicit (`available`, `unconfigured`, `pending_review`, `archive_only`, or `unavailable`) and never implies unapproved access. The existing connector flow stores AES-GCM provider-token records behind a key-provider interface and supports archive admission, tenant-scoped corrections/export/delete, health/readiness, and content/secret-free audits. Production SQL starts at `apps/api/migrations/001_durable_backend.sql`.
- `apps/mobile` is the Expo Router universal client for iOS, Android, and web. Its runnable web MVP now provides an explicitly labeled synthetic demo or consented normalized-JSON import, deterministic behavioral/interest/attention metrics, per-record provenance and derivation drill-down, limitations/confidence, corrections, complete JSON export, and browser-session deletion. It does not claim live platform connectivity, complete coverage, diagnosis, or production persistence.
- The Social Life Blueprint specification now defines the next product layer: a consented unified timeline plus explainable themes, relationships, chapters, achievements, adventures, counts/consolidations, heartbreak/recovery reflections, persuasion-pattern transparency, optional AI storylines, and personalized-video planning. Every derived object must carry source evidence, confidence, limitations, correction/hide/delete/export controls, and no-diagnosis/no-false-fact boundaries.
- Native session references use Keychain/Keystore through `expo-secure-store`; provider tokens remain server-side. Web access tokens must be delivered only through server-managed secure HttpOnly cookies and are never persisted by the client.
- Legacy Python/Django/Tweepy scripts remain source-history/prior-art only and must not be reused with their historical credentials.

## Local verification

```text
npm test
npm run typecheck
npm run build
npm run start:web
npx expo export --platform ios --output-dir dist-ios
npx expo export --platform android --output-dir dist-android
npm audit --omit=dev --json
```

Run the local API (health/privacy contract only):

```text
export LOCAL_DATA_KEY_BASE64="$(node -e "process.stdout.write(require('node:crypto').randomBytes(32).toString('base64'))")"
export OAUTH_REDIRECT_URIS="app://oauth/callback"
npm run build
npm run start:api
curl http://127.0.0.1:3001/healthz
curl http://127.0.0.1:3001/readyz
```

Run deterministic synthetic/consented-fixture API E2E and persistence/concurrency tests with `npm run test -w @tweet-between-the-lines/api`. The local server's `x-tenant-id`, `x-subject-id`, and `x-actor-id` headers are a trusted-auth-proxy development contract, not production authentication. The in-memory and atomic-file repositories and environment key provider are injectable test/local adapters; production still requires a transactional PostgreSQL binding with verified RLS, managed KMS/HSM and IAM evidence, real session verification, managed queue workers, malware scanning/sandbox infrastructure, official provider-specific code exchange/revocation adapters, provider credentials/review, rate controls, monitoring, backup/restore evidence, and deployment verification. The default local OAuth exchanger deliberately fails rather than fabricating provider access.

`npm run build` includes the production static web export at `apps/mobile/dist`. `npm run start:web` launches the local browser app. The web journey works without credentials by choosing **Use synthetic demo**; personal JSON imports require explicit consent and the normalized event fields shown in the UI. These exports verify JavaScript bundles, not signed store releases. Production hosting, live OAuth/provider archive adapters, physical-device runs, TestFlight, Android internal-track verification, durable server persistence/workers, and live infrastructure controls remain release gates and must not be represented as complete until evidence exists.

## Public web deployment evidence

- Durable public web MVP URL: `https://tweetbetweenthelines.vercel.app`.
- Immutable deployment URL: `https://tweetbetweenthelines-8x7w3cgwv-itmeansbigmountains-projects.vercel.app` (Vercel deployment `dpl_48iL5zGA17zczz25v4rNVi6xSQsg`).
- Verification command: `PLAYWRIGHT_BROWSERS_PATH=/opt/data/.cache/ms-playwright node .hermes-public-web-smoke.cjs https://tweetbetweenthelines.vercel.app`.
- Result: passed synthetic fixture intake, traceable metric/profile display, provenance/limitations, correction, JSON export, delete, and zero console/page errors.
- Deployment config: `vercel.json` builds with `npm run build` and serves `apps/mobile/dist`.
- Evidence boundary: the durable URL verifies the current static Expo web MVP from Git commit `072e95cc704452826522bb9522c44d98524e9bca`; it does not verify live OAuth/providers, durable backend operations, signed mobile releases, or production-readiness gates listed below.

## Non-negotiable boundaries

- User-owned data and user-controlled consent
- Official APIs/exports; no credential scraping
- Least-privilege OAuth and source-specific revocation
- Explainable metrics with provenance and uncertainty
- Export and complete deletion
- No mental-health diagnosis from social-media activity
- Validated self-report screening kept separate from observational signals
- Security, privacy, bias, multilingual, legal, and clinical review before public health-related claims

## Planned platform coverage

The connector registry will investigate Google/YouTube, Meta platforms, X, TikTok, Reddit, LinkedIn, Snapchat, Discord, Bluesky, Pinterest, Tumblr, Twitch, Spotify, and other material sources. Coverage will be labeled honestly as official API, official archive import, manual import, restricted, or unsupported.
