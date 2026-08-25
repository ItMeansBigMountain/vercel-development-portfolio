# Zapier-Free Clip Review Bridge

Use this pattern when a clipping/publishing project needs Zapier-style routing/review but the user does not have Zapier premium webhooks, social publishing credentials are not ready, or upload APIs are intentionally gated behind manual review.

## Durable lesson

Do not block the clipping project on webhooks. If Zapier `Catch Hook` is unavailable, build a local/app-bridge review artifact that Zapier-compatible apps can consume later:

```text
rendered MP4 clips
→ review packet JSON/CSV/Markdown
→ Notion/Google Sheets import or Discord/email paste
→ manual/Drive/social upload after review
```

This gives the user useful workflow momentum before paying for Zapier or a posting broker.

## Recommended artifacts

For each rendered clip, include:

- title
- absolute/local clip file path
- status, usually `Needs Review`
- caption
- hashtags
- source URL
- source file
- start/end timestamps
- hook
- duration seconds from `ffprobe` when available
- size MB
- MIME type

Write three packet formats:

- `REVIEW_PACKETS/<name>.json` — machine-readable queue for future code/API actions.
- `REVIEW_PACKETS/<name>.csv` — Notion/Google Sheets import.
- `REVIEW_PACKETS/<name>.md` — Discord/email review message.

## Implementation pattern

A reusable script should accept either:

```bash
python3 scripts/build_clip_review_packet.py --manifest CLIP_PLANS/<plan>/clip_manifest.json --name <plan>-review
python3 scripts/build_clip_review_packet.py --clips-dir EXPORTS/<folder> --name <folder>-review
```

Manifest mode should preserve richer metadata from `clip_manifest.json`; directory mode should infer sane titles from MP4 filenames.

## Verification pattern

Smoke-test without relying on real copyrighted media:

```bash
python3 -m py_compile scripts/build_clip_review_packet.py
mkdir -p TMP/review-packet-test/exports TMP/review-packet-test/plan
ffmpeg -y \
  -f lavfi -i color=c=black:s=1080x1920:d=1 \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac \
  TMP/review-packet-test/exports/test-clip.mp4
python3 scripts/build_clip_review_packet.py --manifest TMP/review-packet-test/plan/clip_manifest.json --outdir TMP/review-packet-test/packets --name smoke-test
python3 scripts/build_clip_review_packet.py --clips-dir TMP/review-packet-test/exports --outdir TMP/review-packet-test/packets --name smoke-test-dir
```

Then assert JSON has clips, CSV has rows, Markdown starts with `# Clip Review Packet`, and referenced MP4 paths exist.

## When to upgrade beyond this bridge

Use this bridge as the default until there is a real recurring trigger/action loop. Upgrade to Zapier webhooks, a broker API, native OAuth uploads, or Drive-triggered Zaps only after the project reliably produces clips that need routing.
