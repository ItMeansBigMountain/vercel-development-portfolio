# Project Decommission Workflow

Use this reference when the user asks to delete, retire, or stop seeing a project in the active queue.

## Scope to check

For each project name, check for:

- Source folder: `projects/<project>`
- Generated Vercel/static shell: `projects/_vercel_mvp/<project>`
- Workspace trackers: `README.md`, `WORK_QUEUE.md`, `VERCEL_TRIAGE.md`, `DEPLOY_FINAL_URLS.md`, `DEPLOY_ALL_REPORT.md`
- Bulk deploy scripts or project maps that could recreate the app, e.g. `deploy_all_projects.py`
- Remote Vercel project, if credentials are available

## Recommended sequence

1. Inspect the target folder contents enough to ensure it is the intended project.
2. Delete the source folder and any generated shell.
3. Remove active queue rows and plan-only lists.
4. Update historical trackers with `deleted per user request` and optionally `formerly <url>` rather than deleting all mention of the historical deployment.
5. Remove the project from automation/static shell maps so future bulk-deploy passes do not resurrect it.
6. If a Vercel token is available, list projects, find the exact project slug, delete it, then list again and verify absence.
7. Verify local absence and that the active queue no longer contains the project.

## Verification commands/patterns

```bash
test ! -e projects/<project> && test ! -e projects/_vercel_mvp/<project> && echo 'local folders absent'
```

Use a content search across the workspace to confirm only intentional historical/deleted notes remain.

For Vercel API deletion, avoid printing tokens. Report only project slug/id and HTTP status, never credentials.

## Pitfalls

- Deleting only `projects/<project>` leaves `_vercel_mvp/<project>` behind, which can keep the stale app alive in reports or future deploy scripts.
- Leaving the project in `WORK_QUEUE.md` causes future agents to pick it again.
- Leaving bulk deploy maps unchanged can recreate the supposedly deleted shell.
- Erasing all historical report rows can make old URLs confusing later; mark them as deleted/formerly deployed instead.
