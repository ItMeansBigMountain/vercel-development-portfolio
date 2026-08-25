# Pythonista Automation Tick Implementation Pattern

Use this when the user wants “autonomous” iPhone software that tracks things without manually opening Pythonista.

## Durable iOS constraint

Pythonista cannot run as a permanent silent background daemon on normal iOS. The practical architecture is a fast one-shot script launched by Siri Shortcuts Automations, URL schemes, Share Sheet, or manual launcher.

## Recommended shape

```text
cellphone_scripts/
  toolkit/
    agent_tick.py
    launcher.py
    lib/
      storage.py
      ios_runtime.py
    tools/
      where_was_i.py
      clipboard_history.py
      location_reminders.py
    data/
      *.json
```

## `agent_tick.py` responsibilities

Each tick should:

1. Capture current location if available.
2. Read clipboard if available and store only new values.
3. Check location reminders against the latest location.
4. Append to local JSON stores.
5. Return/print a short summary for Shortcuts logs.
6. Exit quickly.

Do not pretend it is always running. Phrase it as “autonomous-ish” or “Shortcuts-triggered.”

## Testability pattern

Separate iOS runtime wrappers from pure logic:

- `ios_runtime.py` lazily imports Pythonista modules (`location`, `clipboard`, etc.).
- Tool classes accept injected providers for location/clipboard in tests.
- JSON persistence uses small stdlib-only helpers.
- Desktop tests validate storage, dedupe, geofence math, and tick orchestration without Pythonista installed.

## Good first tools

- `where_was_i.py`: private location timeline with note + map link.
- `clipboard_history.py`: local clipboard snapshots with dedupe/search/classification.
- `location_reminders.py`: reminder records with radius checks.

## Shortcuts setup notes

Create iOS Automations for:

- Time of day.
- Arrive/leave locations.
- Focus Mode changes.
- Bluetooth/CarPlay connect/disconnect.
- Action Button or Back Tap.

Each automation runs/open Pythonista URL such as:

```text
pythonista3://toolkit/agent_tick.py?action=run
```

## Pitfalls

- Do not auto-send safety/emergency messages from a tick; prepare drafts only.
- Do not store more clipboard/location history than the user understands; document local JSON files and privacy.
- Avoid third-party packages so scripts remain Pythonista-compatible.
