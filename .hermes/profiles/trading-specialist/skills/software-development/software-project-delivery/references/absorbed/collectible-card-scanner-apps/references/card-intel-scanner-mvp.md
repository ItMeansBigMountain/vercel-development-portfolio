# Card Intel Scanner MVP Notes

## Session Context

The user reported that manual/name search worked well, but image scanning was not reliable enough. They clarified the desired product direction: apply card price intelligence to **live video or recorded video** and automatically attach price overlays that follow the card, similar to Snapchat face filters. The core selling point should be quick comparison of prices across multiple platforms.

## What Worked

- Manual name search provided solid data and should remain a fallback.
- A static React/Vite frontend deployed to Vercel is sufficient for an MVP.
- Condition/grade lenses add immediate valuation value even before full computer vision works.
- A localStorage watchlist gives collectors a useful save/compare loop without accounts or backend setup.

## Implemented Pattern

For `card-intel-scanner`:

- Added condition profile/lens choices:
  - Raw HP/DMG
  - Raw LP/MP
  - Raw NM
  - Graded 8
  - Graded 9
  - Graded 10
- Used multipliers/estimated boosts where exact condition pricing is unavailable.
- Added a saved watchlist backed by `localStorage` key `card-intel-watchlist-v1`.
- Kept manual search, OCR/image path, and camera scan-zone experiences available.
- Deployed to Vercel and verified the production alias.

## Product Direction to Preserve

The next version should treat still-image OCR as an input method, not the end state. The compelling version is:

1. User points live camera at a card or uploads a recorded video.
2. App samples frames and extracts likely card identity.
3. App stabilizes identity over multiple frames.
4. App renders a price badge near/on the card.
5. Badge follows the card or scan-zone anchor and opens multi-platform comps.
6. User can switch condition/grade lens and save to watchlist.

## Recommended Recorded-Video Approach

- Accept a video file upload.
- Extract frames every 500-1000ms initially.
- Run OCR only on sampled/cropped frames.
- Deduplicate candidate card names across frames.
- Rank candidates by frequency + OCR confidence + API match quality.
- Show a timeline/list of detected cards with price cards.
- Later, add actual bounding-box tracking; do not block the MVP on perfect AR tracking.

## Pricing/Comparison UX Notes

- Always distinguish market/reference prices from active listing prices.
- Show marketplace/source names clearly.
- Label estimated grade/condition adjustments as estimates.
- Let users compare raw vs graded quickly because this is a major collector decision point.

## Pitfalls Observed

- Image scanning can fail even when lookup data is strong; do not remove manual search.
- The scanner's value proposition should not be described as just recognizing a card. The business value is reducing friction in price comparison across platforms while scanning/browsing cards.
