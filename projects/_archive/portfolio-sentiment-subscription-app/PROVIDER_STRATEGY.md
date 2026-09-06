# Free-First Data Provider Strategy

## Date: 2026-05-04

## Goal

Enable the app to run without credentials using free/fallback sources, with clear upgrade paths for paid providers.

## Provider Priority Order

1. **Sample Data (always available)**
   - Location: `sample-data/news.json`, `sample-data/watchlist.json`
   - No credentials required
   - Used for local development and offline mode

2. **RSS Feeds (free, no auth)**
   - Sources: Yahoo Finance, MarketWatch, Reuters Tech
   - Parse headlines and basic sentiment
   - Fallback when API keys unavailable

3. **Free API Tiers (with limits)**
   - NewsAPI.org (free tier: 500 requests/day)
   - Finnhub (free tier: 60 requests/minute)
   - Alpha Vantage (free tier: 5 requests/minute)
   - Requires user-provided API key in `.env`

4. **Reddit/X (later, auth required)**
   - Subreddit sentiment (e.g., r/investing, r/stocks)
   - Requires OAuth/approval
   - Marked as optional future enhancement

## Configuration

### `.env.example` additions

```env
# Provider selection: sample | rss | newsapi | finnhub | alpha_vantage
NEWS_PROVIDER=sample

# Free tier API keys (user must provide)
NEWS_API_KEY=
FINNHUB_API_KEY=
ALPHA_VANTAGE_API_KEY=

# RSS fallback sources (comma-separated URLs)
RSS_SOURCES=https://feeds.reuters.com/reuters/marketsNews.rss,https://www.marketwatch.com/rss/topstories
```

## Implementation Notes

- App defaults to `sample` provider when no credentials provided
- Each provider implements a common interface: `fetchNews(tickers: string[]): Promise<Article[]>`
- Provider chain: try preferred, fallback to next on failure/rate-limit
- All providers are read-only; no trading or account actions

## Validation

- [ ] `provider-strategy.md` exists
- [ ] Local sample fallback passes `/api/dashboard` validation
- [ ] `.env.example` updated with provider config names