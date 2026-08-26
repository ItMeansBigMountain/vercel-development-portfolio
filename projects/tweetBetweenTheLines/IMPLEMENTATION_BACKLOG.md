# tweetBetweenTheLines — Social Life Blueprint Implementation Backlog

Last updated: 2026-08-25
Source spec: `SOCIAL_LIFE_BLUEPRINT.md`
Status: implementation backlog for downstream engineering/review; task sizes assume the existing TypeScript/Expo workspace.

## Sequencing principles

- Build deterministic, consented, source-backed flows before AI/story/video.
- Keep first-party sign-in, source linking, archive import, analytics, AI, and media consent separated.
- Every shipped slice must expose evidence, confidence, limitations, correction/hide/delete/export controls, and no-diagnosis boundaries.
- Prefer small TDD slices in `packages/domain`, then wire API/mobile.
- Do not claim production readiness until release-gate evidence exists.

## Milestone 0 — Product/doc alignment

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-000 | designer | Keep README and plan linked to Blueprint spec/backlog | README and DEVELOPMENT_PLAN point to `SOCIAL_LIFE_BLUEPRINT.md` and this backlog | `grep -R "SOCIAL_LIFE_BLUEPRINT\|IMPLEMENTATION_BACKLOG" README.md DEVELOPMENT_PLAN.md` |
| BL-001 | reviewer | Review blueprint for safety/privacy/product contradictions | Reviewer signs off or returns changes; no implementer self-approval | Kanban review handoff |

## Milestone 1 — Domain model foundation

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-101 | software-developer | Add `LifeEvent` model and converter from current `MetricEvent` | Supports event kinds in spec; preserves source/record/provenance/deletion lineage; rejects missing tenant/source/consent | Domain unit tests for valid/invalid conversions |
| BL-102 | software-developer | Add `BlueprintCard` type and card factory contract | Card factory requires evidence refs, confidence reasons, formula/model provenance, limitations, and controls; cannot create visible card with no evidence unless type explicitly abstains | Type tests + negative runtime tests |
| BL-103 | software-developer | Add correction/hide/delete state model for derived cards | Corrections do not mutate source event; hidden/deleted cards excluded from default snapshot; correction exported | Unit tests for correction lineage |
| BL-104 | software-developer | Extend confidence model for Blueprint modules | Confidence reasons include event count, supporting evidence, source count, date coverage, and missing categories | Tests around low-volume/missing source cases |
| BL-105 | reviewer | Domain safety review | No card factory allows diagnosis/protected-trait/relationship-fact claims without user confirmation | Code review + red-team strings |

## Milestone 2 — Timeline MVP

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-201 | software-developer | Build deterministic timeline grouping service | Groups by month/year/source/kind; includes coverage gaps; revoked sources excluded | Unit tests using synthetic fixture |
| BL-202 | designer | Implement mobile Timeline tab UX | Empty/imported/revoked/deletion-pending states; filter chips; evidence access; 44 px targets | Browser/mobile screenshot review |
| BL-203 | software-developer | Add timeline export shape | Export includes events, coverage gaps, consent IDs, parser versions, corrections | JSON snapshot test |
| BL-204 | reviewer | Timeline accessibility/safety review | No complete-history or diagnosis copy; coverage warnings visible | Manual preview + automated checks |

## Milestone 3 — Blueprint deterministic cards

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-301 | software-developer | Implement theme cards | Deterministic repeated labels/topics with evidence and missing-data caveats | Unit tests for counts/confidence/evidence |
| BL-302 | software-developer | Implement count cards | Posts/messages/views/listens/searches/reactions/follows by source/category/window | Unit tests for category/window counts |
| BL-303 | software-developer | Implement consolidation cards | Duplicate/stale/unsupported-source suggestions use reversible neutral copy | Unit tests for suggestions and no-shame copy fixtures |
| BL-304 | software-developer | Implement chapter proposal cards | Neutral time-bounded proposals; user rename stored as correction | Unit tests for split/rename behavior |
| BL-305 | software-developer | Implement achievement/adventure cards | Opt-in generation; no streak pressure/public leaderboard; evidence-backed counts only | Unit tests + copy snapshot |
| BL-306 | software-developer | Implement persuasion-pattern transparency cards | Uses ad/interests/recommendation-like/export evidence only when present and consented; no manipulation/intent claims | Unit tests with missing ad data and explicit ad data |
| BL-307 | reviewer | Blueprint card safety review | All cards have evidence/confidence/limitations/controls; no prohibited claims | Snapshot review and red-team phrase scan |

## Milestone 4 — Relationships and user-authored meaning

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-401 | software-developer | Add person/entity clustering as draft-only suggestions | Default labels are source/account handles; no friend/partner/family labels until user confirms | Unit tests for unconfirmed relationship display |
| BL-402 | designer | Relationship evidence drawer and confirmation UI | Rename, mark private, split/merge, hide/delete are visible and understandable on mobile | Mobile preview QA |
| BL-403 | software-developer | Persist relationship corrections and privacy flags | Corrections affect future snapshots; private labels excluded from export unless user includes them | API/domain tests |
| BL-404 | reviewer | Sensitive relationship review | Confirm no automatic heartbreak/romance/family inference | Manual review |

## Milestone 5 — Heartbreak/recovery reflection lane

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-501 | designer | Design user-initiated reflection period flow | User names period, selects sources/time windows, sees non-diagnostic boundary before analysis | Prototype/screenshot review |
| BL-502 | software-developer | Implement reflection-period model | Period cannot be auto-created from social data; source/time consent is explicit | Unit tests for blocked automatic creation |
| BL-503 | software-developer | Generate deterministic reflection summaries | Output uses selected time windows, evidence, limitations, supportive prompts; no diagnosis/crisis triage | Unit tests + prohibited-language tests |
| BL-504 | reviewer | Clinical/safety gate | Block launch until qualified review if any screener/health-adjacent claims are added | Review record |

## Milestone 6 — Sources, consent, and deletion center

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-601 | software-developer | Expand consent receipt schema for Blueprint/media flags | Includes AI and media-generation consent states, category, purpose, retention, locale, policy version | API tests |
| BL-602 | designer | Sources tab UX | Source status, categories, coverage, parser warnings, revoke/delete/export visible | Mobile preview QA |
| BL-603 | software-developer | Deletion lineage for Blueprint descendants | Deleting source invalidates events/cards/storylines/video plans; reconciliation receipt emitted | E2E deletion test |
| BL-604 | reviewer | Privacy controls review | Export/revoke/delete available independent of tier/payment | Review checklist |

## Milestone 7 — Optional AI storylines

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-701 | software-developer | Add AI narrative consent gate | Blocks without current source/category/purpose consent; deterministic features remain available | Unit/API tests |
| BL-702 | software-developer | Build minimized narrative payload builder | Payload excludes raw archives, credentials, unselected DMs/text, provider tokens; includes evidence aggregate IDs | Canary tests |
| BL-703 | software-developer | Add unsafe output validator | Blocks diagnosis, protected traits, causation, professional decisioning, crisis prediction, relationship facts | Red-team corpus tests |
| BL-704 | designer | Stories tab UX for draft/approve/edit/delete | AI story is labeled, editable, deletable, and shows model/prompt/analyzer provenance | Mobile preview QA |
| BL-705 | reviewer | AI safety/privacy review | No AI job consumes quota or stores output after validation failure/user cancel | Review tests |

## Milestone 8 — Personalized video planning/render gate

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-801 | designer | Design video consent/storyboard planner | User selects cards, style, audience, evidence, and private-only default; rendering separate confirmation | Prototype review |
| BL-802 | animator | Define motion-ready storyboard schema | Scene list references Blueprint cards, evidence-safe copy, aspect ratios, no raw private content by default | Schema review |
| BL-803 | software-developer | Store video plan metadata/deletion lineage | Prompt/source cards/model/provider/asset IDs/user approvals captured; delete removes descendants | Unit/API tests |
| BL-804 | reviewer | Media safety review | No face/voice clone, third-party likeness, minors, health/crisis, public share without explicit consent | Review checklist |

## Milestone 9 — Entitlements and economics instrumentation

| ID | Owner | Task | Acceptance criteria | Verification |
| --- | --- | --- | --- | --- |
| BL-901 | software-developer | Map Blueprint limits to existing tiers | Free/Premium/Premium+AI enforce deterministic, comparison, AI generation, and source/account limits; rights never paywalled | Entitlement tests |
| BL-902 | software-developer | Add content-free cost/usage telemetry | Logs reason classes/counts only; no raw text, filenames, prompts, or model output | Telemetry tests and log scan |
| BL-903 | business-operator | Validate pricing with design partners | 10–15 interviews; paid-conversion signal or revised package | Research handoff |
| BL-904 | reviewer | Billing/privacy review | Failed payment never blocks export/revoke/delete/corrections/safety info | Review checklist |

## Release gate checklist

- [ ] `npm test` passes.
- [ ] `npm run typecheck` passes.
- [ ] Mobile web preview has Timeline/Blueprint/Sources/Stories/Control tabs and no console errors.
- [ ] Evidence/confidence/limitations/controls appear on every visible card.
- [ ] Consent/revoke/export/delete E2E passes with synthetic and consented redacted fixtures.
- [ ] AI/story/video features remain disabled without explicit consent and review.
- [ ] Prohibited-language red-team suite passes.
- [ ] Legal/privacy/security/platform-policy review completed for each enabled source lane.
- [ ] Reviewer approves; implementer does not self-approve.

## Specialist handoffs

- `software-developer`: BL-101 through BL-704, BL-901/902 implementation.
- `designer`: BL-202, BL-402, BL-501, BL-602, BL-704, BL-801 UX artifacts.
- `animator`: BL-802 motion-ready storyboard schema.
- `business-operator`: BL-903 pricing validation.
- `reviewer`: every review gate and release approval.
