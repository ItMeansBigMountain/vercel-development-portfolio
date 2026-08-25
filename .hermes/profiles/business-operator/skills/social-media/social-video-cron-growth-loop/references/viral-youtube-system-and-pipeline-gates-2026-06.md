# Viral YouTube System + Pipeline Gates — 2026-06

Session learning from a faceless/newsletter YouTube pipeline hardening pass.

## Research-backed operating rules

- YouTube packaging is a billboard: title + thumbnail/on-screen first frame must create the click/stop, but retention must fulfill the promise.
- Optimize for CTR plus retention, not either alone. If CTR is high and retention drops early, the title/hook overpromised or the first beat is too slow.
- Shorts should win the first 1-3 seconds with a high-contrast curiosity hook and immediate motion/change.
- Use hook -> context -> receipts/proof -> implication -> identity/action close.
- Avoid intros, welcomes, or public source-process disclosures in Shorts metadata.
- Make title, description, narration, and on-screen text semantically aligned.
- Change visual state every 2-4 seconds: cut, zoom, caption emphasis, accent, progress, or new asset.
- Timing is a cohort test, not magic. For this user's US/Texas audience, start with Tue/Wed 12-6 PM CT, weekday 12-3 PM CT, evening 7-9 PM CT, and weekend YouTube windows; replace with Studio analytics once available.

## Script defaults

Cold-open patterns:

- `This looks like X. It is really Y.`
- `If you only saw the headline, you missed the money.`
- `Nobody is talking about the real problem with X.`

Beat timing:

- 0-3s: scroll-stop hook + strong first frame.
- 3-10s: fast context, no preamble.
- 10-35s: 2-3 receipts/examples.
- 35-55s: reversal/implication/why it matters.
- Final 3-5s: action line that loops back to the hook.

Identity/action CTA examples:

- `Build one proof today.`
- `Save the signal.`
- `Move before it becomes obvious.`

## Pipeline hardening pattern

For newsletter/faceless video automation, do not let missing auth or provider state produce a traceback or placeholder upload. It should produce a clear JSON blocker and exit safely.

Quality gates before upload:

- `python3 -m py_compile` for changed scripts.
- TTS provider is live: ElevenLabs or Google Cloud TTS. Local/flite voices are review/dry-run only unless explicitly approved.
- Prefer stock visuals: Pexels/Pixabay video, then photos, then vetted fallback. Dynamic/text-only is draft quality.
- `ffprobe` final video and require:
  - vertical 1080x1920 for Shorts/newsletter vertical lane;
  - nonzero duration;
  - audio stream present.
- Dry-run uploader must return JSON before public upload.
- Source email may only be trashed after verified YouTube `video_id`.

## Concrete fix patterns from the session

- Add explicit constants for ideal Shorts duration, max scene count, and reusable viral hook captions.
- Use `len(script["beats"])` for progress-bar denominator instead of hard-coded scene counts.
- Replace raw missing-token tracebacks with a safe JSON blocker, e.g. `blocked: true`, `error`, `detail`, and `profile`.
- Convert social video cron from script-only/no-agent to agent-driven when fresh research, viral packaging, and decision-making are expected.
- Remove missing/obsolete skill references from cron jobs and attach existing umbrella skills instead.

## Durable local artifact

The user-facing viral system doc for the faceless project was written to:

`/opt/data/HeRmEz/projects/faceless-youtube-channel/VIRAL_YOUTUBE_SYSTEM.md`

Future runs should read it when operating that project, but the class-level rules above are the reusable skill knowledge.
