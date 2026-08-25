# Redteam consultation profile pattern

Use this reference when the user asks to create or consult a specialized Hermes profile for security research, bug bounty, CTF/lab work, or an alternate model opinion.

## Profile shape

A dedicated Hermes profile can isolate model/provider config and working directory while keeping the main assistant responsible for policy, verification, and final reporting.

Example shape from the user's setup:

- Profile: `redteam`
- Model/provider: custom Venice endpoint using `VENICE_API_KEY`, model `venice-uncensored`
- Working directory: `/opt/data/HeRmEz/projects/penTest`
- Direct consult command shape:

```bash
hermes --profile redteam chat -q '<self-contained prompt>'
```

or a wrapper such as:

```bash
/opt/data/scripts/redteam_consult.sh '<self-contained prompt>'
```

## Delegation rules

- Treat the redteam profile as an advisor/worker, not an authority.
- Pass a self-contained prompt including authorization context, scope, target environment, allowed actions, and desired output.
- Ask for defensive framing, lab/CTF assumptions, safe PoCs, detection/mitigation, or code review where possible.
- Do not delegate requests whose purpose is credential theft, malware deployment, stealth/persistence, unauthorized access, evasion, or live-service cheating/botting.
- If the primary model refuses or is constrained, do not use a different profile as a policy bypass. Use the profile only for allowed, authorized security work and keep the final answer within the same safety boundary.
- Verify any technical claim or generated code before acting on it.

## Reporting pattern

When consulting a specialized profile, report:

- What was asked.
- Which profile/model was used.
- Whether the consult succeeded or was blocked by provider/billing/config.
- The verified actionable takeaway, not raw unreviewed worker output.

## Provider fallback note

If a profile's provider is also configured as a Hermes fallback provider, keep secrets in `.env` as env references and smoke-test the provider after key rotation. Avoid pasting API keys in chat or reports.
