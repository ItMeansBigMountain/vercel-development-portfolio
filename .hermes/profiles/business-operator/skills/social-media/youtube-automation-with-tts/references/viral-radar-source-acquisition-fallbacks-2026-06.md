# Viral Radar source acquisition fallbacks — 2026-06

Use this when Viral Radar needs source video media from a creator URL and YouTube blocks a VPS/headless downloader with `Sign in to confirm you’re not a bot`.

## Durable lesson

Before switching to paid clipping APIs, first harden and test the existing source-acquisition path. The correct order for this user's Viral Radar lane is:

1. Use an existing local/cached source MP4 if present.
2. Use an official/archive/direct MP4 fallback URL if the manifest provides one.
3. Try the maintained local downloader stack (`yt-dlp`) with compatibility options.
4. If local download still fails due to YouTube bot verification, require one of:
   - browser/exported cookies,
   - logged-in browser cookie source,
   - residential proxy,
   - user-provided Drive/local source MP4,
   - or only then an official clipping/import API such as OpusClip/Choppity/Vizard/Klap/MuAPI.

## Local downloader hardening pattern

- Keep `yt-dlp` current before debugging YouTube extraction issues.
- Try multiple YouTube clients, not just one: `mweb,web_safari,tv,ios,android`.
- Use PO-token/bgutil provider if already installed.
- Use Node as a JS runtime when available for signature/challenge handling.
- Respect env-driven auth/network inputs:
  - `YOUTUBE_COOKIES_FILE`
  - `YTDLP_COOKIES_FILE`
  - `YTDLP_COOKIES_FROM_BROWSER`
  - `YTDLP_PROXY`
  - `HTTPS_PROXY`
  - `HTTP_PROXY`

## Important pitfall

Do not present external clipping APIs as the first/only fix when the user asks to fix the current system. First patch and smoke-test the current downloader. If the smoke test still returns YouTube bot verification, report that as a real platform/IP/auth blocker and name the minimum missing input: cookies, proxy, local/Drive MP4, or provider API key.

## Reporting pattern

Be concise and separate:

- **Fixed locally:** script/code/version changes made.
- **Verified:** exact smoke command/result.
- **Still blocked by:** the remaining external requirement.

Avoid implying the pipeline is fixed if source acquisition still needs cookies/proxy/source media/provider credentials.
