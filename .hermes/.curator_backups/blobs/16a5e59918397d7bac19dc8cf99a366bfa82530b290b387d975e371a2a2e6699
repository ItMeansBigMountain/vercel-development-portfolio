# RuneLite side-panel dimensions and WhosGrindingPanel sizing pattern

Session-derived reference for OSRS/RuneLite Swing side panels in the HeRmEz plugin portfolio.

## Authoritative constants

Probe the active RuneLite client jar instead of guessing panel width:

```bash
JAR=$(find /opt/data/.gradle/caches/modules-2/files-2.1/net.runelite/client -type f -name 'client-*.jar' | sort | tail -1)
javap -classpath "$JAR" -verbose net.runelite.client.ui.PluginPanel \
  | sed -n '/public static final int PANEL_WIDTH/,+6p;/public static final int SCROLLBAR_WIDTH/,+6p;/public static final int BORDER_OFFSET/,+6p'
```

Observed in the current workspace RuneLite client:

- `PluginPanel.PANEL_WIDTH = 225`
- `PluginPanel.SCROLLBAR_WIDTH = 17`
- `PluginPanel.BORDER_OFFSET = 6`

For scrollable side panels with 4 px content padding, use this safe content budget:

```text
safe content width = 225 - 17 - (6 * 2) - (4 * 2) = 188 px
```

## Implementation pattern

Create a small package-local dimensions helper and test it. Example from WhosGrindingPanel:

```java
final class WhosGrindingPanelDimensions
{
    static final int CONTENT_PADDING = 4;
    static final int CONTENT_WIDTH = PluginPanel.PANEL_WIDTH
        - PluginPanel.SCROLLBAR_WIDTH
        - (PluginPanel.BORDER_OFFSET * 2)
        - (CONTENT_PADDING * 2);
    static final int CONTROL_HEIGHT = 24;
    static final int ROW_ACTION_WIDTH = 26;
    static final int ROW_GAP = 3;
    static final int ROW_HORIZONTAL_PADDING = 8;
    static final int MEMBER_TEXT_WIDTH = CONTENT_WIDTH - ROW_ACTION_WIDTH - ROW_GAP - ROW_HORIZONTAL_PADDING;
}
```

Add a unit test that asserts the current constants and row budget. This turns UI-width regressions into test failures before screenshots/user review.

## Practical UI rules

- Never design custom side-panel content against the full 225 px; reserve scrollbar, border offset, and padding.
- Use `JScrollPane.HORIZONTAL_SCROLLBAR_NEVER` for plugin side panels.
- Put long text in HTML labels with explicit `body style='width:...px'` using the safe content width.
- Use compact 24 px controls and 24–26 px action buttons.
- Prefer a dropdown + small refresh/action button over multiple wide toggles.
- Put compact activity/status icons in rows and move detail text behind click-to-detail.
- For child/parent delivery, push the plugin repo first, then update the HeRmEz parent submodule pointer and any docs under `projects/osrs-plugins/`.

## Windows/local handoff pitfall

If an unrelated submodule has a broken `.gitmodules` mapping, broad recursive updates can fail with errors such as:

```text
fatal: No url found for submodule path 'projects/viral-clip-radar' in .gitmodules
```

For OSRS-only handoff, give a path-scoped update so the user can proceed while the unrelated submodule is fixed separately:

```bat
git submodule sync --recursive
git submodule update --init --recursive projects/osrs-plugins/WhosGrindingClanPanel
```

Do not tell the user to run the same broad recursive command again after they report this error; either fix the unrelated `.gitmodules` entry explicitly or scope the update to the target OSRS plugin path.
