# Discord Channel Routing Pattern — 2026-07

Use this reference when the user asks to organize Discord channels, write channel topics, or decide where work belongs.

## Current confirmed routing

- `#general`: global commands, orchestration, cron/admin, morning/operator reports.
- `#coding`: coding/dev, repos, debugging, deployments, PRs, tests/logs, project implementation. The user skipped a separate `#projects` channel because coding can absorb project/app work.
- `#personal`: personal life, family, goals, and private coaching context.
- Business channel `<#1524172425393340516>`: business/monetization and also school-career/Jared coding tutoring when the user routes it there.

## Recommended separate channels when present

- `#youtube-automation`: faceless newsletter videos, Viral Radar clips, YouTube Shorts, upload queues/rate limits, Trapiistan vs Classical Echos routing, creator clipping backlog.
- `#trading`: Robinhood, portfolio scans, power-hour monitor, watchlists, P/L, market reports, trading cron output.
- `#business`: affiliate marketing, TikTok Shop, Shopify, Stripe, offers, monetization, Jared/kids coding tutoring as a business, parent updates, pricing/packages, income-oriented career growth.
- `#gaming`: OSRS/RuneLite, game servers, Minecraft/modpacks, Pokémon emulator, mobile game ideas.
- `#security-redteam`: red team/pentest/adversarial testing/security reviews.
- `#ops-alerts`: noisy cron/watchdog/backup/failure alerts if the server gets cluttered.

## Response format preference

When the user says “one by one,” do not dump the full channel plan. Provide exactly one channel at a time:

1. `## Channel N: #name`
2. one-sentence purpose
3. short “Use it for” bullet list
4. one copy-paste `text` block for the channel description/topic
5. ask them to say “next”

Keep it terse and mobile-friendly.

## Copy/paste prompt templates

### YouTube automation

```text
YouTube automation lane for faceless newsletter videos and Viral Radar creator clips.

Use this channel for:
- Faceless/newsletter videos → upload only to Trapiistan/Sosai.
- Viral Radar creator clips → upload only to Classical Echos.
- Shorts generation, clipping, transcripts, titles, descriptions, hashtags, upload queues, quota/rate-limit recovery, and content-calendar work.

Rules:
- No placeholder/filler videos.
- Viral Radar must clip real creator/influencer source videos.
- Faceless videos must credit the newsletter/source where appropriate.
- Hashtags belong in descriptions/tags, not titles.
- Keep reports concise with uploaded URLs, blockers, queue counts, and next action.
```

### Trading

```text
Trading and market-ops lane.

Use this channel for:
- Robinhood portfolio, watchlists, positions, orders, P/L, and trading automation.
- Market scans, earnings, options/equity research, power-hour monitoring, and trading journal notes.
- Agentic trading cron reports, risk checks, blockers, and trade-review summaries.

Rules:
- Never place or cancel real trades without explicit confirmation.
- Always separate read-only analysis from real-money actions.
- Include account/risk context, ticker, timeframe, thesis, and blocker when relevant.
- Keep reports concise: setup, signal, risk, action/next step.
```

### Business with Jared/school-career folded in

```text
Business, monetization, tutoring, and career-growth lane.

Use this channel for:
- Affiliate marketing, TikTok Shop, Shopify, Stripe/payment setup, sales funnels, offer creation, and creator/business monetization.
- Jared coding school / kids coding tutoring business: curriculum, student progress, parent communication, pricing, packages, leads, and tutoring operations.
- Career-growth work tied to income: GM Financial growth, cloud certs, resume, interview prep, salary/promotion planning, and SMART goals.
- Kinobody, Stirling Cooper, commerce apps, product ideas, launch plans, and business-growth experiments.

Rules:
- Focus on revenue paths, offer clarity, distribution, and next measurable action.
- For Jared/kids coding tutoring: track lessons, wins, parent-facing updates, student motivation, and next modules.
- For career work: use STAR/resume/salary framing when helpful.
- Separate coding implementation/debugging into #coding.
- Keep updates concise: opportunity, offer/goal, audience, action, blocker.
```

### Gaming

```text
Gaming and game-dev lane.

Use this channel for:
- OSRS/RuneLite plugins, game server setup, Minecraft/modpacks, Pokémon emulator tasks, mobile game ideas, and game-related MVPs.
- Plugin consolidation, gameplay overlays, game automation, game data tools, and gaming content/project ideas.

Rules:
- For RuneLite/OSRS: keep plugins standalone with no cross-plugin dependencies.
- Consolidate overlapping plugin ideas instead of creating duplicates.
- Panels should fit default width, start empty, and avoid fake/demo players.
- Move general repo/debugging work to #coding when it becomes implementation-heavy.
- Keep updates concise: game/project, goal, current status, blocker, next action.
```
