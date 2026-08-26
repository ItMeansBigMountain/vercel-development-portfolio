# tweetBetweenTheLines: user-owned social archive value, portability, and safe local insights

Last updated: 2026-08-25

## Research question

What can a consent-first product lawfully retrieve from 20 years of user-owned social, media, and life-log accounts; where are the gaps; and what high-value insights can be computed locally without scraping, shadow profiling, clinical claims, or manipulative engagement?

## Executive findings

1. The strongest launch path is not universal live OAuth. It is a user-owned archive vault that accepts official downloads, stores provenance and parser versions, computes deterministic local insights, and labels gaps per platform. Google/YouTube, Meta, X, TikTok, Reddit, LinkedIn, Snapchat, Discord, Spotify, Tumblr, Mastodon, and similar services all expose some account data export or data request route, but the coverage, freshness, download windows, format stability, API availability, and third-party portability rights differ materially by platform.[1][2][3][4][5][6][7][8][9][10][11][12]
2. Export files are lawful user-directed inputs, but not complete truth. Official pages repeatedly warn or imply gaps: recent changes may be absent from Google Takeout; Meta/Instagram downloads can take time and expire; TikTok notes that some data may be unavailable, especially data affecting others' privacy and recent 24-48 hour categories; Reddit/Discord requests can take up to 30 days; LinkedIn omits other members' personal data and some relationship fields by privacy choice; Snapchat stores different categories for different periods and may not make all historical data available.[1][2][3][4][5][6][7][8]
3. Regional programmatic portability is emerging but uneven. TikTok's Data Portability API currently covers TikTok users in the EEA/UK for approved apps, with posts/profile, activity, DMs, and all-data scopes; LinkedIn's Member Portability APIs are for EU/EEA/Switzerland members. For non-covered users, archive upload remains the reliable path.[13][14]
4. Consumer-facing archive products prove demand for nostalgic timelines, personal search, cross-source life dashboards, and AI memory, but many are cloud-centric or engagement-habit oriented. Timehop emphasizes daily memories from camera roll and connected accounts and includes streaks/rewards; Exist emphasizes correlations across tracked behavior and subscription alignment; Gyroscope emphasizes health/wearable aggregation and coaching; mymind/Fabric/Me.bot emphasize private personal knowledge or AI memory from user-supplied notes/files/meetings rather than social-archive provenance.[15][16][17][18][19][20][21]
5. The durable opportunity for tweetBetweenTheLines is a privacy-first "archive operating system" for memory and literacy: user-owned timelines, persuasion/ad-literacy, achievements, relationship chapters, and opt-in AI media assembled from user-supplied exports, not scraped platform surfaces or inferred dossiers about non-users.

## Official export and portability capability matrix

| Platform | User can lawfully retrieve | Useful v1 categories | Gaps / caveats | Product stance |
|---|---|---|---|---|
| Google / YouTube | Google Takeout exports selected Google products, including YouTube videos, photos, account activity, and product folders; users can choose one-time or scheduled exports, file type, archive size, and delivery destination.[1] YouTube privacy settings expose watch/search/ad controls and allow data review/download/delete through Google privacy tools.[9] | YouTube watch/search history, uploads/comments where present, Google Photos metadata, ad topics when explicitly selected. | Takeout may not include changes made between request and archive creation; some exports lack timeframe slicing; photos/videos can have OS file timestamp changes while embedded metadata remains original.[1] | Supported archive import after sample validation; OAuth only for reviewed, least-privilege deltas. |
| Facebook | Meta Accounts Center/Facebook settings can export to device or external service; user chooses profile, data categories, date range, format, email, and media quality; JSON is machine-readable and downloads are password-protected.[2] | Posts, reactions, groups/pages/friends/following where present, media, ad/data logs if selected. | Export ready files are available for four days; deleted accounts cannot access account information; some data for additional profiles, including ads info, may require the main profile export.[2] | Manual import first; exact paths sample_required. |
| Instagram / Threads | Instagram Accounts Center can review account history and export to device or external service; users choose categories, date range, format, email, and media quality.[3] | Instagram posts/media captions/comments by user, likes, follows/followers, searches, ad topics if present. Threads only if Meta export confirms current files. | Instagram says export can take up to 30 days and some deleted information may be temporarily stored but not appear in downloads.[3] | Manual import first; Threads blocked until sample confirms. |
| X | X Help search result and official support snippet state users can request an archive from Settings and privacy → Your account → Download an archive of your data, confirm password, then receive email/in-app notification; X developer docs provide OAuth 2.0 PKCE, fine-grained scopes, and rate-limit tables.[4][22][23] | Archive posts, likes, follows, blocks/mutes/lists/bookmarks/DMs where present and consented; API deltas only when access tier permits. | Help page extraction failed live, so archive-request steps are cited from search-result snippet plus existing X developer docs. API limits/costs are tier and endpoint dependent; live OAuth is not an archival guarantee.[4][22][23] | Supported archive import with sample fixtures; API optional after paid/reviewed gate. |
| TikTok | TikTok support snippets state users can request a copy of data that may include username, watch video history, comment history, and privacy settings; TikTok developer docs offer Login Kit and scopes; Data Portability API is available for EEA/UK users through qualified approved apps.[5][13][24][25] | Uploaded video metadata, likes/follows/search/watch/comment history where included; DMs only under explicit scope/import. | Some data may be unavailable, including data affecting others' privacy; last 24-48 hours of some categories may be missing; Data Portability API currently returns data only for EEA/UK users and requires privacy/security review.[5][13] | Manual import first; regional Data Portability API as future reviewed lane. |
| Reddit | Reddit's data-request form returns account data after login; preparation may take up to 30 days; some data is available directly in account settings, including posts, comments, votes, recent IPs, account preferences, and authorized apps.[6] | Posts, comments, votes, saved/subscribed communities, account/app metadata. | Data package timing up to 30 days; email may be required if account access is unavailable.[6] | Supported API + archive import. |
| LinkedIn | LinkedIn data download from Settings & Privacy lets users request specific categories or a larger archive; specific categories may arrive within minutes, larger downloads within 24 hours, available for 72 hours. LinkedIn lists many categories: ad targeting, posts/shares, search queries, connections, jobs, profile, education, messages, recommendations, votes, etc.[7] | Career achievements, profile milestones, posts/articles/shares, search queries, company follows, jobs/applications, learning, ad targeting. | Desktop only; only categories applicable to the account are returned; LinkedIn does not provide People You May Know or Who Viewed Your Profile; connection email addresses may be missing due to other members' privacy choices.[7] | High-value archive import; API restricted/product-gated except regional Member Portability API. |
| Snapchat | Snapchat My Data can be requested from accounts.snapchat.com or app settings; categories include login/account info, profiles, Snap History, Saved Chat History, Memories, purchases, support, friends, location, search history, Bitmoji.[8] | Memories, public Snap/Spotlight/Snap Map metadata, saved chats, friends, location/search where included. | Snapchat says it stores different categories for different periods; not all data collected since signup may be accessible; friend/chat state can affect availability.[8] | Manual import first; media analysis opt-in only. |
| Discord | Discord account data requests cover entire account history; desktop/browser lets the user choose data, mobile requests all data; completion can take up to 30 days; verified email required.[10] | Own message rows, servers/guilds, account/activity metadata, reactions/connections where present. | OAuth is not message-history access; data request cannot be duplicated while pending and is canceled if account is deleted/disabled before completion.[10] | Archive import only for personal messages; OAuth identity/guild metadata only. |
| Spotify | Spotify's automated Download your data returns JSON packages, including playlists, streaming history for the past year, library, search queries, follows, inferences, voice input, prompts, Wrapped data, and an Extended Streaming History package for lifetime account listening when requested.[11] | Listening history, search queries, library, playlists, Wrapped metrics, taste profiles, ad/inference segments. | Extended history is separate from standard account data; precise location/voice/prompts only where applicable and permissioned.[11] | Strong first parser candidate because JSON categories are well documented. |
| Tumblr | Tumblr blog export packages each blog into a ZIP; backup includes posts HTML, media, comments CSV, messages HTML, and blog posts HTML; web only; retained 3 days; max 4 exports per blog/month.[12] | Blog posts, media metadata, comments, messaging representation. | Does not include liked posts; no export to PDF/other formats; each blog must be exported separately.[12] | Supported blog archive parser. |
| Mastodon / Fediverse | Mastodon lets users export follows, lists, blocks, mutes, blocked domains as CSV and request posts/media archive in ActivityStreams 2.0 JSON once every 7 days.[26] | Statuses/outbox, media metadata, follows/favourites/lists depending export. | Posts/media cannot currently be imported into Mastodon due to technical limits; instances may vary.[26] | Supported API + instance archive import with instance-specific manifest. |

## Consumer archive and memory product signals

| Product / category | What it proves | Gaps tweetBetweenTheLines can exploit safely |
|---|---|---|
| Timehop | Mainstream nostalgia demand: daily memories, 1-to-20+ years lookback, camera roll, Facebook/Google Photos/Dropbox/Flickr/Tumblr/Swarm connections, hide/delete controls, sharing, alerts, streaks, badges.[15][16] Timehop's own data page says social account connections and memories include photos, videos, text posts, wall posts, and check-ins from connected services and are used to show memories from this day in the past.[17] | Avoid streak pressure and ad-driven resurfacing; emphasize user-owned local archive, consent ledger, provenance, and distress controls. |
| Exist | Users pay for cross-source behavior understanding, long-term trends, correlations, weekly summaries, mood/manual tracking, and connected services; Exist states it makes money from subscriptions, not selling data.[18] | Bring the correlation value to social archives, but label correlation as descriptive, not causal/clinical; keep raw sources exportable. |
| Gyroscope | Demand exists for "track everything in one place," wearable/life data aggregation, AI coach, and one-number dashboards.[19] | Avoid health-score/diagnosis claims for social data; if health adjacent, keep to user-authored self-report instruments and non-diagnostic reflections. |
| mymind | Users want a private searchable personal store for notes/bookmarks/images/articles, with no social features, vanity metrics, invasive tracking, social pressure, collaboration, or ads according to the company manifesto.[20] | Use "private oasis" positioning for archives; compete on source provenance and time-series reconstruction. |
| Fabric | Personal AI workspaces promise files, notes, ideas, meetings, 50+ integrations, search, memory growth, and agents that know your work.[21] | For social-life archives, require explicit import and consent per source; don't let AI agents act/publish by default. |
| Me.bot / Second Me | Personal AI companions market importing notes/audio and generating/shareable presentations from user records; site claims E2E encryption/local model language.[27] | Opt-in AI media can be valuable, but must have exportable scripts, consent to use likeness/voice/images, and no simulated messages from real people without permission. |

## What can be computed locally with explicit consent

These are product-safe, deterministic or explainable computations from user-uploaded official exports and first-party OAuth records. They should run locally where possible or in a user-specific encrypted processing enclave; they must be re-computable from stored provenance.

### 1. User-owned timeline

- Normalized event stream: `posted`, `commented`, `liked`, `followed`, `searched`, `watched/listened`, `saved`, `applied`, `attended`, `location_checkin`, `profile_changed`, `milestone_added`.
- Calendar views by source, time, topic, medium, and people explicitly present in the user's own records.
- Gaps: show missing ranges, pending exports, platform retention limitations, and parser confidence. Never fill missing history with model-generated events.

### 2. Persuasion and recommendation literacy

- Ad-interest and targeting surfaces the user exported (LinkedIn Ad Targeting, Spotify Inferences, Google/YouTube ad settings/Takeout, Meta ad/data logs if included).[1][2][7][9][11]
- Recommendation-exposure diary from watch/search/listening history: repeated topics, source diversity, binge windows, creator/channel clusters, and explicit "what the platform seems to be showing me" explanations.
- Boundaries: do not infer protected classes, mental health status, political vulnerability, or susceptibility scores. Phrase as "patterns visible in your exported records," not hidden truths.

### 3. Achievements and identity chapters

- LinkedIn profile positions, education, certifications, honors, projects, publications, courses, volunteering, job applications, and articles/shares can support career timelines and achievement summaries.[7]
- YouTube/Tumblr/Reddit/X/Instagram/Facebook posts can support creator milestones, high-output periods, topic evolution, and public/project artifacts where the user owns or authored the content.
- Boundaries: no employer/reference claims beyond exported facts; distinguish original content from reshared/reblogged material.

### 4. Relationship chapters

- Build first-party interaction maps from the user's own comments/messages/replies/reactions, connection timestamps, follows, and shared events where exports include them.
- Useful outputs: "people I talked to most by era," "communities that shaped a season," "long-tail reconnect list," "messages/media I may want to preserve."
- Boundaries: treat third-party names/messages as co-subject data. Default to local-only display, redaction in exports, no public sharing, no scoring friends, no inferred intimacy/compatibility, and no automated outreach without user-authored confirmation.

### 5. Opt-in AI media from archive provenance

- Safe media modes: narrated year-in-review, timeline cards, scrapbook pages, playlist posters, creator portfolio reels, private "on this day" prompts, and user-approved voiceover from user-authored text.
- Required controls: source card for every generated scene, exact list of used records, do-not-use memories/people/topics, likeness/voice/media consent, age and sensitive-content gates, one-click delete, and export of the generated script and provenance.
- Prohibited: deepfake of another person without their consent, clinical or emotional manipulation, griefbait, engagement streak pressure, and synthetic messages from real contacts.

## Retention, provenance, and legal-safe architecture implications

1. Store a source manifest for every import: platform, request date, archive SHA-256, original filenames, parser version, source URLs, consent receipt, selected categories, quarantined files, and fields used in each insight.
2. Make incompleteness visible: per-platform retention caveats, archive expiration windows, regional API restrictions, parser sample status, and "not present in archive" rather than zero values.
3. Keep non-user data minimized: names/handles and message snippets from other people are co-subject data; default to private local rendering and redacted downstream exports.
4. Avoid scraping and credential capture: official OAuth, official exports, regional portability APIs, and user-uploaded files only. Search result snippets may inform research but are not product ingestion sources.
5. Separate observation from self-report: social activity can describe content patterns and habits; it cannot diagnose wellbeing. Clinical or personality claims require validated self-report instruments and review, not passive inference.
6. Use subscription/privacy alignment: Timehop proves nostalgia can become streak/ad driven; Exist proves users will pay for data insight when values are clear. tweetBetweenTheLines should default to paid/private rather than ad-funded persuasion.

## Recommended P0 product direction

1. Build the "Archive Vault" first: user uploads official exports, sees a source-by-source parser report, and gets a downloadable normalized timeline with provenance.
2. Prioritize parser order by structured value and safety: Spotify extended streaming JSON, LinkedIn archive, Google/YouTube Takeout, Tumblr/Mastodon structured exports, Reddit data request, X archive sample-validated, then Meta/TikTok/Snapchat/Discord after current consenting fixtures.
3. Launch with five insight packs:
   - My Timeline: personal events, seasons, and gaps.
   - Persuasion Literacy: exported ad interests, recommendation exposure, search/watch/listen loops.
   - Achievements: career/creator/project milestones from authored records.
   - Relationship Chapters: private, redacted, opt-in maps from first-party interactions.
   - AI Scrapbook: user-approved cards/reels with per-scene provenance.
4. Copy rule: say "official exports and official APIs where available" and "what your archive shows," not "complete social history" or "what platforms know about you."
5. UX rule: every insight has a "why am I seeing this?" drawer with exact records, source caveats, and delete/hide/correct controls.
6. Review gates before public beta: legal/privacy review for co-subject data, clinical-safety review for any wellbeing language, platform-terms review per API, and red-team review for archive upload sandboxing.

## Contradictions and uncertainties

- X and TikTok support pages were intermittently inaccessible to extraction. The X/TikTok archive steps above use search-result snippets plus official developer docs; before implementation, obtain fresh browser captures or user-visible official pages and preserve snapshots in the evidence ledger.[4][5][22][23][24][25]
- Platform export schemas change and official help pages usually describe categories, not stable filenames. Exact parser enablement still requires redacted consenting-user samples or platform-published machine-readable schema.
- Consumer product sites market privacy and AI claims at different depths. Treat marketing claims as positioning evidence, not verified architecture.
- Regional portability APIs are strategically important but cannot be assumed for U.S. users without platform-specific eligibility checks.

## Sources

[1] Google Account Help, "How to download your Google data", retrieved 2026-08-25: https://support.google.com/accounts/answer/3024190
[2] Facebook Help Centre, "Export a copy of your Facebook information", retrieved 2026-08-25: https://www.facebook.com/help/212802592074644
[3] Instagram Help Center, "Review and export a copy of your Instagram information", retrieved 2026-08-25: https://help.instagram.com/181231772500920
[4] X Help search result, "How to access and download your X data", retrieved 2026-08-25: https://help.x.com/en/managing-your-account/accessing-your-x-data
[5] TikTok Support search result, "Requesting your data", retrieved 2026-08-25: https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data
[6] Reddit Help, "How do I request a copy of my Reddit data and information?", retrieved 2026-08-25: https://support.reddithelp.com/hc/en-us/articles/360043048352-How-do-I-request-a-copy-of-my-Reddit-data-and-information
[7] LinkedIn Help, "Download your data", retrieved 2026-08-25: https://www.linkedin.com/help/linkedin/answer/a1339364/downloading-your-account-data
[8] Snapchat Support, "How do I download my data from Snapchat?", retrieved 2026-08-25: https://help.snapchat.com/hc/articles/7012305371156
[9] YouTube, "Privacy settings", retrieved 2026-08-25: https://www.youtube.com/intl/en_us/howyoutubeworks/user-settings/privacy/
[10] Discord Support, "Requesting a Copy of your Data", retrieved 2026-08-25: https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data
[11] Spotify Support, "Understanding your data", retrieved 2026-08-25: https://support.spotify.com/us/article/understanding-my-data
[12] Tumblr Help Center, "Export Your Blog", retrieved 2026-08-25: https://help.tumblr.com/export-your-blog
[13] TikTok for Developers, "Data Portability API Overview for TikTok Users", retrieved 2026-08-25: https://developers.tiktok.com/products/data-portability-api
[14] LinkedIn Help, "Member portability APIs", retrieved 2026-08-25: https://www.linkedin.com/help/linkedin/answer/a6214075
[15] Apple App Store, "Timehop - Memories Then & Now", retrieved 2026-08-25: https://apps.apple.com/ca/app/timehop-memories-then-now/id569077959
[16] Google Play, "Timehop - Memories Then & Now", retrieved 2026-08-25: https://play.google.com/store/apps/details?id=com.timehop&hl=en_US
[17] Timehop, "See My Data", retrieved 2026-08-25: https://www.timehop.com/see-my-data
[18] Exist, "Understand your behaviour", retrieved 2026-08-25: https://exist.io/
[19] Gyroscope, "Track Everything in One Place", retrieved 2026-08-25: https://gyrosco.pe/
[20] mymind, "mymind is the extension for your mind", retrieved 2026-08-25: https://mymind.com/
[21] Fabric, "the AI workspace that thinks with you", retrieved 2026-08-25: https://fabric.so/
[22] X Developer Platform, "OAuth 2.0 Authorization Code Flow with PKCE", retrieved 2026-08-25: https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code
[23] X Developer Platform, "X API Rate Limits", retrieved 2026-08-25: https://docs.x.com/x-api/fundamentals/rate-limits
[24] TikTok Developer Guide, "Login Kit for Web", retrieved 2026-08-25: https://developers.tiktok.com/doc/login-kit-web
[25] TikTok for Developers, "Scopes Overview", retrieved 2026-08-25: https://developers.tiktok.com/doc/scopes-overview
[26] Mastodon documentation, "Moving or leaving accounts", retrieved 2026-08-25: https://docs.joinmastodon.org/user/moving/
[27] Me.bot, "Your Personal AI Companion and Second Me", retrieved 2026-08-25: https://www.me.bot/
