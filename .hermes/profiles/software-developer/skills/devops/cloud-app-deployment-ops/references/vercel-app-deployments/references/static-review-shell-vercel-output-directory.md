# Static review shells and Vercel output-directory drift

When bulk-deploying legacy/plan-only/script folders as Vite static review shells, linked Vercel projects can inherit stale project settings from an earlier app. A common failure is:

```text
Error: No Output Directory named "build" found after the Build completed.
Configure the Output Directory in your Project Settings.
```

This can happen even when `npm run build` succeeds locally because Vite outputs `dist` while the remote project still expects `build`.

## Fix pattern

For each generated static shell, write an explicit `vercel.json` in the deployed shell directory:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}
```

Then build locally and deploy:

```bash
npm install
npm run build
TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"
npx vercel --prod --yes --token "$TOKEN"
```

## Recovery pass for a mostly-successful bulk deploy

1. Parse the URL tracker/report for rows with non-200 or missing URLs.
2. Generate clean Vite shells under `_vercel_mvp_fix/<project>` rather than mutating legacy source.
3. Include the explicit `vercel.json` above.
4. Deploy each fix shell.
5. Update `DEPLOY_FINAL_URLS.md`, `PROJECT_REVIEW_SHEET.md`/`.csv`, and workspace `README.md`.
6. Re-run anonymous HTTP verification across the full final URL table; do not report completion until all intended URLs return public 200.

## Sheet/goal artifacts

For workspace-wide modernization requests, maintain these durable files in `/opt/data/HeRmEz/projects`:

- `PROJECT_REVIEW_GOAL.md` — standing operator goal and checklist.
- `PROJECT_REVIEW_SHEET.md` / `.csv` — per-project classification, tech stack, live URL, HTTP status, and modernization/consumer-psychology notes.
- `DEPLOY_FINAL_URLS.md` — concise verified production URL table.

The review sheet should include both real app deployments and honest static review shells so the user can visually review every legacy project from a live baseline.
