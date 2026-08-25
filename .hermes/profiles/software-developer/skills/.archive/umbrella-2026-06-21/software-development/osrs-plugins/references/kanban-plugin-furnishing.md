# Kanban workflow: one furnishing task per RuneLite plugin

Use this when the user wants the OSRS plugin board filled with one task per plugin so each repository can be completed independently before publishing/testing.

## Discovery

Workspace root is usually:

```bash
/opt/data/HeRmEz/projects/osrs-plugins
```

List actual plugin directories and exclude control/template folders such as `.git`, `_backups`, and `osrs-plugins-boilerplate`.

## Task shape

Create one Kanban task per plugin, normally assigned to `default` unless the user has created a specific coding-worker profile. Use:

- `--workspace dir:<plugin-path>` so the worker runs inside that plugin repository.
- `--skill osrs-plugins` so RuneLite conventions are loaded.
- `--idempotency-key osrs-plugin-furnish-<PluginName>` so repeated seeding does not duplicate cards.
- `--max-runtime 2h` or similar because Gradle/RuneLite cleanup can take time.

## Per-plugin definition of done

Each task body should require the worker to:

1. Inspect code, Gradle config, `runelite-plugin.properties`, README/docs, tests, and git status.
2. Make the plugin feel complete and coherent: README purpose, install/run/test notes, config/feature description, API usage notes if applicable, and manual RuneLite test steps.
3. Verify Java package/class naming and RuneLite metadata are consistent with the plugin name and the `breach-check-osrs` boilerplate conventions.
4. Add or improve lightweight smoke tests where feasible without needing a live RuneLite client.
5. Run both:

```bash
./gradlew test --no-daemon -q
./gradlew assemble --no-daemon -q
```

6. Fix compile/test issues scoped to that plugin only.
7. Leave a clean git state with a local commit if changes were made.
8. Summarize changes, test results, and remaining manual RuneLite testing steps.

## Dependency graph

If there is a broader publishing task, link every per-plugin furnishing task as a parent of that publish task. The publish task should stay in `todo` until all plugin readiness tasks are done.

Do not link unrelated blocked/intake cards as parents of the publish task; only link true readiness dependencies.

## Pitfalls

- Creating many tasks assigned to the same profile can result in many `running` tasks at once if the gateway dispatcher has concurrency available. That is fine for board seeding, but expect resource pressure from simultaneous Gradle builds; use `max-runtime` and monitor diagnostics.
- Use idempotency keys before bulk creation; otherwise repeated attempts will duplicate 20+ cards.
- Keep each task scoped to its own plugin repository. Workers may read siblings for comparison but should not modify them.
- Preserve the parent `osrs-plugins/` directory as a container, not a monorepo, unless the user explicitly changes that preference.
