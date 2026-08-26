# Viral Radar manual batch clip-up pattern — 2026-06

Use this when the user pastes several creator video URLs plus existing `CLIP_PLANS/...` directories and asks to "clip these up".

## Workflow

1. Treat the request as a batch against the listed plan directories, not as fresh discovery.
2. For each plan:
   - Read `source_metadata.json` and `edit_notes.md`.
   - Create or update `clip_manifest.json` even before source acquisition succeeds.
   - Add a concise "manual clip-up pass" section to `edit_notes.md` with selected hook, time range, output path, source attribution, and source status.
3. Use a consistent source path convention:
   - `SOURCES/<video_id>/source.mp4`
   - `EXPORTS/<plan-slug>/<video_id>-viral-radar.mp4`
4. Attempt source acquisition in the normal ladder:
   - existing local source file,
   - direct/fallback URL from manifest,
   - project downloader with logs,
   - configured external clipping provider,
   - user-provided Drive/local MP4.
5. If YouTube blocks the VPS with bot verification and provider credentials are absent, stop truthfully after manifests are prepared. Do not claim the clips were rendered.
6. Write a batch status JSON under `OUTPUTS/` listing created manifests, source blockers, provider blockers, required source file paths, and next action.

## Durable blocker/fix pattern

Do not store "YouTube download impossible" as a rule. Store the fix path:

- add YouTube cookies, commonly `/opt/data/secrets/youtube-cookies.txt` if the project supports that env/config path;
- use a residential proxy;
- configure one real provider key such as `OPUS_CLIP_API_KEY`, `CHOPPITY_API_KEY`, `VIZARD_API_KEY`, `KLAP_API_KEY`, or `MUAPI_API_KEY`;
- or place source MP4s at `SOURCES/<video_id>/source.mp4` and then render with `scripts/render_clip_manifest.py`.

## Reporting style

Keep Discord reporting short:

- list which manifests were created;
- name the exact blocker;
- give the exact source MP4 paths or credential names needed;
- avoid long debugging transcripts unless the user asks.
