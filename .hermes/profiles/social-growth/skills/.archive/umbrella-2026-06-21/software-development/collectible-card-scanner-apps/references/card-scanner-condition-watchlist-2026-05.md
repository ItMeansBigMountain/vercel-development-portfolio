# Card Scanner Condition Lens + Local Watchlist Pattern (2026-05)

Session context: continued development on `/opt/data/HeRmEz/projects/card-intel-scanner`, a React/Vite Pokémon card scanner deployed on Vercel.

## Durable implementation pattern

When a scanner MVP already has search/OCR and multi-source pricing, the next useful slice is often **valuation assumptions + persistence**, not backend auth.

### Condition / grade lens

Add an explicit condition enum and visible multipliers:

```ts
type ConditionKey = 'raw-damaged' | 'raw-lp-mp' | 'raw-nm' | 'graded-8' | 'graded-9' | 'graded-10';

const CONDITION_OPTIONS = [
  { key: 'raw-damaged', label: 'Raw damaged', multiplier: 0.35, note: 'heavy wear / binder copy estimate' },
  { key: 'raw-lp-mp', label: 'Raw LP/MP', multiplier: 0.72, note: 'light-to-moderate play estimate' },
  { key: 'raw-nm', label: 'Raw near mint', multiplier: 1, note: 'baseline marketplace signal' },
  { key: 'graded-8', label: 'Graded 8', multiplier: 1.6, note: 'estimated slab premium' },
  { key: 'graded-9', label: 'Graded 9', multiplier: 2.6, note: 'estimated strong slab premium' },
  { key: 'graded-10', label: 'Graded 10', multiplier: 5, note: 'estimated gem-mint premium' }
];
```

Show the selected label in the estimate panel and, when not raw-NM, show the math (`Base raw NM × multiplier`). This avoids implying the app performed automated grading.

### Local watchlist

For no-login MVPs, persist saved scans locally before adding backend accounts:

```ts
const WATCHLIST_KEY = 'card-intel-watchlist-v1';

type SavedCard = {
  id: string;              // card id + condition to allow separate condition saves
  name: string;
  setName?: string;
  number?: string;
  imageUrl?: string;
  condition: ConditionKey;
  estimatedValue: number | null;
  sources: SourceRow[];    // source snapshot at save time
  savedAt: string;
};
```

Use a versioned localStorage key and cap entries (e.g. last 24) so the MVP remains low-friction and safe without auth/database scope creep.

## UX copy rules

- Call the value a `signal` or `estimate`, not an appraised value.
- State that condition multipliers are adjustable assumptions until visual grading is added.
- Keep eBay sold-comps as the reality-check link for condition, grading, and hype spikes.
- In AR/live mode, route the badge through the same selected condition lens.

## Verification checklist used

- `npm run build` passes.
- Local Vite preview loads.
- Manual browser smoke test: search Pokémon TCG API, click a condition, save to watchlist.
- Confirm `localStorage.getItem('card-intel-watchlist-v1')` contains saved cards.
- Deploy to Vercel and verify alias + deployment URL return HTTP 200.

## Next natural slice

After condition/watchlist ships, prioritize recorded-video frame sampling and stabilized AR confidence/decay states so the app moves closer to live/recorded video price overlays rather than remaining a search tool.
