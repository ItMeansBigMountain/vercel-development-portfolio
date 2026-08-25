---
name: runelite-plugin-development
description: Guide for developing, testing, and publishing RuneLite plugins (common workflow, scaffolding, GitHub repo creation, Gradle build).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [runelite, plugin, development, gradle, git, github]
    related_skills: [github-repo-management, github-code-review]
---

# RuneLite Plugin Development

## Overview
This umbrella skill contains reusable patterns for creating, building, testing, and publishing RuneLite plugins:

* Scaffold a new plugin (Gradle wrapper, Java source, resources, manifest).
* Initialize a Git repository and push to GitHub using the token stored in the environment.
* Run the Gradle build (`./gradlew build` and tests) locally.
* Commit and push incremental changes.
* Integration with Hermes Kanban for task tracking.

The goal is to make a one‑click recipe that takes a plugin name (and optional minimal description) and produces a ready‑to‑build repo on GitHub.

## Workflow
```bash
# Create a new plugin repository
hermes runelite-plugin-development create --name MyPlugin --desc "Simple hello‑world"
```
The command will:
1. Create a directory under `/opt/data/HeRmEz/projects/osrs-plugins/MyPlugin`.
2. Add a `build.gradle`, wrapper scripts, and a minimal Java class.
3. Initialize Git, commit the scaffold, and push to GitHub `username/MyPlugin`.
4. Optionally create the Kanban card for the new plugin.

## Templates
See the `templates/` directory for example `build.gradle`, Java class, and `runelite-plugin.properties` files.

## Pitfalls
- **Gradle wrapper timeout** – if the wrapper download stalls, run `./gradlew wrapper` again inside the repo.
- **GitHub token error** – ensure `GITHUB_ACCESS_TOKEN` is set in `/opt/data/.env` and that the token has `repo` scope.
- **IP whitelisting for external services** – ensure any external API you call (e.g., IntelBase) has the VPS IP whitelisted.

## References
* RuneLite plugin development guide: https://runelite.net/
