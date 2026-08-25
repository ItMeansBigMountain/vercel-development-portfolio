# HeRmEz Vercel triage pattern

This reference captures the reusable pattern from scanning `/opt/data/HeRmEz/projects` after importing legacy projects.

## What to check first

- Confirm token presence without printing it: `VERCEL_TOKEN` or `VERCEL_API_TOKEN`.
- Query Vercel API for existing projects and latest deployment URLs.
- Test public deployment URLs anonymously; if they return `401`, investigate deployment protection/aliases before treating them as manual-test URLs.
- Record findings in `/opt/data/HeRmEz/projects/README.md` and a detailed triage doc such as `projects/VERCEL_TRIAGE.md`.

## Useful project classes

- **Immediate redeploy:** has a working build and existing Vercel project/config.
- **Expo web candidate:** React Native/Expo app; check SDK age and `expo export`/web build behavior.
- **Frontend + backend split:** Angular/React/Vite frontend plus Django/Flask/Express backend; deploy frontend to Vercel and decide separate backend hosting.
- **Backend-only:** Django/Flask/Express; may need serverless adaptation or non-Vercel hosting.
- **Plan/spec only:** README/PROJECT without scaffold; build a new app from the plan.
- **Script/archive:** useful code but not deployable until wrapped in UI/API.

## Example findings format

```markdown
| Project | Type | Current state | What is needed |
|---|---|---|---|
| 3d-react-web | Create React App | `npm run build` passes; existing Vercel project; URL protected | redeploy, fix protection/alias, manual review |
| stockNews | Angular + Django | Angular frontend exists; backend separate | install deps/build frontend; choose backend host |
```

## Common needs to ask the user for

- Whether Vercel deployment protection should be disabled for manual testing.
- Intended public aliases/custom domains.
- Firebase config for apps using Firebase.
- API/backend URL decisions for mobile/web frontends.
- Third-party service credentials only when live integrations are required.
- Database choice/credentials for production backends.
