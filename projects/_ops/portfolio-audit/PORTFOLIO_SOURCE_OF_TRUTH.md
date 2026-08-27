# Portfolio source of truth

Updated: 2026-08-27T03:31:20Z
Task: t_af8709bf

This is the canonical working map for the portfolio cleanup. It separates live inventory from intended product direction. No repository, deployment, domain, alias, or file-hosting state was deleted or changed by this review.

## Verified live inventory snapshot

- GitHub API: 74 visible repos; 1 archived; 15 private; owner counts {'AllRightBet': 2, 'Cup-of-Java': 1, 'EZRA-HOLDINGS': 1, 'ItMeansBigMountain': 64, 'SolidReps': 5, 'walpolsh': 1}.
- Vercel/public URL probes: 55 listed URLs; 54 returned HTTP 200; 1 failed DNS/reachability.
- Public URL reachability only proves the URL serves something right now; it does not prove Vercel account ownership, project identity, release correctness, or that the site should remain hosted.
- Vercel API blocker: every tested endpoint returned 403 forbidden with invalidToken=true. Next credential action: create a fresh Vercel access token for the intended account/team, replace VERCEL_API_TOKEN in the secret store, rerun projects/_ops/portfolio-audit/run_audit.py, and read back exact Vercel project ownership/project IDs before any dehost/delete operation.

## Keep / active

- tweetBetweenTheLines — https://tweetbetweenthelines.vercel.app/ — HTTP 200 live; title: tweetBetweenTheLines. Direction: P0 personal/social/consumer intelligence product; absorbs Consumer Advocate, Social Media Analysis, Twitter Therapy, and selected Watson AI prior art. Repo: ItMeansBigMountain/tweetBetweenTheLines
- Coding School — https://coding-school-platform.vercel.app/ — HTTP 200 live. Direction: canonical teaching product; absorbs Algorithm Academy/Algos, School, Tutoring REPL, and Codology/teaching context. Public URL is canonical by intent, but release content remains separately gated.
- MusicAI — https://musicai-rouge.vercel.app/ — HTTP 200 live; title: MusicAI — Your cross-platform music taste map. Direction: canonical music psychology product; absorbs Music and Music Mood. Repo: ItMeansBigMountain/musicAI
- Journal AI — https://journal-ai-sooty.vercel.app/ — HTTP 200 live; title: Journal AI. Direction: canonical journal/voice/meeting intelligence parent; absorbs Journal App and Local Meeting Transcriber functionality.
- Wornly — https://wornly-two.vercel.app/ — HTTP 200 live; title: Wornly — Shop what’s heating up. Direction: active fashion/social commerce product; GitHub source is fashion-social. Repo: ItMeansBigMountain/fashion-social
- CombatAtlas — no listed Vercel URL in source inventory. Direction: active martial-arts atlas; no Vercel URL was in the 55-URL source list, GitHub repo is active. Repo: ItMeansBigMountain/CombatAtlas
- Clan War Board — https://salmon-dune-01c80c60f.7.azurestaticapps.net/ — HTTP 200 live; title: Clan War Board | Old School RuneScape Clan Battles. Direction: active OSRS service/plugin lane; Azure site remains live, Plugin Hub path comes first. Repo: ItMeansBigMountain/clan-war-board-osrs + ItMeansBigMountain/clan-war-board-service
- BurnoutBoyz — no listed Vercel URL in source inventory. Direction: active auto/planning target for Honda Tech Upgrade prior art; no listed Vercel URL for the target itself.
- Policy Pit — https://policy-pit-app.vercel.app/ — HTTP 200 live. Direction: safer civic product target for TicVoter/TicVoter REST.
- TikTok Shop Commerce — https://tiktok-shop-shopify-commerce.vercel.app/ — HTTP 200 live. Direction: canonical commerce initiative; absorbs Store Code Content Studio.
- Oyama Productions Legal — https://oyama-productions-legal.vercel.app/ — HTTP 200 live. Direction: active landing-page/company presence effort for Oyama Productions.
- trading-journal / trading intelligence — no listed Vercel URL in source inventory. Direction: active target for stockNews and WutHappened catalyst/news functionality; stockNews GitHub repo is already archived. Repo: ItMeansBigMountain/stockNews archived
- Kanban Board — https://technician-double-network-decrease.trycloudflare.com/kanban/ — unreachable: URLError [Errno -2] Name or service not known. Direction: HeRmEz Kanban operations surface; not a Vercel product/dehost target.

## Consolidate into target

Destructive cleanup is pending approval/execution after the target has preserved the useful history/functionality.

- Journal App — https://journal-app-five-delta.vercel.app/ — HTTP 200 live; title: Journal AI. Target: Journal AI. duplicate Journal product identity; live URL already titles as Journal AI.
- Local Meeting Transcriber — https://local-meeting-transcriber-frontend.vercel.app/ — HTTP 200 live; title: LMT. Target: Journal AI. move meeting/transcription capability into Journal AI before retiring duplicate shell.
- Local Meeting Transcriber shell — https://local-meeting-transcriber.vercel.app/ — HTTP 200 live. Target: Journal AI. duplicate/static shell; retire only after Journal AI parity is verified.
- Honda Tech Upgrade — https://honda-tech-upgrade.vercel.app/ — HTTP 200 live; title: Honda Tech Upgrade. Target: BurnoutBoyz. preserve useful planner/history and broaden beyond Honda-only.
- Consumer Advocate — https://consumer-advocate-app.vercel.app/ — HTTP 200 live. Target: tweetBetweenTheLines. use only fitting consumer/social intelligence pieces.
- Algorithm Academy/Algos — https://algos-beta.vercel.app/ — HTTP 200 live. Target: Coding School. move useful exercises/curriculum into Coding School.
- School — https://school-plum-beta.vercel.app/ — HTTP 200 live. Target: Coding School. preserve useful school/teaching context, then remove standalone website after credential-safe project read-back.
- Music — https://music-lac-seven.vercel.app/ — HTTP 200 live. Target: MusicAI. preserve music prior art inside MusicAI.
- Music Mood — https://music-mood-app-chi.vercel.app/ — HTTP 200 live. Target: MusicAI. preserve music psychology/mood prior art inside MusicAI.
- Social Media Analysis — https://social-media-analysis-five.vercel.app/ — HTTP 200 live. Target: tweetBetweenTheLines. obsolete scaffold already maps into tweetBetweenTheLines.
- Twitter Therapy — https://twitter-therapy-app.vercel.app/ — HTTP 200 live. Target: tweetBetweenTheLines. absorb reflection/emotion/narrative layer.
- Store Code Content Studio — https://store-code-content-studio.vercel.app/ — HTTP 200 live. Target: TikTok Shop Commerce. same commerce initiative.
- TicVoter — https://ticvoter.vercel.app/ — HTTP 200 live. Target: Policy Pit. preserve early app/learning value under safer civic concept.
- TicVoter REST API — https://ticvoter-rest-api.vercel.app/ — HTTP 200 live. Target: Policy Pit. keep API only if the new Policy Pit architecture needs it.
- Tutoring REPL — https://tutoring-repl.vercel.app/ — HTTP 200 live. Target: Coding School. fold teaching snippets/examples into Coding School.
- Stock News — https://stock-news-frontend-chi.vercel.app/ — HTTP 200 live; title: StockNewsFrontend. Target: trading-journal / trading intelligence. standalone product retires after catalyst/news parsing is preserved.
- WutHappened — https://wuthappened.vercel.app/ — HTTP 200 live. Target: trading-journal / trading intelligence. older stockNews relationship now routes onward to trading-journal.

## Paused / deferred

- Addictive Mobile Games — https://addictive-mobile-games.vercel.app/ — HTTP 200 live. Direction: future iOS/Android app-store candidate; document native/store path before prioritizing Vercel.
- Tournament Wager — https://tournament-wager-app.vercel.app/ — HTTP 200 live. Direction: deferred because legal/payment/security risk is unresolved.
- Tweet Video Generator — https://tweetvideogenerator.vercel.app/ — HTTP 200 live. Direction: future 2026 viral AI-video/content idea research; current website is not needed.

## GitHub / archive-only

Keep history/source. Remove public hosting only where it is also in the approved dehost queue below.

- Cellphone Scripts — https://cellphonescripts.vercel.app/ — HTTP 200 live. Direction: GitHub-only mobile IDE copy/paste repo; remove Vercel hosting after credential-safe read-back.
- Cloud Automation — https://cloudautomation.vercel.app/ — HTTP 200 live. Direction: learning artifact / future learning arc history; GitHub/local only.
- Deployment Docs — https://deploymentdocs.vercel.app/ — HTTP 200 live. Direction: docs/support artifact; no standalone website needed.
- Docs — https://docs-umber-two-76.vercel.app/ — HTTP 200 live. Direction: docs/support artifact; no standalone website needed.
- Jupyter Notebooks — https://jupyter-notebooks-green.vercel.app/ — HTTP 200 live. Direction: learning/research notebooks; no Vercel hosting needed.
- Legacy Source — https://legacy-src.vercel.app/ — HTTP 200 live. Direction: source/history only.
- Muscle Madness — https://musclemadness-theta.vercel.app/ — HTTP 200 live. Direction: early full-stack learning history; preserve repo/history, not active product.
- Muscle Madness API — https://musclemadness-api.vercel.app/ — HTTP 200 live. Direction: early full-stack learning history; preserve repo/history, not active product.
- Networking — https://networking-ebon.vercel.app/ — HTTP 200 live. Direction: learning artifact; no Vercel hosting needed.
- Scraper Project — https://scraper-project-five.vercel.app/ — HTTP 200 live. Direction: scraping learning artifact; no website needed.
- Selenium — https://selenium-alpha.vercel.app/ — HTTP 200 live. Direction: learning artifact; no Vercel hosting needed.
- Watson AI — https://watsonai.vercel.app/ — HTTP 200 live. Direction: no standalone website; selected patterns may feed tweetBetweenTheLines/MusicAI.
- WebCrawl — https://webcrawl-ochre.vercel.app/ — HTTP 200 live. Direction: crawling/scraping learning artifact; no website needed.

## Approved dehost/delete queue

Important: these are approvals/intent for hosting cleanup only. They are not executed. Before any destructive action, operations must repair Vercel credentials, verify the intended account/team, read back the exact project/alias ownership, and preserve GitHub/local history unless the user gives repo-specific delete approval.

- Cellphone Scripts — https://cellphonescripts.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- API Requests — https://api-requests-one.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- API.Requests — https://apirequests.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Cloud Automation — https://cloudautomation.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Deployment Docs — https://deploymentdocs.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Docs — https://docs-umber-two-76.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Jupyter Notebooks — https://jupyter-notebooks-green.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Legacy Source — https://legacy-src.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- School — https://school-plum-beta.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back; also consolidate useful code/context into Coding School.
- Selenium — https://selenium-alpha.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Networking — https://networking-ebon.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Scraper Project — https://scraper-project-five.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- WebCrawl — https://webcrawl-ochre.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Watson AI — https://watsonai.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Faceless YouTube Channel — https://faceless-youtube-channel-beta.vercel.app/ — HTTP 200 live; title: Faceless YouTube Channel. Pending action: remove/dehost public site after credential-safe project read-back.
- Cox Elementary PTA review shell — https://cox-elementary-pta.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Tweet Video Generator — https://tweetvideogenerator.vercel.app/ — HTTP 200 live. Pending action: remove/dehost public site after credential-safe project read-back.
- Stock News — https://stock-news-frontend-chi.vercel.app/ — HTTP 200 live; title: StockNewsFrontend. Pending action: remove/dehost public site after credential-safe project read-back.

## Unresolved / needs explicit user decision

Do not dehost, delete, or merge these without a new keep/absorb/archive decision.

- Card Intel Scanner — https://card-intel-scanner.vercel.app/ — HTTP 200 live; title: Card Intel Scanner. Decision needed: live frontend exists; no newer explicit keep/absorb/dehost direction found.
- 3D React — https://3d-react-web-itmeansbigmountains-projects.vercel.app/ — HTTP 200 live; title: 3 Dimentional App. Decision needed: older demo/app evidence exists; no newer active parent/dehost instruction found.
- Portfolio Sentiment — https://portfolio-sentiment-subscription-ap.vercel.app/ — HTTP 200 live. Decision needed: likely adjacent to trading-journal/stockNews, but no explicit instruction naming this URL.
- Robinhood Email Reports — https://robinhood-email-reports.vercel.app/ — HTTP 200 live. Decision needed: adjacent to trading ops, but no explicit newer dehost/consolidate direction for this Vercel URL.
- Sleep Dream — https://sleep-dream-app.vercel.app/ — HTTP 200 live. Decision needed: older plan/spec shell; no newer explicit user direction found.
- Survey Analytics — https://survey-analytics-website.vercel.app/ — HTTP 200 live. Decision needed: older plan/spec shell; no newer explicit user direction found.
- TikTok Clone — https://tiktok-clone-eta-one.vercel.app/ — HTTP 200 live. Decision needed: old demo; do not confuse with TikTok Shop Commerce.
- Utility Scripts — https://utilityscripts.vercel.app/ — HTTP 200 live. Decision needed: older inventory says legacy utility scripts/archive/docs, but no newer explicit keep/dehost instruction names this URL.

## Reconciled contradictions

- Newer explicit user direction from the attached portfolio cleanup note wins over older June smoke-test/project-review artifacts. A live HTTP 200 Vercel shell can still be an intended dehost/archive item.
- Stock News is both live at its old frontend URL and archived on GitHub; the intended direction is to preserve useful parsing/catalyst functionality inside trading-journal/trading intelligence and retire standalone Stock News hosting after safe verification.
- Journal App and Local Meeting Transcriber have older standalone app evidence, but current direction makes Journal AI the parent product identity.
- Coding School is the canonical teaching parent by direction, while recent reviewer evidence separately says the production alias still needs release remediation. Treat product direction and release correctness as separate facts.

## Source artifacts checked

- projects/_ops/portfolio-audit/inventory.json
- projects/_ops/portfolio-audit/INVENTORY.md
- projects/_ops/portfolio-audit/authoritative-project-direction-history.md
- /opt/data/cache/documents/doc_76d816784680_message.txt
- /opt/data/kanban/attachments/t_3cf71c36/doc_ee7fbb5cc936_message.txt

## Audit trail

- `python3 projects/_ops/portfolio-audit/run_audit.py` refreshed inventory at 2026-08-27T03:31:03Z and returned the same key counts: 74 GitHub repos, 55 listed deployments, 54 reachable HTTP 200, 1 unreachable, Vercel invalidToken blocker.
- `python3 -m py_compile projects/_ops/portfolio-audit/run_audit.py` passed.
- `python3 -m json.tool projects/_ops/portfolio-audit/inventory.json` passed.
- `git diff --check -- projects/_ops/portfolio-audit` passed.
- Coverage check: all 55 deployment labels from inventory.json are represented in this map. Active initiatives without a listed deployment URL in the source inventory are noted in Keep / active: CombatAtlas, BurnoutBoyz, and trading-journal / trading intelligence.
