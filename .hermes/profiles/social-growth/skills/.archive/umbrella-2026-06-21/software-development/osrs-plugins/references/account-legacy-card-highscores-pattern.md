# Account Legacy Card / RuneLite HiScore-style lookup pattern

Use this when implementing a RuneLite player lookup plugin with a sidebar and right-click player lookup.

## User expectations learned
- Do **not** use chat commands for this plugin class. The UX should match RuneLite HiScore: toolbar side panel + right-click player lookup + manual search field.
- Do **not** claim code was pushed, compiled, or visible in RuneLite unless `git push` and `./gradlew test assemble` actually returned success.
- If the user says they do not see changes to pull, verify `git status`, commit, push, and parent submodule/pointer repo if applicable.

## RuneLite HiScore-style mechanics
- Inject `Provider<MenuManager>` and `ClientToolbar`.
- Build a `PluginPanel` and add it through `NavigationButton.builder().panel(pluginPanel)`.
- Add the toolbar button with `clientToolbar.addNavigation(navButton)` and remove it in `shutDown()`.
- Add player right-click item with `menuManager.get().addPlayerMenuItem("Legacy Card")`; remove it in `shutDown()` and refresh it on config changes.
- Handle player menu clicks via `MenuOptionClicked` where `event.getMenuAction() == MenuAction.RUNELITE_PLAYER` and `event.getMenuOption().equals("Legacy Card")`.
- Cache player names on `MenuOpened` by scanning `event.getMenuEntries()` for `MenuAction.RUNELITE_PLAYER`, using `entry.getPlayer()` and `entry.getIdentifier()`, mirroring RuneLite's HiScore plugin. This helps when the player despawns before click handling.
- When a lookup starts, call `clientToolbar.openPanel(navButton)` on the Swing thread so the side panel becomes visible.

## Swing panel pitfalls
- `NavigationButton.builder().panel(...)` needs a RuneLite `PluginPanel`, not an arbitrary `JPanel`.
- `JTextArea` word wrap is `setLineWrap(true)` plus `setWrapStyleWord(true)`. Do not use nonexistent `setWrapStyleWordWrap`.
- Network lookups must not run on the Swing/client thread. Use a single-thread `ExecutorService`; cancel prior lookup futures before starting a new one; update UI via `SwingUtilities.invokeLater`.

## Useful data sources
- Official OSRS hiscore lite CSV: `https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=<encoded-rsn>`
  - First CSV row is overall: `rank,totalLevel,totalXp`.
- Wise Old Man player endpoint: `https://api.wiseoldman.net/v2/players/username/<encoded-rsn>`
  - Public profile may 404; treat as optional and show a graceful no-profile state.
- TempleOSRS player info: `https://templeosrs.com/api/player_info.php?player=<encoded-rsn>`
  - Useful fields include `Game mode`, `F2p`, `Banned`, `Disqualified`, `Last checked`.
- TempleOSRS player stats: `https://templeosrs.com/api/player_stats.php?player=<encoded-rsn>&bosses=1`
  - Useful fields include `Overall_rank`, `Overall_ehp`, `Overall_ehb`, skill levels/ranks, and boss KC fields.

## Verification sequence
1. Run `JAVA_HOME=/opt/data/jdks/current-java11 ./gradlew clean test assemble --no-daemon` in the plugin repo.
2. Commit and push the plugin repo.
3. If the plugin is nested under `/opt/data/HeRmEz/projects/...`, also commit and push the parent `/opt/data/HeRmEz` pointer.
4. Report the actual commit SHAs and build result, not intended behavior.