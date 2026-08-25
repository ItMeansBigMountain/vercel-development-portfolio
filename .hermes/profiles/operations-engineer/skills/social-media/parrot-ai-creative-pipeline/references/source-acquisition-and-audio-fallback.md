# Source Acquisition and Audio-First Fallback

Use this when a creator-clipping job finds a valid public source but cannot acquire the video from the rendering host.

## Internet-first diagnosis

Before repeating local attempts, crowdsource the current failure mode from:

1. Official downloader/provider documentation.
2. Current GitHub issues and discussions.
3. Recent operator reports on relevant forums (for example, r/youtubedl).
4. Official creator pages, RSS feeds, podcast hosts, embeds, and CDNs.

Summarize consensus briefly and cite the useful sources. Do not rely only on prior model context.

## Classify before retrying

Distinguish these stages:

- **Player/API rejection** (`LOGIN_REQUIRED`, bot confirmation before formats): IP reputation, session, or player-attestation gate.
- **GVS/media rejection** (formats exist, media URL returns 403): PO-token, signed URL, client, or session binding may help.
- **Cookie failure**: exported cookies may be stale, malformed, or bound to a different IP/session. Prefer browser extraction on the same egress IP.
- **Render/upload failure**: source already exists; preserve the rendered artifact and queue metadata.

A healthy PO-token provider does not imply it can repair player/API rejection. GVS tokens cannot create media URLs when the player API refuses to return formats. After one well-instrumented deterministic retry, change route instead of looping.

## Acquisition route order

1. Existing valid retry queue and local media.
2. Exact official creator media.
3. Authenticated browser/session on the same residential egress IP.
4. Official RSS enclosure, podcast CDN, or creator-hosted direct file.
5. Rights-cleared user-provided local media.
6. Residential acquisition worker that validates and syncs media to the render host.

Never treat an embed page, thumbnail, zero-byte placeholder, process exit 0, or audio-only file as acquired video. Verify the actual file with `ffprobe` and require nonzero size, expected duration, and decodable streams.

## Audio-first fallback

When exact official audio is available but video is not:

1. Verify provenance from the creator's official page/RSS feed and retain the stable enclosure URL, not an expiring redirect.
2. Download and verify format, duration, size, and audio stream with `ffprobe`.
3. Transcribe locally with word timestamps.
4. Review the full transcript and select 20–55 second standalone moments with complete sentence boundaries.
5. Correct obvious ASR errors in displayed captions only after checking the audio; preserve meaning.
6. Render 9:16 audio-led clips with synchronized captions, episode artwork, waveform/motion, speaker identification, and clear source attribution.
7. Validate every output for 1080x1920 video, decodable audio, expected duration, and nonzero size before queue/upload.

Do not disguise audio fallback as original video footage. Titles and descriptions must state the source truthfully.

## Bounded transcription recipe

For long audio on a memory-constrained host:

- Use `faster-whisper` CPU `int8` with a small model.
- Convert and process approximately 10-minute, mono 16 kHz chunks.
- Limit CPU threads/workers.
- Write each chunk's JSON and a completion marker before advancing.
- Resume completed chunks after interruption.
- Preserve global word timestamps by adding each chunk offset.

An exit `-9` is not success. Check resource pressure, then reduce model size/concurrency and checkpoint; do not rerun unchanged.

## FFmpeg waveform pitfall

`showwaves` consumes audio, not video. Branch the graph explicitly:

```text
[0:v]...background...[bg];
[1:a]showwaves=... [wave];
[bg][wave]overlay=...,...captions...[v]
```

Map `[v]` and the original audio stream separately.

## Queue and reporting semantics

- `queue_count=0` with never-rendered deficits is blocked/partial, not success.
- Only rendered upload failures belong in an upload retry queue.
- Preserve failed source records, logs, transcripts, and valid partial media.
- Report status, uploaded URLs, queue count, and exact blocker in a laconic format.

## Session example: Huberman / Fei-Fei Li

For YouTube ID `N5AQFYtqx8Q`, the official stable RSS enclosure was:

```text
https://traffic.megaphone.fm/SCIM5701398040.mp3
```

It was verified as a complete MP3 (~2:08:12). A chunked `tiny.en` transcription produced 1,806 timestamped segments, from which five distinct 39–47 second audio-led clips were selected and rendered. The reusable lesson is the verified official-audio fallback—not this specific episode.