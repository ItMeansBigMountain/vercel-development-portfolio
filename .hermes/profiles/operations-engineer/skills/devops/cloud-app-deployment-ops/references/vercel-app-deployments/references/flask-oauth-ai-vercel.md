# MusicAI-style Flask integrations on Vercel

Use this reference when turning an imported/legacy Flask app with OAuth + API credentials into a live Vercel demo without rebuilding it from scratch.

## Pattern

1. **Pick up the existing app first.** Inspect the legacy Flask entrypoint (`musicAI.py`, `app.py`, etc.), templates, `.env.example`, and tests before considering a rewrite.
2. **Make env names compatible instead of renaming everything.** Add aliases in the integration layer when legacy code expects old names. For Watson NLU, accept common variants such as `WATSON_API_KEY`, `WATSON_SERVICE_URL`, `WATSON_NLU_APIKEY`, `WATSON_NLU_URL`, `IBM_NLU_API_KEY`, and `IBM_NLU_URL`.
3. **Add a Vercel Python entrypoint** while leaving the legacy app intact:

   ```python
   # api/index.py
   from pathlib import Path
   import sys

   PROJECT_ROOT = Path(__file__).resolve().parents[1]
   if str(PROJECT_ROOT) not in sys.path:
       sys.path.insert(0, str(PROJECT_ROOT))

   from musicAI import application as app
   application = app
   ```

4. **Add `vercel.json` routes** for the Flask app:

   ```json
   {
     "version": 2,
     "builds": [{ "src": "api/index.py", "use": "@vercel/python" }],
     "routes": [{ "src": "/(.*)", "dest": "api/index.py" }]
   }
   ```

5. **Expose low-risk verification routes.** Add `/healthz` that only reports booleans like `spotify_configured`, never secret values. Add a small direct API/UI path (for example `/api/analyze-text` and `/analyze-text`) that can verify Watson or another integration without requiring OAuth login.
6. **Deploy with explicit env vars** if using `npx vercel`, because local `.env` is ignored by Vercel unless imported/set:

   ```bash
   set -a; . ./.env; set +a
   npx vercel --prod --yes --token "$VERCEL_API_TOKEN" \
     --env SPOTIFY_CLIENT_ID="$SPOTIFY_CLIENT_ID" \
     --env SPOTIFY_CLIENT_SECRET="$SPOTIFY_CLIENT_SECRET" \
     --env SPOTIFY_CALLBACK_URL="$SPOTIFY_CALLBACK_URL" \
     --env GENIUS_API_KEY="$GENIUS_API_KEY" \
     --env WATSON_API_KEY="$WATSON_API_KEY" \
     --env WATSON_SERVICE_URL="$WATSON_SERVICE_URL" \
     --env FLASK_SECRET_KEY="$FLASK_SECRET_KEY"
   ```

7. **OAuth callback discipline.** After deployment, set the production callback in the third-party developer dashboard exactly as the live app emits it, including scheme, host, path, and trailing slash. For Spotify this was `https://<alias>/login/`. Then redeploy/update the app env to use the same `SPOTIFY_CALLBACK_URL`.
8. **Verify anonymously.** Check `/healthz`, a no-login UI route, and a no-login API route from the public alias. For OAuth, fetch the homepage and parse the generated Spotify authorize URL to confirm `redirect_uri` and `response_type=code`.
9. **Update trackers.** Update workspace URL trackers, credential-status docs, and work queue with live URLs and remaining manual OAuth-dashboard steps.

## Pitfalls

- Do not print secrets in chat, docs, or diffs. Use `<set>`/boolean reporting.
- Do not rely on local `.env` being picked up by Vercel automatically.
- Do not mark OAuth fully tested until the provider dashboard callback has been added and a live login round trip has been attempted.
- Serverless Vercel Flask is fine for demos/read-mostly flows; avoid local files for durable user-token storage in production because serverless filesystems are ephemeral.
