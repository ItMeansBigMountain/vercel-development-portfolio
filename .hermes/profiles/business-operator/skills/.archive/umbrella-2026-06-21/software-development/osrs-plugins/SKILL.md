---
name: osrs-plugins
description: OSRS RuneLite plugin development guide covering project structure, API integration, and publishing workflow.
tags: [runescape, osrs, plugin-development, runelite]
---
# OSRS RuneLite Plugin Development Guide

## Portfolio Review Workflow

When the user asks to review the OSRS plugin portfolio, use `references/portfolio-review-pattern.md`: inventory child repos under `/opt/data/HeRmEz/projects/osrs-plugins`, run sequential Java 11 `./gradlew clean test assemble --no-daemon` checks, save a JSONL report, then give a product-maturity review instead of only build status. For the current post-GitHub-import completion plan, also load `references/osrs-portfolio-completion-2026-06.md`: Vercel is not a blocker for RuneLite plugins, 17/17 active child plugins passed the Java 11 build review, and the recommended completion order is AccountLegacyCard → BossReadinessScore → RivalRadar → clan activity panel → lightweight utility batch.

For Account Legacy Card handoff and user clone requests, load `references/account-legacy-card-handoff-2026-06.md`: give the GitHub clone URL first (`https://github.com/ItMeansBigMountain/account-legacy-card-osrs.git`), then the local backup/worktree path. The user clarified that each child directory under `/opt/data/HeRmEz/projects/osrs-plugins/` is intended to be its own standalone Git repo, while the parent folder is a portfolio/backup container.

For RuneLite Plugin Hub submissions, load `references/runelite-plugin-hub-contributor-pr-workflow.md`: child plugin repo build/test/push comes first, then update the user's `plugin-hub` fork manifest `plugins/<slug>` with the full child commit SHA, push a branch, provide the `runelite/plugin-hub` compare URL, and finally push the parent HeRmEz submodule pointers. RuneLite plugins do not need Vercel deployment.

## User Workspace Layout

When working on this user's RuneLite plugin projects, inspect `/opt/data/HeRmEz/projects/osrs-plugins` first. The directory is a parent folder for multiple plugin projects; each plugin should become its own repository when requested. Use `https://github.com/ItMeansBigMountain/breach-check-osrs.git` as the boilerplate/reference structure, but verify where it is cloned locally before copying from it. See `references/workspace-repo-layout.md` for the exact workspace paths and repo-splitting workflow, and `references/plugin-repo-stabilization-checklist.md` for the stabilization checklist used when cleaning a messy multi-plugin parent directory.

## Project Structure

```
my-plugin/
├── build.gradle or build.gradle.kts
├── settings.gradle
├── gradlew / gradlew.bat
├── gradle/wrapper/
├── runelite-plugin.properties or plugin.json
├── src/main/java/com/example/myplugin/
│   ├── MyPluginPlugin.java        # Main plugin class
│   ├── MyPluginConfig.java        # Configuration interface
│   └── MyPluginOverlay.java       # Optional UI overlay
├── src/test/java/
├── src/test/resources/logback-test.xml
└── README.md                      # Documentation
```

For the user's `/opt/data/HeRmEz/projects/osrs-plugins` workspace, treat the parent directory as a container only. Each child plugin should be its own Git repository with the full top-level Gradle/RuneLite structure above. Use `https://github.com/ItMeansBigMountain/breach-check-osrs.git` or a verified local clone as the boilerplate/reference structure, and keep the parent HeRmEz repo from swallowing plugin internals.

## Plugin Development Patterns

This umbrella covers both the general RuneLite/OSRS plugin lifecycle and the user's local multi-repo scaffolding workflow. Prefer this skill over the older narrow OSRS/RuneLite plugin skills.

### 1. Plugin Entry Point
```java
@Slf4j
@PluginDescriptor(
    name = "My Plugin",
    description = "Brief description of functionality",
    tags = {"tag1", "tag2"}
)
public class MyPluginPlugin extends Plugin {
    @Inject private Client client;
    @Inject private MyPluginConfig config;
    
    @Override
    protected void startUp() { /* initialization */ }
    @Override
    protected void shutDown() { /* cleanup */ }
}
```

### 2. Configuration Interface
```java
@ConfigGroup("myplugin")
public interface MyPluginConfig extends Config {
    @ConfigItem("showOverlay", "Show Overlay")
    @Slider(base = 1, max = 10, step = 1, raw = false)
    default int showOverlay() { return 5; }
}
```

### 3. Event Handling
```java
@Subscribe
public void onChatMessage(ChatMessage event) {
    // Handle chat events
}

@Subscribe
public void onGameTick(GameTick event) {
    // Handle periodic game events
}
```

## API Integration

### Shared Clients
- **WOMApiClient**: Accesses WiseOldMan API for player data and competition tracking
- **TempleApiClient**: Accesses TempleOSRS API for boss kill counts and competition data

### Boss/autocomplete data

When a plugin needs an all-boss dropdown or autocomplete, do not hard-code the full boss list as the primary source. Prefer a merged live index from GearScape `/api/monster` and OSRS Wiki `Category:Bosses`, fetched in a background executor with local fallback data. See `references/boss-autocomplete-api-integration.md` for endpoints, matching rules, Swing side-panel autocomplete behavior, and verification smoke-test expectations.

### Example API Usage
```java
// Get player XP from WiseOldMan
String response = WOMApiClient.getPlayerGains(playerName);
double xp = parseXPFromResponse(response);

// Parse numeric values from API response
private static final Pattern XP_PATTERN = Pattern.compile("(?:total_gained|xp)\\s*[:=]\\s*(\\d+)", Pattern.CASE_INSENSITIVE);
private double parseXPFromResponse(String response) {
    Matcher m = XP_PATTERN.matcher(response);
    if (m.find()) {
        try {
            return Double.parseDouble(m.group(1));
        } catch (NumberFormatException ignored) {}
    }
    return 0;
}

// Combine data from both APIs for robust results
double combinedXP = (womXP + templeXP) / 2.0;
```

## Kanban Furnishing Workflow

When the user wants every plugin prepared for testing/publishing, seed one Kanban task per plugin instead of bundling the whole parent directory into one card. See `references/kanban-plugin-furnishing.md` for the exact task body pattern, idempotency-key convention, dependency fan-in to a publish task, and pitfalls around simultaneous Gradle builds.

## Scaffolding New Plugin Repos

Use this workflow when the user asks to create, scaffold, build, or publish an individual RuneLite plugin as its own repository. For batch publishing many already-scaffolded child plugins to one GitHub repo each, also use `references/bulk-publish-child-repos.md` for the safe one-by-one test/commit/create/push/verify loop, GitHub token handling, and boilerplate exclusion pitfalls:

1. Create the plugin directory under `/opt/data/HeRmEz/projects/osrs-plugins/<plugin-name>`.
2. Copy the verified boilerplate (`breach-check-osrs` or local `osrs-plugins-boilerplate`) rather than hand-writing wrapper files.
3. Rename package, plugin class, config class, overlay class, and `runelite-plugin.properties`/metadata consistently.
4. Run `chmod +x gradlew` if needed, then `./gradlew test` or `./gradlew build`.
5. Initialize Git inside the child plugin directory, commit the scaffold, and push to a dedicated GitHub repository when requested.
6. When pushing with an environment token, check `GITHUB_ACCESS_TOKEN` as well as `GITHUB_TOKEN`/`GH_TOKEN`; if using a token-bearing HTTPS remote for push, immediately reset `origin` to the clean public URL afterward.
7. Optionally add the child repo as a submodule or ignored nested repo in the parent workspace, depending on the user's current repo strategy.
8. For batches, create one Kanban task per plugin and a fan-in publish task rather than one giant parent-folder task. If the user explicitly says "one by one," process and verify each plugin sequentially: Gradle test, commit, create repo, push, `git ls-remote` verify, then move to the next.

### Java 11 in constrained containers

When working in the user's Hostinger VPS / Docker Hermes container, Java may be missing and `sdk`/`brew` may not exist. Install a user-local Java 11 instead of relying on apt/root access:

```bash
mkdir -p /opt/data/jdks
cd /opt/data/jdks
curl -L --fail -o temurin11.tar.gz '<Temurin 11 Linux x64 tarball from Adoptium>'
tar -xzf temurin11.tar.gz
ln -sfn /opt/data/jdks/<extracted-jdk-dir> /opt/data/jdks/current-java11
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:/opt/hermes/.venv/bin:/opt/data/.local/bin:$PATH"
```

Persist those exports in `/opt/data/.env`, `/opt/data/.bashrc`, and/or `/opt/data/.profile` when appropriate.

### Scaffolding pitfalls

- Missing `gradlew` permission: run `chmod +x gradlew` after copying boilerplate.
- Package rename not exhaustive: update Java packages, imports, plugin metadata, tests, and README examples.
- GitHub token scope: repo creation requires a token/`gh` auth with repo permissions.
- Nested repo confusion: verify `git remote -v` and parent `.gitignore`/submodule state before committing.
- Gradle wrapper downloads can stall; retry from the plugin directory and keep simultaneous batch builds limited.

## Publishing Workflow

1. **Fork** the `runelite/plugin-hub` repository
2. **Create** a new plugin directory under `plugins/`
3. **Add** required files: `src/`, `plugin.json`, `README.md`, `build.gradle`
4. **Verify** build with `./gradlew assemble`
5. **Submit** a Pull Request with:
   - Clear description of functionality
   - Screenshots or GIFs demonstrating features
   - Explanation of API usage (if applicable)
6. **Address** any feedback from maintainers

## Best Practices

- **Performance**: Minimize game thread blocking; use background executors for API calls
- **Memory Management**: Clear caches and resources during `shutdown()`
- **User Experience**: Provide meaningful notifications and visual feedback
- **RuneLite sidebar fit**: Side panels must fit the narrow RuneLite plugin sidebar. Avoid long control labels, wide fixed-size grids, unbounded HTML labels, and horizontal scrollbars. When a panel feels too big from the sides, compact labels/copy, use bounded HTML text widths, shrink grid cells/buttons, cap combo boxes/buttons to a fixed sidebar-safe width, and verify with a screenshot. Verify the post-analysis/result state too: long boss titles, summary lines, and equipment grids can overflow even when empty controls fit. See `references/runelite-sidebar-compact-ui.md` and `references/boss-readiness-gear-ui-pitfalls.md`.
- **OSRS source hygiene**: Treat Old School RuneScape as separate from RuneScape 3. Use only Old School RuneScape Wiki URLs (`https://oldschool.runescape.wiki/w/...`) and OSRS/RuneLite item IDs for OSRS plugins; never link to or infer from RuneScape 3 pages. For equipment UIs, each displayed item should be clickable (icon/name area) to its OSRS Wiki item page, and tests should assert generated item wiki URLs start with `https://oldschool.runescape.wiki/w/`.
- **Boss readiness gear accuracy**: Live gear APIs can be stale or omit current OSRS megarares/current bossing gear. Merge live gear with a local OSRS Wiki/RuneLite-ID-backed fallback list, but let curated local rows override same-name live rows when they carry important metadata like `twoHanded`, canonical names, fallback item IDs, or filtering status. Include/test weapons such as Tumeken's shadow, twisted bow, bowfa, blowpipe, scorching bow, zaryte crossbow, purging staff, emberlight, soulreaper axe, scythe, noxious halberd, and other current high-end gear. Filter temporary/minigame/game-mode-specific gear such as Corrupted Gauntlet `corrupted`/`attuned`/`perfected`/`basic` items plus Deadman, Leagues, Trailblazer, Shattered Relics, Raging Echoes, relic hunter, seasonal, competitive, and trophy items before recommending. Model two-handed weapons so the shield slot is omitted/disabled when appropriate, including when the user cycles to a 2H weapon alternative; broad 2H patterns should cover bows excluding crossbows, godswords, mauls, halberds, spears, 2h swords, soulreaper axe, and similar current OSRS weapons. See `references/boss-readiness-gear-ui-pitfalls.md` and `references/boss-readiness-gear-currentness.md`.
- **Error Handling**: Gracefully handle API failures with user-friendly messages
- **Versioning**: Follow semantic versioning and update `plugin.json` accordingly
- **Documentation**: Keep README updated with usage examples and configuration options
- **Testing**: Implement verification scripts to validate API integrations

## Local testing / developer handoff

When the user asks how to run a plugin locally, give direct Gradle commands from the child plugin repo first, not a long explanation: `./gradlew run --no-daemon` with Java 11 active. For repeatable handoff across many plugins, add/update `DEVELOPER_CHEATSHEET.md` in each active child repo. See `references/local-run-and-cheatsheet-pattern.md` for macOS/Windows/Linux Java 11 setup, Gradle verification commands, RuneLite manual test flow, and parent submodule hygiene.

## Common Issues & Troubleshooting

- **API Rate Limits**: Implement caching strategies and respect API usage policies
- **Network Failures**: Use fallback mechanisms and provide user feedback
- **Plugin Conflicts**: Ensure proper dependency isolation and version checking
- **Build Failures**: Verify Gradle configuration, Java 11/JAVA_HOME, wrapper permissions, and dependency versions
- **Runtime Errors**: Check plugin logs and use `notifier.notify()` for user feedback
- GitHub repo creation failures: verify `GITHUB_ACCESS_TOKEN`/`GITHUB_TOKEN`/`GH_TOKEN`, `gh auth status`, token scope, and remote URL before pushing
- Bulk child-repo publishing: exact-name exclude templates/boilerplates before generic build-file detection, stage only source/docs/metadata, and sanitize token-bearing remotes after push
- IP whitelisting for external APIs: ensure any external service used by a plugin has the VPS IP whitelisted before debugging plugin logic

### UI Component Pitfalls
- **NavigationButton panel type**: The `NavigationButton.builder().panel()` method requires a `PluginPanel` instance, NOT `JPanel`. Using `JPanel` causes compilation error: `incompatible types: JPanel cannot be converted to PluginPanel`. Fix: Wrap your JPanel content in a new `PluginPanel` subclass or restructure to use PluginPanel directly.
- **JTextArea word wrapping**: Use `setLineWrap(true)` plus `setWrapStyleWord(true)` for side-panel text areas. `setWrapStyleWordWrap(true)` is not a Swing `JTextArea` method and causes `cannot find symbol` compilation errors.
- **HiScore-style player lookup plugins**: Use `ClientToolbar` + `NavigationButton` + `PluginPanel` for a visible sidebar, `MenuManager.addPlayerMenuItem(...)` for right-click player lookup, and `MenuOptionClicked` with `MenuAction.RUNELITE_PLAYER` to handle clicks. Do not substitute chat commands when the desired UX is RuneLite HiScore-style. See `references/account-legacy-card-highscores-pattern.md` for the Account Legacy Card implementation notes and API endpoints.
- **Push discipline for nested OSRS plugin repos**: After changes pass `JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew clean test assemble --no-daemon`, commit/push the plugin repo and also commit/push the parent `/opt/data/HeRmEz` pointer when the plugin is nested under the user's Git-backed workspace. Never tell the user changes are available to pull until `git push` has actually succeeded.
- **Config field naming**: Config interface method names must match exactly what the plugin references. A typo like `showOnC` instead of `showOnLogin` causes `cannot find symbol` compilation errors. Always verify the getter name matches across both `AccountLegacyCardConfig.java` and the plugin class.

## Resources

- [RuneLite Client API Documentation](https://github.com/runelite/client)
- [WiseOldMan API Documentation](https://oldschool.runescape.wiki/w/Wise_Old_Man_API)
- [TempleOSRS API Documentation](https://oldschool.runescape.wiki/w/TempleOSRS_API)
- `references/temple-wom-api-patterns.md` — TempleOSRS/Wise Old Man endpoint and Java 11 HTTP client notes merged from the old narrow OSRS plugin-development skill.
- `references/runelite-plugin-hub-workflow.md` — plugin-hub `create_new_plugin.py --noninteractive`, build/run, and submission workflow.
- [RuneLite Plugin Hub](https://github.com/runelite/plugin-hub)
- `references/user-product-direction.md` — Durable user direction for the current OSRS plugin portfolio: rejected ideas to avoid recreating, consolidated RivalRadar scope, clan side-panel behavior, robust hiscore/account API aggregation, progress timeline semantics, opponent PvP timers, and GearScape-inspired boss readiness UX.
- `references/gearscape-bis-research.md` — GearScape-inspired automatic boss BiS/best-available setup research: observed data endpoints, client-side worker flow, payload/result shapes, and a safer RuneLite MVP algorithm that uses OSRS Wiki/RuneLite data rather than depending on GearScape runtime APIs.
- `references/boss-readiness-side-panel-pattern.md` — concrete Boss Readiness Score implementation pattern: Java DTO/enums, local gear recommendation engine, RuneLite `ClientToolbar` side-panel wiring, config refresh behavior, and Java 11 Gradle verification commands.
- `references/boss-autocomplete-api-integration.md` — merged GearScape + OSRS Wiki boss autocomplete pattern: public endpoints, weighted matching, editable Swing combo box behavior, offline fallback, and smoke-test checks.