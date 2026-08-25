---
name: browser-assisted-personal-applications
description: "Use when helping the user find, evaluate, and apply to real-world personal services or programs via the browser: local clinics/programs, intake forms, appointments, memberships, applications, and similar web forms."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [browser, applications, forms, local-search, intake, appointments]
---

# Browser-Assisted Personal Applications

## Overview

Use this skill when the user asks Hermes to start, apply for, sign up for, schedule, or otherwise operate a personal real-world service through websites. The goal is to actively use browser/web tools to find the best official intake path, identify requirements, gather only needed information, and submit only after explicit confirmation.

## Workflow

1. **Localize first.** If the service depends on location, search using the user's current stated city/suburb and nearby metro. Do not assume old location context; accept mid-turn corrections immediately and pivot.
2. **Prefer official program/provider pages.** Use official application/intake pages over directory pages, SEO articles, or patient-facing pages meant for recipients rather than applicants.
3. **Compare nearby options briefly.** Capture the nearest credible option and one fallback, especially when one location is closer but has stricter eligibility or a weaker application flow.
4. **Open the application form before asking for data.** Inspect form fields/placeholders so the user only has to provide the exact required fields. For branded or multi-location programs, inspect the application's actual location choices before promising that the requested city is supported; a city-specific marketing page does not guarantee that city appears in the intake form.
5. **Resolve location mismatches before account creation.** If the requested city is absent from the form, do not silently choose another branch. Pause, show the available branches, and offer to find an official local provider. Preserve any entered data only while the page remains open; do not submit.
6. **Summarize requirements before submission.** List eligibility constraints, location/visit frequency, compensation/costs if shown, contact info, and any consent implied by required fields (for example, a phone field that authorizes calls/texts even when the user previously declined reminders).
7. **Ask for explicit submit permission.** Filling fields may be okay after the user provides data, but do not submit personal, medical, financial, legal, or identity-related applications without a final confirmation.
8. **Protect sensitive data.** Do not save completed form contents or personal medical details in memory/skills. Store only reusable workflow notes or public provider quirks.
9. **Handle account credentials separately.** Do not ask users to paste an existing/reused password into chat. Prefer a user-entered browser handoff when available; otherwise ask for a newly generated, site-unique password only when the account page is ready, never repeat it in summaries, and do not retain it after entry.
10. **Advance one page at a time.** For long medical or identity applications, collect only the fields visible on the current page, fill them, inspect the next page, and continue iteratively. Do not ask for the entire medical history before seeing the actual field wording.

## Browser/Form Tactics

- If search-engine browser navigation hits bot detection, use `web_search` for discovery, then navigate directly to the official result.
- If button clicks do not visibly navigate, inspect anchors with browser console, e.g. list link text/hrefs, then navigate directly to the real URL.
- On forms where the accessibility tree hides labels, inspect `input`, `textarea`, and `select` placeholders/names/ids to derive the field list. For long Gravity Forms or similar pages, map each field container's visible text to its contained control IDs; this exposes conditional questions and consent language without guessing.
- For custom Material UI selects that do not open on a normal click, focus the `[role="combobox"]` and press Space, then inspect/click the rendered `[role="option"]` items. Verify the selected text/value afterward.
- Prefill only stable, user-supplied non-medical details while researching a replacement provider. Do not infer address, age, height, ancestry, family history, infectious-disease answers, or other eligibility facts.
- Verify location selectors against the live options before telling the user that their requested city is supported. Never infer that a public office/recipient page implies the applicant portal offers that city. If the requested city is absent, fill only non-controversial fields, leave the location unset, and ask the user to choose among actual options or authorize finding a different local provider.
- For custom Material UI selectors, a click may not expose options and `document.querySelectorAll('select')` may be empty. Focus `[role="combobox"]`, press `Space`, then inspect/click the rendered `[role="listbox"] [role="option"]` entries. Treat the opened listbox as the authoritative option set for that page load.
- If a page is for consumers/patients rather than applicants/donors/workers, keep searching for "become", "apply", "donor application", "intake", or "provider application" pages.

## Safety and Consent

- Treat medical, fertility, identity, financial, and employment-adjacent forms as sensitive.
- Never infer sensitive answers such as age, height, medical history, citizenship, sexual history, or health status.
- Never submit a form just because the user said "start"; collect the required fields and obtain explicit confirmation right before the submit click.
- If eligibility criteria may exclude the user, present them neutrally and let the user decide whether to proceed.

## References

- `references/sperm-donor-program-intake.md` — notes from a Chicago-suburbs sperm donor program search and form-inspection pattern.
- `references/denver-sperm-donor-intake.md` — Fairfax location-selector mismatch, official Denver alternative, consent wording, and long-form inspection pattern.

## Verification Checklist

- [ ] Official/local provider page found.
- [ ] Eligibility and logistics summarized from the page.
- [ ] Form fields inspected rather than guessed.
- [ ] User supplied all required personal fields.
- [ ] Explicit final confirmation obtained before submitting.
- [ ] Contact info or application URL given if not submitted.
