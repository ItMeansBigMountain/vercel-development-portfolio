# Portfolio Sentiment Subscription App - MVP Spec

- **Date:** 2026-05-03
- **Legacy base:**
  - `legacy-src/financial-market-ml`
  - `legacy-src/news-webcrawler-app`

## Goal

Create a presentable subscription app that summarizes market/news sentiment for a user-selected watchlist or portfolio.

## MVP user flow

1. User opens dashboard.
2. User enters or selects ticker symbols.
3. App fetches recent news headlines/articles from a safe provider or sample-data mode.
4. App calculates basic sentiment and market context.
5. App displays:
   - watchlist summary
   - sentiment score per ticker
   - latest relevant headlines
   - basic trend/market context
   - email/report preview
6. Subscription/paywall remains stubbed until provider is chosen.

## Initial architecture

```text
frontend/          Presentable dashboard UI
backend/           API for watchlist, news ingestion, sentiment, reports
legacy-src/        Read-only imported reference code
sample-data/       Offline fixtures for safe local development
scripts/           Migration/adaptation scripts
```

## Recommended stack

Use a simple modern web stack when implementation starts:

- Frontend: Next.js or Vite React
- Backend: FastAPI or Next.js API routes
- Data: SQLite locally first, Postgres later
- Sentiment: start with TextBlob/VADER or transformer only after simple baseline works
- Reports: local generated HTML/email preview before real email delivery

## `.env.example` variables to support

```env
APP_ENV=development
APP_BASE_URL=http://localhost:3000
DATABASE_URL=sqlite:///./local.db
NEWS_API_KEY=
MARKET_DATA_PROVIDER=yfinance
SENTIMENT_PROVIDER=baseline
EMAIL_PROVIDER=disabled
EMAIL_FROM=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

## Legacy code reuse plan

| Legacy source | Reuse | First action |
| --- | --- | --- |
| `financial-market-ml` | Market features, notebooks, ticker workflows, yfinance examples | Extract only reusable functions; avoid notebook-first architecture |
| `news-webcrawler-app` | Crawler/newsletter shape | Convert crawler into provider interface with sample-data mode |

## Constraints

- Do not use real financial credentials in code.
- Do not commit `.env`.
- Keep sample-data mode working without external APIs.
- Avoid trading actions. This app reports/educates only.
- Subscription/payment integration is manual/approval-sensitive before real keys are used.

## First implementation slice

Create a local sample dashboard that reads `sample-data/news.json` and `sample-data/watchlist.json`, computes baseline sentiment, and renders a clean portfolio sentiment summary.

## Validation

Before marking implementation done:

```powershell
# chosen stack will define exact commands later
# expected gate: install, lint/typecheck, local run/build, and sample dashboard screenshot/check
```
