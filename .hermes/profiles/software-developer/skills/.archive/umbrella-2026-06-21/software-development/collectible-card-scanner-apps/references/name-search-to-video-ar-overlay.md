# Name Search Works, Image Scan Failed — Product Direction Note

## Session signal

The user reported that manual/name search worked perfectly and produced solid data, but image scanning did not work. They clarified the strategic destination: apply the same pricing data to live or recorded video and automatically attach a price badge/filter that follows each card, similar to Snapchat puppy-dog-ear face filters.

## Durable product lesson

Do not treat a working name search as the final product. Name search validates the data layer and fallback UX. The differentiated product is video-native card intelligence:

1. Detect/recognize a card in live or recorded video.
2. Stabilize recognition across frames.
3. Attach a tracking AR-style price overlay to the card.
4. Let the user compare prices across multiple platforms quickly.

## Recommended next technical move when still-image scanning fails

- Preserve manual search as the reliable fallback and demo path.
- Instrument the failed image path before rewriting it: capture OCR output, candidate parsing, image dimensions, preprocessing state, and error states.
- Improve still-image recognition only enough to feed the video pipeline: crop/contrast/grayscale/sharpen, then candidate matching.
- Move toward sample-and-stabilize video rather than OCR every frame.
- Cache successful card lookups so repeated frame recognition does not refetch pricing data.

## UX direction

The overlay should behave like a social filter:

- follows the card/scan region;
- shows a concise price badge;
- uses confidence states so it can say scanning/candidate/confirmed;
- allows tap/click to open multi-platform comparison;
- makes source comparison the selling point, not just card identification.

## Kill/scale signal

Scale the video overlay direction if users can scan several cards in a binder/tabletop video and get stable, useful multi-source price badges with minimal manual correction. Kill or narrow the scope if recognition remains too unstable without controlled capture conditions.
