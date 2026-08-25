---
name: osrs-plugin-scaffolding
description: Scaffold, build, and publish individual RuneScape (RuneLite) plugins as independent Git repositories.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osrs, runelite, plugin, scaffolding, git, github]
    related_skills: [github-repo-management, hermes-agent-skill-authoring]
---

# OSRS Plugin Scaffolding

## Overview
This skill encapsulates the end‑to‑end workflow for creating a new RuneLite OSRS plugin, building it, and publishing it to a dedicated GitHub repository. It is intended for the user’s standard workspace layout:
```
/opt/data/HeRmEz/projects/osrs-plugins/<plugin-name>
```
Each plugin lives in its own Git repository and is tracked as a sub‑module of the main `HeRmEz` repo.

## Prerequisites
- Java 11 installed and `JAVA_HOME` set (already configured in the environment).
- Gradle wrapper (`gradlew`) present in the plugin directory.
- `GITHUB_ACCESS_TOKEN` available in the environment (loaded from `/opt/data/.env`).
- The `github-repo-management` skill is available for repo creation and pushing.

## Step‑by‑step Procedure
1. **Create plugin directory**
   ```bash
   PLUGIN=$1   # name of the plugin, e.g. AccountLegacyCard
   BASE=/opt/data/HeRmEz/projects/osrs-plugins
   mkdir -p "$BASE/$PLUGIN"
   cd "$BASE/$PLUGIN"
   ```
2. **Copy boilerplate** – the repository `osrs-plugins-boilerplate` contains a minimal RuneLite plugin skeleton. Clone or copy its contents:
   ```bash
   cp -r /opt/data/HeRmEz/projects/osrs-plugins-boilerplate/* "$BASE/$PLUGIN/"
   ```
3. **Rename package and class** – replace placeholder `com.example.plugin` with a unique package based on the plugin name and rename the main class.
   ```bash
   PACKAGE="com.osrs.$PLUGIN.toLowerCase()"
   # Use sed or a script to replace occurrences in *.java and plugin properties
   ```
4. **Validate build**
   ```bash
   ./gradlew test   # should succeed with the placeholder test
   ```
5. **Create GitHub repo** – use the `github-repo-management` skill (or `gh` CLI) with the token from the environment.
   ```bash
   REPO_URL=$(gh repo create "YourOrg/$PLUGIN" --public --source . --remote origin)
   ```
6. **Push initial commit**
   ```bash
   git add .
   git commit -m "feat: initial scaffold for $PLUGIN"
   git branch -M main
   git push -u origin main
   ```
7. **Add as sub‑module to main HeRmEz repo** (optional, if you want the parent repo to track it):
   ```bash
   cd /opt/data/HeRmEz
   git submodule add "$REPO_URL" "projects/osrs-plugins/$PLUGIN"
   git commit -m "chore: add $PLUGIN as submodule"
   git push origin main
   ```
8. **Create Kanban task** – generate a “Furnish OSRS plugin: <PLUGIN>” task in the default board.
   ```bash
   hermes kanban create "Furnish OSRS plugin: $PLUGIN" --status running
   ```

## Pitfalls & Workarounds
- **Missing `gradlew` permission** – run `chmod +x gradlew` after copying the boilerplate.
- **Package rename not exhaustive** – ensure you also update `runelite-plugin.properties` and any `import` statements.
- **GitHub token scope** – the token must have `repo` permissions; otherwise repo creation fails.
- **Submodule URL mismatch** – after creating the repo, verify the remote URL (`git remote -v`) points to the newly created GitHub repo before committing the submodule.
- **API rate limits** – creating many repos quickly may hit GitHub’s secondary rate limits; insert a short `sleep 2` between creations if you automate a batch.

## References
- `references/osrs_plugin_boilerplate.md` – description of the boilerplate layout.
- `scripts/create_osrs_plugin.py` – a ready‑to‑run Python script that automates steps 1‑6 for a given plugin name.

---

*This skill is versioned; update the `version` field when you extend or refactor the workflow.*
