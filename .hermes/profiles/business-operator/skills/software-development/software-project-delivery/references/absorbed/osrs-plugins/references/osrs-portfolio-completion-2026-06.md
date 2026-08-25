# OSRS plugin portfolio completion notes (2026-06)

Use this reference when the user asks to finish/review the OSRS RuneLite plugin portfolio after GitHub/project-folder reconciliation.

## Current portfolio shape

- Active container: `/opt/data/HeRmEz/projects/osrs-plugins`.
- Individual GitHub repos may also exist as sibling folders under `/opt/data/HeRmEz/projects/<repo-name>-osrs` after portfolio imports.
- Treat the `osrs-plugins` child repos as the active development workspace unless the user explicitly asks to work from a sibling clone.
- Do not let Vercel deployment block OSRS completion: these are Java/RuneLite plugins, not Vercel web apps. Completion means Gradle build/test, manual RuneLite QA, docs/screenshots, GitHub push, and plugin-hub submission prep.

## Verified build-review pattern

Sequential Java 11 check used successfully:

```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
cd /opt/data/HeRmEz/projects/osrs-plugins
for d in */; do
  [ -f "$d/build.gradle" ] || continue
  [ "$d" = "osrs-plugins-boilerplate/" ] && continue
  (cd "$d" && chmod +x gradlew && ./gradlew clean test assemble --no-daemon --console=plain)
done
```

Durable report location from the 2026-06 review:

- Build JSONL: `/opt/data/HeRmEz/projects/_ops/osrs-review-20260614/build-report.jsonl`
- Product summary: `/opt/data/HeRmEz/projects/_ops/osrs-review-20260614/summary.md`
- Static product review JSON: `/opt/data/HeRmEz/projects/_ops/osrs-product-review.json`

That run passed `17/17` active child plugins.

## Product completion order

Ship-first / polish-first:

1. `AccountLegacyCard` — serious side-panel/API product; toolbar/sidebar, player-menu lookup, hiscore/API behavior.
2. `BossReadinessScore` — flagship side-panel/API product; verify compact UI, OSRS Wiki URLs, and modern gear accuracy.
3. `RivalRadar` — make this the consolidation target for rival/race/nemesis/KC comparison ideas.
4. Clan activity panel — consolidate `WhosGrindingClanPanel`, `ClanGrindHeatmap`, and possibly `GroupIronProgressBoard`.
5. Lightweight utility publish batch — `IceBarrageTimer`, `BossStreaks`, `SkillStreaks`, `NameChangeWatcher`, `PersonalProgressTimeline`, `CompetitionOverlay`.

Consolidate rather than publish separately unless user revives them explicitly:

- Into `RivalRadar`: `BossKCRivalLookup`, `BossRaceCreator`, `SkillNemesis`, `SkillRaceCreator`.
- Into `AccountLegacyCard`: `SmartHiscoreLookup`, unless manual testing proves it has a distinct UX.

## Reporting guidance

For this user, keep OSRS portfolio reports concise in Discord:

- build pass/fail count
- report paths
- strongest repos
- thin/consolidate repos
- next concrete plugin to finish

Avoid giant tables unless they explicitly ask for one.