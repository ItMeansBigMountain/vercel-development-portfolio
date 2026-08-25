# HeRmEz static MVP reframe + Card Intel Scanner pattern

Session pattern from converting a plan-only/legacy project folder into a live Vercel review app.

## When to use

Use this when the user changes the product direction of an existing project folder or asks to make any project reviewable quickly. Prefer a static Vite MVP if the new direction can be validated without accounts, durable storage, or paid APIs.

## Workflow

1. Reframe the project in-place first, then rename the folder if the old name is misleading.
   - Example: `pokemon-go-qr-trade-site` became `card-intel-scanner` after the user said it should scan Pokémon cards and aggregate prices instead of being Pokémon Go related.
2. Replace stale scope/docs immediately so future agents do not resurrect the old concept:
   - `README.md`
   - `SCOPE.md`
   - `PROJECT.md`
   - workspace `README.md`
   - workspace `VERCEL_TRIAGE.md`
   - workspace `WORK_QUEUE.md`
3. Build the smallest reviewable static MVP before backend work.
4. Run local verification:
   - `npm install`
   - `npm run build`
   - optional `npm run preview` + anonymous local HTTP check
   - bundle probe for expected source strings when browser automation is unavailable
5. Deploy with token fallback:
   - `TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"`
   - `npx --yes vercel@latest deploy --prod --yes --token "$TOKEN"`
6. Newly-created Vercel projects may default to deployment protection. Patch public review access, then verify anonymously:
   - `PATCH https://api.vercel.com/v9/projects/<project>` with `{ "ssoProtection": null }`
7. Record both deployment URL and alias in the workspace trackers.

## Card-price scanner MVP specifics

For an unofficial Pokémon card price scanner, a no-backend static MVP can be enough for first review:

- Image upload/camera input.
- Browser OCR with `tesseract.js` as an assistive query extractor.
- Manual correction/search field because OCR on trading cards is noisy.
- Public Pokémon TCG API search for card metadata.
- Aggregate available price fields from:
  - TCGplayer market/low/mid where present.
  - Cardmarket trend/average/low where present.
  - eBay sold-comps search link for real-world condition/graded validation.
- Calculate only a simple blended median from available numeric signals; do not overclaim automated valuation.

## Verification probes

Remote anonymous check shape:

```bash
python3 - <<'PY'
import json, re, urllib.request, urllib.parse
urls = [
  'https://<deployment>.vercel.app',
  'https://<alias>.vercel.app',
]
for url in urls:
    r=urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=30)
    html=r.read().decode(errors='ignore')
    print(url, r.status, r.getheader('content-type'), len(html), '<expected app title>' in html)
    for src in re.findall(r'<script[^>]+src="([^"]+)"', html)[:1]:
        js_url=url+src if src.startswith('/') else src
        js=urllib.request.urlopen(urllib.request.Request(js_url, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read().decode(errors='ignore')
        print('bundle', len(js), '<expected feature string>' in js)

q='name:"*Charizard*"'
api='https://api.pokemontcg.io/v2/cards?q='+urllib.parse.quote(q)+'&pageSize=1'
r=urllib.request.urlopen(urllib.request.Request(api, headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'}), timeout=30)
data=json.loads(r.read().decode())
card=data['data'][0]
print('pokemon-tcg-api', r.status, card['name'], bool(card.get('tcgplayer')), bool(card.get('cardmarket')))
PY
```

## Pitfalls

- Do not keep old product scope files after a direction change; they cause future queue work to drift backward.
- Do not treat OCR output as identification. Keep manual correction and likely-match selection.
- Do not imply eBay prices are directly available unless using an API; a sold-comps link is a reviewable MVP compromise.
- Do not report Vercel success until both the production URL and alias are anonymously accessible with HTTP 200.
