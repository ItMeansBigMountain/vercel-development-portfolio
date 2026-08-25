---
name: osrs-plugin-development
category: gaming
description: Develop Runelite plugins for Old School RuneScape using the DMM Timer as boilerplate template
tags: [osrs, runelite, pvp, java]
version: 1.0.1
author: hermes-agent
dependencies: [Java 11, Gradle wrapper]
---

# OSRS Plugin Development

## Trigger
When developing Runelite plugins for Old School RuneScape, especially PvP utility plugins like ice barrage timers, spell trackers, or combat overlays.

## Plugin Structure
All OSRS plugins follow the Runelite plugin descriptor pattern:
```java
@PluginDescriptor(
    name = "Plugin Name",
    description = "Plugin description",
    tags = {"tag1", "tag2", "pvp"}
)
public class PluginNamePlugin extends Plugin
{
    @Inject private Client client;
    @Inject private ConfigManager configManager;
    @Inject private PluginNameConfig config;
    @Inject private OverlayManager overlayManager;
}
```

## Core Components
1. **Main Plugin Class** - `@PluginDescriptor`, event handlers
2. **Config Class** - Annotation-based configuration
3. **Overlay Class** - Visual representation
4. **Utility Classes** - API clients, data models

## Event Handling Patterns
- `@Subscribe public void onChatMessage(ChatMessage event)` - Detect combat hits, spell casts
- `@Subscribe public void onGameTick(GameTick tick)` - Timer updates, periodic checks
- `@Subscribe public void onConfigChanged(ConfigChanged event)` - Config updates

## Starter Template
Use `osrs-plugins-boilerplate` directory or copy `DeadmanBreachPlugin.java` as starting point.

## Container/VPS setup notes
When working in the user's Hostinger VPS Docker Hermes container, Java may be missing and `sdk`/`brew` may not exist. Install a user-local Java 11 instead of relying on apt/root access:
```bash
mkdir -p /opt/data/jdks
cd /opt/data/jdks
curl -L --fail -o temurin11.tar.gz '<Temurin 11 Linux x64 tarball from Adoptium>'
tar -xzf temurin11.tar.gz
ln -sfn /opt/data/jdks/<extracted-jdk-dir> /opt/data/jdks/current-java11
```
Then set:
```bash
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:/opt/hermes/.venv/bin:/opt/data/.local/bin:$PATH"
```
Persist these in `/opt/data/.env`, `/opt/data/.bashrc`, and/or `/opt/data/.profile` when appropriate.

## Local multi-repo layout
For `/opt/data/HeRmEz/projects/osrs-plugins`, treat the parent directory as a container only. Each child plugin directory should be its own Git repo and should contain the same top-level structure as the `breach-check-osrs` boilerplate: `build.gradle`, `settings.gradle`, `gradlew`, `gradlew.bat`, `gradle/wrapper/`, `runelite-plugin.properties`, `src/main/java`, `src/test/java`, and `src/test/resources/logback-test.xml`. The parent HeRmEz repo should ignore plugin internals so they can later be pushed as separate GitHub repositories or moved to an organization.

## References
- `references/api-patterns.md` - TempleOSRS and WiseOldMan API endpoint patterns
- `references/combat-message-formats.md` - Common OSRS chat message formats for spells
- `templates/IceBarrageTimerPlugin.java` - Timer plugin boilerplate
