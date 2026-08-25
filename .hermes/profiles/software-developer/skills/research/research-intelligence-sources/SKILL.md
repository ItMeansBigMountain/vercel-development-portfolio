---
name: research-intelligence-sources
description: "Use when gathering external research intelligence from papers, blogs/RSS, prediction markets, or an LLM-focused knowledge base. Umbrella for source selection, retrieval, and synthesis workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, intelligence, arxiv, rss, blogs, prediction-markets, knowledge-base]
    related_skills: [webhook-subscriptions, operator-morning-reports]
---

# Research Intelligence Sources

## Overview

Use this umbrella when the user needs current or domain-specific intelligence from external research sources. Pick the source by information type, retrieve data with the appropriate tool/script/API, and synthesize findings with citations or source handles.

## Source Selection

| Need | Source mode | Notes |
|---|---|---|
| Academic ML/science papers | arXiv | Search by keyword, author, category, or paper ID; inspect abstracts before summarizing. |
| Ongoing blog/news monitoring | Blog/RSS watcher | Prefer feed-backed monitoring for recurring source surveillance; summarize deltas rather than full archives. |
| Market-implied forecasts | Polymarket | Query markets, prices, orderbooks, and history; distinguish market probability from factual truth. |
| LLM knowledge-base exploration | LLM wiki | Build/query an interlinked markdown knowledge base for model concepts, papers, and terminology. |
| Local service/application intake | Web search + browser | Search by the user's actual location, prefer official provider pages with application/contact handles, and summarize eligibility before asking for personal details. |

## Workflow

1. Clarify the research question and decide whether it needs current web facts, papers, market odds, a local knowledge base, or a local provider/application flow.
2. Use the narrowest source that answers the question; avoid mixing sources unless cross-validation matters.
3. For location-sensitive services, use the user's current/corrected location immediately; if the user corrects the location mid-turn, pivot rather than continuing with the earlier geography.
4. Capture durable handles: arXiv IDs, feed URLs, market slugs/IDs, page paths, provider application URLs, contact emails/phones, addresses, or source URLs.
5. Summarize evidence separately from interpretation, including eligibility requirements and any “no walk-ins/apply first” constraints before requesting personal information.
6. If submitting an application or lead form, gather only fields required by the page and get explicit user confirmation before sending any personal details.
7. If the task is recurring, convert it to a monitor/subscription rather than a one-off search.

## Re-homed Playbooks

Former source-specific skills are preserved as support packages:

- `references/arxiv/original-skill.md` plus `references/arxiv/scripts/` for arXiv search helpers.
- `references/blogwatcher/original-skill.md` for RSS/blog monitoring commands and delta-report conventions.
- `references/polymarket/original-skill.md` plus `references/polymarket/references/` and scripts for market data queries.
- `references/llm-wiki/original-skill.md` for constructing and querying an LLM-focused markdown knowledge base.

## Pitfalls

- Do not treat a prediction market price as a verified fact; label it as market-implied probability.
- Do not summarize papers from titles alone; inspect abstracts and, when needed, the paper text.
- Do not make recurring monitoring depend on ad-hoc web searches if an RSS/API source exists.
- Do not keep working from an inferred/old location after the user provides a corrected location; restart local-provider searches around the corrected geography.
- Do not submit application, medical, financial, or other personal-intake forms until the user has provided the exact required fields and explicitly confirmed submission.
- Keep source-specific scripts in their re-homed package directories and update paths if promoting them into first-class umbrella scripts.

## Verification Checklist

- [ ] Source choice matches the research question.
- [ ] Each claim has a source handle or citation.
- [ ] Current facts were checked with live tools.
- [ ] Market/probability claims are labeled as such.
- [ ] Recurring monitoring tasks include a delta-oriented reporting plan.
