---
name: intelbase
description: Use when the user asks to use IntelBase for authorized email intelligence lookups, breach exposure checks, or to recall IntelBase API details.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [intelbase, osint, breach-check, api, email-lookup]
    related_skills: [professional-work]
---

# IntelBase

## Overview

IntelBase is an API for authorized email intelligence lookups. The documentation index is at `https://docs.intelbase.is/llms.txt`; the scanned docs currently expose one API endpoint: `POST https://api.intelbase.is/lookup/email`.

Use this skill only for legitimate, authorized checks: the user's own accounts, accounts where the account holder consented, or organization-approved security work. Do not use it for doxxing, stalking, harassment, or broad attempts to gather private details about arbitrary people.

## When to Use

- The user asks to check an email address with IntelBase.
- The user asks how the IntelBase API works.
- The user asks for breach/exposure intel for an account they own or are authorized to assess.
- The user asks to reuse the local IntelBase helper script.

Do **not** treat IntelBase as a name/person search engine. The public docs currently document email lookup only.

## API Details

- Documentation introduction: `https://docs.intelbase.is/introduction`
- Documentation index: `https://docs.intelbase.is/llms.txt`
- API intro: `https://docs.intelbase.is/api-reference/introduction.md`
- Email endpoint docs: `https://docs.intelbase.is/api-reference/endpoint/lookup_email.md`
- OpenAPI spec: `https://docs.intelbase.is/api-reference/openapi.json`
- Base URL: `https://api.intelbase.is`
- Auth header: `x-api-key: <INTEL_BASE_API_KEY>`
- Docs note: caller IP must be whitelisted in the IntelBase dashboard.

### Endpoint

```http
POST /lookup/email
content-type: application/json
x-api-key: <INTEL_BASE_API_KEY>

{
  "email": "person@example.com",
  "timeout_ms": 15000,
  "include_data_breaches": false,
  "exclude_modules": []
}
```

Request fields:

- `email` string, required.
- `timeout_ms` integer, optional; maximum lookup time in milliseconds.
- `include_data_breaches` boolean, optional.
- `exclude_modules` array of strings, optional.

## Local Helper

A reusable helper script is available in the user's Git-backed workspace:

```bash
python /opt/data/HeRmEz/scripts/intelbase_lookup.py user@example.com --i-am-authorized
python /opt/data/HeRmEz/scripts/intelbase_lookup.py user@example.com \
  --include-data-breaches \
  --timeout-ms 30000 \
  --i-am-authorized
```

Compatibility wrapper:

```bash
python /opt/data/scripts/intel_base_search.py user@example.com --i-am-authorized
```

The helper reads `INTEL_BASE_API_KEY` from the process environment, `/opt/data/.env`, or `~/.hermes/.env`.

## Workflow

1. Confirm the lookup is authorized/consensual. If the request is to investigate an arbitrary person, refuse that part and offer safe alternatives (e.g., explain how the user can check their own exposure).
2. Use the documented email endpoint only; do not invent name, phone, username, or address endpoints.
3. Run the helper with `--i-am-authorized` and any optional flags requested.
4. Summarize results carefully. Avoid dumping sensitive personal data unnecessarily; focus on actionable security remediation such as password resets, MFA, passkeys, and breach monitoring.
5. If the API returns an IP whitelist or auth error, tell the user to whitelist the VPS IP in the IntelBase dashboard.

## Common Pitfalls

1. **Wrong auth style.** IntelBase uses `x-api-key`, not `Authorization: Bearer`.
2. **Wrong endpoint.** The documented endpoint is `https://api.intelbase.is/lookup/email`, not `https://intelbase.com/api/v1/search`.
3. **Assuming name search exists.** The public OpenAPI spec currently includes only `/lookup/email`.
4. **Forgetting IP whitelisting.** The docs explicitly state that the caller IP must be whitelisted.
5. **Leaking the API key.** Never print or commit `INTEL_BASE_API_KEY`.

## Verification Checklist

- [ ] API key exists in environment or `/opt/data/.env`.
- [ ] Caller IP is whitelisted in IntelBase if API returns authorization/IP errors.
- [ ] Lookup target is authorized/consensual.
- [ ] Helper command includes `--i-am-authorized`.
- [ ] Response is summarized without unnecessary sensitive data exposure.
