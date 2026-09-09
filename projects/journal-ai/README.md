# Journal AI

A local-first clickable journal MVP for quick self-reflection.

## Status

The original Vite/TypeScript meeting MVP remains in `frontend/journal-app`. A shared Expo Router client now lives in `apps/mobile` and exports for web, iOS, and Android.

Canonical public preview (not production):
- https://journal-bshzaek8o-itmeansbigmountains-projects.vercel.app

The retired aliases `journal-ai-sooty.vercel.app` and `journal-app-five-delta.vercel.app` are intentionally not canonical.

The Expo client supports on-device journals, durable local/offline changes, tombstone deletion, journal export, consent-gated meeting import, processing status, notification permission/reminders, optional OAuth deep-link handling, and native secure session storage. Journal bodies and meeting metadata currently use platform app storage and are not encrypted at rest. OAuth, real transcription, verified media erasure, and account sync remain future integrations; do not claim those paths are live.

## Universal client

```bash
cd apps/mobile
npm install
npm run typecheck
npx expo-doctor
npm run build:web
npm run build:ios
npm run build:android
```

`eas.json` contains development, internal-preview, and production App Bundle profiles. Store-signing credentials, TestFlight submission, Android internal-track upload, physical-device QA, and any production deployment are intentionally outside this preview phase; local Metro exports are not releases.

## Architecture notes

- Meeting recording/transcription is planned as a consented Journal AI capability, not a separate product fork.
- See `MEETING_INTELLIGENCE_DIRECTION.md` for the audited Local Meeting Transcriber migration map, reusable .NET/Expo/WhisperX/pyannote/Ollama/Terraform pieces, and security/privacy gates.
- Do not archive `../local-meeting-transcriber` until the migrated behavior is implemented, verified, and traceable back to the source history.
- The legacy Django API is reference-only and must not be used as the Journal AI preview or backend without an authenticated privacy-first rewrite.

## Local development

```bash
cd apps/mobile
npm install
npm run typecheck
npm run build:web
npx expo start --web
```

The legacy Vite demo can still be checked without making it canonical:

```bash
cd frontend/journal-app
npm install
npm test
npm run build
```

## Environment

Local configuration should come from `.env`. Do not commit real secrets. Keep committed examples in `.env.example`.
