# RuneLite Plugin Hub PR submission rules

Use this checklist when submitting plugins to `runelite/plugin-hub`.

## Submission isolation

- Each PR must add or update exactly one file under `plugins/<plugin-id>`.
- Each marker contains only the plugin repository URL and one immutable full commit SHA.
- Verify the live PR file list through `GET /repos/runelite/plugin-hub/pulls/{number}/files`; do not infer isolation from the PR title or local branch name.
- Run the plugin's clean Java 11 `test assemble` build before submission.

## One-open-PR-per-author rule

The repository may enforce only one open PR per author. This is separate from the one-plugin-per-PR rule: two individually correct plugin PRs can still conflict because they are both open under the same author.

Before opening or reopening a submission:

1. Search all open PRs authored by the account.
2. Choose the plugin priority with the user when more than one submission is pending.
3. Close the lower-priority open PR with a concise explanation before opening the priority PR.
4. Never combine two plugin markers to avoid the open-PR limit.
5. Preserve the deferred plugin branch and immutable child SHA for later resubmission.

## Closed PR that cannot reopen

A maintainer may close a PR to regenerate expired build artifacts, but repository rules can still reject reopening with HTTP 422. If the maintainer explicitly says to open a new submission:

1. Keep the old PR as review-history evidence.
2. Create a fresh branch from current upstream `master`, not a stale fork default branch.
3. Add only the one marker file.
4. Carry prior actionable review feedback and its resolved child SHA into the new PR body.
5. Verify the replacement PR's live file list contains exactly the expected marker.

Do not repeatedly retry reopening after a rule-driven 422; follow the maintainer's stated replacement path.

## Review surfaces and artifact refresh

Inspect issue comments, formal reviews, inline review comments, check runs, and PR state. Plugin Hub bot comments can identify the resolved child commit and whether a fresh build/reviewer pass is required. A green local build does not replace the official Plugin Hub build.

## Follow-up etiquette

- Keep comments concise, factual, and non-demanding.
- State the exact child SHA and verification performed when resolving feedback.
- Avoid repeated queue-check comments when no new action or evidence exists.
- If a submission is deferred due to the one-open-PR limit, say it will be reintroduced as its own PR after the priority plugin is resolved.
