# RuneLite Plugin Hub Development Workflow

## Overview

This document captures the workflow for developing RuneLite plugins using the plugin-hub infrastructure.

## Key Commands

### Creating a New Plugin

Use `create_new_plugin.py` from the plugin-hub repository:

```bash
python3 /path/to/plugin-hub/create_new_plugin.py \
  --noninteractive \
  --name "PluginName" \
  --package "com.author.pluginname" \
  --author "YourName" \
  --description "Brief description" \
  --output_directory /path/to/output
```

**Important**: The `--noninteractive` flag is REQUIRED in automated/Hermes sessions. Without it, the script will wait for stdin input and fail with EOFError.

### Build and Test

```bash
cd plugin-name
./gradlew build
./gradlew run  # For testing in RuneLite dev client
```

## Plugin Structure

Standard structure after generation:

```
plugin-name/
├── build.gradle
├── settings.gradle
├── runelite-plugin.properties
├── src/main/java/com/author/pluginname/
│   ├── PluginNamePlugin.java
│   └── PluginNameConfig.java
├── src/test/java/
└── build/
```

## Submission to Plugin Hub

1. Fork https://github.com/runelite/plugin-hub
2. Add your plugin entry in `plugins/` directory:
   ```
   repository=https://github.com/yourname/plugin-name.git
   commit=<full-40-char-commit-hash>
   ```
3. Create PR following template

## API Integration Patterns

### WOM (WiseOldMan) API

For OSRS stats tracking:

- Base: `https://api.wiseoldman.net/`
- Key endpoints: `/player/{username}`, `/player/{username}/history`
- Rate limits apply - cache responses

### TempleOSRS API

Alternative stats source:

- Base: `https://templeosrs.com/api/`
- Endpoints for hiscores, competition data

## Pitfalls

- **Never omit `--noninteractive`**: In automated environments, the script will hang waiting for input
- **Test in dev client first**: Use `./gradlew run` to verify plugin loads correctly
- **Follow BSD 2-Clause license**: Required for plugin-hub submission
- **Dependency verification**: Plugin-hub requires cryptographic hash verification for third-party deps

## Session Notes

2026-05-26: Successfully scaffolded 19 OSRS plugins for portfolio development. All used identical boilerplate structure with unique package names.