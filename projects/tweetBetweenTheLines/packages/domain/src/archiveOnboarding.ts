export type ArchiveOnboardingPlatform = {
  id: string
  label: string
  parserVersion: string
  status: 'enabled' | 'sample-required'
  officialUrl: string
  requestSteps: readonly string[]
  expected: readonly string[]
  categories: readonly string[]
  privacyWarning: string
  filenameHints: readonly string[]
}

export const ARCHIVE_INSTRUCTION_VERSION = 'tweetbetweenthelines-archive-registry@1'
export const ARCHIVE_MAX_COMPRESSED_BYTES = 250_000_000

export const ARCHIVE_ONBOARDING_PLATFORMS: readonly ArchiveOnboardingPlatform[] = [
  { id: 'x_twitter', label: 'X / Twitter', parserVersion: 'x_twitter_archive@1', status: 'enabled', officialUrl: 'https://help.x.com/en/managing-your-account/how-to-download-your-x-archive', requestSteps: ['Open Settings and privacy.', 'Choose Your account, then Download an archive of your data.', 'Verify your identity, request the archive, and wait for the X notification or email.', 'Download the ZIP without extracting or renaming it.'], expected: ['ZIP with data/tweets.js, data/like.js, and following/follower files when included'], categories: ['posts', 'likes', 'follows'], privacyWarning: 'X archives can include profile details, direct-message metadata, contacts, and ad activity. Only supported categories are imported.', filenameHints: ['twitter', 'x-', 'archive'] },
  { id: 'spotify', label: 'Spotify', parserVersion: 'spotify_archive@1', status: 'enabled', officialUrl: 'https://support.spotify.com/us/article/understanding-my-data', requestSteps: ['Open Spotify Account privacy settings.', 'Request Download your data; request Extended streaming history if you need longer coverage.', 'Wait for Spotify’s email, then download the package.', 'Upload the downloaded ZIP without changing its contents.'], expected: ['ZIP containing StreamingHistory_music_*.json, endsong_*.json, or YourLibrary.json'], categories: ['watch_history', 'likes'], privacyWarning: 'Listening history can reveal routines, interests, and approximate activity times.', filenameHints: ['spotify', 'mydata', 'extended'] },
  { id: 'mastodon_fediverse', label: 'Mastodon / Fediverse', parserVersion: 'mastodon_instance_export@1', status: 'enabled', officialUrl: 'https://docs.joinmastodon.org/user/moving', requestSteps: ['Sign in to your Mastodon instance in a browser.', 'Open Preferences, then Import and export → Data export.', 'Request or download the available archive.', 'Keep the instance export as a ZIP for upload.'], expected: ['Instance ZIP with outbox.json and relationship CSV files when provided'], categories: ['posts', 'likes', 'follows'], privacyWarning: 'Exports vary by instance and may include private or followers-only posts. Unknown files are quarantined.', filenameHints: ['mastodon', 'archive', 'export'] },
  { id: 'google_youtube', label: 'Google / YouTube', parserVersion: 'google_youtube_archive@1', status: 'sample-required', officialUrl: 'https://takeout.google.com/', requestSteps: ['Open Google Takeout and deselect all products.', 'Select YouTube and YouTube Music, then choose the history data you want.', 'Create the export and wait for Google’s download email.', 'Download a ZIP. Do not upload exports containing unrelated Google products.'], expected: ['Takeout ZIP; YouTube watch-history.json and search-history.json may be present'], categories: ['watch_history', 'searches'], privacyWarning: 'Takeout can contain unrelated mail, location, photos, or account data. Export only YouTube and YouTube Music.', filenameHints: ['takeout', 'youtube'] },
  { id: 'bluesky_atproto', label: 'Bluesky / AT Protocol', parserVersion: 'bluesky_atproto_repo@1', status: 'sample-required', officialUrl: 'https://atproto.com/guides/account-migration', requestSteps: ['Follow the official repository export or account-migration instructions for your PDS.', 'Download the repository CAR file.', 'For this ZIP-only intake, place only repo.car in a ZIP without modifying the CAR.', 'Upload that ZIP; raw CAR decoding remains deterministic and versioned.'], expected: ['ZIP containing repo.car or reviewed decoded app.bsky.* JSON records'], categories: ['posts', 'likes', 'follows'], privacyWarning: 'Repository exports can include records not shown in the public app. Review the package before upload.', filenameHints: ['bsky', 'bluesky', 'repo'] },
  { id: 'tumblr', label: 'Tumblr', parserVersion: 'tumblr_blog_export@1', status: 'sample-required', officialUrl: 'https://help.tumblr.com/export-your-blog', requestSteps: ['Open the blog’s Settings in Tumblr.', 'Choose Export, then start the export for that blog.', 'Wait until the backup is ready and download its ZIP.', 'Repeat per blog; upload one blog ZIP at a time.'], expected: ['Per-blog ZIP with posts, media, HTML, or posts.json depending on export version'], categories: ['posts'], privacyWarning: 'Media and draft/private post content may be present. Media is not analyzed in this version.', filenameHints: ['tumblr', 'blog', 'export'] },
]

export type ArchiveSelectionValidation = { ok: true; platform: ArchiveOnboardingPlatform; confidence: 'high' | 'medium'; warnings: string[] } | { ok: false; error: string }

export function validateOnboardingArchive(platformId: string, file: { name: string; size: number }): ArchiveSelectionValidation {
  const platform = ARCHIVE_ONBOARDING_PLATFORMS.find((item) => item.id === platformId)
  if (!platform) return { ok: false, error: 'Choose a supported platform first.' }
  if (!file.name.toLowerCase().endsWith('.zip')) return { ok: false, error: 'Choose the original ZIP archive. Extracted folders, JSON, CAR, TAR, and RAR files are not accepted.' }
  if (file.size <= 0) return { ok: false, error: 'The selected ZIP is empty.' }
  if (file.size > ARCHIVE_MAX_COMPRESSED_BYTES) return { ok: false, error: 'This ZIP is over the 250 MB upload limit. Request a smaller platform export or split it at the platform.' }
  const lower = file.name.toLowerCase()
  const filenameMatch = platform.filenameHints.some((hint) => lower.includes(hint))
  return { ok: true, platform, confidence: filenameMatch ? 'high' : 'medium', warnings: filenameMatch ? [] : ['The filename does not identify the platform. The secure importer must confirm the internal layout before any records are promoted.'] }
}
