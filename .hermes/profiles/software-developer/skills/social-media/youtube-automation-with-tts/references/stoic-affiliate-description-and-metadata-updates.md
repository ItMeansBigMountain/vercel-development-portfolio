# Stoic Affiliate Descriptions and Existing-Video Metadata

Use this pattern when the user wants Daily Stoic, Ryan Holiday, or Robert Greene product marketing in YouTube descriptions.

## Revenue truthfulness

A normal product URL is marketing, not necessarily an owner-attributed affiliate link. Before claiming the channel will earn commissions:

1. Search configuration for the owner's actual affiliate tag or tracking URLs.
2. Confirm the merchant/program accepts the channel and permits YouTube promotion.
3. If no owner-attributed link exists, use an approved direct product link but state that it will not generate commission for the user yet.
4. Never imply that a creator-owned `geni.us` link credits the user's affiliate account.

For books, Amazon Associates is a practical fallback program, but enrollment and a user-owned tracking tag are required.

## Description layout

Put the offer block before the editorial description and support links:

```text
Go deeper with Daily Stoic Life: <configured URL>
Ryan Holiday — The Obstacle Is the Way: <configured URL>
Robert Greene — The 48 Laws of Power: <configured URL>
Affiliate disclosure: Some links may be affiliate links. If you purchase through them, I may earn a commission at no extra cost to you.

<video-specific description>
<channel/support links>
```

Avoid emoji in metadata when the upload stack has previously encountered `invalidDescription` Unicode failures.

Recommended configuration names:

- `DAILY_STOIC_AFFILIATE_URL`
- `RYAN_HOLIDAY_AFFILIATE_URL`
- `ROBERT_GREENE_AFFILIATE_URL`

Direct product links may be safe fallbacks, but label them internally as non-monetized until replaced by owner-attributed URLs.

## New uploads

Build the block only for Stoic/Daily Stoic content, not every newsletter type. Add a regression test that verifies:

- the three offers appear;
- the disclosure appears;
- the offer block precedes the normal description/support section;
- configured URLs override direct fallbacks.

Run the focused test and then the complete metadata/script test module.

## Existing uploads

Do not infer edit capability from scopes serialized in a token file. Metadata updates require a live `videos.update(part="snippet")` probe against a video owned by the expected channel.

Safe sequence:

1. Resolve candidate video IDs from the immutable upload ledger.
2. Call `channels.list(mine=True)` and verify the exact expected channel ID.
3. Fetch each current snippet with `videos.list(part="snippet")`.
4. Preserve title, tags, and category while prepending the offer block.
5. Make the update idempotent by detecting an existing block.
6. Read the snippet back after the update.
7. Report exact updated video IDs/URLs.

If `videos.update` returns `403 youtube.video/forbidden`, stop the migration and report that future uploads are configured but old videos remain unchanged. Reauthorize or repair the metadata-edit grant before retrying. Do not repeatedly replay the same update or claim success based on the token's stored scope list.

## Disclosure and compliance

- Keep the disclosure conspicuous and near the links.
- Do not claim endorsement by Ryan Holiday, Robert Greene, or Daily Stoic.
- Follow the affiliate program's rules for price statements, trademarks, link shortening, and social-media placement.
- Preserve a distinction between direct creator/store links and the channel owner's commission-bearing links.
