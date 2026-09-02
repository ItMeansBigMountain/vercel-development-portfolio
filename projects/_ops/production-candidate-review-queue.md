# Production-candidate application review queue

Generated: 2026-09-02T17:17:55.506694+00:00

## Gate

- Vercel is development/staging only.
- Oyama must personally test and approve an Actions-traceable preview before any production work.
- Manual/untraceable Vercel deployments do not qualify.
- Current result: **0/11 candidates eligible for Oyama review**; no production promotion was performed.

## Recommended review order

### 1. tweetBetweenTheLines
- Repo: https://github.com/ItMeansBigMountain/HeRmEz (`projects/tweetBetweenTheLines`)
- Immutable preview: https://tweetbetweenthelines-2hr5230u9-itmeansbigmountains-projects.vercel.app
- Persistent preview: missing
- Browser: 2/2 strict desktop/mobile checks passed
- GitHub Actions: .github/workflows/tweet-between-the-lines-vercel-dev.yml; latest: failure
- Blocker: Remote workflow exists but its only run failed before tests/build/deploy because projects/tweetBetweenTheLines/package-lock.json was absent at remote commit 5d1fd04272fec8b46e085aa1871b2ca5e80add4f; no stable preview alias exists. Reconcile remote history/source first, then rerun Actions.

### 2. Journal AI
- Repo: https://github.com/ItMeansBigMountain/HeRmEz (`projects/journal-ai`)
- Immutable preview: https://journal-qmx4djhze-itmeansbigmountains-projects.vercel.app
- Persistent preview: missing
- Browser: 1/2 strict desktop/mobile checks passed
- GitHub Actions: missing on default branch; latest: no run
- Blocker: Preview is manual/untraceable (Vercel gitSource=null), has no stable alias, and desktop emits an unexplained 404 console error. A local workflow exists but is not on GitHub's default branch.

### 3. Coding School / Algorithm Academy
- Repo: https://github.com/ItMeansBigMountain/HeRmEz (`projects/coding-school-platform`)
- Immutable preview: https://coding-school-platform-5hh2k4xao-itmeansbigmountains-projects.vercel.app
- Persistent preview: missing
- Browser: 1/2 strict desktop/mobile checks passed
- GitHub Actions: missing on default branch; latest: no run
- Blocker: Preview is manual/untraceable (Vercel gitSource=null), has no stable alias, and mobile viewport overflows (scrollWidth > clientWidth). Local CI/preview workflow is not on GitHub's default branch.

### 4. CombatAtlas Web
- Repo: https://github.com/ItMeansBigMountain/CombatAtlas (`projects/CombatAtlas`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: No Vercel Preview-environment deployment exists; existing Vercel deployment is target=production and is not an acceptable review build. No matching GitHub Actions Vercel-development workflow is present on the repository default branch.

### 5. CombatAtlas Universal
- Repo: https://github.com/ItMeansBigMountain/CombatAtlas (`projects/CombatAtlas/mobile`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: No Vercel Preview-environment deployment exists; existing Vercel deployment is target=production and is not an acceptable review build. Local production-only workflow is not published and violates the Vercel-development-only policy.

### 6. Wornly
- Repo: https://github.com/ItMeansBigMountain/fashion-social (`projects/_archive/wornly`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: No Vercel Preview-environment deployment exists; existing Vercel deployment is target=production and is not an acceptable review build. No matching GitHub Actions Vercel-development workflow is present on the repository default branch.

### 7. Card Intel Scanner
- Repo: https://github.com/ItMeansBigMountain/HeRmEz (`projects/_archive/card-intel-scanner`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: No Vercel Preview-environment deployment exists; existing Vercel deployment is target=production and is not an acceptable review build. No matching GitHub Actions Vercel-development workflow is present on the repository default branch.

### 8. Honda Tech Upgrade
- Repo: https://github.com/ItMeansBigMountain/HeRmEz (`projects/honda-tech-upgrade`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: No Vercel Preview-environment deployment exists; existing Vercel deployment is target=production and is not an acceptable review build. No matching GitHub Actions Vercel-development workflow is present on the repository default branch.

### 9. MusicAI
- Repo: https://github.com/ItMeansBigMountain/HeRmEz (`projects/MusicAI`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: No Vercel Preview-environment deployment exists; existing Vercel deployment is target=production and is not an acceptable review build. No matching GitHub Actions Vercel-development workflow is present on the repository default branch.

### 10. BurnoutBoyz
- Repo: https://github.com/ItMeansBigMountain/HeRmEz (`projects/burnoutBoyz`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: Local gates were recorded passing, but no Vercel development project/preview or remote GitHub Actions workflow exists; final reviewer card remains blocked.

### 11. Clan War Board service
- Repo: https://github.com/ItMeansBigMountain/clan-war-board-service (`projects/osrs-plugins/services/clan-war-board-service`)
- Immutable preview: missing
- Persistent preview: missing
- Browser: not runnable; no acceptable preview URL
- GitHub Actions: missing on default branch; latest: no run
- Blocker: Standalone GitHub repo exists, but there is no GitHub Actions-backed Vercel development deployment. Azure/production migration is explicitly out of scope. RuneLite plugin verification remains Gradle/RuneLite/Plugin Hub only.

## Existing preview browser findings

- tweetBetweenTheLines: desktop/mobile 200, correct identity, no overflow/console/page/network errors (2/2 pass); still fails traceability and persistent-alias gates.
- Journal AI: mobile passes; desktop has one unexplained 404 console error (1/2 pass); preview has `gitSource=null` and no alias.
- Coding School: desktop passes; 390×844 mobile overflows horizontally (1/2 pass); preview has `gitSource=null` and no alias.

## Reconciliation notes

- GitHub currently exposes only two remote workflows in HeRmEz: tweetBetweenTheLines Vercel development and EAS preview. The only Vercel-development run failed before build/deploy.
- Local untracked workflows for Coding School and CombatAtlas are not remote CI evidence. CombatAtlas local deploy workflow also targets production and must not be used under this policy.
- Existing Vercel aliases and target=production deployments were preserved as historical baselines, not endorsed as production releases.
- `dist` is a known duplicate/misnamed tweetBetweenTheLines Vercel project and is excluded as a separate product candidate; it was not deleted.
- Static review shells and retired apps are excluded because HTTP 200 is not product readiness.

## Safety

- Production promotions: 0
- Deployments/history deleted: 0
- Aliases changed: 0
- Secrets printed or stored: no
