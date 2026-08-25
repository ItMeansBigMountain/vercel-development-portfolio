# cellphone_scripts 2026 Scope Notes

Derived from a session scoping `/opt/data/HeRmEz/projects/cellphone_scripts`, an older Pythonista iOS script collection.

## Existing Inventory Shape

- `requests_dataScience/` — API/demo scripts: NASA, air quality, recipes, Pokémon, VIN, memes, advice, FBI, COVID.
- `business_tools/` — email read/send, Google reviews, interest calculator, file naming.
- `health_apps/` — mood chart, workout extraction, workout planning.
- `networking/` — IP geolocation, MD5 cracking, DDoS demo.
- `algos/` — sorting, distance, slope, magic squares, animation learning demos.

## Key Lesson

For 2026, the durable opportunity is not “random Python scripts.” It is a **Pythonista Pocket Toolkit**: iPhone automations launched from Share Sheet, clipboard, Photos, Files, and Siri Shortcuts.

## Good First Sprint

1. Create shared toolkit helpers: storage, iOS input, simple UI, config.
2. Build `toolkit_launcher.py` as a central menu.
3. Modernize three practical scripts first:
   - `DailyMoodChart.py` → `mood_tracker.py`
   - `file_naming_convention.py` → `smart_renamer.py`
   - `memeGenerator.py` → `meme_studio.py`
4. Add Shortcuts setup notes per tool.
5. Archive unsafe/outdated networking scripts, especially DDoS-style demos.

## Pythonista Modules Worth Remembering

Pythonista exposes iOS-specific modules useful for this class of work: `appex`, `clipboard`, `contacts`, `location`, `photos`, `reminders`, `speech`, `ui`, `scene`, `notification`, `objc_util`, and `shortcuts`.

## Product Principles

- One script equals one obvious phone job.
- Prefer Share Sheet/clipboard/photo input over typing.
- Prefer local/private storage over cloud accounts.
- Customer-facing tools should be tap-friendly and immediate.
- Hardcoded secrets must become configuration examples, never active defaults.
