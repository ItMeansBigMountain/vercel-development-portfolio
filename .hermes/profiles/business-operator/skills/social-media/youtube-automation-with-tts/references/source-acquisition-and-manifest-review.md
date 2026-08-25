# YouTube Source Acquisition and Clip-Plan Integrity

## Purpose
Use for Viral Radar jobs that discover a creator video but cannot acquire valid source media, or whose generated clip manifest is unreviewed.

## Queue semantics
Distinguish durable states:
- **Rendered upload failure:** valid rendered media exists; preserve it in the upload retry queue with complete metadata.
- **Never-rendered source deficit:** source acquisition failed before rendering; do not call an empty upload queue success. Track it separately as `blocked_source`/backlog deficit.
- **Planning deficit:** a source was selected but no reviewed clip windows exist. This is not an upload failure and not completed work.

## Bounded acquisition ladder
For the exact creator-original source:
1. Reuse a valid local source only after `ffprobe` confirms nonzero, decodable audio/video and plausible duration.
2. Try authenticated `yt-dlp` with the approved cookie file and relevant player clients.
3. Try maintained alternatives such as pytubefix/OAuth only within the approved account-risk boundary.
4. Use a configured residential proxy when permitted.
5. Search for an official creator/podcast-hosted downloadable copy or rights-cleared local source.
6. Accept a user-supplied MP4 at the canonical source path.

Do not repeat a deterministic cloud-IP bot-check attempt unchanged. After cookies plus alternate clients fail with the same bot detection, move to a meaningfully different path: fresh residential cookies/proxy, official alternate media, or user-supplied source.

## Search discipline
“Find them” means identify and verify exact source identity, then locate legitimate obtainable media—not simply rediscover the same YouTube page. Match creator, title, duration, and episode/video ID where available. Do not use questionable piracy mirrors or unrelated footage.

## Placeholder protection
A zero-byte or undecodable `source.mp4` is a placeholder, never a source. It must fail preflight before rendering. Preserve diagnostic logs but do not count it as queued media.

## Manifest review gate
Auto-spaced windows and generic titles are planning scaffolds, not reviewed clips. Before rendering:
- Obtain transcript/audio/video context.
- Ensure each window starts with a coherent hook and ends at a natural thought boundary.
- Remove sponsor reads, intros/outros, duplicate ideas, and contextless fragments.
- Replace generic or unrelated titles with truthful claims grounded in the actual excerpt.
- Confirm five windows are materially distinct when the job requires 5/5.

Never publish a generic hook such as “money mistake” or “winners separate” when the transcript/clip does not support it.

## Completion criteria
Report success only after valid source acquisition, reviewed windows, rendered clips, externally verified uploads, and durable ledger entries. Otherwise report the precise partial state and next meaningful acquisition action.