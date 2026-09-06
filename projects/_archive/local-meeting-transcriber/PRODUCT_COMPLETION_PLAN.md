# Local Meeting Transcriber — Completion Plan

Status: active build candidate. Current Vercel app is only a static review shell; `local-meeting-transcriber-frontend` is broken/empty on Vercel.

## Product goal
A local-first meeting/class transcriber that records or imports audio, produces transcripts, extracts summaries/action items, and archives Zoom/class meeting assets.

## MVP frontend
- Upload audio/video file.
- Optional browser microphone recording.
- Meeting list with searchable transcript archive.
- Detail page with transcript, summary, action items, speakers, timestamps.
- Export: Markdown, PDF, JSON.
- "Class archive" folder concept to match Gmail `Hermes/Archive/Zoom Meeting Assets`.

## MVP backend
- FastAPI or Django API.
- Local file storage under project data directory.
- Transcription adapter interface:
  - local Whisper/faster-whisper when available,
  - external provider only if explicitly configured.
- Summarization adapter through Hermes/LLM pipeline.
- SQLite database for meetings, transcript chunks, summaries, source email/message references.

## Integrations
- Gmail: route Zoom meeting-assets emails into label `Hermes/Archive/Zoom Meeting Assets`; optionally ingest linked metadata/attachments later.
- Calendar: attach meeting summaries to event context when appropriate.
- Drive export optional later.

## Build order
1. Replace static Vercel shell with real frontend scaffold.
2. Build backend `/health`, `/meetings`, `/upload`, `/transcribe`, `/summarize` endpoints.
3. Add SQLite schema and local storage.
4. Add a sample audio fixture and smoke test.
5. Deploy frontend + backend or choose Render/Railway for backend if Vercel serverless limits are poor for transcription.

## Acceptance criteria
- User can upload a short audio file.
- Backend returns transcript + summary.
- Frontend shows a meeting archive entry.
- Tests and live health checks pass.
