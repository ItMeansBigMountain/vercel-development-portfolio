# tweetBetweenTheLines — User-Owned Social Life Blueprint

Last updated: 2026-08-25
Status: buildable product/design specification; implementation, legal/privacy, security, accessibility, platform-policy, and qualified clinical review remain release gates.

## One-line product promise

The Social Life Blueprint lets a user combine consented official account archives and approved account connections into a private, explainable life timeline: themes, relationships, chapters, achievements, adventures, counts, consolidation suggestions, recovery reflections, persuasion-pattern transparency, and optional user-approved AI storylines/videos — always with evidence, confidence, edit/delete controls, and no unsupported claims.

## Product stance

1. The user owns the data and interpretation. The product proposes reflections; it does not declare facts about identity, relationships, health, intent, or causation.
2. Official data only. Ingestion uses official OAuth/API access, official account exports, or transparent manual user-provided inputs. No credential scraping, cookie reuse, or “we logged into your account for you.”
3. Evidence before story. Every card, chapter, count, relationship edge, adventure, and storyline cites source evidence or aggregate IDs, source/date/category coverage, confidence, analyzer/model version, limitations, and controls to correct/hide/delete.
4. Deterministic first, AI optional. Timelines, counts, consolidations, confidence, and safety gates are deterministic. AI may only summarize approved evidence into labeled narratives after separate opt-in.
5. Non-diagnostic reflection. Heartbreak/recovery and wellbeing-adjacent language are private reflection prompts, never diagnosis, crisis prediction, treatment advice, protected-trait inference, or professional decisioning.
6. Delight without pressure. Achievements and adventures should feel like a personal scrapbook, not gamified surveillance or manipulative growth hacking.

## MVP definition

The MVP should extend the current Expo/web deterministic demo into a persistent, consented “Blueprint” experience with five core loops:

1. **Bring data in safely**
   - First-party app sign-in stays separate from social-source consent.
   - User imports a normalized JSON fixture or one supported official archive parser behind the sandbox gates in `ARCHIVE_SCHEMA_AND_FIXTURE_PLAN.md`.
   - Each source has a consent receipt, source status, categories selected, retention choice, and revoke/delete path.
2. **Build a unified timeline**
   - Normalize posts, messages, reactions, views, listens, searches, import notes, and supported archive rows into `LifeEvent` records.
   - Display a mobile-first timeline grouped by year/month/week with source chips, kind chips, confidence, and evidence access.
   - Missing windows and unsupported categories appear as coverage gaps, not zeros.
3. **Show explainable blueprint cards**
   - Themes, chapters, relationships, achievements, adventures, attention/media counts, consolidations, persuasion-pattern transparency, and optional recovery reflections appear as cards.
   - Each card has: summary, why shown, confidence, evidence drawer, formula/analyzer version, limitations, correction, hide, export, and delete controls.
4. **Let the user edit the meaning**
   - User can rename chapters, merge/split themes, mark relationships private/incorrect, redact evidence, add personal notes, and delete any derived object without mutating source records.
   - Corrections become first-class evidence that future snapshots must respect.
5. **Export or delete everything**
   - Export includes sources, consent receipts, normalized events, cards, corrections, AI/storyline provenance if present, deletion manifest, and checksums.
   - Deletion follows the source lineage and reconciliation rules in `PRIVACY_SAFETY_ARCHITECTURE.md`.

Out of MVP: live multi-platform scheduled refresh, native app-store release, public social sharing, automated video generation, health screeners, crisis flows beyond static resource guidance, minors, workplace/third-party assessment, and “complete history from every platform” claims.

## Source ingestion and consent model

### Source lanes

| Lane | User experience | Backend behavior | MVP support |
| --- | --- | --- | --- |
| First-party account sign-in | “Create/sign into BetweenLines” | App identity only; no social-history consent | Required |
| Official OAuth/API source | “Connect Spotify/Reddit/etc.” with exact scopes | PKCE/state, token vault, connector status, source consent receipt, revocation | Optional for one low-risk approved source only after provider review |
| Official archive import | “Upload the export you requested from the platform” | Quarantine, scan, deterministic parser, manifest, normalized events | Required for first supported parser or normalized JSON fixture |
| Manual/import note | “Add a note, label, or self-declared milestone” | User-authored event with provenance `manual_user_entry` | Required for corrections/chapters; not treated as platform proof |

### Consent receipt fields

Each consent receipt must include: tenant ID, subject ID, actor ID, source ID, acquisition lane, platform/account label, selected categories, excluded categories, purpose, retention policy, policy-copy version, locale, grant/revocation time, source docs/terms links where relevant, AI consent state, media-generation consent state, and deletion lineage root.

Consent cannot be bundled across import, scheduled refresh, sensitive reflections, AI narratives, media generation, marketing, telemetry, or cross-account comparison. All optional consent defaults off.

## Unified data model

Use these product-level models as the implementation target. They intentionally sit above current `MetricEvent` so engineering can map the existing domain package forward without losing compatibility.

```ts
type SourceLane = 'first_party_identity' | 'official_oauth_api' | 'official_archive' | 'manual_user_entry';
type LifeEventKind = 'post' | 'message' | 'reaction' | 'view' | 'listen' | 'search' | 'follow' | 'save' | 'purchase' | 'location_checkin' | 'calendar' | 'photo_or_media' | 'import_note';
type ConfidenceLevel = 'insufficient' | 'low' | 'medium' | 'high';

type LifeEvent = {
  id: string;
  tenantId: string;
  subjectId: string;
  sourceId: string;
  sourceLane: SourceLane;
  sourceRecordId: string;
  occurredAt: string;
  kind: LifeEventKind;
  title?: string;
  contentExcerpt?: string;
  locale?: string;
  peopleRefs: string[];
  placeRefs: string[];
  mediaRefs: string[];
  topicRefs: string[];
  metadata: Record<string, string | number | boolean | null>;
  provenance: {
    consentReceiptId: string;
    parserOrConnectorVersion: string;
    rawObjectRef?: string;
    deletionLineage: string[];
    fieldClassifications: Record<string, 'official_field' | 'derived_deterministic' | 'user_correction' | 'product_metadata'>;
  };
};

type BlueprintCard = {
  id: string;
  tenantId: string;
  subjectId: string;
  snapshotId: string;
  type: 'theme' | 'relationship' | 'chapter' | 'achievement' | 'adventure' | 'count' | 'consolidation' | 'heartbreak_recovery_reflection' | 'persuasion_pattern' | 'ai_storyline' | 'personalized_video_plan';
  title: string;
  summary: string;
  status: 'draft' | 'visible' | 'hidden' | 'corrected' | 'deleted';
  confidence: { level: ConfidenceLevel; score: number; reasons: string[] };
  evidenceRefs: Array<{ eventId: string; sourceId: string; sourceRecordId: string; excerpt?: string; matched?: string[] }>;
  coverage: Array<{ sourceId: string; categories: string[]; firstEventAt?: string; lastEventAt?: string; missingWarnings: string[] }>;
  formulaOrModel: { kind: 'deterministic' | 'ai'; name: string; version: string; inputDigest: string };
  limitations: string[];
  userControls: { canRename: boolean; canCorrect: boolean; canHide: boolean; canDelete: boolean; canExport: boolean };
};
```

## Blueprint modules

### 1. Life Timeline

Goal: make the imported archive feel like a browsable life record, not a black-box score.

- Entry states: no data, validating import, imported with warnings, source revoked, deletion pending, deletion complete.
- Grouping: Today/this month, month, year, custom chapter.
- Filters: source, kind, person, place, theme, confidence, hidden/corrected.
- Each timeline item shows source chip, date, kind, excerpt/metadata, “why visible,” and source evidence.
- Required warning: “This timeline only includes selected imported sources and categories.”

### 2. Themes

Themes are repeated interests, communities, creators, topics, media, places, or activities. They are deterministic aggregate clusters first.

- Formula examples: repeated token/category counts, source/category counts, change-over-time split.
- Avoid: “you love X,” “your true identity,” “you are political/religious/sexual orientation.”
- Copy pattern: “In this selected slice, {theme} appeared in {count} events across {sources}. Confidence is {level} because {reasons}.”

### 3. Relationships

Relationships are evidence-linked interaction clusters, not labels about the relationship’s nature.

- Allowed: “frequent interaction with @name/source label,” “shared events,” “conversation/activity windows.”
- User must name/confirm the relationship label before it becomes visible as “friend,” “partner,” “family,” etc.
- Sensitive relationship inferences default hidden and cannot be pushed in notifications.
- Controls: rename, mark private, split/merge duplicate people, remove all relationship-derived cards.

### 4. Chapters

Chapters are time-bounded story containers. Deterministic proposals use bursts, life-event notes, source/time boundaries, and user edits.

- Default proposal names are neutral: “Spring 2024 activity burst,” “Music-heavy month,” “New community cluster.”
- User-approved chapter names become user corrections, not model facts.
- Each chapter shows included/excluded sources and missing time windows.

### 5. Achievements and adventures

Achievements/adventures are opt-in celebratory cards drawn from user-visible evidence.

- Examples: “100 runs logged,” “Most active learning week,” “First post in a new community,” “Concert/travel/photo cluster.”
- Avoid competitive scarcity, shame, streak pressure, addiction-style rewards, and public leaderboards.
- User can disable achievement/adventure generation entirely.

### 6. Counts and consolidations

Counts should help users understand and clean their footprint.

- Counts: posts/messages/views/listens/searches/reactions/follows by source/category/window.
- Consolidations: likely duplicate accounts, repeated topics, dead sources, stale connected accounts, redundant exports, unsupported files, and retention cleanup suggestions.
- Consolidation copy must be reversible and non-alarming: “You may want to review…” not “You must…”

### 7. Heartbreak/recovery reflection

This is a private reflection lane for user-named breakup/recovery periods. It must never infer heartbreak automatically from posts, DMs, follows, blocks, sad language, or music taste.

- Entry: user creates a private reflection period and may choose sources/categories/time windows.
- Output: timeline of user-approved memories, supportive prompts, sentiment/attention changes with limitations, and self-authored notes.
- Required boundary: “This is not mental-health assessment, crisis detection, or relationship judgment.”
- If a user self-reports imminent harm, route to static emergency/professional-help resources; do not use social data or AI to triage.

### 8. Persuasion-pattern transparency

Goal: show how platforms and creators may have influenced attention without claiming manipulation or intent.

- Inputs: ad/interests exports where explicitly available, watch/search/recommendation-like records when official exports include them, creator/media repetition, session/rhythm aggregates.
- Cards: “Repeated recommendation loops,” “Ad/topic labels found in export,” “Attention rhythm shifts,” “Creator/topic concentration.”
- Copy: “This pattern may reflect platform design, your choices, available data, or missing data; it does not prove persuasion or intent.”
- Never infer protected traits or use cards for ads, employment, credit, insurance, policing, or eligibility.

### 9. Optional AI storylines

AI storylines turn selected deterministic cards into a readable private narrative.

- Separate opt-in per source/category/purpose/policy version.
- Payload contains minimized aggregate evidence and approved excerpts only; no raw archives, credentials, DMs by default, unselected text, or provider tokens.
- Output is draft until user approves, edits, or deletes.
- Each storyline displays AI provider/model/prompt/analyzer versions, generated time, confidence/limitations, source links, and “delete this AI output.”
- Unsafe outputs are blocked without consuming quota.

### 10. Personalized videos

Personalized videos are an explicit media-generation feature, not an automatic upsell.

- Require two separate consents: AI narrative consent and media-generation consent.
- User selects included cards/evidence, style, duration, audience (“private only” by default), and whether any personal images/names may be used.
- Default generated asset is a storyboard/video plan until the user confirms rendering.
- No face/voice cloning, third-party likeness, private messages, relationship labels, minors, health/crisis content, or public sharing without explicit consent and review.
- Store generation metadata: prompt, source cards, model/provider, asset IDs, render time, user approvals, deletion lineage.

## Mobile-first UX specification

### Navigation model

Primary tabs:

1. **Timeline** — life events with filters and coverage gaps.
2. **Blueprint** — cards for themes, relationships, chapters, achievements, adventures, counts, consolidations, persuasion patterns, and optional reflections.
3. **Sources** — consent receipts, source status, import/revoke/delete, parser warnings.
4. **Stories** — optional AI storylines and video plans, disabled until consented.
5. **Control** — export, deletion center, privacy settings, entitlements, support.

### Card anatomy

Every card uses the same accessible skeleton:

- Type chip + source/category coverage chip.
- User-editable title.
- Plain-language summary with confidence level.
- “Why am I seeing this?” drawer.
- Evidence preview: 1–3 rows plus “view all evidence.”
- Limitations and missing-data warning.
- Controls: rename/correct, hide, delete, export.
- AI/media status if applicable.

### Evidence drawer requirements

The evidence drawer must show:

- source name and account label;
- source record ID or stable record reference;
- date/time and category;
- excerpt or aggregate row;
- matched terms/metadata fields;
- parser/connector/formula version;
- confidence reasons;
- buttons to remove this evidence from the derived card, hide the card, delete the source, or export.

### Accessibility and visual rules

- Minimum 44 px touch targets.
- Text contrast target: WCAG AA or better; sensitive warning text cannot rely on color alone.
- Plain-language confidence: “High confidence from 180 records across 3 sources,” not only percentages.
- Skeleton/loading states must disclose that no analysis has run yet.
- Empty states must invite import/synthetic demo without shaming or fear.
- Mobile evidence drawers must be bottom sheets or full-screen panels; never tiny modals.
- Destructive actions need clear scope and reversible pending state where backend deletion is reconciling.

## Safety, privacy, and policy rules

1. No diagnosis, crisis prediction, protected-trait inference, causation claims, or professional decisioning.
2. Relationship labels require user confirmation before becoming relationship facts.
3. Heartbreak/recovery is user-initiated and private by default.
4. AI and video are opt-in, revocable, and deleteable; deterministic features cannot require AI.
5. Every insight can be corrected, hidden, exported, or deleted.
6. Raw archives, credentials, unselected DMs, direct provider tokens, and unrelated sources cannot enter AI/media prompts.
7. Missing data must be visible at card and snapshot level.
8. Source revocation invalidates descendants; re-consent does not resurrect deleted data.
9. Telemetry is content-free and cannot log raw text, filenames, prompts, model outputs, or sensitive answers.
10. Public sharing is out of MVP; if added later, it must strip evidence by default and require a preview.

## Entitlement fit

The existing `PRODUCT_TIERS_AND_ENTITLEMENTS.md` remains canonical. Blueprint-specific mapping:

| Capability | Free | Premium | Premium + AI |
| --- | --- | --- | --- |
| Timeline/current snapshot | Latest snapshot from allowed import quota | 24 saved snapshots and comparisons | Same |
| Blueprint cards | Deterministic cards from current snapshot | Deterministic cards plus history/cross-source comparison | Same |
| Relationship/chapter edits | Yes | Yes | Yes |
| Export/delete/corrections | Always available | Always available | Always available |
| AI storylines | Not available | Not available | 10 successful generations/month |
| Personalized video plans/renders | Not available in MVP | Not available in MVP | Post-MVP gated add-on only after media consent and cost review |

No tier may hide evidence, confidence, correction, export, revoke, delete, or no-diagnosis safety copy.

## Success criteria

### Activation and comprehension

- At least 70% of design partners who start an import reach a visible timeline or clear rejection reason.
- At least 50% open at least one evidence/derivation drawer during first session.
- At least 80% can correctly answer, in interview, that cards cover only selected sources and are not diagnosis.

### Trust and control

- 95% of generated cards expose evidence, confidence, limitations, and controls in automated UI checks.
- 100% of revocation/delete flows produce a pending/completed/failed receipt.
- Correction/hide/delete controls are discoverable in moderated mobile testing without facilitator hints.

### Safety

- 0 diagnostic/protected-trait/causal/professional-decision claims in automated narrative validation and reviewer spot checks.
- 0 AI/video generations without current specific consent receipt.
- All health-adjacent/self-report features remain blocked until qualified review evidence exists.

### Economics and reliability

- Import rejection reasons are actionable for at least 90% of failed attempts.
- Median deterministic card generation under 5 seconds for MVP-sized imports.
- Variable-cost instrumentation covers import parse, storage, export, deletion, and AI generation before billing launch.

## Release gates

1. Domain model and tests for `LifeEvent`, `BlueprintCard`, evidence refs, corrections, and deletion lineage.
2. Mobile UI for Timeline, Blueprint, Sources, Stories, and Control with accessibility smoke tests.
3. Import/consent/revoke/export/delete E2E with synthetic and consented redacted fixtures.
4. Narrative/media consent gate and unsafe-output validator before any AI copy ships.
5. Security/privacy/legal/platform-policy review for each source lane.
6. Reviewer approval; implementer must not self-approve.
