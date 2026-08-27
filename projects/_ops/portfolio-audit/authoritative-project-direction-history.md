# Authoritative project-direction reconciliation

Generated: 2026-08-27T03:09:31Z
Task: t_3bd6e94e
Scope: /opt/data/cache/documents/doc_76d816784680_message.txt plus recovered later/earlier Hermes conversation and Kanban evidence.

## Executive decision map

Newest explicit user/project-direction evidence wins. The strongest later source is the attached direction on task t_3cf71c36, recovered at `/opt/data/kanban/attachments/t_3cf71c36/doc_ee7fbb5cc936_message.txt`; it gives explicit dehost, consolidate, parent, and standby instructions for many of the URLs. Older June 2026 project-review/smoke-test tasks are treated as inventory/deployment evidence, not durable product direction, where they conflict with later August 2026 consolidation direction.

Important limitation: the current Vercel inventory artifact shows 403 `forbidden` / `invalidToken`, so live Vercel ownership/state could not be authoritatively refreshed from the Vercel API in this lane. GitHub inventory was readable from `/opt/data/HeRmEz/projects/_ops/portfolio-audit/github.json`; it shows `ItMeansBigMountain/stockNews` already archived, while most other named repos are unarchived. This artifact does not alter deployments or repos.

## Evidence key

- [S1] User source inventory: `/opt/data/cache/documents/doc_76d816784680_message.txt`, lines 5-64.
- [S2] Later attached user direction: `/opt/data/kanban/attachments/t_3cf71c36/doc_ee7fbb5cc936_message.txt`, lines 1-90.
- [K1] Task t_3cf71c36 body: canonical parents include tweetBetweenTheLines, Coding School, MusicAI, Journal AI, BurnoutBoyz, Policy Pit/TicVoter, and TikTok Shop commerce; preserve history and do not delete repositories.
- [K2] Task t_2b26c214 body: full-system cleanup/canonicalization/dehosting master card; same canonical parents; OSRS plugins remain Plugin Hub first and do not need Vercel.
- [K3] Task t_7767afa3 body: remove only explicitly unwanted Vercel sites while preserving GitHub history and restartability.
- [K4] Task t_de9f41d3: tweetBetweenTheLines recovered prior art from tweetBetweenTheLines, watsonAI, social-media-analysis, MusicAI OAuth patterns, and Journal AI insight patterns; preserve useful history. Session evidence: @session:researcher/20260824_004244_41ffd2 and Kanban task table.
- [K5] Task t_b5fa76dd: obsolete social-media-analysis scaffold archived and tweetBetweenTheLines canonicalized. Kanban task table.
- [K6] Task t_f7853ee4 body: Journal AI is the only parent; consolidate Journal App, Local Meeting Transcriber frontend, and other transcriber implementation; eliminate duplicate deployment/product identities.
- [K7] Task t_5a44dee3 and t_3fba1f36: Local Meeting Transcriber capabilities mapped/migrated into Journal AI; standalone shell should be retired only after verified end-to-end behavior. Session evidence: @session:researcher/20260824_004244_41ffd2.
- [K8] Task t_35c95492 body: Coding School absorbs Algorithm Academy/Algos, School, and Tutoring REPL teaching value; close standalone product/deploy assumptions.
- [K9] Task t_257a388f/t_aef86443/t_9c72176a: Coding School remains canonical, but production alias still serves the old shell and deployment remediation is blocked/pending reviewer/ops. Session evidence: @session:researcher/20260826_004419_00b48e and @session:researcher/20260826_005140_e4ad75.
- [K10] Task t_3fbc911d: Music and Music Mood are prior art to absorb into MusicAI; MusicAI keeps web/iOS/Android target.
- [K11] Task t_283b0608: Honda Tech Upgrade prior art maps into BurnoutBoyz; not Honda-only; preserve legacy history.
- [K12] Task t_d0e291f9/t_7ca4517d/t_000a4e25: Wornly is an active commerce product with web/iOS/Android and Stripe/fulfillment work. Kanban task table.
- [K13] Task t_d1c1935a/t_160aa964/t_dbf76a0d/t_ta_45077dcc: stockNews useful parsing migrates into trading-journal/catalyst feed; standalone stockNews deployment/repo retirement is pending/partly complete. Session evidence: @session:researcher/20260825_192710_bef8a6.
- [K14] Task t_bc379a4c/t_751397c2/t_1d52ee80/t_c716057f: CombatAtlas remains active and public remediation was independently re-reviewed/pass-gated. Session evidence: @session:researcher/20260825_221212_24291f.
- [K15] Task t_935c8981/t_a4e796ac: TicVoter + TicVoter REST API reconcile into a safer Policy Pit civic concept; no production relaunch until the safer direction is set.
- [K16] Task t_35725dec/t_f1628582: Store Code Content Studio and TikTok Shop Commerce consolidate into one commerce initiative/repo.
- [K17] Task t_869afd92/t_923b40d5: Cellphone Scripts becomes a GitHub-only mobile IDE copy/paste repo; no hosted website.
- [K18] Task t_f17c2e74: Cloud Automation, API Requests, docs, notebooks, Selenium, Networking, scraping, and Muscle Madness history are learning artifacts, not individual products.
- [G1] GitHub inventory artifact: `/opt/data/HeRmEz/projects/_ops/portfolio-audit/github.json`; stockNews is archived; HeRmEz, CombatAtlas, clan-war-board repos, fashion-social, local-meeting-transcriber, musicAI, Codology, tweetBetweenTheLines, etc. are visible.
- [V1] Vercel inventory artifact: `/opt/data/HeRmEz/projects/_ops/portfolio-audit/vercel.json`; Vercel API currently returns 403 `forbidden` / `invalidToken`.
- [P1] `/opt/data/HeRmEz/projects/PROJECT_REVIEW_SHEET.md` lines 17-61: June inventory classifications and earlier consolidation notes.
- [P2] `/opt/data/HeRmEz/projects/Codology/PROJECT_HANDOFF_CONTEXT.md` lines 1-31: Codology retired from active orchestration as of 2026-06-29; future target Coding School/algos.
- [P3] `/opt/data/HeRmEz/projects/stockNews/readme.md` lines 139-140: older stockNews/wutHappened consolidation note; superseded in target by later trading-journal direction [K13].
- [P4] `/opt/data/HeRmEz/projects/local-meeting-transcriber/PRODUCT_COMPLETION_PLAN.md` lines 1-41: older active build-candidate plan; superseded by later Journal AI consolidation direction [K6][K7] for product identity.

## Classification table

| Project / URL from source inventory | Classification | Canonical target / action | Evidence | Confidence |
|---|---|---|---|---|
| Kanban Board — https://technician-double-network-decrease.trycloudflare.com/kanban | canonical active | HeRmEz Kanban operations surface; not a portfolio product to dehost through Vercel. | [S1][K1] | Medium |
| Clan War Board — https://salmon-dune-01c80c60f.7.azurestaticapps.net/ | canonical active | Keep as OSRS Clan War Board service/site; current direction is sync stale Azure site to plugin features, Plugin Hub first. | [S1][K2] plus t_1d4edb50/t_98dbbc56/t_96efa923 | High |
| Coding School — https://coding-school-platform.vercel.app/ | canonical active | Teaching parent; absorbs Algorithm Academy/Algos, School, Tutoring REPL, and coding-learning context. Current production alias remediation is pending/blocked. | [S1][S2][K8][K9] | High |
| tweetBetweenTheLines — https://tweetbetweenthelines.vercel.app/ | canonical active | P0 canonical personal/social/consumer-data intelligence product; absorbs Consumer Advocate, social-media-analysis, Twitter Therapy, and selected watsonAI/OAuth prior art. | [S1][S2][K4][K5] | High |
| Wornly — https://wornly-two.vercel.app/ | canonical active | Active commerce/fashion product; preserve mature web/commerce backend and shared web/iOS/Android clients. | [S1][K12][G1] | High |
| Journal AI — https://journal-ai-sooty.vercel.app/ | canonical active | Journal parent; absorbs Journal App and transcriber/meeting-intelligence prior art. | [S1][S2][K6][K7] | High |
| Journal App — https://journal-app-five-delta.vercel.app/ | absorbed/merged | Absorb into Journal AI; eliminate duplicate deployment/product identity. | [S1][S2][K6] | High |
| MusicAI — https://musicai-rouge.vercel.app/ | canonical active | Music psychology/music parent; absorbs Music and Music Mood. | [S1][S2][K10] | High |
| Card Intel Scanner — https://card-intel-scanner.vercel.app/ | unclear / paused | June evidence says viable frontend app; no newer explicit consolidation/dehost instruction found. Keep as unclear until user decides whether it is product, demo, or archive. | [S1][P1] plus t_10e16837/t_c56ed2de/t_7f0c089f | Medium |
| Local Meeting Transcriber — https://local-meeting-transcriber-frontend.vercel.app/ | absorbed/merged | Absorb into Journal AI meeting-intelligence functionality; retire duplicate shell after verified Journal AI parity. | [S1][S2][K6][K7][P4] | High |
| Local Meeting Transcriber shell — https://local-meeting-transcriber.vercel.app/ | absorbed/merged | Same as above: duplicate/static shell, not independent product identity. | [S1][S2][K6][K7] | High |
| Honda Tech Upgrade — https://honda-tech-upgrade.vercel.app/ | absorbed/merged | Consolidate into BurnoutBoyz; broaden to all makes, preserve deterministic planner/history. | [S1][S2][K11] | High |
| Faceless YouTube Channel — https://faceless-youtube-channel-beta.vercel.app/ | dehost/delete approved | User explicitly said this did not need a website and was out of line. Preserve history only; no standalone site. | [S1][S2][K3] | High |
| Cox Elementary PTA review shell — https://cox-elementary-pta.vercel.app/ | paused/deferred + dehost | Stop hosting and put on standby so it can be resumed later. Preserve source/history. | [S1][S2][K3] | High |
| 3D React — https://3d-react-web-itmeansbigmountains-projects.vercel.app/ | archive-only / unclear | Earlier app/smoke-test evidence exists, but no later explicit active parent or dehost instruction found. Treat as archive/demo until user revives. | [S1][P1] plus t_88ef221f/t_f15890f2 | Medium |
| Addictive Mobile Games — https://addictive-mobile-games.vercel.app/ | paused/deferred | User wants app-store/iOS/Android path documented; keep as future app-store candidate, not necessarily current Vercel priority. | [S1][S2] plus t_d06a9f2e | High |
| API Requests — https://api-requests-one.vercel.app/ | dehost/delete approved | Remove Vercel URL; preserve GitHub/history if present. | [S1][S2][K3] | High |
| API.Requests — https://apirequests.vercel.app/ | dehost/delete approved | Same as API Requests; remove duplicate Vercel URL; preserve GitHub/history if present. | [S1][S2][K3][G1] | High |
| Cellphone Scripts — https://cellphonescripts.vercel.app/ | archive-only / GitHub-only | Convert to GitHub-only mobile IDE copy/paste repo; remove Vercel hosting. | [S1][S2][K17] | High |
| Cloud Automation — https://cloudautomation.vercel.app/ | archive-only / GitHub-only | Keep as learning artifact in GitHub; remove Vercel website. | [S1][S2][K18] | High |
| Consumer Advocate — https://consumer-advocate-app.vercel.app/ | absorbed/merged | Consolidate into tweetBetweenTheLines where useful; discard mismatched standalone app work. | [S1][S2][K4] | High |
| Algorithm Academy/Algos — https://algos-beta.vercel.app/ | absorbed/merged | Close standalone deployment; move useful curriculum/exercise context into Coding School. | [S1][S2][K8] | High |
| Deployment Docs — https://deploymentdocs.vercel.app/ | dehost/delete approved | Does not need a Vercel URL; preserve docs/history as GitHub/local learning/support artifact if useful. | [S1][S2][K3][K18] | High |
| Docs — https://docs-umber-two-76.vercel.app/ | dehost/delete approved | Same as Deployment Docs. | [S1][S2][K3][K18] | High |
| Jupyter Notebooks — https://jupyter-notebooks-green.vercel.app/ | archive-only / GitHub-only | No Vercel URL needed; keep notebooks as learning/research artifacts with safe offline execution context. | [S1][S2][K18] plus @session:researcher/20260606_070914_5ef402 | High |
| Legacy Source — https://legacy-src.vercel.app/ | dehost/delete approved | No Vercel URL needed; preserve as source/history only. | [S1][S2][K3] | High |
| Muscle Madness — https://musclemadness-theta.vercel.app/ | archive-only / GitHub-only | User frames it as early full-stack learning history; later learning-arc tasks include Muscle Madness history rather than a product lane. | [S1][S2][K18] | Medium-High |
| Muscle Madness API — https://musclemadness-api.vercel.app/ | archive-only / GitHub-only | Same Muscle Madness learning/history bucket unless a future user direction revives it. | [S1][S2][K18] | Medium-High |
| Music — https://music-lac-seven.vercel.app/ | absorbed/merged | Absorb useful prior art into MusicAI; remove duplicate product identity. | [S1][S2][K10] | High |
| Music Mood — https://music-mood-app-chi.vercel.app/ | absorbed/merged | Absorb useful prior art into MusicAI. | [S1][S2][K10] | High |
| Networking — https://networking-ebon.vercel.app/ | archive-only / GitHub-only | No Vercel URL needed; learning artifact. | [S1][S2][K18] | High |
| Oyama Productions Legal — https://oyama-productions-legal.vercel.app/ | canonical active | Flesh out as landing page for user/company Oyama Productions. | [S1][S2] plus t_b1b5f156 | High |
| Policy Pit — https://policy-pit-app.vercel.app/ | canonical active / consolidate target | Safer civic concept parent for TicVoter/TicVoter REST; implementation/CI pending. | [S1][K15] | High |
| Portfolio Sentiment — https://portfolio-sentiment-subscription-ap.vercel.app/ | unclear | Likely overlaps trading-journal/stockNews direction, but no explicit newer instruction naming this URL found. Do not dehost without confirmation. | [S1][K13][P1] | Medium |
| Robinhood Email Reports — https://robinhood-email-reports.vercel.app/ | unclear / likely absorb into trading ops | Adjacent to robinhood-daily/trading-journal, but no explicit newer dehost/consolidate direction found for this Vercel URL. | [S1][G1][K13] | Medium |
| School — https://school-plum-beta.vercel.app/ | absorbed/merged + dehost | No Vercel URL needed; teaching value goes into Coding School. | [S1][S2][K8] | High |
| Scraper Project — https://scraper-project-five.vercel.app/ | archive-only / GitHub-only + dehost | User explicitly said no website; keep useful scraping learning/artifact context only. | [S1][S2][K3][K18] | High |
| Selenium — https://selenium-alpha.vercel.app/ | archive-only / GitHub-only + dehost | User explicitly repeated Selenium does not need a website; keep as learning artifact. | [S1][S2][K3][K18] | High |
| Sleep Dream — https://sleep-dream-app.vercel.app/ | unclear / paused | June inventory says plan/spec review shell; no explicit later user direction found. Preserve, but do not prioritize/dehost without confirmation. | [S1][P1] | Medium |
| Social Media Analysis — https://social-media-analysis-five.vercel.app/ | absorbed/merged | Absorbed into tweetBetweenTheLines; obsolete scaffold archived. | [P1][K4][K5] | High |
| Stock News — https://stock-news-frontend-chi.vercel.app/ | absorbed/merged + dehost/archive | Newer direction consolidates stockNews into canonical trading-journal catalyst/news feed; standalone deployment/repo retirement pending/reviewed. | [S1][S2][K13][G1][P3] | High |
| Store Code Content Studio — https://store-code-content-studio.vercel.app/ | absorbed/merged | Consolidate into TikTok Shop Commerce initiative/repo. | [S1][S2][K16] | High |
| Survey Analytics — https://survey-analytics-website.vercel.app/ | unclear / archive-only candidate | June inventory says plan/spec shell; no later explicit direction found. | [S1][P1] | Medium |
| TicVoter — https://ticvoter.vercel.app/ | absorbed/merged | Reconcile into safer Policy Pit product direction; preserve early learning significance; web/iOS revival possible under Policy Pit, not standalone. | [S1][S2][K15] | High |
| TicVoter REST API — https://ticvoter-rest-api.vercel.app/ | absorbed/merged | Reconcile into Policy Pit; REST API remains separate only if the new architecture requires it. | [S1][S2][K15] | High |
| TikTok Clone — https://tiktok-clone-eta-one.vercel.app/ | unclear / archive-only candidate | No explicit later direction found; do not confuse with TikTok Shop Commerce. Treat as old demo/archive unless revived. | [S1][P1] | Medium |
| TikTok Shop Commerce — https://tiktok-shop-shopify-commerce.vercel.app/ | canonical active | Canonical TikTok Shop commerce parent/initiative; absorbs Store Code Content Studio. | [S1][S2][K16] | High |
| Tournament Wager — https://tournament-wager-app.vercel.app/ | paused/deferred | User expressed legal/security/payment-risk concern; do not build/deploy until business/legal/security scope is clarified. | [S1][S2] | High |
| Tutoring REPL — https://tutoring-repl.vercel.app/ | absorbed/merged | Consolidate into the teaching app / Coding School. | [S1][S2][K8] | High |
| Tweet Video Generator — https://tweetvideogenerator.vercel.app/ | paused/deferred + dehost current site | Research modern 2026 viral AI-video role for content creation; current website not needed. | [S1][S2] plus t_10d9aa9a | High |
| Twitter Therapy — https://twitter-therapy-app.vercel.app/ | absorbed/merged | Fully absorb into tweetBetweenTheLines reflection/emotion/narrative layer; retire duplicate active direction. | [P1][K4] plus t_c80a4a38 | High |
| Utility Scripts — https://utilityscripts.vercel.app/ | archive-only / GitHub-only | No newer active product direction found; June inventory already classed as legacy scripts/archive/docs. | [S1][P1] | Medium-High |
| Watson AI — https://watsonai.vercel.app/ | archive-only / selected prior-art absorption | User says no website; selected OAuth/analysis patterns can feed tweetBetweenTheLines/MusicAI, but no standalone site. | [S1][S2][K4] | High |
| WebCrawl — https://webcrawl-ochre.vercel.app/ | archive-only / GitHub-only + dehost | User explicitly says no website; retain useful crawling/scraping learning context only. | [S1][S2][K3][K18] | High |
| WutHappened — https://wuthappened.vercel.app/ | absorbed/merged | Older note merged it into stockNews; newer stockNews direction moves the useful news/catalyst pieces into trading-journal. | [S1][K13][P3] | High |

## Canonical active parents / initiatives

1. tweetBetweenTheLines — active P0, absorbs Consumer Advocate, social-media-analysis, Twitter Therapy, selected watsonAI/OAuth prior art. [S2][K4][K5]
2. Coding School — active teaching parent, absorbs Algorithm Academy/Algos, School, Tutoring REPL, and other teaching mini-project context. [S2][K8][K9]
3. MusicAI — active music psychology parent, absorbs Music and Music Mood. [S2][K10]
4. Journal AI — active journal/voice/meeting parent, absorbs Journal App and Local Meeting Transcriber variants. [S2][K6][K7]
5. Wornly — active commerce/fashion product. [K12][G1]
6. CombatAtlas — active martial-arts atlas; release remediation has reviewer-pass evidence. [K14][G1]
7. Clan War Board / OSRS plugin ecosystem — active OSRS lane; Azure site stale sync work pending, Plugin Hub first. [K2]
8. BurnoutBoyz — active target for Honda Tech Upgrade prior art, broader than Honda. [S2][K11]
9. Policy Pit — active safer civic concept target for TicVoter/TicVoter REST. [S2][K15]
10. TikTok Shop Commerce — active commerce initiative target for Store Code Content Studio. [S2][K16]
11. Oyama Productions landing page — active personal/company landing-page effort. [S2]
12. trading-journal / trading intelligence — active target for stockNews/wutHappened catalyst/news functionality; stockNews GitHub repo is already archived in the inventory. [K13][G1]

## Approved dehost / remove-from-Vercel set

Destructive action must still be executed by operations with credential verification and no repo deletion. The user has explicitly approved removal of these websites from Vercel or equivalent hosting: Cellphone Scripts, API Requests, API.Requests, Cloud Automation, Deployment Docs, Docs, Jupyter Notebooks, Legacy Source, School, Selenium, Networking, Scraper Project, WebCrawl, Watson AI, Faceless YouTube Channel, Cox Elementary PTA shell, current Tweet Video Generator website, and standalone Stock News after consolidation. [S2][K3][K13][K17][K18][V1]

## Contradictions and reconciliation

- Earlier June review artifacts often classified Vercel shells as deployable/live because they were smoke-testable. Later August user direction explicitly says many of those shells should not be websites. Newer August direction wins for product/hosting status. [P1][S2]
- `/opt/data/HeRmEz/projects/PROJECT_REVIEW_SHEET.md` says stockNews was the active merged portfolio news app and wutHappened was its archive; later tasks route stockNews itself into trading-journal and archive/retire stockNews. Newer trading-journal direction wins. [P1][P3][K13]
- Local Meeting Transcriber had an older standalone active completion plan; later Journal AI consolidation makes it functionality inside Journal AI, not a separate product identity. Newer Journal AI direction wins. [P4][K6][K7]
- Coding School production URL is canonical by intent, but current evidence says the public alias still served an old review shell during the latest reviewer gate and the operations remediation was blocked. Treat it as canonical active with release-state blocker, not as proof that the app is currently correct. [K9]
- Vercel API inventory could not be refreshed due 403 invalid token. Any operation to remove/dehost must first fix Vercel credentials and re-read ownership/project mapping. [V1]

## Recommendations for the downstream reviewer

1. Verify this map against parent inventory task t_70484558 before publishing a final user-facing map.
2. Treat all dehost/delete items as approved intent but pending execution; require Vercel credential repair and exact project ownership read-back before operations changes.
3. Do not rely on the `doc_ee7fbb5cc936_message.txt` cache path in task bodies; the live file is attached at `/opt/data/kanban/attachments/t_3cf71c36/doc_ee7fbb5cc936_message.txt`.
4. For unclear items (Card Intel Scanner, 3D React, Portfolio Sentiment, Robinhood Email Reports, Sleep Dream, Survey Analytics, TikTok Clone, Utility Scripts), request an explicit keep/absorb/dehost decision rather than inferring destructive action.
5. Keep GitHub history by default. Even approved dehosting should remove public hosting/aliases only, not delete repositories, unless the user later gives repo-specific delete/archive approval.
