# Amazon Associates — Primary References

Re-check these pages before operational or policy-sensitive changes.

- Associates Central: https://affiliate-program.amazon.com/home
- Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement
- Commission Income Statement: https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ
- Program Policies index: https://affiliate-program.amazon.com/help/operating/policies
- FTC endorsement guidance: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- PA-API documentation/deprecation notice: https://webservices.amazon.com/paapi5/documentation/
- Creators API introduction: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction

## Current implementation facts

- Screenshot supplied 2026-08-11 proves the user can access a US Amazon Associates dashboard.
- Visible tools include SiteStripe, Link Checker, Product Advertising API, Manage Your Tracking IDs, and Creators API.
- Screenshot does not prove a tracking ID, tax status, payment configuration, API credential, or payable earnings total.
- PA-API documentation says it will be deprecated 2026-05-15 and directs developers to Creators API.
- Creators API is REST-based and supports SearchItems, GetItems, GetVariations, and GetBrowseNodes. Official prerequisites include marketplace enrollment, API registration/credentials, and at least 10 qualifying sales in the past 30 days.
- Amazon Special Links must use the user's actual tracking ID. A plain Amazon product URL is marketing but does not establish user commission attribution.

## Getting paid (US program)

- Direct deposit: minimum $10; no processing fee.
- Amazon gift certificate: minimum $10; no processing fee.
- Check: minimum $100; a $15 processing fee normally applies.
- Below-threshold commissions roll forward.
- Tax interview must be completed and IRS-validated before payment.
- Amazon says it issues a 1099 by January 29 to an eligible Associate paid at least $600 in the prior calendar year, or where taxes were withheld, subject to entity exemptions.
- Earnings require qualifying shipped/streamed/downloaded-and-paid activity and may be reduced by disqualifications, returns, cancellations, and excluded charges. A standard Special Link session generally ends after 24 hours, an order, or another Associate link; eligible cart additions can qualify if ordered within 89 days.

## Disclosure baseline

Amazon requires both the account-associated sentence `As an Amazon Associate I earn from qualifying purchases.` and a legally sufficient disclosure near Special Links. FTC guidance for a YouTube endorsement calls for disclosure in the video itself—not only the description; audio plus visual is preferred. Keep the description disclosure before truncation.

## Approval and governance

- Amazon evaluates an application after 3 qualifying sales in the first 180 days; self-purchases do not qualify.
- Declare each exact public site/channel where links appear and keep the inventory current.
- Normal tracking-ID limit is 100 per Associates account; use stable channel/campaign IDs, never viewer-identifying IDs.
- Payments are ordinarily issued monthly, about 60 days after the earning month, once threshold and valid tax information requirements are met.
- Policy automation should monitor the live Agreement and Policies for changes, but route legal interpretation and certifications to a human.

## Creators API implementation

- PA-API passed its documented 2026-05-15 deprecation date; new work targets Creators API.
- Creators API uses OAuth 2.0 client credentials and new credentials; legacy AWS/SigV4 credentials do not carry over.
- North America token endpoint: `https://api.amazon.com/auth/o2/token`; scope `creatorsapi::default`; token lifetime is documented as 3600 seconds.
- Catalog base: `https://creatorsapi.amazon/catalog/v1`; send bearer token, `x-marketplace`, matching body marketplace, and a real marketplace-valid `partnerTag`.
- Initial allocation is documented as 1 TPS and 8,640 transactions/day; use batching, token caching, a rate limiter, and exponential backoff for 429/5xx.
- Store exact API-vended `detailPageURL` values without deleting Amazon parameters.
- Cache offers/prices no longer than 1 hour; other product metadata/image URLs no longer than 24 hours. Never cache Amazon image binaries.
- Avoid embedding exact price/availability into permanent videos; say `check current price` instead.
- Creators API has no documented earnings/reporting operation. Ingest user-exported Associates reports; do not scrape authenticated Associates Central.

## Reporting and OneLink

- Associates Central exports XLSX, tab-delimited text, and XML. Parse supplied exports locally and reconcile by tracking ID.
- OneLink can redirect US links to supported marketplaces. Amazon full and short links are supported; third-party shorteners are not supported for OneLink.
- Marketplace enrollment, tax/payment setup, destination preferences, and irreversible country-store closure decisions remain human-controlled.

## Prohibited automation highlights

No self/family-manufactured orders, fake engagement, incentives, cookie stuffing, forced clicks, hidden links, misleading redirects, Amazon-mark paid-search bidding, unapproved app links, customer-review links, unsolicited email/SMS/DM links, scraping, stale price claims, or Amazon image archives.

## Data model boundary

Store tracking IDs and public Special Links. Do not store raw TIN/SSN, bank data, passwords, cookies, or API secret values. Store only secure references for secrets/documents.
