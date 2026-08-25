# Faceless YouTube audit lessons — 2026-06

Use this when auditing or rebuilding the user's faceless/newsletter YouTube automation.

## Key workflow corrections

- **Key presence is not readiness.** Do not treat `ELEVENLABS_API_KEY` or an AI-video provider env var as enough. Preflight should make a live API/account check where possible and report whether the provider can actually render today.
- **Fail closed on quality.** If ElevenLabs or equivalent realistic TTS fails, or AI/relevant B-roll generation is unavailable, stop at storyboard/script package. Do not upload flite/static/text-slide fallback content.
- **The renderer must match the quality gate.** A script that merely checks for provider keys but still renders FFmpeg text slides/flite audio is not compliant. The generation path must actually call voice generation and B-roll generation before upload.
- **Storyboard-only is the safe intermediate.** When providers are not ready, create `source_email.json`, `script.md`, `broll_prompts.json`, and `package.json`; do not upload or trash the newsletter email.
- **Email deletion stays after verified upload.** Source/newsletter Gmail messages are trashed only after YouTube returns a verified `video_id`. Junk/spam cleanup has separate user approval, but source newsletters are protected until used.
- **OAuth is channel-specific.** Metadata cleanup may require a different token than upload. Verify `channels().list(mine=True)` owns the target videos before updating descriptions/tags.
- **Public metadata hides production.** Never expose AI/faceless/automation/source-email mechanics in public title/description/tags. Put support links in descriptions and keep source metadata local.

## Audit checklist

1. Run provider preflight.
2. Confirm target YouTube token/channel.
3. Inspect upload logs for duplicate titles, public/private status, and metadata quality.
4. Inspect renderer code: does it call real TTS and real B-roll generation, or only draw text scenes?
5. Verify upload gating: no final upload when quality providers fail.
6. Verify source-email deletion gate.
7. Keep/pause crons depending on whether one manually reviewed sample has passed.
