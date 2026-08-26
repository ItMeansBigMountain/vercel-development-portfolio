import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { createWorker } from 'tesseract.js';
import './styles.css';

type CardMarket = {
  averageSellPrice?: number;
  lowPrice?: number;
  trendPrice?: number;
  suggestedPrice?: number;
  reverseHoloSell?: number;
  reverseHoloTrend?: number;
};

type TcgPlayerPrice = {
  low?: number;
  mid?: number;
  high?: number;
  market?: number;
  directLow?: number;
};

type PokemonCard = {
  id: string;
  name: string;
  number?: string;
  rarity?: string;
  set?: { name: string; series?: string; printedTotal?: number; releaseDate?: string };
  images?: { small?: string; large?: string };
  tcgplayer?: { url?: string; prices?: Record<string, TcgPlayerPrice> };
  cardmarket?: { url?: string; prices?: CardMarket };
};

type SourceRow = {
  source: string;
  metric: string;
  value: number | null;
  url?: string;
};

type ConditionKey = 'raw-damaged' | 'raw-lp-mp' | 'raw-nm' | 'graded-8' | 'graded-9' | 'graded-10';

type ConditionOption = {
  key: ConditionKey;
  label: string;
  multiplier: number;
  note: string;
};

type SavedCard = {
  id: string;
  name: string;
  setName?: string;
  number?: string;
  imageUrl?: string;
  condition: ConditionKey;
  estimatedValue: number | null;
  sources: SourceRow[];
  savedAt: string;
};

const API = 'https://api.pokemontcg.io/v2/cards';
const LIVE_SCAN_INTERVAL_MS = 3200;
const WATCHLIST_KEY = 'card-intel-watchlist-v1';

const FALLBACK_CARDS: PokemonCard[] = [
  {
    id: 'demo-charizard-4-102',
    name: 'Charizard',
    number: '4/102',
    rarity: 'Rare Holo',
    set: { name: 'Base Set', series: 'Base', printedTotal: 102, releaseDate: '1999/01/09' },
    images: { small: 'https://images.pokemontcg.io/base1/4.png', large: 'https://images.pokemontcg.io/base1/4_hires.png' },
    tcgplayer: { url: 'https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&q=Charizard%204%2F102', prices: { holofoil: { low: 180, mid: 260, high: 499, market: 315 } } },
    cardmarket: { url: 'https://www.cardmarket.com/en/Pokemon/Products/Search?searchString=Charizard+4%2F102', prices: { trendPrice: 280, averageSellPrice: 265, lowPrice: 170 } }
  },
  {
    id: 'demo-charizard-ex-obsidian',
    name: 'Charizard ex',
    number: '223/197',
    rarity: 'Special Illustration Rare',
    set: { name: 'Obsidian Flames', series: 'Scarlet & Violet', releaseDate: '2023/08/11' },
    images: { small: 'https://images.pokemontcg.io/sv3/223.png', large: 'https://images.pokemontcg.io/sv3/223_hires.png' },
    tcgplayer: { url: 'https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&q=Charizard%20ex%20223%2F197', prices: { holofoil: { low: 35, mid: 50, high: 95, market: 58 } } },
    cardmarket: { url: 'https://www.cardmarket.com/en/Pokemon/Products/Search?searchString=Charizard+ex+223%2F197', prices: { trendPrice: 55, averageSellPrice: 51, lowPrice: 34 } }
  }
];

const CONDITION_OPTIONS: ConditionOption[] = [
  { key: 'raw-damaged', label: 'Raw damaged', multiplier: 0.35, note: 'heavy wear / binder copy estimate' },
  { key: 'raw-lp-mp', label: 'Raw LP/MP', multiplier: 0.72, note: 'light-to-moderate play estimate' },
  { key: 'raw-nm', label: 'Raw near mint', multiplier: 1, note: 'baseline marketplace signal' },
  { key: 'graded-8', label: 'Graded 8', multiplier: 1.6, note: 'estimated slab premium' },
  { key: 'graded-9', label: 'Graded 9', multiplier: 2.6, note: 'estimated strong slab premium' },
  { key: 'graded-10', label: 'Graded 10', multiplier: 5, note: 'estimated gem-mint premium' }
];

function money(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}

function cleanOcr(text: string) {
  return text
    .replace(/[^a-zA-Z0-9\s'’.-]/g, ' ')
    .split(/\s+/)
    .filter((word) => word.length > 2)
    .slice(0, 8)
    .join(' ')
    .trim();
}

function priceRows(card: PokemonCard): SourceRow[] {
  const rows: SourceRow[] = [];
  const tcg = card.tcgplayer?.prices || {};
  for (const [variant, prices] of Object.entries(tcg)) {
    rows.push({ source: 'TCGplayer', metric: `${variant} market`, value: prices.market ?? prices.mid ?? null, url: card.tcgplayer?.url });
    rows.push({ source: 'TCGplayer', metric: `${variant} low`, value: prices.low ?? null, url: card.tcgplayer?.url });
  }
  const cm = card.cardmarket?.prices;
  if (cm) {
    rows.push({ source: 'Cardmarket', metric: 'trend', value: cm.trendPrice ?? null, url: card.cardmarket?.url });
    rows.push({ source: 'Cardmarket', metric: 'avg sell', value: cm.averageSellPrice ?? null, url: card.cardmarket?.url });
    rows.push({ source: 'Cardmarket', metric: 'low', value: cm.lowPrice ?? null, url: card.cardmarket?.url });
  }
  rows.push({
    source: 'eBay',
    metric: 'sold comps search',
    value: null,
    url: `https://www.ebay.com/sch/i.html?_nkw=${encodeURIComponent(`${card.name} ${card.set?.name || ''} ${card.number || ''} pokemon card`)}&LH_Sold=1&LH_Complete=1`
  });
  return rows;
}

function conditionByKey(key: ConditionKey) {
  return CONDITION_OPTIONS.find((option) => option.key === key) || CONDITION_OPTIONS[2];
}

function adjustForCondition(value: number | null, condition: ConditionKey) {
  if (value === null) return null;
  return value * conditionByKey(condition).multiplier;
}

function median(values: number[]) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

async function recognizeText(source: File | HTMLCanvasElement) {
  const worker = await createWorker('eng');
  try {
    const result = await worker.recognize(source);
    return result.data.text || '';
  } finally {
    await worker.terminate();
  }
}

function App() {
  const [query, setQuery] = useState('Charizard');
  const [cards, setCards] = useState<PokemonCard[]>(FALLBACK_CARDS);
  const [selectedId, setSelectedId] = useState(FALLBACK_CARDS[0]?.id || '');
  const [loading, setLoading] = useState(false);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [ocrText, setOcrText] = useState('');
  const [error, setError] = useState('');
  const [cameraActive, setCameraActive] = useState(false);
  const [liveScanning, setLiveScanning] = useState(false);
  const [scanStatus, setScanStatus] = useState('Camera idle');
  const [condition, setCondition] = useState<ConditionKey>('raw-nm');
  const [watchlist, setWatchlist] = useState<SavedCard[]>(() => {
    try {
      return JSON.parse(localStorage.getItem(WATCHLIST_KEY) || '[]') as SavedCard[];
    } catch {
      return [];
    }
  });

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const intervalRef = useRef<number | null>(null);
  const scanningRef = useRef(false);
  const lastAutoTermRef = useRef('');

  const selected = useMemo(() => cards.find((card) => card.id === selectedId) || cards[0], [cards, selectedId]);
  const rows = selected ? priceRows(selected) : [];
  const baseEstimate = median(rows.map((row) => row.value).filter((value): value is number => typeof value === 'number'));
  const estimate = adjustForCondition(baseEstimate, condition);
  const conditionOption = conditionByKey(condition);

  useEffect(() => {
    localStorage.setItem(WATCHLIST_KEY, JSON.stringify(watchlist));
  }, [watchlist]);

  function saveSelectedCard() {
    if (!selected) return;
    const saved: SavedCard = {
      id: `${selected.id}-${condition}`,
      name: selected.name,
      setName: selected.set?.name,
      number: selected.number,
      imageUrl: selected.images?.small,
      condition,
      estimatedValue: estimate,
      sources: rows,
      savedAt: new Date().toISOString()
    };
    setWatchlist((current) => [saved, ...current.filter((item) => item.id !== saved.id)].slice(0, 24));
  }

  function removeSavedCard(id: string) {
    setWatchlist((current) => current.filter((item) => item.id !== id));
  }

  async function searchCards(searchTerm = query, silent = false) {
    const term = searchTerm.trim();
    if (!term) return;
    if (!silent) setLoading(true);
    setError('');
    try {
      const q = `name:${JSON.stringify(`*${term}*`)}`;
      const url = `${API}?q=${encodeURIComponent(q)}&pageSize=12&orderBy=-set.releaseDate`;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Pokémon TCG API returned ${response.status}`);
      const data = await response.json();
      setCards(data.data || []);
      setSelectedId(data.data?.[0]?.id || '');
      if (!data.data?.length) setError('No card match. Try the exact card name or set number.');
    } catch (err) {
      const fallback = FALLBACK_CARDS.filter((card) => card.name.toLowerCase().includes(term.toLowerCase()) || term.toLowerCase().includes('charizard'));
      if (fallback.length) {
        setCards(fallback);
        setSelectedId(fallback[0].id);
        setError('Live Pokémon TCG API is unavailable from this environment, so showing built-in demo comps. Add an API key/proxy before app-store release.');
      } else {
        setError(err instanceof Error ? err.message : 'Search failed');
      }
    } finally {
      if (!silent) setLoading(false);
    }
  }

  async function scanImage(file: File) {
    setOcrLoading(true);
    setError('');
    setOcrText('');
    try {
      const raw = await recognizeText(file);
      const cleaned = cleanOcr(raw);
      setOcrText(raw.trim());
      if (cleaned) {
        setQuery(cleaned);
        await searchCards(cleaned);
      } else {
        setError('Scan did not find readable card text. Type the card name manually.');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Image scan failed');
    } finally {
      setOcrLoading(false);
    }
  }

  function stopCamera() {
    if (intervalRef.current) {
      window.clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    setCameraActive(false);
    setLiveScanning(false);
    setScanStatus('Camera idle');
  }

  async function startCamera() {
    setError('');
    if (!navigator.mediaDevices?.getUserMedia) {
      setError('This browser does not expose camera access. Try Chrome/Safari over HTTPS or localhost.');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: 'environment' },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setCameraActive(true);
      setScanStatus('Camera ready. Hold a card inside the yellow frame.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to start camera');
    }
  }

  async function scanCurrentFrame() {
    if (scanningRef.current || !videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    if (!video.videoWidth || !video.videoHeight) return;

    scanningRef.current = true;
    setLiveScanning(true);
    setScanStatus('Reading card text from live camera…');

    try {
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d', { willReadFrequently: true });
      if (!context) throw new Error('Could not read camera frame');

      // OCR the center guide area instead of the whole frame. This is faster and avoids
      // background text poisoning the card-name search.
      const cropWidth = Math.floor(video.videoWidth * 0.68);
      const cropHeight = Math.floor(video.videoHeight * 0.52);
      const cropX = Math.floor((video.videoWidth - cropWidth) / 2);
      const cropY = Math.floor((video.videoHeight - cropHeight) / 2);
      canvas.width = cropWidth;
      canvas.height = cropHeight;
      context.filter = 'contrast(1.28) brightness(1.08) saturate(0.82)';
      context.drawImage(video, cropX, cropY, cropWidth, cropHeight, 0, 0, cropWidth, cropHeight);

      const raw = await recognizeText(canvas);
      const cleaned = cleanOcr(raw);
      setOcrText(raw.trim());

      if (!cleaned) {
        setScanStatus('No readable text yet. Move closer, reduce glare, or tap Search manually.');
        return;
      }

      setQuery(cleaned);
      if (cleaned.toLowerCase() === lastAutoTermRef.current.toLowerCase()) {
        setScanStatus(`Still tracking: ${cleaned}`);
        return;
      }

      lastAutoTermRef.current = cleaned;
      setScanStatus(`Detected “${cleaned}” — loading price comps…`);
      await searchCards(cleaned, true);
    } catch (err) {
      setScanStatus('Live scan paused after a frame error. Try again or use upload/manual search.');
      setError(err instanceof Error ? err.message : 'Live camera scan failed');
    } finally {
      scanningRef.current = false;
      setLiveScanning(false);
    }
  }

  function toggleLiveScan() {
    if (!cameraActive) return;
    if (intervalRef.current) {
      window.clearInterval(intervalRef.current);
      intervalRef.current = null;
      setScanStatus('Live scan paused. Camera remains open.');
      return;
    }

    scanCurrentFrame();
    intervalRef.current = window.setInterval(scanCurrentFrame, LIVE_SCAN_INTERVAL_MS);
  }

  useEffect(() => stopCamera, []);

  return (
    <main className="shell">
      <section className="hero panel">
        <div>
          <p className="eyebrow">card intel / price recon</p>
          <h1>Card Intel Scanner</h1>
          <p className="lede">
            Scan, search, or use live camera mode on a Pokémon card. The app identifies readable card text, matches it against the Pokémon TCG database, and overlays price signals from TCGplayer, Cardmarket, and eBay sold comps.
          </p>
        </div>
        <div className="mission-box">
          <strong>Live mode</strong>
          <span>Hold a card inside the camera frame and the price badge follows the scan zone like an AR filter.</span>
        </div>
      </section>

      <section className="grid">
        <article className="panel controls">
          <p className="eyebrow">01 / live scan</p>
          <h2>Identify the card</h2>

          <div className={`camera-box ${cameraActive ? 'active' : ''}`}>
            <video ref={videoRef} playsInline muted autoPlay />
            <div className="scan-guide" aria-hidden="true">
              {selected && (
                <div className="ar-price-tag">
                  <span>{selected.name}</span>
                  <strong>{money(estimate)}</strong>
                </div>
              )}
            </div>
            {!cameraActive && <div className="camera-placeholder">Camera preview appears here</div>}
          </div>
          <canvas ref={canvasRef} className="capture-canvas" />

          <div className="camera-actions">
            <button onClick={cameraActive ? stopCamera : startCamera}>{cameraActive ? 'Stop camera' : 'Start camera'}</button>
            <button disabled={!cameraActive || liveScanning} onClick={toggleLiveScan}>
              {intervalRef.current ? 'Pause realtime scan' : liveScanning ? 'Scanning…' : 'Realtime scan'}
            </button>
            <button disabled={!cameraActive || liveScanning} onClick={scanCurrentFrame}>Scan frame once</button>
          </div>
          <p className="status-line">{scanStatus}</p>

          <div className="condition-panel">
            <span>Condition / grade lens</span>
            <div className="condition-grid">
              {CONDITION_OPTIONS.map((option) => (
                <button
                  className={condition === option.key ? 'active' : ''}
                  key={option.key}
                  onClick={() => setCondition(option.key)}
                  type="button"
                >
                  {option.label}
                </button>
              ))}
            </div>
            <small>{conditionOption.note}. This is an adjustable assumption until visual grading is added.</small>
          </div>

          <label className="dropzone">
            <input type="file" accept="image/*" capture="environment" onChange={(event) => event.target.files?.[0] && scanImage(event.target.files[0])} />
            <span>{ocrLoading ? 'Scanning image…' : 'Upload / camera still'}</span>
            <small>Fallback OCR grabs visible card text. Manual correction stays available.</small>
          </label>

          <label className="field">
            <span>Card name or OCR result</span>
            <input value={query} onChange={(event) => setQuery(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && searchCards()} placeholder="Charizard, Pikachu, Umbreon VMAX…" />
          </label>
          <button disabled={loading || ocrLoading} onClick={() => searchCards()}>{loading ? 'Searching…' : 'Search prices'}</button>
          {error && <p className="error">{error}</p>}
          {ocrText && <details><summary>OCR raw text</summary><pre>{ocrText}</pre></details>}

          <div className="matches">
            <h3>Matches</h3>
            {cards.length === 0 ? <p className="muted">Search or run realtime scan to load possible card matches.</p> : cards.map((card) => (
              <button className={`match ${selected?.id === card.id ? 'active' : ''}`} key={card.id} onClick={() => setSelectedId(card.id)}>
                <span>{card.name}</span>
                <small>{card.set?.name} #{card.number} · {card.rarity || 'unknown rarity'}</small>
              </button>
            ))}
          </div>
        </article>

        <article className="panel results">
          <p className="eyebrow">02 / aggregate</p>
          {!selected ? (
            <div className="empty">No card selected.</div>
          ) : (
            <>
              <div className="card-head">
                {selected.images?.small && <img src={selected.images.small} alt={selected.name} />}
                <div>
                  <h2>{selected.name}</h2>
                  <p>{selected.set?.name} · #{selected.number} · {selected.rarity || 'rarity unknown'}</p>
                  <div className="estimate">
                    <span>{conditionOption.label} signal</span>
                    <strong>{money(estimate)}</strong>
                    {baseEstimate !== null && condition !== 'raw-nm' && <small>Base raw NM: {money(baseEstimate)} × {conditionOption.multiplier}</small>}
                  </div>
                </div>
              </div>

              <div className="result-actions">
                <button onClick={saveSelectedCard} type="button">Save to watchlist</button>
                <span>{conditionOption.label} · {conditionOption.note}</span>
              </div>

              <div className="price-table">
                {rows.map((row, index) => (
                  <a className="price-row" href={row.url} target="_blank" rel="noreferrer" key={`${row.source}-${row.metric}-${index}`}>
                    <span>{row.source}</span>
                    <em>{row.metric}</em>
                    <strong>{money(row.value)}</strong>
                  </a>
                ))}
              </div>

              <div className="operator-note">
                <strong>Read:</strong> TCGplayer market is the US liquidity signal. Cardmarket is EU demand/trend. eBay sold comps validate reality for condition, grading, and hype spikes. The condition lens adjusts the blended estimate as a visible assumption, not an automated grade. Live scan OCR focuses on the yellow guide box; use bright, glare-free light for the best hit rate.
              </div>
            </>
          )}
        </article>
      </section>

      <section className="panel watchlist">
        <div className="section-head">
          <div>
            <p className="eyebrow">03 / saved comps</p>
            <h2>Local watchlist</h2>
          </div>
          <span>{watchlist.length} saved</span>
        </div>
        {watchlist.length === 0 ? (
          <p className="muted">Save cards after scanning/searching to compare condition assumptions across refreshes. Stored locally in this browser.</p>
        ) : (
          <div className="watch-grid">
            {watchlist.map((item) => (
              <article className="watch-card" key={item.id}>
                {item.imageUrl && <img src={item.imageUrl} alt={item.name} />}
                <div>
                  <strong>{item.name}</strong>
                  <span>{item.setName} #{item.number} · {conditionByKey(item.condition).label}</span>
                  <em>{money(item.estimatedValue)} saved {new Date(item.savedAt).toLocaleDateString()}</em>
                </div>
                <button onClick={() => removeSavedCard(item.id)} type="button">Remove</button>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="panel disclaimer">
        <strong>Source note:</strong> This MVP uses the public Pokémon TCG API for card metadata, TCGplayer, and Cardmarket pricing where available, plus an eBay sold-comps search link. It is unofficial and not affiliated with Pokémon, Nintendo, TCGplayer, Cardmarket, or eBay.
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
