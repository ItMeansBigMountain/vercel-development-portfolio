# Cross-platform clipping sources for YouTube channels

Use this when a user wants to build a clipping workflow that discovers content from non-YouTube platforms and republishes transformed clips to YouTube.

## Rumble discovery pattern

- Start with publicly visible Rumble listing pages that return server-side HTML, e.g. `https://rumble.com/editor-picks`.
- Rumble search/category/channel pages may be protected differently from listing pages. If a source returns a 403, record the source error and continue with any accessible source instead of treating the entire scan as failed.
- Parse listing cards as top-level `div.videostream thumbnail__grid--item` blocks. Avoid splitting on nested class names such as `videostream__views`, or the parser can cut off views/comments from the card.
- Extract and preserve at least: source platform, source URL, title, creator/channel, visible views, visible comments, and discovery page URL.
- Rumble listing cards often expose views/comments but not duration. Treat results as discovery leads; inspect the source page or run yt-dlp metadata before editing.

## Download/edit pattern

- Prefer a human-approved candidate workspace such as `CLIP_PLANS/<candidate>/` before downloading or clipping.
- If a Rumble video URL is technically downloadable with `yt-dlp`, allow the same local clipping path as YouTube/local files.
- For gated Rumble pages, support browser-cookie retry flags rather than declaring the source impossible:

```bash
yt-dlp --cookies-from-browser chrome "https://rumble.com/v...html"
# or pass a cookies.txt file:
yt-dlp --cookies /path/to/cookies.txt "https://rumble.com/v...html"
```

- When creating 9:16 clips from landscape sources, scale to 1920px tall before center-cropping, e.g. `scale=-2:1920,crop=1080:1920`. Scaling to 1080px wide first can make the height too small for a 1920px crop.

## YouTube publishing framing

Use stronger transformative framing than a basic repost. A good default angle is:

> What blew up on Rumble that YouTube viewers missed.

Require commentary, context, captions, source attribution, and private-first review before upload. For controversial/political personalities or claims, add a policy/copyright review checkpoint before public publishing.
