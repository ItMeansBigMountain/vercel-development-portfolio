---
name: google-workspace
description: "Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python."
version: 1.1.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials (downloaded from Google Cloud Console)
metadata:
  hermes:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, Email, OAuth]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [himalaya]
---

# Google Workspace Skill

## YouTube OAuth / upload tokens

On this user's workspace, use the unified helper `/opt/data/scripts/google_reauth_workflow.py` for repeatable reauth across Google Workspace profile tokens and YouTube channel upload tokens. It inventories profiles, generates fresh profile-scoped PKCE auth URLs, exchanges labeled localhost callbacks, and verifies harmless live probes without printing secrets. Examples: `python3 /opt/data/scripts/google_reauth_workflow.py inventory`, `workspace-auth-url personal-secondary`, `youtube-auth-url classicalechos`, `workspace-exchange <profile> '<callback>'`, `youtube-exchange <profile> '<callback>'`, `verify workspace <profile>`, `verify youtube <profile>`.

When reauthing YouTube upload automation, see `references/youtube-oauth-callback-exchange.md` for the callback exchange pattern, scope set, localhost `OAUTHLIB_INSECURE_TRANSPORT=*** pitfall, channel identity verification, and explicit-token uploader check. After a token verifies, replay the actual failing cron/script and inspect its `YOUTUBE_UPLOAD_TOKEN` default/env propagation; a stale script default can keep producing `invalid_grant` against a different channel token even though the freshly reauthed token is valid.

For YouTube downloader/source-acquisition login errors (`Sign in to confirm you're not a bot`, `LOGIN_REQUIRED`, pytubefix `BotDetection`), this user's current workflow is device login with the **Classical Echos** account, not normal YouTube upload OAuth. Use `social-video-cron-growth-loop/references/youtube-device-login-reauth-workflow.md`; cached token path is `/opt/data/secrets/pytubefix-classical-echos/tokens.json`, and Viral Radar should download with pytubefix OAuth (`--no-ytdlp --try-pytubefix --oauth --pytubefix-client WEB`).

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — through Hermes-managed OAuth and a thin CLI wrapper. When `gws` is installed, the skill uses it as the execution backend for broader Google Workspace coverage; otherwise it falls back to the bundled Python client implementation.

## References

- `references/gmail-search-syntax.md` — Gmail search operators (is:unread, from:, newer_than:, etc.)
- `references/gmail-inbox-audit-and-cleanup.md` — multi-profile Gmail Inbox audit/cleanup pattern, exact Inbox counting via `labelIds=['INBOX']`, approval-first cleanup workflow, and current user email triage policy.
- `references/gmail-email-sorting-agent-rules.md` — Hermes-level deterministic Gmail sorting rules and labels, including the Robinhood account-vs-Robinhood Snacks newsletter split.
- `references/email-sorting-expanded-profile-scan-2026-07.md` — current expanded email-sort/review coverage across readable profiles, full scan verification, and affan.fareed@gmail.com Inbox review guidance.
- `references/email-sorting-full-scan-and-profile-expansion-2026-07.md` — Full-scan/profile-expansion workflow for adding all readable Google email accounts to the deterministic sorter, excluding stale aliases and revoked tokens.
- `references/gmail-cron-auth-block-resilience.md` — Pattern for multi-profile Gmail cron jobs: catch per-profile auth/scope failures, continue healthy profiles, report structured `blocked` statuses, and avoid misleading traceback-only cron errors.
- `references/junk-cleanup-newsletter-deletion-boundary.md` — user-specific boundary: known junk/spam cleanup is pre-approved, but newsletter/source emails are deleted only after use/verified YouTube upload.
- `references/gmail-personal-cleanup-routing-2026-06-29.md` — personal Gmail full-permission policy, confirmed junk senders, Robinhood/Zoom/Grammarly routing rules, and duplicate-newsletter handling across `affan.fareed@gmail.com` and `fareed320@gmail.com`.
- `references/personal-email-cleanup-routing-2026-06.md` — current personal Gmail cleanup/routing policy: both personal accounts have full Workspace write access, Robinhood/Zoom routing labels, Grammarly personal-info hold, affan-vs-fareed320 duplicate newsletter handling, and verification steps.
- `references/gmail-inbox-audit-pattern.md` — read-only Gmail inbox/subscription audit workflow, real Inbox counting pattern, classification/reporting guidance, and destructive-action confirmation rules.
- `references/calendar-service-account.md` — service-account setup for Calendar automation when the user shares calendars with the service account.
- `references/credential-requirements.md` — required Google credential files and setup verification
- `references/google-credential-inventory-pattern.md` — safe workflow for inventorying Google credential files by project/purpose without exposing secrets
- `references/durable-google-secret-storage.md` — durable non-git storage pattern for Google secrets/tokens with env path references, permission locking, git untracking, and verification
- `references/google-project-api-permissions-probe.md` — safe command/API probe pattern for producing enabled-API and permission/access tables per Google project
- `references/drive-service-account-cache.md` — Drive-backed cache pattern for service-account writable folders/Shared Drives, MP4 backup manifests, and safe local deletion after confirmed upload
- `references/drive-cache-memory-extension.md` — Google Drive as a durable Hermes cache / memory-extension pattern, including OAuth vs service-account pitfalls
- `references/drive-projects-curriculum-knowledge-base.md` — Build a canonical Drive folder/index, comprehensively rebrand native and uploaded artifacts, add the root as a Gemini Drive Project source, and verify the distinction between a folder and a Project.
- `references/multi-profile-google-oauth.md` — Profile-scoped OAuth for managing multiple Gmail/Workspace identities with separate tokens, PKCE pending state, action policies, browser/redirect pitfalls, and smoke tests.
- `references/profile-oauth-batch-callback-exchange.md` — Batch exchange pattern when the user returns multiple `localhost` callback URLs in one message/file; includes exact helper commands, live probes, and the pitfall of refreshing with ungranted scope supersets.
- `references/google-oauth-scope-reauth-matrix.md` — Decide whether enabling additional Google APIs requires OAuth reauth; includes Workspace baseline scopes, YouTube upload/private-data scope guidance, API-key distinction, and verification probes.
- `references/youtube-oauth-callback-exchange.md` — User-specific YouTube reauth repair: full upload/metadata/read/analytics scope set, profile-specific pending files, and channel identity verification after exchange.
- `references/recurring-oauth-health-and-callback-batch.md` — Recurring Google/YouTube auth health workflow: verify Workspace and YouTube lanes separately, generate fresh labeled callback URLs, require channel identity checks, and make dependent crons report structured blocked statuses instead of misleading OKs.
- `references/shared-oauth-token-scope-preservation.md` — Diagnose scope collapse caused by narrow consumers overwriting shared tokens; repair from existing broad refresh grants before reauthorizing, enforce canonical lane scope unions, atomic exchange, strict live verification, and realistic persistence limits.
- `references/google-oauth-durable-reauth-handoff-2026-06.md` — Current pattern for generating all Workspace/YouTube OAuth URLs, explaining long-lived refresh-token limits from Google docs, and saving a persistent non-secret handoff file with find/regenerate/exchange/verify commands.
- `references/auth-error-triage-batch-reauth-2026-06.md` — When the user asks to look back at auth errors, combine session-history recovery with live `google_reauth_workflow.py` inventory/verify probes, regenerate fresh labeled callback bundles, and verify account/channel identity before replaying blocked jobs.
- `references/replay-failed-google-cron-runs-after-reauth.md` — After OAuth repair, search history for affected jobs/scripts, rerun each failed attempt one by one, make multi-profile jobs skip/report blocked profiles instead of crashing, and distinguish scheduler OK from product success.
- `references/user-google-account-scope-map-2026-06.md` — User-specific account aliases, full/read-only scope policy, mass OAuth refresh workflow, and Discord bullet-format reporting preference.
- `references/personal-main-invalid-scope-repair-2026-06.md` — Legacy repair pattern for `personal-main` / `affan.fareed@gmail.com`; superseded for current scope policy by full Workspace read/write permission including Gmail read/modify/send.
- `references/personal-main-readonly-reauth.md` — Legacy filename; current content covers repairing `personal-main` / `affan.fareed@gmail.com` by generating full Workspace OAuth URLs and verifying live identity.

## Scripts

- `scripts/setup.py` — OAuth2 setup (run once to authorize)
- `scripts/google_api.py` — compatibility wrapper CLI. It prefers `gws` for operations when available, while preserving Hermes' existing JSON output contract.

### Multi-account / profile-scoped OAuth

When the user wants Hermes to manage multiple Gmail or Google Workspace accounts, do **not** run the single-token setup repeatedly into `google_token.json`; that overwrites the previous account. Use the profile-scoped pattern in `references/multi-profile-google-oauth.md`: maintain a profile registry, generate one auth URL per profile with `login_hint`, store pending PKCE state separately per profile, exchange callbacks as `<profile>: <redirect URL>`, and save tokens under `/opt/data/google_profiles/<profile>/google_token.json` (or the profile-specific equivalent). Make users confirm the consent-screen email because `login_hint` is not an account lock. For this user's current account map and scope policy, load `references/user-google-account-scope-map-2026-06.md` and `references/user-google-oauth-account-map-2026-06.md` before generating URLs; if registry entries, memory, and reference docs disagree, reconcile to the latest explicit user instruction and report the conflict. For durable/no-manual-expiration OAuth, generate each profile URL with `access_type=offline` and `prompt=consent` so Google issues a refresh token; explain that Google may still revoke/expire tokens for security, testing-mode, or inactivity reasons. For read-only daily briefing use cases, prefer a pre-run collector script that reads each named token, summarizes Gmail/Calendar/Drive signals, strips invisible Gmail tracking characters, and hides credential/recovery-looking Drive filenames before the LLM sees the context.

### Service-account Calendar route

If the user provides a Google Cloud **service-account JSON** and wants Calendar automation without personal OAuth, use the service-account route in `references/calendar-service-account.md` instead of the OAuth setup below. Save the JSON as a credentials file with mode `600`, set `GOOGLE_APPLICATION_CREDENTIALS` in the Hermes env file, and have the user share the target calendar with the service account's `client_email`. A successful auth check may still show zero calendars until the user shares a calendar. Continue to use personal OAuth for Gmail/Drive/Docs/Sheets as a Google user, or when the user wants Hermes to act exactly as their account.

### Credential inventory and project organization

When the user asks to find, identify, or organize Google credentials across the workspace, use `references/google-credential-inventory-pattern.md`. Inventory only safe metadata: path, credential type, project ID, service-account email or redacted OAuth client ID, file mode, duplicate paths, active env references, and known purpose. Never paste private keys, client secrets, access tokens, refresh tokens, or full API keys into docs or chat. Group duplicate credentials by project/principal, tighten credential file modes to `600` when safe, and do not move/delete/rename credentials until env/app references are updated in the same change.

When the user wants credentials to survive VPS/container restarts without being backed up by Git, use `references/durable-google-secret-storage.md`: copy credentials into a persistent non-repo secrets tree, expose only stable path references through `.env`, lock modes to `700`/`600`, update `.gitignore`, remove any already-tracked credential files with `git rm --cached --force`, verify with `git ls-files` and `git check-ignore --no-index`, and remind the user that untracking does not erase old Git history if secrets were previously pushed.

When the user asks to repair `personal-main` / `affan.fareed@gmail.com` OAuth, especially expired/revoked tokens or missing scopes, load `references/personal-main-readonly-reauth.md` (legacy filename; content now documents full access). Generate a profile-scoped URL for the full Workspace bundle including Gmail read/modify/send, keep pending PKCE state isolated under `/opt/data/google_profiles/personal-main/`, and verify the returned Gmail profile email before reporting the main account context as restored.

When the user wants Hermes to manage multiple Gmail/Google Workspace accounts as separate internet identities or project lanes, use `references/multiple-google-account-profiles.md
  - path: references/user-google-account-scope-map-2026-06.md
    description: User-specific account aliases, scope policy, and content automation account split.`. Keep each account isolated with a named credential directory and a per-command `HERMES_HOME` override; maintain a non-secret profile inventory under the user's workspace; never mix tokens between identities.

When the user asks for enabled APIs, permissions, or a table of Google projects, use `references/google-project-api-permissions-probe.md`. Actively run safe read-only probes instead of guessing from credential filenames: Service Usage for enabled APIs, Cloud Resource Manager/IAM policy where available, and harmless product endpoint probes for Calendar, Drive, Gmail, Sheets, Docs, and YouTube. If the user explicitly asks for a table, provide a compact Markdown table even if the user's normal Discord preference is bullet-style replies.

When the user enables additional Google APIs and asks whether OAuth must be redone, use `references/google-oauth-scope-reauth-matrix.md`. Key rule: API enablement is project-side, OAuth scopes are token-side. If the token already has the needed scope, just smoke-test again; if the action needs a new scope (for example YouTube upload), generate fresh OAuth URLs and reauth the relevant profile(s).

Keep Google Workspace service-account credentials separate from YouTube OAuth credentials: Workspace/personal-assistant automation can use service accounts when resources are shared/delegated, while YouTube channel uploads/analytics/private reads generally require user OAuth. Public YouTube metadata reads may use an API key or service-account credential when `youtube.googleapis.com` is enabled for the project; verify with a live `videos?chart=mostPopular` probe before reporting readiness.

### Drive service-account cache route

When the user wants Hermes to use Google Drive as durable cache/backing storage for generated files, especially MP4s, use `references/drive-service-account-cache.md`. Important pitfall: service accounts do not have normal personal Drive storage quota, so uploads to service-account-owned My Drive can fail even when auth works. Prefer a service-account-writable Shared Drive or shared folder ID, set it as the Drive cache parent, pass `supportsAllDrives=True` / `includeItemsFromAllDrives=True`, and delete local media only after Drive confirms the upload and a manifest has been written.

## First-Time Setup

The setup is fully non-interactive — you drive it step by step so it works
on CLI, Telegram, Discord, or any platform.

Define a shorthand first:

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"
```

### Step 0: Check if already set up

```bash
$GSETUP --check
```

If it prints `AUTHENTICATED`, skip to Usage — setup is already done.

### Step 1: Triage — ask the user what they need

Before starting OAuth setup, ask the user TWO questions:

**Question 1: "What Google services do you need? Just email, or also
Calendar/Drive/Sheets/Docs?"**

- **Email only** → They don't need this skill at all. Use the `himalaya` skill
  instead — it works with a Gmail App Password (Settings → Security → App
  Passwords) and takes 2 minutes to set up. No Google Cloud project needed.
  Load the himalaya skill and follow its setup instructions.

- **Email + Calendar** → Continue with this skill, but use
  `--services email,calendar` during auth so the consent screen only asks for
  the scopes they actually need.

- **Calendar/Drive/Sheets/Docs only** → Continue with this skill and use a
  narrower `--services` set like `calendar,drive,sheets,docs`.

- **Full Workspace access** → Continue with this skill and use the default
  `all` service set.

**Question 2: "Does your Google account use Advanced Protection (hardware
security keys required to sign in)? If you're not sure, you probably don't
— it's something you would have explicitly enrolled in."**

- **No / Not sure** → Normal setup. Continue below.
- **Yes** → Their Workspace admin must add the OAuth client ID to the org's
  allowed apps list before Step 4 will work. Let them know upfront.

### Step 2: Create OAuth credentials (one-time, ~5 minutes)

Tell the user:

> You need a Google Cloud OAuth client. This is a one-time setup:
>
> 1. Create or select a project:
>    https://console.cloud.google.com/projectselector2/home/dashboard
> 2. Enable the required APIs from the API Library:
>    https://console.cloud.google.com/apis/library
>    Enable: Gmail API, Google Calendar API, Google Drive API,
>    Google Sheets API, Google Docs API, People API
> 3. Create the OAuth client here:
>    https://console.cloud.google.com/apis/credentials
>    Credentials → Create Credentials → OAuth 2.0 Client ID
> 4. Application type: "Desktop app" → Create
> 5. If the app is still in Testing, add the user's Google account as a test user here:
>    https://console.cloud.google.com/auth/audience
>    Audience → Test users → Add users
> 6. Download the JSON file and tell me the file path
>
> Important Hermes CLI note: if the file path starts with `/`, do NOT send only the bare path as its own message in the CLI, because it can be mistaken for a slash command. Send it in a sentence instead, like:
> `The JSON file path is: /home/user/Downloads/client_secret_....json`

Once they provide the path:

```bash
$GSETUP --client-secret /path/to/client_secret.json
```

If they paste the raw client ID / client secret values instead of a file path,
write a valid Desktop OAuth JSON file for them yourself, save it somewhere
explicit (for example `~/Downloads/hermes-google-client-secret.json`), then run
`--client-secret` against that file.

### Step 3: Get authorization URL

Use the service set chosen in Step 1. Examples:

```bash
$GSETUP --auth-url
```

On this installation, the setup script emits the exact authorization URL as plain text and requests the full Workspace scope set by default: Gmail read/send/modify, Calendar, Drive, Contacts readonly, Sheets, and Docs. It does not currently support `--services` or `--format` flags.

Agent rules for this step:
Agent rules for this step:
- Send that exact URL to the user as a single line.
- For Discord/chat users, paste every generated OAuth URL directly in the chat. Do not only save them to a VPS file or tell the user to open a file on the server; they may not access VPS files. A saved handoff file is fine as a backup, but the actionable URLs must be returned in-chat.
- Tell the user that the browser will likely fail on `http://localhost:1` after approval, and that this is expected.
- Tell them to copy the ENTIRE redirected URL from the browser address bar.
- If the user gets `Error 403: access_denied`, send them directly to `https://console.cloud.google.com/auth/audience` to add themselves as a test user.

### Step 4: Exchange the code

The user will paste back either a URL like `http://localhost:1/?code=4/0A...&scope=...`
or just the code string. Either works. The `--auth-url` step stores a temporary
pending OAuth session locally so `--auth-code` can complete the PKCE exchange
later, even on headless systems:

```bash
$GSETUP --auth-code "THE_URL_OR_CODE_THE_USER_PASTED" --format json
```

**Headless callback handoff rule:** when the browser cannot reach a localhost
callback on the Hermes host, have the user paste the entire callback URL. For
Google's `http://localhost:1` flow, pass that URL directly to `--auth-code` (do
not try to browse to port 1). For any future Google flow that starts a real
loopback callback listener, forward the pasted URL to that active listener
only after validating its `state` against the pending OAuth session. Never log,
repeat, or retain the one-time authorization code after exchange.

If `--auth-code` fails because the code expired, was already used, or came from
an older browser tab, it now returns a fresh `fresh_auth_url`. In that case,
immediately send the new URL to the user and have them retry with the newest
browser redirect only.

### Step 5: Verify

```bash
$GSETUP --check
```

Should print `AUTHENTICATED`. Setup is complete — token refreshes automatically from now on.

### Notes

- Token is stored at `~/.hermes/google_token.json` and auto-refreshes.
- Pending OAuth session state/verifier are stored temporarily at `~/.hermes/google_oauth_pending.json` until exchange completes.
- If `gws` is installed, `google_api.py` points it at the same `~/.hermes/google_token.json` credentials file. Users do not need to run a separate `gws auth login` flow.
- A Google AI Studio / Gemini API key (`GOOGLE_API_KEY` or `GEMINI_API_KEY`) is **not** enough for private Google Workspace data. It can call some Google APIs only where API-key auth is supported (for example public calendar data), and the target API must be enabled in the Google Cloud project. Personal Gmail/Calendar/Drive/Docs/Sheets actions require OAuth with a Desktop OAuth client JSON plus the user approval flow above.
- To revoke: `$GSETUP --revoke`

## Usage

All commands go through the API script. Set `GAPI` as a shorthand:

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
```

### Gmail

```bash
# Search (returns JSON array with id, from, subject, date, snippet)
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail search "has:attachment filename:pdf newer_than:7d"

# Read full message (returns JSON with body text)
$GAPI gmail get MESSAGE_ID

# Send
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1><p>Details...</p>" --html
$GAPI gmail send --to user@example.com --subject "Hello" --from '"Research Agent" <user@example.com>' --body "Message text"

# Reply (automatically threads and sets In-Reply-To)
$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
$GAPI gmail reply MESSAGE_ID --from '"Support Bot" <user@example.com>' --body "Thanks"

# Labels
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
```

#### User-specific Gmail routing/cleanup rules

For this user's personal Gmail cleanup and routing, load `references/user-gmail-routing-cleanup-rules.md` before modifying labels or trashing messages. It covers full Gmail permissions for both personal accounts, Grammarly personal-information handling, Robinhood/Zoom routing, and duplicate newsletter cleanup from `affan.fareed@gmail.com`.

#### Recurring Gmail sorting reports

When a recurring email sorter modifies messages, its user-facing report must be auditable rather than count-only. Group results by the named Google Workspace profile **and full account email address**, then list every sorted message with at least:

- subject (or `(no subject)`),
- sender/from header (or `Unknown sender`), and
- destination label.

A compact preferred shape is:

```text
**personal-main — affan.fareed@gmail.com** (2 sorted)
- **Message subject** — Sender <sender@example.com> → `Hermes/Newsletters`
```

Keep the total count as a summary, but never use profile counts as a substitute for the per-message list. If a profile is blocked, continue healthy profiles and report the blocked profile with both its profile name and account email address.

For `no_agent` cron jobs, remember that delivery is the script's stdout verbatim: update and verify the formatter in the script itself rather than only changing the cron prompt. Prefer consuming the sorter's structured JSON (`email`, `matches[].subject`, `matches[].from`, `matches[].label`) and run both a shell syntax check and a small synthetic-format fixture before considering the change complete. Do not rerun an `--apply` sorter merely to test report formatting, because that can cause unintended additional mailbox changes.

#### Gmail audits and subscription cleanup

When auditing email, subscriptions, billing notices, newsletters, or junk mail, use the read-only workflows in `references/gmail-inbox-audit-and-cleanup.md` and `references/gmail-inbox-audit-pattern.md` before proposing cleanup. Key rules:

- Audit first; do not delete, spam-report, archive, unsubscribe, or modify labels during discovery.
- For multi-profile setups under `/opt/data/google_profiles/<profile>/google_token.json`, iterate each profile and use harmless Gmail probes (`users.getProfile`, `labels.list`, metadata-only message reads).
- Count the *actual Inbox* by iterating `messages.list(labelIds=["INBOX"])`; do not treat `users.getProfile().messagesTotal` or broad `resultSizeEstimate` as Inbox counts.
- Classify results as: confirmed important/priority, interesting or morning-report source, known junk, likely junk/consumer marketing, and needs review.
- Broad keyword searches can false-positive on newsletter text; follow up high-value categories with exact `from:` probes before reporting them as important.
- Before any cleanup, show the exact account/profile, sender, message count, proposed action, and examples for approval.

### Calendar

```bash
# List events (defaults to next 7 days)
$GAPI calendar list
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

# Create event (ISO 8601 with timezone required)
$GAPI calendar create --summary "Team Standup" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar create --summary "Lunch" --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z --location "Cafe"
$GAPI calendar create --summary "Review" --start 2026-03-01T14:00:00Z --end 2026-03-01T15:00:00Z --attendees "alice@co.com,bob@co.com"

# Delete event
$GAPI calendar delete EVENT_ID
```

### Drive

```bash
# Search existing files
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5

# Get metadata for a single file
$GAPI drive get FILE_ID

# Upload a local file (auto-detects MIME type)
$GAPI drive upload /path/to/report.pdf
$GAPI drive upload /path/to/image.png --name "Logo.png" --parent FOLDER_ID

# Download (binary files download as-is; Google-native files export to a
# sensible default — Docs→pdf, Sheets→csv, Slides→pdf, Drawings→png)
$GAPI drive download FILE_ID
$GAPI drive download DOC_ID --output ~/doc.pdf
$GAPI drive download DOC_ID --export-mime text/plain --output ~/doc.txt

# Create a folder
$GAPI drive create-folder "Reports"
$GAPI drive create-folder "Q4" --parent FOLDER_ID

# Share
$GAPI drive share FILE_ID --email alice@example.com --role reader
$GAPI drive share FILE_ID --email alice@example.com --role writer --notify
$GAPI drive share FILE_ID --type anyone --role reader        # anyone with link
$GAPI drive share FILE_ID --type domain --domain example.com --role reader

# Delete — defaults to trash (reversible). Use --permanent to skip the trash.
$GAPI drive delete FILE_ID
$GAPI drive delete FILE_ID --permanent
```

### Contacts

```bash
$GAPI contacts list --max 20
```

### Sheets

```bash
# Create a new spreadsheet
$GAPI sheets create --title "Q4 Budget"
$GAPI sheets create --title "Inventory" --sheet-name "Stock"

# Read
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"

# Write
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# Append rows
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

### Docs

```bash
# Read
$GAPI docs get DOC_ID

# Create a new Doc (optionally seeded with body text)
$GAPI docs create --title "Meeting Notes"
$GAPI docs create --title "Draft" --body "First paragraph..."

# Append text to the end of an existing Doc
$GAPI docs append DOC_ID --text "Additional content to append"
```

## Output Format

All commands return JSON. Parse with `jq` or read directly. Key fields:

- **Gmail search**: `[{id, threadId, from, to, subject, date, snippet, labels}]`
- **Gmail get**: `{id, threadId, from, to, subject, date, labels, body}`
- **Gmail send/reply**: `{status: "sent", id, threadId}`
- **Calendar list**: `[{id, summary, start, end, location, description, htmlLink}]`
- **Calendar create**: `{status: "created", id, summary, htmlLink}`
- **Drive search**: `[{id, name, mimeType, modifiedTime, webViewLink}]`
- **Drive get**: `{id, name, mimeType, modifiedTime, size, webViewLink, parents, owners}`
- **Drive upload**: `{status: "uploaded", id, name, mimeType, webViewLink}`
- **Drive download**: `{status: "downloaded", id, name, path, mimeType}`
- **Drive create-folder**: `{status: "created", id, name, webViewLink}`
- **Drive share**: `{status: "shared", permissionId, fileId, role, type}`
- **Drive delete**: `{status: "trashed" | "deleted", fileId, permanent}`
- **Contacts list**: `[{name, emails: [...], phones: [...]}]`
- **Sheets get**: `[[cell, cell, ...], ...]`
- **Sheets create**: `{status: "created", spreadsheetId, title, spreadsheetUrl}`
- **Docs create**: `{status: "created", documentId, title, url}`
- **Docs append**: `{status: "appended", documentId, inserted_at, characters}`

## Rules

- **Never perform destructive actions (delete, trash, label as spam, unsubscribe) without explicit user approval.**
- **When multiple OAuth profile tokens exist, always prompt the user to select the target profile before any Gmail/Calendar/Drive operation.**

1. **Never send email, create/delete calendar events, delete Drive files, share files, or modify Docs/Sheets without confirming with the user first.** Show what will be done (recipients, file IDs, content, share role) and ask for approval. For `drive delete`, prefer the default trash (reversible) over `--permanent`.
2. **Check auth before first use** — run `setup.py --check`. If it fails, guide the user through setup.
3. **Use the Gmail search syntax reference** for complex queries — load it with `skill_view("google-workspace", file_path="references/gmail-search-syntax.md")`.
4. **Calendar times must include timezone** — always use ISO 8601 with offset (e.g., `2026-03-01T10:00:00-06:00`) or UTC (`Z`).
5. **Respect rate limits** — avoid rapid-fire sequential API calls. Batch reads when possible.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup Steps 2-5 above |
| `REFRESH_FAILED` | Token revoked or expired — redo Steps 3-5 |
| `HttpError 403: Insufficient Permission` | Missing API scope — `$GSETUP --revoke` then redo Steps 3-5 |
| `AUTHENTICATED (partial)` or "Token missing scopes" | New write capabilities (Drive write/delete, Docs create/edit) require re-authorization. `$GSETUP --revoke` then redo Steps 3-5 to grant the upgraded scopes. |
| `calendar_count: 0` after service-account auth | Auth works, but no calendars have been shared with the service account yet. Share the target calendar with the service account `client_email`; see `references/calendar-service-account.md`. |
| `HttpError 403: Access Not Configured` | API not enabled — user needs to enable it in Google Cloud Console |
| `ModuleNotFoundError` | Run `$GSETUP --install-deps` |
| Advanced Protection blocks auth | Workspace admin must allowlist the OAuth client ID |
| Redirect URI mismatch           | Ensure `redirect_uri` in token exchange exactly matches one of the URIs registered in Google Cloud Console (check `client_secret.json`). |
| Invalid grant                   | Authorization code expired or already used; generate a fresh auth URL and obtain a new code from the browser. |

## Revoking Access

```bash
$GSETUP --revoke
```
