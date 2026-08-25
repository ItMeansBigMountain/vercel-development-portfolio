---
name: macos-automation
description: "Use when operating Apple/macOS apps and services from Hermes: Notes, Reminders, Messages, Find My, or background GUI computer-use automation. Provides command-first workflows plus fallback UI automation guidance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [macos, apple, automation, notes, reminders, imessage, findmy, computer-use]
    related_skills: []
---

# macOS Automation

## Overview

This is the class-level umbrella for Apple/macOS local automation. Prefer command-line tools when a purpose-built CLI exists, and fall back to background GUI automation only when no reliable API/CLI path is available.

## When to Use

- Manage Apple Notes, Apple Reminders, iMessage/SMS, or Find My from a macOS host.
- Drive macOS desktop apps through screenshots, clicks, typing, scrolling, or drag/drop without stealing the user's focus.
- Combine Apple app automation with verification screenshots or CLI read-backs.

## Capability Map

### Notes: `memo`

Use for create/search/edit workflows in Apple Notes. Verify the tool exists before promising a result.

- Create or append structured notes.
- Search existing notes before creating duplicates.
- Prefer CLI read-back or a Notes search after writing.

### Reminders: `remindctl`

Use for add/list/complete workflows in Apple Reminders.

- Normalize natural-language due dates before writing.
- List after creating or completing reminders to verify state.
- Avoid guessing list names: inspect available lists when the target is not obvious.

### Messages: `imsg`

Use for sending and reading iMessage/SMS.

- Confirm recipient identity when a name could resolve to multiple people.
- Prefer explicit phone/email handles when supplied.
- Verify send status or recent conversation state when available.

### Find My

Use when locating Apple devices or AirTags on macOS.

- Prefer a scripted/screenshot workflow because Find My exposes little automation surface.
- Capture the map result and report uncertainty, timestamp, and visible location text.
- For repeated tracking, take timestamped screenshots and compare locations over time.

### Background GUI Computer Use

Use for any macOS app with no CLI/API path.

- Capture first; reason about the visible UI; act in small steps; capture again.
- Keep interactions background-safe: do not steal the user's cursor, keyboard focus, or Space.
- Use text input patterns that target the intended field; avoid blind typing.

## Standard Workflow

1. Identify the Apple capability and choose the narrowest reliable tool.
2. Check prerequisites: host is macOS, CLI is installed, account/app state is available.
3. Perform a small action.
4. Verify with CLI read-back or screenshot.
5. Report the result with any uncertainty (especially for maps/location screenshots).

## Common Pitfalls

1. **Using GUI automation before checking for a CLI.** Notes, Reminders, and Messages usually have better command paths.
2. **Treating location screenshots as exact coordinates.** Report what is visible and when it was captured.
3. **Sending messages without identity disambiguation.** Names are not unique; resolve or ask when ambiguous.
4. **Blind background typing.** Always capture before and after UI actions.

## Verification Checklist

- [ ] Correct app/service and account context confirmed.
- [ ] Tool availability checked before use.
- [ ] State-changing action verified by read-back or screenshot.
- [ ] Ambiguities and uncertainty reported clearly.
