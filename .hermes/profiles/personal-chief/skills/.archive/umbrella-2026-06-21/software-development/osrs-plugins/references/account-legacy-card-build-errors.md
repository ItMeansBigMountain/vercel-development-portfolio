# Account Legacy Card Build Errors Reference

This document captures the specific compilation errors and fixes encountered during development of the Account Legacy Card plugin.

## Error 1: NavigationButton Panel Type Mismatch

**Error Message:**
```
error: incompatible types: JPanel cannot be converted to PluginPanel
            .panel(panel)
                   ^
```

**Cause:** The `NavigationButton.builder().panel()` method expects a `PluginPanel` instance, but the code was passing a `JPanel`.

**Fix:**
```java
// Wrong:
navButton = NavigationButton.builder()
    .panel(panel)  // panel is JPanel
    .build();

// Correct:
navButton = NavigationButton.builder()
    .panel(new PluginPanel() {
        @Override
        public void paint(Graphics2D g) {
            // Custom painting if needed
        }
    })
    .build();
```

## Error 2: JTextArea Method Name

**Error Message:**
```
error: cannot find symbol
        resultArea.setWrapStyleWordWrap(true);
                  ^
  symbol:   method setWrapStyleWordWrap(boolean)
```

**Cause:** The method name is `setWrapStyleWordWrap` (with capital W), not `setWrapStyleWordWrap`.

**Fix:**
```java
// Correct method name:
resultArea.setLineWrap(true);
resultArea.setWrapStyleWordWrap(true);
```

## Error 3: Config Field Name Mismatch

**Error Message:**
```
error: cannot find symbol
        if (gameStateChanged.getGameState() == GameState.LOGGED_IN && config.showOnC)
                                                                            ^
  symbol:   variable showOnC
  location: variable config of type AccountLegacyCardConfig
```

**Cause:** The config interface method name `showOnC` doesn't exist in `AccountLegacyCardConfig`.

**Fix:**
Ensure the config interface has the correct method:
```java
@ConfigItem("showOnLogin", "Show On Login")
default boolean showOnLogin() { return false; }
```

And the plugin references it correctly:
```java
if (gameStateChanged.getGameState() == GameState.LOGGED_IN && config.showOnLogin())
```

## Prevention Checklist

- [ ] Verify NavigationButton panel type is PluginPanel, not JPanel
- [ ] Use correct JTextArea method names: `setWrapStyleWordWrap(true)` (capital W)
- [ ] Match config method names exactly between interface and plugin usage
- [ ] Run `./gradlew clean test assemble --no-daemon -q` after each change