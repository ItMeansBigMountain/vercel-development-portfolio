# MusicAI profile, meme fallback, and single-song analysis pattern

Use when a MusicAI-style app needs a durable user profile and manual song analysis alongside provider playlist scans.

## Product expectations

- Treat the app as a user profile/account product, not only a provider dashboard.
- Show connected provider state and obvious connection actions on the profile/dashboard.
- Use provider profile images when available.
- If no provider avatar exists, keep the original fun meme-generator feel by using a meme/avatar fallback.
- Do not let external meme APIs be a hard dependency: attempt Imgflip or the configured meme provider, then fall back to a locally generated SVG/data URL avatar so profile pictures never break.
- Keep a public or low-friction song analyzer where users can paste a YouTube URL or type a song name and scan tracks one by one.

## Implementation pattern

1. Profile/avatar
   - Build a profile view model from the internal MusicAI account, current browser session, and connected provider profiles.
   - Avatar priority: provider image/picture/avatar URL -> generated meme URL -> local fallback asset.
   - Keep the meme generator best-effort and timeout-bounded.
   - If the meme API returns auth errors or missing data, generate a local SVG/data-URL meme avatar instead of showing a broken image.

2. Connection management
   - Keep provider cards visible from the dashboard/profile, with connected/disconnected/roadmap state.
   - The profile should reinforce “one MusicAI account, many connected providers.”

3. Single-song scanner
   - Add a route such as `/analyze-song` and JSON API such as `/api/analyze-song`.
   - Accept either `query`, `song`, or `url`.
   - Parse YouTube video IDs from `youtube.com/watch?v=`, `youtu.be/`, and shorts URLs when possible.
   - If a connected YouTube token exists, resolve richer video metadata via YouTube Data API; otherwise analyze the typed query string directly.
   - Reuse the same analyzer/cache infrastructure as playlist item analysis.
   - Cache manual song analysis with a stable key based on normalized query or provider video ID, analyzer version, and input hash.

4. Playlist analysis UX
   - When playlist analysis can take a while, default to a smaller batch such as 25 items to avoid serverless timeouts.
   - Offer larger batch sizes after the first cached pass.
   - Show a loading/progress message so “Analyze every song” does not look like a no-op.
   - Make per-song result cards visible below the aggregate summary.

## Verification

- Unit-test local meme fallback without configured meme credentials.
- Unit-test single-song cache: same query should hit cache on second analysis.
- Unit-test playlist analysis route with mocked YouTube playlist metadata/items and analyzer output.
- Add Playwright coverage for `/analyze-song` and `/api/analyze-song`.
- Production verify `/healthz`, `/analyze-song`, `/api/analyze-song`, and protected playlist-analysis behavior.
