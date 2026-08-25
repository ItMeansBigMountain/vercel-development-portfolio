# Venice-backed red-team consultation profile

Session learning from configuring a dedicated Hermes red-team specialist profile.

## Provider facts

- Venice API is OpenAI-compatible for chat completions.
- Base URL: `https://api.venice.ai/api/v1`
- Hermes provider: `custom`
- Hermes API mode: `chat_completions`
- Example model used: `venice-uncensored`
- Store the key as `VENICE_API_KEY` in the profile env file and reference `${VENICE_API_KEY}` from config.

## Example profile config excerpt

```yaml
model:
  provider: custom
  base_url: https://api.venice.ai/api/v1
  default: venice-uncensored
  api_key: ${VENICE_API_KEY}
  api_mode: chat_completions
terminal:
  cwd: /opt/data/HeRmEz/projects/penTest
toolsets:
  - terminal
  - file
  - web
  - search
  - session_search
  - skills
  - todo
agent:
  environment_hint: >-
    Red Team consultation profile for authorized security research only. Use
    Venice as the primary model. Work from /opt/data/HeRmEz/projects/penTest
    when relevant. Provide adversarial analysis, bug bounty methodology,
    lab/CTF guidance, defensive detection, and safe PoCs. Do not assist with
    credential theft, malware deployment, stealth/persistence, unauthorized
    attacks, evasion of safety systems, or cheating/botting live services.
```

## Consult wrapper pattern

Create `/opt/data/scripts/redteam_consult.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
PROMPT="${*:-}"
if [[ -z "$PROMPT" ]]; then
  echo "Usage: redteam_consult.sh 'question for redteam'" >&2
  exit 2
fi
exec /opt/data/.local/bin/hermes --profile redteam chat -q "$PROMPT"
```

Then smoke-test:

```bash
/opt/data/scripts/redteam_consult.sh 'Reply exactly: redteam consult online'
```

## Pitfalls

- Do not paste or persist raw Venice keys in config or skill docs. If a key appears in chat or a cached document, recommend rotating it.
- Venice can return HTTP 402 when the account has no USD/Diem credits. Treat that as a billing/account setup blocker, not a Hermes configuration failure.
- Do not describe the specialist as an unrestricted bypass. It is a consultation profile for authorized security work; the main agent still applies safety and authorization boundaries.
