# IBM Watson NLU app-integration repair pattern

Session-derived pattern for repairing multiple app integrations that depend on IBM Watson Natural Language Understanding (NLU) after credentials have changed or legacy Tone Analyzer code no longer works.

## Trigger

- A repo contains several Python/JS apps referencing Watson, IBM NLU, Tone Analyzer, or old `WATSON_*` environment variables.
- The user wants Watson-dependent projects fixed broadly, not just one endpoint.
- A working Watson NLU API key is available in a local credential JSON file or secure environment variables.

## Secure discovery

Search broadly, but do not print secrets:

```bash
cd /path/to/workspace
rg -n "Watson|watson|Natural Language|NLU|ToneAnalyzer|Tone Analyzer|WATSON_|IBM_WATSON" projects
```

Then inspect likely wrappers first (`watson.py`, `watson_service.py`, API view/controller files) before patching callers. Check `.gitignore` before touching `.env` files.

## Credential compatibility layer

Prefer a shared wrapper pattern per app that accepts several legacy env var names plus a local file fallback:

- API key env names: `WATSON_API_KEY`, `WATSON_APIKEY`, `WATSON_NLU_APIKEY`, `IBM_WATSON_API_KEY`
- URL env names: `WATSON_SERVICE_URL`, `WATSON_INSTANCE_URL`, `WATSON_NLU_URL`, `IBM_WATSON_SERVICE_URL`
- Local fallback file: `/opt/data/credentials/ibm-nlu-api-key.json` when available in this environment
- Default NLU API version: `2022-04-07`

Do not hardcode API keys in committed code. `.env` files may be updated locally if ignored by git, but committed code should load from env/file and fail clearly when credentials are absent.

## Tone Analyzer compatibility

IBM Watson Tone Analyzer is deprecated/commonly unavailable. If legacy code expects calls like `toneLogin()` / `tone_CLIENT(...)`, implement compatibility helpers on top of NLU sentiment/emotion instead of trying to resurrect Tone Analyzer credentials.

Recommended behavior:

1. `toneLogin()` returns the NLU client.
2. `tone_CLIENT(client, text)` calls NLU analyze with sentiment and emotion features.
3. Return a tone-like shape that preserves old caller expectations, but label it as compatibility in code comments.

## Verification workflow

Run focused smoke tests for every integration rather than only importing modules:

```bash
python3 - <<'PY'
# Example shape only: import the app wrapper, login, analyze harmless text,
# and print language + sentiment label without printing credentials.
PY
```

For web APIs, verify the real endpoint path locally or in staging with a harmless request and check that the response identifies Watson as the analyzer or contains NLU-derived fields.

Also run existing tests. Watch for app modules that launch servers on import; wrap `application.run(...)`/`app.run(...)` with `if __name__ == '__main__':` so test imports do not hang.

## Deployment notes

For serverless deployments, update provider environment variables after local verification. For Vercel specifically, remove/re-add or update env vars for production/preview/development as needed, then redeploy and verify the live endpoint. Pass tokens without echoing them and never include secret values in summaries.

## Safety checklist

- [ ] No full API keys, passcodes, or tokens printed in chat or committed logs.
- [ ] Existing provider outputs that redact keys are not treated as usable secrets.
- [ ] Credential JSON files have restrictive permissions where possible.
- [ ] `.env` files remain untracked or ignored.
- [ ] Tracked files are scanned for the active secret before commit.
- [ ] Each affected app has a real smoke test or existing test run.
