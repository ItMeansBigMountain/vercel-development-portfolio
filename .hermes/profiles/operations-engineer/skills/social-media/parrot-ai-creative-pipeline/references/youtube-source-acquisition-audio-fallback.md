# YouTube Source Acquisition and Audio-First Fallback

## Trigger
Use when a public creator video is discoverable but YouTube rejects automated acquisition with `LOGIN_REQUIRED`, bot confirmation, HTTP 403/400, or invalid/zero-byte media.

## Research-first diagnosis
Before repeatedly changing flags, crowdsource the current failure mode from:

1. yt-dlp official FAQ and PO-token/EJS guides.
2. Current yt-dlp GitHub issues matching the exact error and hosting environment.
3. Recent operator reports from r/youtubedl or comparable technical forums.
4. Creator-owned pages, RSS feeds, podcast hosts, embeds, and official mirrors.

Separate evidence from inference and keep source URLs. Do not assume cookies or PO tokens solve every YouTube gate.

## Failure classification

- **GVS/format 403:** PO-token or JS-challenge tooling may help.
- **Player API `LOGIN_REQUIRED` before formats:** commonly an IP/player-attestation gate. A GVS PO token cannot fix a rejection that occurs before media URLs are returned.
- **Cookies work locally but fail on VPS:** cookies and request IP/session context may not match; avoid endless cookie refresh loops.
- **Zero-byte or `ffprobe` failure:** acquisition failed. Never queue or render it as valid media.

Use bounded attempts. Once the same deterministic class is reproduced across current yt-dlp + cookies + configured PO-token path, change the acquisition route rather than retrying unchanged.

## Acquisition ladder

1. Exact creator-owned direct media or official CDN/RSS enclosure.
2. Exact legitimate creator mirror.
3. Current yt-dlp with supported JS runtime and PO-token provider where the failure class fits.
4. Residential acquisition worker/home device, followed by validated sync to the render host.
5. Rights-cleared local source supplied by the user.
6. If exact official audio exists, use the audio-first fallback below.

## Audio-first fallback

When full video is unavailable but the creator publishes the same episode as an official MP3:

1. Download from the stable RSS enclosure/CDN URL; avoid temporary signed redirects.
2. Verify nonzero size, codec, duration, and provenance with `ffprobe` and the official feed/page.
3. Transcribe locally with timestamped segments and words.
4. Select real, self-contained 20–55 second moments from transcript meaning—not evenly spaced or generic windows.
5. Cut exact audio and render a clearly audio-led vertical clip using synchronized captions, speaker labels, episode artwork, waveform/motion graphics, licensed contextual visuals, and explicit source attribution.
6. Use truthful titles based on the spoken moment; never imply original video footage when it is not present.

## Memory-bounded transcription
For long episodes or low-memory hosts:

- Probe available RAM and disk first.
- Prefer CPU `int8`, a small model, low thread count, and one worker.
- Decode to temporary 16 kHz mono chunks (for example 10 minutes each).
- Write each chunk transcript atomically plus a completion marker.
- Delete temporary WAV chunks after successful transcription.
- Resume from checkpoints after interruption; never restart a two-hour file from zero.
- Preserve word-level timestamps when captions need synchronization.

An OS exit `-9` is a signal to reduce model/worker/chunk pressure, not to repeat the same command unchanged.

## Queue semantics

- An empty upload queue is not success when source-ready clips were never rendered.
- Distinguish `source_blocked` deficits from rendered upload failures.
- Only rendered upload failures belong in the upload retry queue.
- Preserve provenance, transcript, selection rationale, and failure logs.

## Verification

- Official source provenance recorded.
- Media passes `ffprobe` and duration is plausible.
- Transcript timestamps map to the source.
- Clip is self-contained and title matches speech.
- Visual treatment is truthful about audio-only provenance.
- Upload success requires a verified public video ID/URL, not merely exit code 0.
