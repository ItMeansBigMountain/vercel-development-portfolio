# Card Intel Scanner

Unofficial Pokémon card scanner and price aggregation MVP.

## Status

Vercel-ready static React/Vite prototype implemented for review. This replaces the original Pokémon Go friend-code concept.

## What it does

- Upload/camera-scan a Pokémon card image.
- Uses browser OCR via `tesseract.js` to extract likely card text.
- Lets the user correct/search the card name manually.
- Searches the public Pokémon TCG API.
- Aggregates available price signals from:
  - TCGplayer market/low prices
  - Cardmarket trend/average/low prices
  - eBay sold-comps search link
- Shows a blended median signal from available numeric prices.

## MVP constraints

- No accounts.
- No inventory database yet.
- No paid API keys required.
- OCR is a first-pass assistant, not guaranteed identification.
- Condition/grading is not automated yet; users must validate against eBay sold comps.

## Commands

```bash
npm install
npm run build
npm run dev
```

## Environment

No runtime secrets are required for the MVP. Do not commit real secrets. Keep committed examples in `.env.example`.
