# YouTube Data API trend ingestion notes

Use this reference when a user wants to discover trending/viral YouTube videos, not just summarize a single supplied URL.

## Credential modes

For public video metadata and trend discovery, try credentials in this order:

1. `YOUTUBE_API_KEY` for public reads such as `videos.list(chart=mostPopular)` and `search.list(order=viewCount)`.
2. `GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json` or an explicit `--credentials` flag if the project has service-account JSON and the user says that project has YouTube Data API enabled.
3. User OAuth for channel-private operations: uploads, private channel reads, YouTube Analytics, or actions that must act as the user's YouTube channel.

Never print service-account JSON contents or private keys. It is safe to report path, project id, client email, file mode, and whether a private key field exists.

## Minimal verification probe

Before building a larger pipeline, run one cheap API call and report the actual result:

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    "/path/to/service-account.json",
    scopes=["https://www.googleapis.com/auth/youtube.readonly"],
)
yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
resp = yt.videos().list(
    part="snippet,statistics,contentDetails",
    chart="mostPopular",
    regionCode="US",
    maxResults=3,
).execute()
print([(i["id"], i["snippet"]["title"]) for i in resp.get("items", [])])
```

## Common API responses

- `accessNotConfigured` / "YouTube Data API v3 has not been used ... or it is disabled" means the credential's Google Cloud project does not currently have `youtube.googleapis.com` enabled, or enablement has not propagated. Do not claim success; tell the user which credential path/project was tested and what Google returned.
- `youtubeSignupRequired` or no linked channel usually means the credentials are not tied to a YouTube channel. Use user OAuth for channel-private workflows.
- Service-account JSON can be valid for Google Cloud/Workspace tasks while still failing YouTube Data API if the exact project behind the key lacks API enablement.

## Trend discovery fields to request

For candidate ranking, fetch:

- `snippet.title`, `snippet.channelTitle`, `snippet.publishedAt`
- `contentDetails.duration`
- `statistics.viewCount`, `statistics.commentCount`, `statistics.likeCount` when available

Prefer long-form candidates by parsing ISO-8601 durations and filtering for 20+ minutes before clipping analysis.

## Long-form viral clipping pipeline pattern

Use this pattern when the user wants a standalone clipping/trend-arbitrage channel that discovers long-form viral videos (podcasts, interviews, debates) and turns them into short-form ideas.

1. **Keep discovery separate from publishing.** Public YouTube Data API reads can use API keys/service accounts; uploads, private channel reads, and channel management require user OAuth with `https://www.googleapis.com/auth/youtube.upload`.
2. **Start from seeded niches and people.** Keep a small config of seed queries and relevance keywords, e.g. controversial public figures, founder/money/AI podcasts, or other niche clusters the user requests.
3. **Search for long-form candidates.** Use `search.list(order=viewCount, type=video, q=<seed>)`, then enrich with `videos.list(part=snippet,statistics,contentDetails)` and `channels.list(part=statistics)`.
4. **Rank by clip potential, not just total views.** Score candidates using a weighted mix of views-per-day, comment density, creator scale/subscribers, duration, recency, and keyword relevance.
5. **Create one physical workspace per candidate.** A `CLIP_PLANS/<sanitized-title-or-id>/` folder should hold metadata JSON, transcript files, edit notes, and eventual clip specs. This makes human review and later automation easier than burying candidates in one flat CSV.
6. **Select segments only after transcript/timestamp review.** For each candidate, pull transcripts when available and identify hooks, conflicts, surprising claims, emotional peaks, or self-contained explanations before clipping.
7. **Require transformation and attribution.** Avoid lazy reuploads. Clip plans should include commentary, captions, context, analysis, or other transformative framing plus the original source URL/channel attribution.
8. **Smoke-test with a concrete query.** For example, a query like `Andrew Tate podcast` should return long-form candidates from viral/interview channels, create at least one clip workspace, and preserve source URLs before any upload work begins.

### Minimal local project shape

For a reusable clipping project, prefer:

- `CONFIG/viral_channels.json` — niche seeds, keywords, duration thresholds, and scoring weights.
- `scripts/viral_channel_discovery.py` — discovery/ranking CLI with `--query`, `--credentials`, `--limit`, and `--create-plans` style flags.
- `scripts/clip_video.py` — local ffmpeg helper for approved timestamp ranges only.
- `scripts/upload_to_youtube.py` — upload helper that exits clearly when user OAuth token is missing.
- `CLIP_PLANS/` — candidate workspaces containing source metadata, transcript/edit notes, and planned clips.
