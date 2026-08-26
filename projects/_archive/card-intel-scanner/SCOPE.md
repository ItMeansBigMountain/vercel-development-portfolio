# Card Intel Scanner - MVP Scope

## Goal

Create a fast mobile-first web app that scans or searches Pokémon trading cards and aggregates price signals so the user can quickly decide whether a card is worth buying, selling, grading, or researching deeper.

## Core Features

1. **Image Scan / Upload** – User can take or upload a card photo from mobile.
2. **OCR Assist** – Browser-side OCR extracts visible card text as a starting search query.
3. **Manual Correction** – User can edit the OCR query because card scans are noisy.
4. **Card Matching** – Search the public Pokémon TCG API and list likely matches with set, number, rarity, and image.
5. **Price Aggregation** – Show available TCGplayer and Cardmarket price signals.
6. **Sold Comps Link** – Provide an eBay sold-comps query for reality-checking condition, grading, and hype.
7. **Blended Signal** – Calculate a simple median from available numeric price points.
8. **Condition / Grade Lens** – Let users switch between raw damaged, LP/MP, NM, and graded 8/9/10 assumptions.
9. **Local Watchlist** – Save scanned cards, selected condition, source snapshot, and estimated value in browser storage.

## Constraints

- No backend for MVP.
- No paid API keys required.
- No accounts or inventory database yet.
- OCR is assistive, not authoritative.
- Condition and grading are not automated; user must validate against sold comps.
- App is unofficial and not affiliated with Pokémon, Nintendo, TCGplayer, Cardmarket, or eBay.

## Next Steps

- Mobile-test the live camera OCR + condition/watchlist flow on real cards.
- Add recorded-video upload/frame sampling so users can price cards from existing clips.
- Stabilize the AR badge across multiple frames and show confidence/decay states.
- Add backend only if we need durable portfolio tracking, alerts, or paid marketplace APIs.

## Validation Method

- `npm run build` passes.
- Preview server returns HTTP 200.
- Vercel production alias returns HTTP 200.
- Condition selector visibly changes the estimate label/multiplier.
- Watchlist persists under `card-intel-watchlist-v1`.
- Built bundle contains scanner/pricing source logic.
- Pokémon TCG API returns card metadata and pricing with browser-style request headers.
