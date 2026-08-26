# Plugin Hub single-submission sequencing

Use this when several RuneLite plugins are ready but Plugin Hub permits only one active submission for the author.

## Separate the two constraints

1. **One plugin per PR:** inspect the live PR file list. A correct Plugin Hub PR normally changes exactly one marker such as `plugins/<plugin-id>`.
2. **One open PR per author:** this is a queue/concurrency rule. Two separate one-marker PRs can each be structurally correct while still violating the open-PR limit.

Do not tell the user a PR contains two plugins unless the live changed-file list proves it. Read issue comments, reviews, inline comments, PR state, and files before acting.

## Priority and closure sequence

When the user explicitly prioritizes plugin A over plugin B:

1. Verify A’s child commit, prior technical feedback, branch existence, and marker diff.
2. Add a concise comment to B explaining it is being closed temporarily under the one-open-PR rule.
3. Close B.
4. Attempt to reopen A only if preserving its review history is useful.
5. If GitHub returns HTTP 422 or the maintainer requested a fresh submission, create a replacement branch from current upstream `master`; do not combine plugins.
6. Add exactly one marker and cite the earlier PR plus resolved feedback in the replacement body.
7. Verify the live PR file list is exactly `[plugins/<plugin-id>]`.
8. Reintroduce B as its own PR only after A is merged/closed.

Preserve an existing PR’s queue position by default, but explicit user priority overrides that default. Do not argue for preserving the lower-priority PR after the user has chosen the order.

## Feature submissions versus maintenance revisions

Treat completed-plugin maintenance updates (icon corrections, README-only changes, minor polish) as real marker-update PRs that consume the same one-open-PR-per-author slot.

When the user defines an ordered release train:

1. Record the full queue explicitly: current pending PR, next new plugin, then completed-plugin revisions.
2. Do not open a maintenance revision while a higher-priority new-plugin submission is pending or being finalized.
3. A child repository may receive and publish the approved maintenance commit early, but state clearly that the live Plugin Hub version remains pinned to the old SHA until its later marker-update PR merges.
4. After the current PR merges, finish and locally validate the next new plugin before submitting it; do not let already-prepared maintenance revisions jump the queue merely because their child SHAs exist.
5. Submit deferred maintenance revisions one at a time only after higher-priority feature/plugin work reaches the user-approved queue position.
6. Monitor only the currently open PR; keep deferred items as local task state rather than opening speculative branches/PRs.

This ordering is a workflow decision, not a technical readiness claim. A green child build does not authorize changing the user’s release priority.

## Reintroducing the deferred PR after the priority PR merges

When plugin A merges and plugin B was closed only for sequencing:

1. Verify A is truly `merged=true`, its official build succeeded, and its PR changed one marker.
2. Retire A's monitor so a completed submission is not polled forever.
3. Move A's child repo from `pr-review-pending/` to `completed/` and advance the parent gitlink to the exact accepted child SHA.
4. Inspect every feedback surface on B's old PR. Distinguish a sequencing closure from maintainer-requested changes.
5. Attempt to reopen B's original PR first. A successful reopen preserves review history and is preferable to creating a duplicate.
6. If reopened, do not assume its old Plugin Hub branch is current. Rebuild the branch from current upstream `master`, recreate exactly one marker pinned to B's latest tested child SHA, and push with `--force-with-lease=<branch>:<observed-old-sha>`.
7. Verify the live PR file list is exactly one marker, wait for the official `build` check, and inspect issue comments, reviews, and inline comments again.
8. Post at most one concise status note explaining that A merged, B was reopened, the branch was refreshed from current upstream, and local plus official builds are green.
9. Start a low-noise monitor for B; silence it unless feedback is actionable or the PR merges.

Never force-push from an unverified stale local branch. Resolve and pin the observed remote branch SHA first so `--force-with-lease` protects concurrent changes.

## Immutable child SHA update loop

For any child change after submission, including README-only documentation:

1. Inspect source and make the child change.
2. Run appropriate validation; documentation-only changes still need `git diff --check`, while code changes need the Java 11 clean build.
3. Commit and push the child first.
4. Update only `commit=<full-child-sha>` in the Plugin Hub marker branch.
5. Commit and push the marker update.
6. Read back the live PR files and marker content; confirm no second plugin entered the PR.
7. Recheck the official Plugin Hub build and every feedback surface.

## Documenting network/API usage

When asked what APIs a plugin contacts, inspect actual HTTP clients, URL constants, request builders, and browser-open links. Distinguish:

- external API endpoints actually called;
- public web pages merely opened on click;
- local RuneLite Client API integrations that are not network requests;
- build dependencies that are not contacted services.

README documentation should state endpoint families, purpose, HTTP behavior, fallback behavior, and whether the plugin has a custom backend, authentication/API keys, uploads, or telemetry. Never infer “no telemetry” from dependencies alone—search the source.
