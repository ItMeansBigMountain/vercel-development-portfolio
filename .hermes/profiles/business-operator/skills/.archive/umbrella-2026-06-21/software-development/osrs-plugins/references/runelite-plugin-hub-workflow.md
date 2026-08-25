# RuneLite Plugin Hub Workflow

Copied into the `osrs-plugins` umbrella from `project-portfolio-roadmapping/references/runelite-plugin-hub-workflow.md` because this is RuneLite-domain procedure, not portfolio-roadmapping knowledge.

## Creating a New Plugin from Plugin Hub

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

**Important:** `--noninteractive` is required in automated/Hermes sessions. Without it, the script waits for stdin and can fail with `EOFError`.

## Build and Test

```bash
cd plugin-name
./gradlew build
./gradlew run  # test in RuneLite dev client
```

## Submission to Plugin Hub

1. Fork `https://github.com/runelite/plugin-hub`.
2. Add your plugin entry under `plugins/`:
   ```text
   repository=https://github.com/yourname/plugin-name.git
   commit=<full-40-char-commit-hash>
   ```
3. Create the PR using the plugin-hub template.

## Pitfalls

- Never omit `--noninteractive` in automated runs.
- Test in the dev client (`./gradlew run`) before plugin-hub submission.
- Follow BSD 2-Clause licensing expectations for plugin-hub submission.
- Plugin-hub requires cryptographic hash verification for third-party dependencies.
