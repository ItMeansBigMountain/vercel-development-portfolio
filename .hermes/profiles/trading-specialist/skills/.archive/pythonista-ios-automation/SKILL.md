---
name: pythonista-ios-automation
description: Build and modernize Pythonista for iOS scripts into tap-friendly iPhone/iPad automation toolkits.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [pythonista, ios, shortcuts, automation, python, mobile]
platforms: [ios, linux, macos]
triggers:
  - Pythonista
  - iOS Python scripts
  - cellphone scripts
  - Siri Shortcuts with Python
  - Share Sheet automation
  - iPhone automation toolkit
---

# Pythonista iOS Automation

Use this skill when working on Pythonista/iOS script collections, especially older terminal-style Python scripts that should become useful phone-native tools.

## Core Direction

Modern Pythonista value comes from **iPhone-native workflows**, not random terminal demos:

- Share Sheet input via `appex`
- Clipboard workflows via `clipboard`
- Photos/files input and output
- Siri Shortcuts / Pythonista URL launchers
- Simple `ui` screens for tap-friendly tools
- Local/private data storage where possible
- Notifications, reminders, contacts, speech, location, and `objc_util` only when useful

Default product framing: **Pocket Toolkit** — one obvious phone task per script.

## Modernization Checklist

1. Inventory scripts by user outcome, not folder name.
2. Identify which scripts should become phone tools, which remain learning demos, and which should be archived.
3. Replace `input()`-heavy flows with Share Sheet, clipboard, file/photo picker, or a small `ui` form.
4. Move hardcoded secrets into config/env examples and document iOS Keychain or manual setup.
5. Avoid unsafe public demos in the active toolkit; quarantine DDoS/cracking-style scripts under an archive folder.
6. Add a central launcher script for non-Shortcuts usage.
7. Add Shortcuts setup notes for each daily-use script.
8. Test on desktop only for pure logic; clearly mark iOS-only modules that require Pythonista.
9. For "always running"/tracking requests, build a one-shot `agent_tick.py` runner for Siri Shortcuts Automations rather than a fake background daemon.

## Autonomous-ish Tracking Pattern

When the user asks for software that is constantly running on iPhone, explain the iOS constraint briefly and implement the practical pattern: **Shortcuts-triggered automation ticks**. A tick script should run quickly, capture context, update local/private JSON state, issue useful notifications, then exit. Good tick tools include location timeline logging, clipboard history, and location-based reminder checks. See `references/pythonista-ios-automation/automation-tick-pattern.md` for a reusable implementation shape and testing strategy.

## High-Value 2026 Script Ideas

- Share Sheet text cleaner/summarizer/reply drafter
- Receipt scanner and local expense logger
- Personal CRM quick log from contacts/clipboard
- Mood and habit micro-dashboard
- Workout timer/planner/tracker
- Photo batch resize/rename/watermark/compress tool
- Clipboard command center for URLs, text, images, phone numbers, addresses
- Meeting notes summarizer from pasted transcript
- Smart iCloud/photo file renamer
- Phone API playground with saved endpoints
- Meme/microcontent generator
- Location/parking/context logger
- Personal safety check-in script that prepares, but does not auto-send, messages
- JSON/regex/hash/base64 developer scratchpad
- Web-to-Markdown clipper

## Suggested Folder Shape

```text
cellphone_scripts/
  toolkit/
    launcher.py
    lib/
      storage.py
      ios_input.py
      simple_ui.py
      config.py
    tools/
      mood_tracker.py
      smart_renamer.py
      meme_studio.py
      clipboard_center.py
      receipt_logger.py
  archive/
    original_scripts/
    unsafe_or_obsolete/
  docs/
    shortcuts_setup.md
    pythonista_setup.md
```

## Pitfalls

- Don’t call it modernized if it still requires terminal prompts for every action.
- Don’t put API keys, email passwords, or personal addresses in scripts.
- Don’t auto-send safety/emergency messages; prepare drafts and ask for user confirmation.
- Don’t overbuild web dashboards when the user wants something runnable directly on iPhone.
- Don’t assume every Python package works in Pythonista; prefer stdlib and Pythonista’s built-in iOS modules.

## References

- `references/pythonista-ios-automation/cellphone-scripts-2026-scope.md` — session-derived scope for converting a Pythonista script archive into a Pocket Toolkit.
- `references/pythonista-ios-automation/automation-tick-pattern.md` — reusable pattern for "always running" Pythonista requests using Siri Shortcuts-triggered one-shot ticks.
