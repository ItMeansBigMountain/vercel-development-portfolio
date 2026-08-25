---
name: operator-morning-reports
description: "Proactive daily operator-style morning reports: local pulse, market outlook, project/work source, numerology, challenge, priority prompt."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [morning-report, cron, productivity, market-outlook, personal-ops]
    related_skills: [google-workspace, blogwatcher, polymarket]
---

# Operator Morning Reports

## When to use

Use this skill when configuring, editing, troubleshooting, or producing the user's proactive daily morning check-in/report.

This is not a generic greeting. The user explicitly wants a **report** that helps them operate their day.

## User-specific current requirements

- Delivery time: around **8:30–9:00 AM Central time**. A good cron default is `30 14 * * *` UTC for 8:30 AM CST; adjust for daylight saving only if the scheduler/user context requires it.
- Current location context: **Chicago, Illinois** until the user says they moved.
- Birth date for numerology: **06/30/1995**.
- Capability-oriented framing: the user does not want project-first planning. Projects are disposable execution vehicles; reports should emphasize durable systems, leverage, reusable assets, trend intelligence, and execution loops.
- Trend Radar must be included every morning but must be very short: bullet the word/phrase, then one small sentence on why it is trending and what it means for the user. Avoid scoring fields unless the user asks for deeper analysis.
- Include **Google Search pulse** every morning: latest top searched words/phrases from Google Trends / Daily Trends / credible trend recaps, with what changed and why it matters.
- Include **Google Workspace data** in the morning report: upcoming calendar events, planned activities, and relevant Gmail messages. Prefer the `google-workspace` skill's named-profile OAuth pattern and the user's profile-scoped tokens under `/opt/data/google_profiles/<profile>/google_token.json`; fall back to single-token setup only when that is the active environment. For this user's configured report, use `/opt/data/scripts/google_morning_context.py` as the read-only pre-run collector; see `references/google-workspace-multi-profile-morning-context.md`.
- Apply the user's **consumer data liberation / personal data mirror** lens when interpreting workspace, email, Grammarly, writing, calendar, content, and app-usage signals. The user wants personal metrics to reveal subconscious patterns, communication tone, interests, energy drains, identity reinforcement, and the “frequency”/impact they are emanating. Treat this as a product/research theme: convert raw data into traceable self-knowledge, not just a list of notifications; see `references/personal-data-mirror-lens.md`.
- Include an **Email priority + cleanup** mini-section every morning. Prioritize billing/charges/receipts, Chase, Apple receipts/Card, cloud services, AI APIs, Robinhood, Ticketmaster ticket/venue info, myQ/Chamberlain garage alerts, GitGuardian/security, official/vehicle renewal notices, and similar life/admin signals. **Landing is priority only for Standby/rent-impacting logistics**: bump/rebook notices, active stay changes, payments/rent, parking, mail/packages, pets, or support; do not surface generic Landing marketing as priority. Do not read/summarize Credit Karma emails unless they indicate a credit-score drop or serious credit-risk/identity/duplicate-charge signal. TLDR is useful for latest news but should be sourced only from `fareed320@gmail.com`; TLDR on other accounts is duplicate cleanup. Kino Body and Daily Stoic are interesting/source-worthy and should be summarized, then treated as post-review cleanup candidates when appropriate. Grammarly Insights should be treated as interesting self-metrics/profile data. For TLDR, Kino Body, Daily Stoic, and Grammarly Insights: summarize through the lens of the user's known profile/interests, draw appealing personal insights, then list them as newsletter cleanup candidates with sender/category/title and ask whether to clean them up. Junk categories include FoundersCard, Yieldi, Crunch, Higgsfield, Fundrise, Kling AI, Instagram notifications, Lumen marketing, Chess.com nags, YEEZY, City Experiences, LELO, GNC, and generic consumer sales/promotional emails. When doing broader subscription cleanup, first audit all subscriptions/newsletters across profiles read-only, classify keep/source/review/junk, then ask for scoped approval before unsubscribe/report-spam/delete actions; see `references/email-triage-cleanup-policy.md`. Junk action for an approved scope means unsubscribe when practical, report as spam when appropriate, and delete/trash. **Daily automation**: Once senders/categories are approved for cleanup, automatically process junk/unsubscribe daily without re-prompting.
- Known junk/spam cleanup is approved for recurring operation without per-item review. For newsletter/source emails, summarize/use them first and delete only after the requested YouTube video upload is verified. For ambiguous or important Google Workspace actions (Gmail non-junk, Calendar, Drive), still ask before destructive changes.
- Include **game-changing AI + coding news** every morning, but keep it minimalistic and Discord-readable: model releases, developer tools, agent frameworks, coding platforms, major product launches, policy/platform shifts, and practical opportunities.
- Include **social conversation pulse** every morning: top topics being discussed across major social platforms/communities when verifiable, with source/context notes and a signal/noise read. Present as simplified bullets, not Markdown tables or paragraphs.
- Do not use a portfolio-tracking section inside the morning report itself unless the user re-adds it. The user now wants a **separate post-morning Agentic portfolio market scan** after the morning report, covering Robinhood Agentic account updates, market scan, technical/fundamental analysis, and tool/system upgrades. Keep the morning report concise; let the separate scan do trading depth.
- Instead of portfolio, report whether the day looks **bullish or bearish** in one compact line and the primary reason why. Do not present separate bull-case/bear-case arguments unless the user asks.
- Include a short **“You’ll probably find this interesting”** section for weird/high-leverage items that match the user's tastes: AI agents, coding leverage, markets, internet culture, automation, community/client websites, collectibles/card scanning, and asymmetric opportunities.
- Include a daily challenge that improves the user socially, professionally, mentally, or physically.
- When Google Workspace OAuth is connected, use the `google-workspace` skill's named-profile pattern for Gmail/Calendar inputs. Keep morning-review mail/calendar output grouped by account/profile, summarize only high-signal items, and do not take write actions (send email, create/delete events, share/edit/delete files) without explicit confirmation.
- Include a **Portfolio heartbeat** section for all Robinhood accounts: account value, cash/buying power, positions, and 24h gain/loss. Also surface relevant news for any stock the user owns. Keep this section brief; detailed analysis lives in the separate post-morning Agentic portfolio market scan.
- Do **not** include the old 14-Day Self-Improvement Challenge check-in, habit boxes, one-second-rule tracker, or `done: meditation...` reply prompt. The user explicitly removed that recurring section on 2026-06-11.

## Required report shape

Use this structure unless the user changes it:

1. **Quick opener** — date/day and grounded operator tone.
2. **Location pulse** — Chicago weather/conditions and practical implications for the day.
3. **Market pulse** — not portfolio. Say only whether today looks **bullish** or **bearish**, plus one concise reason why and one thing to watch. No pro/con argument format.
4. **Portfolio heartbeat** — all Robinhood accounts: account value, cash/buying power, positions, 24h gain/loss, and relevant news for owned stocks. Keep brief.
5. **Search + social pulse** — latest top searched Google words/phrases and top social topics. Each bullet should be the trending word/phrase plus one small sentence explaining why it is moving and what it means for the user. No tables, no long source notes.
6. **Game-changing AI + coding news** — compact bullets only. Each bullet is a small headline plus one short sentence explaining the news and practical implication.
7. **Capability + trend radar** — 3–5 emerging internet/culture/tech/consumer trends worth watching. Each bullet should be the word/phrase plus one short sentence explaining why it matters and the capability/reusable asset angle. No velocity/spread/money/saturation scoring unless requested.
8. **Work source / operating pulse** — pull from available workspace/project context, recent work queue, reminders, and connected tools. Organize by durable capabilities/systems first; mention projects only as temporary vehicles. Identify the highest-leverage next action.
9. **You'll probably find this interesting** — 1–3 odd/high-leverage items aligned with AI agents, coding leverage, markets, internet culture, automation, community/client websites, collectibles/card scanning, or asymmetric opportunities.
10. **Numerology reading** for 06/30/1995 — frame as reflective/for-fun, not deterministic. Include life path and a date-specific reflection when current date is available.
11. **Daily challenge** — one concrete, measurable challenge doable today; align it with one of the five challenge habits when possible.
12. **One Big Priority prompt** — ask for today's priority plus blockers/context.
13. **Hard Truth / Leverage Move** — one direct but constructive sentence.

## Tone

- Use capability language: “capability to strengthen,” “reusable asset,” “experiment to run,” and “kill/scale signal.”
- Operator-aesthetic: direct, warm, useful, and concise.
- Keep reports easy to skim for a user who has a hard time reading long reports: bold section labels, occasional italics for emphasis, short bullets, no dense paragraphs, no tables.
- News and trend sections should be **minimalistic Discord-readable bullets**: small headline/phrase + one short sentence explaining what happened and what it means to the user.
- Avoid pipe-heavy table syntax in Discord because it may render poorly. Prefer bold labels and `|` separators inside single bullets only if needed.
- Make it feel like a briefing, not a chatbot check-in.
- Avoid fluffy motivation and avoid long essays.
- If current tools/sources are unavailable, say what could not be verified instead of inventing current facts.

## Current-data discipline

For current weather, market/news, expert commentary, or date/time, use tools when available. Do not hallucinate live market conditions or weather.

When running as a cron job:

- The final response is auto-delivered; do not use `send_message`.
- Do not schedule additional cron jobs from inside the cron run.
- Make the prompt self-contained because cron runs do not inherit the current chat context.
- Enable web/current-data tools where possible for market and local pulse.

## Numerology calculation notes

Birth date: 06/30/1995.

Life path calculation:

```text
0+6 + 3+0 + 1+9+9+5 = 33 -> master number 33/6
```

Suggested framing: master 33/6 themes are service, responsibility, creative care, teaching, community, and disciplined compassion. Treat it as reflective language, not fate.

For personal-day style reflection, combine month + day + current year digits and reduce; label it as a light reflection.

## References
- portfolio-heartbeat.md — script that generates the portfolio heartbeat data for the morning report.

- `references/2026-05-user-correction.md` — session-specific correction that established the current report shape and schedule.
- `references/trend-radar-capability-framing.md` — session-specific update adding Trend Radar and capability-oriented planning language.
- `references/minimal-table-news-format.md` — earlier user correction: keep news/trend sections minimalistic and not wordy.
- `references/discord-bullet-format.md` — current correction: Discord renders Markdown tables poorly; use simplified one-line bullets instead of tables/code blocks.
- `references/source-checklist-search-social-ai-market.md` — source checklist for Google search terms/phrases, social topics, AI/coding news, and bullish/bearish market pulse.
- `references/2026-06-chicago-concise-standup.md` — current user correction: Chicago local context, extremely skimmable stand-up shape, single bullish/bearish market read, and one-sentence trend/news bullets.
- `references/google-workspace-multi-profile-morning-context.md` — current multi-profile Google context collector pattern, account roles, read-only safety rules, sanitization, and verification steps for the morning report cron.
- `references/email-triage-cleanup-policy.md` — session-specific email triage and cleanup policy: Landing importance, TLDR/source handling, known junk senders, subscription audit flow, and destructive-action permission rules.

## Pitfalls

- Do not send only “What’s your one big priority?” when the user asked for a report. That was previously corrected.
- Do not include portfolio holdings/performance by default; the user replaced that with expert bullish/bearish outlook.
- Do not treat any prior city as permanent; current known local context is Chicago until the user updates it.
- Do not claim memory was updated based on one-off daily tasks. Only save durable preferences, stable patterns, or recurring goals.
- Do not over-explain the setup in the report itself; deliver the report.
