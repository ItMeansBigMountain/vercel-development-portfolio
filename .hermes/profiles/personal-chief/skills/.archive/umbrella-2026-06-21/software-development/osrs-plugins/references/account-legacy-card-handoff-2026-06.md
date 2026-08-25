# Account Legacy Card handoff and repo-boundary notes (2026-06)

Use this reference when the user asks for the "hit URL", clone URL, local path, or next work item for Account Legacy Card or another OSRS plugin child project.

## User correction captured

- `/opt/data/HeRmEz/projects/osrs-plugins/<PluginName>` is a **backup/local child repo** location for the user to clone from / work against.
- Each child directory under `/opt/data/HeRmEz/projects/osrs-plugins/` is intended to be a **separate Git repository** for one OSRS plugin project.
- Do **not** treat the parent `osrs-plugins` directory as the single canonical repo for all plugin code.
- When the user asks for a project URL, give the GitHub clone URL first, then the local backup path.

## AccountLegacyCard current handoff facts

- Local backup/worktree: `/opt/data/HeRmEz/projects/osrs-plugins/AccountLegacyCard`
- GitHub clone URL: `https://github.com/ItMeansBigMountain/account-legacy-card-osrs.git`
- Branch: `main`
- Expected clean handoff check:

```bash
git -C /opt/data/HeRmEz/projects/osrs-plugins/AccountLegacyCard remote get-url origin
git -C /opt/data/HeRmEz/projects/osrs-plugins/AccountLegacyCard branch --show-current
git -C /opt/data/HeRmEz/projects/osrs-plugins/AccountLegacyCard status --short
```

## Handoff response pattern

When the user asks to clone locally, answer directly:

```bash
git clone https://github.com/ItMeansBigMountain/account-legacy-card-osrs.git
```

Then include the repo page URL and local backup path:

- Repo: `https://github.com/ItMeansBigMountain/account-legacy-card-osrs`
- Local backup/worktree: `/opt/data/HeRmEz/projects/osrs-plugins/AccountLegacyCard`

## Repo-boundary hygiene

- Keep child plugin repos as independent repos with their own `origin` remotes.
- Keep parent `/opt/data/HeRmEz` from swallowing child plugin internals; ensure child repo dirs are ignored or otherwise intentionally handled.
- If modifying a child plugin, commit/push inside the child repo first. Only then update any parent workspace pointer/docs if needed.
- Before saying a plugin is ready for the user to pull/clone, verify the child repo push with `git ls-remote` or equivalent.

## Vercel note

Vercel deployment/tokens are not a blocker for OSRS RuneLite plugins. These are Gradle/Java plugin projects; completion should focus on build/test, RuneLite manual QA, README/screenshots, and plugin-hub submission prep.
