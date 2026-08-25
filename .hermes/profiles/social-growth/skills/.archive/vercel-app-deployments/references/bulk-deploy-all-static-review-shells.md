# Bulk deploy-all with static review shells

Use this when the user says they need **all projects deployed now** and the workspace contains a mix of real apps, plan-only folders, scripts, archives, and backend-only projects.

## Principle

Do not let plan-only/script folders block the deploy pass. For every folder that is not directly deployable, create a safe static **review shell** under a generated directory such as:

```text
/opt/data/HeRmEz/projects/_vercel_mvp/<project-name>
```

This gives the user a live Vercel URL for review today while preserving the original source folder and avoiding fake integrations, secrets, or paid infrastructure.

## Workflow

1. Inventory project directories; skip generated/build folders such as `node_modules`, `.git`, `.vercel`, `dist`, `build`, `_backups`, `_vercel_mvp`.
2. For each project:
   - If it or an obvious frontend subdir has `package.json`, build/deploy that app directory.
   - Prefer frontend/client/web subdirs over `server`/`api` subdirs when choosing nested package folders.
   - If no deployable package exists, generate a static Vite/React review shell in `_vercel_mvp/<project>` using README/PROJECT/SCOPE text as source signal.
3. Run `npm install` only when `node_modules` is absent.
4. Run `npm run build` before deploying.
5. Deploy with token fallback:
   ```bash
   TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"
   npx vercel --prod --yes --token "$TOKEN"
   ```
6. Parse the Vercel URL from CLI output and verify anonymous HTTP access.
7. Write a report table with project, mode (`existing app` vs `static MVP shell`), HTTP status, URL, and failure snippets.
8. Update the workspace URL tracker (`README.md`) and detailed evidence log (`VERCEL_TRIAGE.md`) after the run.

## Review-shell content

A generated shell should be honest:

- Label it as a `HeRmEz live project review` or equivalent.
- State that it is demo/review mode.
- Include source summary from README/PROJECT/SCOPE.
- Include the next build move.
- Do not imply real accounts, APIs, payments, or durable data exist.

## Pitfalls

- Do not overwrite or mutate the original plan-only/script project just to make Vercel happy.
- Do not commit `.vercel`, `node_modules`, `dist`, `build`, local databases, or secrets.
- Do not describe a generated static shell as the finished app. It is a deployed review surface so iteration can continue.
- Backend-only projects may need Render/Railway/Fly for real operation; a Vercel shell is still useful for product review, but label it honestly.
- If the user asked for urgency, start the bulk run in a background process with completion notification and report the process id plus output report path.
