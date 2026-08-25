# Internet-First YouTube Acquisition Troubleshooting

## Trigger
Use when YouTube source acquisition fails with bot confirmation, HTTP 400/403, login-required, PO-token, or cloud/VPS-only behavior.

## Research before retrying
Do not rely only on prior context or repeatedly vary local flags. First crowdsource the current state from:

1. yt-dlp official wiki: FAQ, Extractors, PO Token Guide, and EJS/JavaScript runtime guidance.
2. Recent yt-dlp GitHub issues matching the exact error, hosting class, and release date.
3. Current r/youtubedl/server-operator reports for recurrence patterns and operational workarounds.
4. Creator-owned sites, podcast RSS feeds, official hosts, and legitimate CDNs for exact alternate media.

Prefer recent primary sources. Separate official requirements from community anecdotes, and cite links in the operational report.

## Durable diagnosis pattern
Reports commonly show that a video can work on a residential laptop while failing on AWS/GCP/OVH/VPS networks. Cookies may fail when exported on one IP and used on another. Therefore classify separately:

- stale/malformed cookies;
- data-center IP reputation or temporary rate block;
- missing JavaScript challenge runtime;
- missing PO-token provider/plugin;
- provider server alive but undiscovered by yt-dlp;
- exact source unavailable or restricted.

A listening bgutil server is not proof of integration. Run verbose yt-dlp diagnostics and require evidence similar to:

```text
PO Token Providers: <provider name>
JS Challenge Providers: <available runtime/provider>
```

If diagnostics say `PO Token Providers: none`, install/configure the matching yt-dlp provider plugin in the **same Python environment that executes downloads**. If they say all JS challenge providers are unavailable, configure a supported runtime (for example Node/Deno per current yt-dlp EJS docs). Do not start another bgutil server merely because the provider is undiscovered; first check whether the expected port already has a healthy helper.

## Acquisition ladder
1. Validate any existing file with `ffprobe`; reject zero-byte/undecodable placeholders.
2. Research the current upstream recommendations and matching real-world reports.
3. Check verbose yt-dlp provider/runtime discovery.
4. Repair PO-token plugin/runtime wiring, then make one bounded retest.
5. Use browser cookies produced on the same egress IP where practical.
6. Move acquisition to a residential machine or route through an approved residential connection/proxy.
7. Search creator-owned pages, RSS enclosures, podcast hosts, and official CDNs.
8. Accept a rights-cleared user-supplied local source.

Do not loop deterministic cloud-IP failures. Reduce concurrency after suspected rate/IP blocks and avoid repeatedly challenging YouTube from the same flagged address.

## Alternate-media integrity
An official podcast MP3 can establish duration, transcript context, and truthful clip windows, but it is not a substitute for creator video when the requested product requires original footage. Record provenance and validate duration/size. Continue seeking matching video or explicitly report audio-only partial acquisition.

## Reporting style
For this user, report laconic sections:

- `Community consensus`
- `Our exact diagnosis`
- `Fix being applied`
- `Remaining blocker`

Include short raw failure excerpts in fenced blocks and links to the official/community evidence. Do not present generic speculation as a conclusion.
