# RuneLite Side Panel Delivery Notes

Use this reference when implementing or QAing RuneLite external plugins with compact sidebar panels, especially the user's OSRS plugin portfolio.

## Durable UI lessons

- Treat default RuneLite sidebar width as a hard constraint. A build passing is not enough if controls trail off to the right.
- Prefer narrow dropdowns, icon buttons, and wrapped HTML labels with explicit preferred/maximum sizes.
- Set both preferred and maximum dimensions for Swing controls in horizontal rows, especially `JComboBox` and small refresh/remove buttons.
- If a data source is broken or unreliable in the live client, remove it from the visible UI until the scanner is proven. Keep internal model extensibility if useful, but do not ship broken dropdown options.
- For broad social panels, avoid clan-first naming unless clan support is a verified product goal. Use neutral player/friend language.

## Who's Grinding Panel first-pass pattern

- Product name: `Who's Grinding Panel` even if the historical repo path still contains `WhosGrindingClanPanel`.
- Active visible sources: `Friends Chat` and `Friends List`.
- Hide/remove broken `Clan Chat` source from the active UI until RuneLite clan API behavior is verified in a live client.
- `showOfflineFriends` should be a real config checkbox that gates offline friends from the friends-list scanner:

```java
config.showOfflineFriends() || friend.getWorld() > 0
```

- Use compact at-a-glance icons for online/offline/source status and provide click-to-detail scaffolding for tracker information.
- Detail scaffolding can show name, source, online/offline, world, first seen, last seen, last status change, and a summary before full Wise Old Man/TempleOSRS/hiscore enrichment exists.

## Verification pattern

```bash
cd /opt/data/HeRmEz/projects/osrs-plugins/<PluginName>
export JAVA_HOME=/opt/data/jdks/current-java11
export PATH="$JAVA_HOME/bin:$PATH"
./gradlew clean test assemble --no-daemon --console=plain
```

For UI wording cleanup, grep visible docs/metadata/source strings for obsolete labels, for example:

```bash
grep -RIn "Clan Chat\|Track clan\|Who's Grinding Clan Panel\|clan chat activity" README.md plugin.json runelite-plugin.properties src/main/java || true
```

## Manual QA checklist

1. Launch with `./gradlew run --no-daemon`.
2. Confirm plugin display name and RuneLite config name.
3. Check default sidebar width: source selector and refresh button must both be visible.
4. Toggle config checkboxes and verify UI/source behavior.
5. Click a player row and verify detail view/dialog is readable.
6. Log out/in and confirm no stale UI crash.
