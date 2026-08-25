---
name: collectible-card-scanner-apps
description: "Use when building or improving collectible card scanner, price intelligence, watchlist, OCR, live-video, recorded-video, or AR overlay apps. Prioritizes OCR-first MVPs, multi-platform price comparison, and product UX that turns card identification into actionable valuation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [collectibles, cards, scanner, ocr, video, ar, pricing, react, vercel]
    related_skills: [test-driven-development, systematic-debugging, requesting-code-review]
---

# Collectible Card Scanner Apps

## Overview

Use this skill for apps that identify collectible trading cards from text, still images, live camera feeds, or recorded video, then enrich the result with prices, condition assumptions, collection/watchlist state, and marketplace comparison. The product value is not merely card lookup: it is fast, low-friction price intelligence that follows the user's collecting workflow.

For this user, the north star is a **live or recorded video AR overlay**: recognize cards in-camera and attach a price badge/filter that tracks the card like Snapchat puppy-dog ears. The selling point should be easy comparison across multiple price sources/platforms, not a single static price.

## When to Use

- Building or updating card scanner apps: Pokémon, sports cards, TCGs, slabs, raw cards, lots, binders, or marketplace browsing helpers.
- Adding OCR, image upload, camera scanning, live video, recorded-video sampling, or AR-style overlays.
- Designing pricing UX: TCGplayer, eBay sold comps, Cardmarket, PriceCharting, PSA/CGC/BGS grades, raw condition estimates, confidence bands.
- Adding watchlists, saved scans, collection valuation, comps review, condition lenses, or price alerts.
- Turning a search-only MVP into a scanner/video product.

Do **not** use this skill for generic ecommerce search unless collectible card identification, condition, grading, or marketplace price comparison is central.

## Product Principles

1. **OCR-first, but video-native as the destination.** Start with reliable name/set/number extraction from text or frames. Then stabilize results across frames so the product feels like live AR, not a one-off image upload.
2. **Multi-platform comparison is the moat.** A single API price is useful but not differentiated. Always expose source, condition, recency, and price spread across platforms.
3. **Condition changes the answer.** Raw damaged, LP/MP, NM, graded 8/9/10, and slab company should be first-class inputs or lenses. Show estimates as assumptions, not facts, when the app cannot inspect condition directly.
4. **Fast confidence beats perfect recognition.** In video, prefer a rolling confidence score and stable badge after repeated agreement across frames rather than blocking for one perfect OCR pass.
5. **Mobile-first collector flow.** Optimize for one-handed scanning at a shop/show: large scan zone, instant feedback, saved watchlist, compare prices, and quick rescan.

## MVP Architecture Pattern

For a static React/Vite app deployed to Vercel:

- **Frontend:** React + TypeScript + CSS modules or app stylesheet.
- **OCR:** Tesseract.js or browser-side OCR for initial MVP. Keep a manual name search fallback.
- **Lookup:** Pokémon TCG API or domain-specific card APIs where available.
- **Pricing:** Normalize data into a shared structure: `source`, `label`, `marketPrice`, `low`, `mid`, `high`, `url`, `updatedAt`, `condition`, `confidence`.
- **Persistence:** Use `localStorage` for MVP watchlists/collections before a database is configured.
- **Deployment:** Vercel static frontend first; add serverless/API routes only when data aggregation or credentials require it.

## Recommended Data Model

```ts
type ConditionKey =
  | 'raw-damaged'
  | 'raw-lp-mp'
  | 'raw-nm'
  | 'graded-8'
  | 'graded-9'
  | 'graded-10';

type PriceSource = {
  source: 'tcgplayer' | 'cardmarket' | 'ebay' | 'pricecharting' | 'psa' | 'manual';
  label: string;
  value: number | null;
  currency: string;
  url?: string;
  condition?: ConditionKey;
  confidence?: number;
  updatedAt?: string;
};

type SavedCard = {
  id: string;
  name: string;
  setName?: string;
  number?: string;
  imageUrl?: string;
  condition: ConditionKey;
  estimatedValue: number | null;
  sources: PriceSource[];
  savedAt: string;
};
```

## Still Image and OCR Workflow

1. Accept camera capture and file upload.
2. Preprocess before OCR where possible: crop scan zone, increase contrast, grayscale, sharpen, and downscale huge images.
3. Extract candidate text.
4. Parse likely card name, set code, collector number, and year.
5. Search card API using the strongest candidate first; provide manual correction/search if confidence is weak.
6. Show multiple matches with image thumbnails rather than auto-selecting when ambiguous.
7. Compute price rows per source and condition lens.
8. Allow save-to-watchlist from any result.

## Live/Recorded Video Workflow

For live or recorded video, do not OCR every frame blindly. Use a sample-and-stabilize loop:

1. Sample frames every N milliseconds or on meaningful motion pauses.
2. Crop to scan zone or detected card quadrilateral.
3. OCR frame candidates and keep a rolling window of recent predictions.
4. Stabilize only when the same card candidate wins across several frames or confidence crosses a threshold.
5. Render an AR-style price badge near the detected card region.
6. Keep the badge sticky for a short decay window so it does not flicker during motion.
7. Let the user tap a badge to open detailed multi-platform comps and save to watchlist.

### AR Overlay Behavior

- Badge should follow the card bounding box or scan-zone anchor.
- Show concise label: card name + best estimate + condition lens.
- Use color/confidence states: scanning, candidate, confirmed, stale.
- Include a manual correction affordance because OCR will fail on glare, sleeves, binders, and motion blur.

## Marketplace Comparison Pattern

Normalize every marketplace into comparable rows. Prefer this display order:

1. Best available market/reference price for the selected condition.
2. Recent sold comps where available.
3. Active listings clearly labeled as asking prices, not value.
4. Raw vs graded comparison when a grading lens is selected.
5. Source links so the user can verify.

When exact comps are unavailable, label estimates clearly, for example: `Estimated from NM raw x 0.72 LP/MP multiplier` or `Estimated graded premium from raw market price`.

## Watchlist Pattern

Use local watchlist for MVPs unless the user asks for accounts/cloud sync:

- Store under a versioned key, e.g. `card-intel-watchlist-v1`.
- Include condition, source snapshot, and timestamp so future price changes can be compared.
- Use an id that combines the card id and selected condition when the same card may be saved under raw/graded assumptions.
- Cap the list for no-backend MVPs (for example, newest 24) so localStorage stays lightweight.
- Provide remove action and count.
- Avoid requiring auth for the first useful version.

## Verification Checklist

- [ ] Manual name search works when OCR fails.
- [ ] Image upload/camera still path handles blank OCR without crashing.
- [ ] Condition/grade lens visibly changes valuation and is labeled as an assumption when estimated.
- [ ] When condition is not raw-NM, the UI shows the base value and multiplier rather than implying automated grading.
- [ ] At least two marketplace/source rows are shown where data exists, or unavailable sources are gracefully labeled.
- [ ] Watchlist persists across refresh using the expected localStorage key and stores condition + source snapshot.
- [ ] Production build succeeds.
- [ ] Local preview smoke test covers search, condition selection, and watchlist save/remove.
- [ ] Vercel deployment returns HTTP 200 for both deployment URL and friendly alias when present.
- [ ] Mobile viewport is usable: scan zone, cards, and buttons are not cramped.
- [ ] For video features, overlay does not flicker wildly and stabilizes across multiple frames.

## Common Pitfalls

1. **Shipping only name search and calling it scanning.** Name search is a fallback. The scanner product should move toward image/video capture and overlays.
2. **Treating one API price as the value.** The user specifically values easy comparison across multiple platforms.
3. **Ignoring condition and grading.** Raw/graded assumptions must be visible, adjustable, and saved with the card.
4. **Overpromising computer vision.** If condition inspection, exact grade recognition, or real-time tracking is heuristic, say so in the UI and in the summary.
5. **OCR on every video frame.** This wastes CPU and produces flicker. Sample frames, stabilize candidates, and cache results.
6. **Making auth/database mandatory too early.** For MVP watchlists and demos, localStorage is usually enough.

## References

- `references/card-intel-scanner-mvp.md` — Session-specific implementation notes from the Card Intel Scanner Vercel MVP: condition lenses, local watchlist, and next recorded-video AR direction.
- `references/name-search-to-video-ar-overlay.md` — Product direction note from user feedback: name search/data layer worked, image scanning failed, next value is live/recorded video AR price overlays with multi-platform comparison.
- `references/card-scanner-condition-watchlist-2026-05.md` — Concrete React/Vite pattern for adding condition multipliers, localStorage watchlists, UX copy, and Vercel verification after OCR/search already works.
