# Small-Business Agentic AI Services — Google Drive Production Pattern

Use this reference when turning a Hermes-powered AI automation consultancy or managed-service idea into a real, sellable Google Workspace asset library.

## Business boundary

- Treat this venture as independent from unrelated businesses even when they share the same Google account.
- Create a distinct root folder, project index, numbered subfolders, and client-delivery area.
- The user's current operating account is `personal-main` / `affan.fareed@gmail.com` until a dedicated business Workspace account is justified.
- Keep every artifact for this venture under its own root; never place files in Algorithm Academy or another business folder.

## Positioning rule

Do not sell “Hermes installation” as the primary value. Installation is an implementation component. Sell a measurable business outcome:

> We install a secure AI operator inside your business, connect it to the tools you already use, and train it to complete valuable work—not merely answer questions.

Customer-facing language should emphasize saved owner time, faster lead response, consistent follow-up, reduced administrative burden, fewer missed opportunities, and continuous capability growth. Technical materials may describe Hermes, profiles, memory, skills, cron, webhooks, MCP, integrations, and approval gates.

## Offer architecture

A practical introductory ladder:

- **AI Opportunity Audit:** $750; workflow map, risk/access review, conservative ROI, and fixed-price recommendation. Credit toward implementation when appropriate.
- **Agentic Starter:** $3,500 setup + $1,250/month; one agent profile, one high-value workflow, one recurring owner briefing, knowledge starter, controls, documentation, and managed optimization.
- **Managed AI Operator:** $6,500 setup + $2,250/month; multiple workflows, integrations, custom skills, monitoring, monthly capability improvement, and quarterly roadmap.
- **Agentic Growth Partner:** from $12,000 setup + $4,500/month; custom integrations, multiple profiles/agents, cross-functional workflows, advanced support, and continuous experimentation.

Treat these as working prices, not universal guarantees. Define workflow, integration, user, support, change, and variable-usage boundaries. Prefer smaller scope over permanent discounts. Client normally pays model/API, hosting, and third-party software costs directly.

## Minimum Drive package

Create native Google Docs for:

1. Project index and business boundary
2. Offer architecture and service packages
3. Flagship offer (initially “AI Front Office”)
4. Marketable capability catalog
5. Sales discovery script
6. AI Opportunity Audit questionnaire
7. Proposal and scope template
8. Client onboarding and access checklist
9. Security, human-approval, and data policy
10. Implementation and acceptance playbook
11. Monthly client performance report
12. Case-study/proof template
13. Landing-page and outreach copy
14. Pricing economics and guardrails

Create a native Google Sheet with at least:

- ROI Calculator
- Sales Pipeline
- Client Metrics
- Delivery Costs

Create a visually inspected promotional flier and place it under Sales and Marketing. Until the permanent brand and contact route are selected, label them as placeholders rather than inventing details.

## Recommended folder structure

```text
Agentic AI Automation Business
├── 00 - Project Index
├── 01 - Positioning and Offers
├── 02 - Capability Catalog
├── 03 - Sales and Marketing
├── 04 - Discovery and Audit
├── 05 - Proposals and Onboarding
├── 06 - Delivery and Operations
├── 07 - Security and Governance
├── 08 - Finance and ROI
├── 09 - Case Studies
└── 10 - Client Delivery
```

## Capability-catalog pattern

Organize pitches by business outcome, not tool name:

- Sales and lead management
- Customer service
- Marketing and local growth
- Administration
- Email and calendar
- Finance support with human control
- Recruiting and training
- Research and decision support
- Documents and knowledge
- Technical/digital operations
- Scheduled and event-triggered operations

Select only relevant capabilities for each prospect. Tie each to revenue, time, risk, or customer experience. Never imply unrestricted autonomous action.

## Security and human control

Always define least privilege, client separation, dedicated identities, secret storage, audit/reporting, failure behavior, duplicate prevention, budget limits, and shutdown procedures. Sensitive messages, public publishing, financial transfers, refunds, legal/medical/employment decisions, record deletion, and credential changes normally require explicit human approval.

## ROI model

Useful editable inputs:

- Occurrences per month
- Minutes per occurrence
- Loaded hourly labor cost
- Error/rework avoided
- Leads recovered
- Average customer gross profit
- Model/software cost
- Monthly management fee
- Setup fee

Calculate monthly labor value, recovered gross profit, net monthly value, first-year cost/value, payback months, and first-year ROI. Label examples as assumptions, not promises.

## Production workflow

1. Confirm target Google profile and verify Workspace identity.
2. Search for an existing exact root folder to avoid duplicates.
3. Create the root and numbered subfolders.
4. Create native Docs and Sheets in their final folders.
5. For automation scripts, derive the profile token from `HERMES_HOME` rather than embedding or printing credential paths; invoke with the intended profile’s `HERMES_HOME`.
6. Create the flier locally, render it, inspect clipping/contrast/alignment, revise, then upload it.
7. Read back a representative Doc, Sheet range/formulas, root metadata/owner, and flier parent/owner.
8. Keep files private until the user separately approves sharing permissions.
9. Report the canonical root URL and direct links to major assets.

## Drive Project distinction

A Drive folder and a Gemini Drive Project are different objects. Build the canonical folder/index through the Drive API. If the account has the Drive Projects UI, add the root folder as the Project source so future files remain included. Do not claim the UI Project exists unless it was verified in the signed-in account interface.
