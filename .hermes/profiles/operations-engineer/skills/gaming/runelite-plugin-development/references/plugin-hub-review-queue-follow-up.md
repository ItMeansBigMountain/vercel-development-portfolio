# Plugin Hub review-queue follow-up

Use this after an upstream RuneLite Plugin Hub PR has a successful official `build` check but remains at `Requires maintainer review`.

## First verify that the author is not blocking review

Inspect all current surfaces before posting:

1. Issue comments: `GET /repos/runelite/plugin-hub/issues/{pr}/comments`
2. Formal reviews: `GET /repos/runelite/plugin-hub/pulls/{pr}/reviews`
3. Inline comments: `GET /repos/runelite/plugin-hub/pulls/{pr}/comments`
4. Check runs for the PR head SHA
5. Labels and assignees from `GET /repos/runelite/plugin-hub/issues/{pr}`

Do not follow up when the PR has `waiting for author`, `build failed`, requested changes, or an unanswered maintainer question. Resolve those in the existing PR first.

## Preserve the original PR

RuneLite's contributor guide asks authors to keep corrections in one PR and be patient for review. Never close and re-upload merely to regain attention. A replacement PR loses review history, duplicates notifications, and can look like queue manipulation.

Update the pinned plugin SHA on the existing marker branch when code changes. Keep one plugin marker per PR.

## Low-noise escalation

- New green PR: wait; the red Plugin Hub policy check titled `Requires maintainer review` is expected.
- After a reasonable quiet period, use one polite queue-check. Do not repeatedly bump the thread.
- Prefer the RuneLite Discord's appropriate public plugin-development/support channel for a combined queue check when several PRs are waiting.
- Never use or share bot links labeled `Internal use only`, and do not ping individual maintainers unless they invited it.
- If Discord is unavailable or gives no clarification, add one concise comment to each existing PR, then wait for a response.
- Tailor the single follow-up to the actual review gate. If a maintainer named a concern such as file I/O, acknowledge that the requested context was provided, invite concrete changes, and state that the author can respond promptly. Do not merely say “bump,” ask for expedited treatment, or imply entitlement to completion.

Suggested new-plugin comment:

```text
Friendly review-queue check: the official build is green, and I do not see any outstanding author actions. Please let me know if additional information or changes would help with review. Thanks!
```

Suggested re-review comment:

```text
Friendly re-review check: the requested change was addressed in plugin commit `<full SHA>`, and the official build is green. Please let me know if anything else is needed. Thanks!
```

## Posting safely through GitHub API

Before POSTing, read comments again to avoid writing over a fresh maintainer response. Then create an issue comment:

```text
POST /repos/runelite/plugin-hub/issues/{pr}/comments
{"body":"..."}
```

Verify the returned `html_url`, comment ID, author login, and exact body before reporting success.

## Reporting status

Clearly distinguish:

- `build=success`: official packaging passed.
- `Requires maintainer review`: waiting on humans, not a code failure.
- `waiting for author` or requested changes: author action required.
- merged: complete.

Report the direct PR and follow-up-comment URLs. Do not promise that a bump will accelerate review.
