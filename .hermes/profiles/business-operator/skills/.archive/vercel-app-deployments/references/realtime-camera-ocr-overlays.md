# Realtime camera OCR overlays for static Vite MVPs

Use this when evolving a static scanner/search MVP into a browser-only live camera demo without adding backend infrastructure.

## Pattern

1. Keep the reliable manual/name search path as the source of truth.
2. Add `navigator.mediaDevices.getUserMedia` only as a progressive enhancement; show a clear fallback when camera access is unavailable.
3. Render the stream into a `<video playsInline muted autoPlay>` element and keep a hidden `<canvas>` for frame capture.
4. OCR a cropped guide area rather than the full frame. A centered crop reduces background text and makes browser OCR faster.
5. Run live OCR on a throttled interval, not every video frame. Around 3 seconds is a safe MVP default for `tesseract.js`.
6. Guard against overlapping OCR jobs with a ref/lock such as `scanningRef.current`.
7. De-dupe repeated detected terms before firing API searches to avoid rate/noise issues.
8. Draw an AR-style overlay in CSS over the scan guide. For an MVP, let the price badge follow the scan zone; true object tracking can come later.
9. Always keep upload/still-image scan and manual search fallbacks visible.

## Implementation notes

- Camera permissions require HTTPS in production or localhost in development.
- Use rear camera preference for mobile: `facingMode: { ideal: 'environment' }`.
- Stop tracks on teardown: `stream.getTracks().forEach(track => track.stop())`.
- Apply light canvas preprocessing before OCR, e.g. `contrast(1.28) brightness(1.08) saturate(0.82)`.
- Avoid presenting this as full visual recognition/tracking unless an object detector/tracker is actually implemented. Phrase accurately: "OCR-based realtime scanning with an AR-style fixed scan-zone price overlay."

## Product direction from user feedback

When the user says manual/name search works but image scan is unreliable, treat manual search as validated demand and image recognition as the technical risk. Do not keep polishing generic OCR as if it were the product. The higher-value target is a live-video or recorded-video price-comparison overlay:

- Detect/identify the card in a video frame, then attach a price badge to the card like a Snapchat-style face/puppy-ear filter.
- The selling point is not just recognizing a card; it is making prices easy to compare across multiple marketplaces/platforms.
- Keep the overlay honest in early MVPs: fixed scan-zone badge first, then lightweight tracking, then true object/card tracking when the recognition pipeline is reliable.
- Model the data shape around marketplace comparisons from the beginning: `{ source/platform, condition, low/median/high, lastSold/listing, url, timestamp }` rather than a single price string.
- For recorded video, process sampled frames and stabilize repeated detections before displaying a moving price badge; avoid firing marketplace lookups on every frame.

## Verification

- Run the local production build, e.g. `npm run build` for Vite.
- Deploy normally via Vercel if requested.
- Verify the public alias returns HTTP 200.
- Fetch the deployed JS bundle and confirm strings like `getUserMedia`, `Start camera`, or `Realtime scan` appear if browser visual QA is unavailable.
- For price-comparison overlays, verify both paths: manual/name search still returns marketplace comparison data, and the video/camera UI can display the same comparison payload as an overlay without needing a successful visual scan.
