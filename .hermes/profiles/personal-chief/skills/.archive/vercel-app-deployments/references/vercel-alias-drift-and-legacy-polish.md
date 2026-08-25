# Vercel Alias Drift + Legacy App Polish Notes

Use this when continuing a multi-project Vercel triage/polish pass where some projects have both real app deployments and static review-shell deployments.

## Problem pattern

A friendly alias can drift to the wrong deployment. In this session, a project README/tracker claimed the alias was the real app, but browser verification showed the alias serving a generic static review shell. The real app still existed at an older production deployment URL.

## Verification pattern

1. Do not trust tracker rows alone. Open the alias in the browser and confirm the page content matches the expected app, not a placeholder shell.
2. If an alias serves a shell, open the latest known real-app deployment URL from project docs/tracker and verify it visually.
3. Repoint the alias explicitly:

```bash
TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"
npx vercel alias set <real-deployment-host>.vercel.app <friendly-alias>.vercel.app --token "$TOKEN"
```

4. Reload the friendly alias in the browser and verify expected app content.
5. If further changes are needed, build/export from the actual deployable subdirectory, deploy production, and verify the alias after deploy.

## Expo web app pattern

For nested Expo apps, run export from the Expo subdirectory, not the monorepo/root:

```bash
cd <project>/<expo-subdir>
npx expo export --platform web
TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"
npx vercel deploy --prod --yes --token "$TOKEN"
```

If tests live at the parent/root, run them from the root separately, then return to the Expo subdirectory for export/deploy.

## Browser QA checks for education/quiz apps

For quiz-style apps, visual verification should include at least:

- Friendly alias serves the real app, not a static shell.
- Header/action buttons are readable, not invisible native-button artifacts.
- First question screen shows all answer options without important controls being cut off in the initial viewport, or scrolling is clearly possible.
- Console has no JS errors after starting the quiz.

## Durable lesson

For bulk-deployed legacy workspaces, static review shells are useful as placeholders but dangerous if aliases later point to them by accident. Always verify by page content and be ready to repoint aliases before spending time debugging the wrong deployment.