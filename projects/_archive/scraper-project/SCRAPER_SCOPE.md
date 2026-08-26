# Scraper Project - Scope

- **Date:** 2026-05-03
- **Legacy base:**
  - `legacy-src/news-webcrawler-app`
  - `legacy-src/web-crawl`
  - `legacy-src/reddit-scraper`

## Immediate target

Build a reusable **news/provider ingestion layer** that can feed the Portfolio Sentiment Subscription App.

This avoids random scraping chaos. First target is not “scrape the whole internet.” First target is:

```text
provider/search source -> normalized headline records -> JSON output -> portfolio sentiment app
```

## Output format

Each item should normalize to:

```json
{
  "title": "headline text",
  "summary": "short summary or blank",
  "url": "https://example.com/story",
  "source": "provider/source name",
  "date": "YYYY-MM-DD",
  "tickers": ["AAPL", "MSFT"],
  "raw": {}
}
```

## First safe source strategy

1. **Sample provider** — local JSON only, already used by portfolio MVP.
2. **RSS/news provider** — use public RSS feeds or a selected API only after source choice.
3. **Site scraper** — only when robots/terms/rate limits allow it.
4. **Reddit/Twitter/X scripts** — treat as separate provider because auth/API rules are fragile.

## Rules

- Do not run aggressive crawlers.
- Respect robots.txt, site terms, and rate limits.
- Default to cached/sample data.
- All API keys must come from `.env`.
- Do not commit `.env`, tokens, cookies, or browser profiles.
- No account login scraping unless manually approved.

## Proposed project structure

```text
scraper-project/
  src/
    config.py
    providers/
      sample.py
      rss.py
      legacy_adapter.py
    normalize.py
    export_json.py
  sample-data/
    headlines.json
  legacy-src/
    ...imported old code...
```

## Legacy reuse notes

| Legacy source | Useful parts | Caution |
| --- | --- | --- |
| `news-webcrawler-app` | crawler/newsletter structure | One unreadable placeholder/artifact was skipped during import |
| `web-crawl` | spider/link map, finviz script | Needs rate limiting and safer boundaries |
| `reddit-scraper` | trend extraction concepts | API/auth rules may have changed; do not assume it still runs |

## First implementation slice

Create a tiny provider interface with:

- `sample` provider reading local JSON
- normalizer function
- export command that writes normalized `headlines.json`

## Validation

```powershell
cd C:\Users\faree\Desktop\OpEnCLAw\scraper-project
python -m py_compile src\*.py src\providers\*.py
python src\export_json.py --provider sample --out sample-data\headlines.normalized.json
```

## Blockers / user decisions needed later

- Pick the first real source/API for live news ingestion.
- Provide API credentials manually if needed.
- Approve any source-specific scraping that may touch terms/rate-limit boundaries.
