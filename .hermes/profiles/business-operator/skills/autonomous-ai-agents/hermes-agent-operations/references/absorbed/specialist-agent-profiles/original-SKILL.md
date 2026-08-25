---
name: specialist-agent-profiles
description: "Configure and operate dedicated Hermes specialist profiles with separate model providers, working directories, tools, env secrets, and consultation wrappers."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, profiles, custom-providers, multi-agent, consultation, redteam]
---

# Specialist Agent Profiles

Use this skill when the user wants a named Hermes agent/profile for a recurring class of work, such as security review, design, research, review, or any workflow that benefits from a separate model, working directory, tools, and standing instructions.

## Core pattern

1. **Create or inspect the profile first.**
   - `hermes profile list`
   - `hermes profile create <name> --clone default` if it does not exist.
2. **Keep secrets out of config.** Put provider keys in the profile env file, e.g. `/opt/data/profiles/<name>/.env`, and reference them in config as `${ENV_VAR}`.
3. **Configure the profile model explicitly.** For OpenAI-compatible custom endpoints, set:
   ```yaml
   model:
     provider: custom
     base_url: https://example.com/v1
     default: model-id
     api_key: ${PROVIDER_API_KEY}
     api_mode: chat_completions
   ```
4. **Set a profile-specific working directory** under `terminal.cwd` when the agent has a canonical repo or workspace.
5. **Use a scoped toolset** rather than copying all tools blindly. Give the specialist the tools it needs for its role.
6. **Add a standing `agent.environment_hint`** that defines the profile's job, operating boundaries, default repo, and any user-specific conventions.
7. **Create a consult wrapper** when the main agent should query the specialist from future sessions. Prefer a simple script such as `/opt/data/scripts/<profile>_consult.sh` that runs:
   ```bash
   hermes --profile <profile> chat -q "$PROMPT"
   ```
8. **Smoke-test the profile** with a harmless exact-output prompt before reporting readiness.

## Red-team / security specialist profile rules

When creating a security-focused specialist profile, keep the role useful but bounded:

- Good uses: authorized security research, lab/CTF work, TryHackMe/HackTheBox, scoped bug bounty methodology, defensive review, exploit explanation, safe proof-of-concepts, detection logic, and tool usage in owned environments.
- Do not position another model/provider as a safety bypass. The main agent may consult a specialist for perspective, but must still apply policy and authorization boundaries before acting on or relaying advice.
- Include explicit boundaries in the profile environment hint: no credential theft, malware deployment, stealth/persistence, unauthorized attacks, live-service game cheating/botting, or safety-control evasion.
- If a provider refuses or lacks credits, record the fixable setup state (billing/credits/API key) and do not claim the specialist is operational until a live smoke test succeeds.

## Verification checklist

- `hermes profile list` shows the profile, model, and alias if configured.
- Profile config references env vars, not raw secrets.
- `hermes --profile <name> chat -q 'Reply exactly: ...'` returns the expected response.
- If using a custom endpoint, test the provider directly or through Hermes and capture HTTP errors without leaking the key.
- Save durable profile details in memory/fact store only at the stable level: profile name, path, model/provider, repo path, consult command, and unresolved account setup such as missing credits.

## References

- `references/venice-redteam-profile.md` — session-specific pattern for a Venice-backed red-team consultation profile.

## Scripts

- `scripts/consult_profile.sh` — reusable wrapper template for querying a named Hermes profile from shell scripts or future agent sessions.
