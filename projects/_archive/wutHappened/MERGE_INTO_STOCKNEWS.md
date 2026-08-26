# Merge into stockNews

`wutHappened` and `stockNews` are the same project.

Use `stockNews` as the active deployed codebase because it already has the live frontend/API and portfolio sentiment baseline.

Use this folder as a source archive for ideas and reusable pieces:

- “What happened today that matters to my portfolio?” framing.
- News gathering experiments.
- Portfolio-aware relevance scoring.
- Script/image/video generation ideas for daily recap content.

Primary direction document:

```text
../stockNews/PRODUCT_DIRECTION.md
```

## What to migrate

- Reusable news source code from `NewsApi.py` after key/security review.
- Script generation ideas from `ScriptGenerator.py`.
- Optional visual/video recap ideas from `ImageGenerator.py` and `VideoGenerator.py`.
- Any useful Colab/demo notes from `readme.md`.

## What not to migrate blindly

- `.env` secrets.
- Hardcoded API keys.
- Generated media artifacts.
- Unreviewed scraping behavior.
