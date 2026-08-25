# User Project Portfolio Operating Model

Use when revisiting the user's coding/project portfolio under `/opt/data/HeRmEz/projects`.

## Retirement / set-aside pattern

The user does not want finished projects to keep burdening active orchestration. When a project is finished, retired, or set aside:

1. Write a local `PROJECT_HANDOFF_CONTEXT.md` in that project.
2. Include: status, what the project is, useful source files, current decision, how to revive it later, and what not to keep in active memory.
3. Remove/decommission live deployments if the user asks, but only after verifying local context exists.
4. Keep retired projects out of active focus lists unless the user explicitly asks to revive them.

Known retired/set-aside examples from 2026-06:
- `cox-elementary-pta` — finished deployed Django client site; maintenance only.
- `Codology` — concept proven; Vercel deployments removed; context preserved for future coding-school work.
- `stockNews` / `stock_news_backend` — retired as standalone backend; useful ideas moved into Agentic trading cron/reporting.

## Active classification preferences

- `local-meeting-transcriber` is an active build candidate and needs a real frontend + backend, not just a static shell.
- `card-intel-scanner`, `combatatlas`, `local-meeting-transcriber`, `journal-ai`, `music`, `social-media-analysis`, and `tiktok-clone` should be reviewed from an end-user perspective when discussing release readiness.
- `selenium` belongs under the web-automation domain; Hermes already performs browser automation, so old Selenium code is reference material unless a Selenium-specific product is needed.
- `jupyter-notebooks` is a data-science / visualization niche to revisit when the user wants notebook-based review of API or document ingestion data.
- `tiktok-shop-shopify-commerce` is primarily ecommerce/business ops for the user's real TikTok Shop / print-on-demand work, not a core coding project.

## Vercel review preference

For Vercel audits, distinguish:
- clean primary alias health (`project.vercel.app`),
- latest deployment health,
- whether the project is a real app vs static review shell,
- whether it should be fixed, retired, or rebuilt.

Do not call a project production-ready just because Vercel returns HTTP 200.