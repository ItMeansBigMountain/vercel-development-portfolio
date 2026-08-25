---
name: kanban-orchestrator
description: Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. The "don't do the work yourself" rule and the basic lifecycle are auto-injected into every kanban worker's system prompt; this skill is the deeper playbook when you're specifically playing the orchestrator role.
version: 3.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing]
    related_skills: [kanban-worker]
---

# Kanban Orchestrator — Decomposition Playbook

> The **core worker lifecycle** (including the `kanban_create` fan-out pattern and the "decompose, don't execute" rule) is auto-injected into every kanban process via the `KANBAN_GUIDANCE` system-prompt block. This skill is the deeper playbook when you're an orchestrator profile whose whole job is routing.

## Profiles are user-configured — not a fixed roster

Hermes setups vary widely. Some users run a single profile that does everything; some run a small fleet (`docker-worker`, `cron-worker`); some run a curated specialist team they've named themselves. There is **no default specialist roster** — the orchestrator skill does not know what profiles exist on this machine.

Before fanning out, you must ground the decomposition in the profiles that actually exist. The dispatcher silently fails to spawn unknown assignee names — it doesn't autocorrect, doesn't suggest, doesn't fall back. So a card assigned to `researcher` on a setup that only has `docker-worker` just sits in `ready` forever.

**Step 0: discover available profiles before planning.**

Use one of these:

- `hermes profile list` — prints the table of profiles configured on this machine. Run it through your terminal tool if you have one; otherwise ask the user.
- `kanban_list(assignee="<some-name>")` — sanity-check a single name. Returns an empty list (rather than an error) for an unknown assignee, so this only confirms a name you're already considering.
- **Just ask the user.** "What profiles do you have set up?" is a fine first turn when the goal needs more than one specialist.

Cache the result in your working memory for the rest of the conversation. Re-asking every turn wastes a tool call.

## When to use the board (vs. just doing the work)

Create Kanban tasks when any of these are true:

1. **Multiple specialists are needed.** Research + analysis + writing is three profiles.
2. **The work should survive a crash or restart.** Long-running, recurring, or important.
3. **The user might want to interject.** Human-in-the-loop at any step.
4. **Multiple subtasks can run in parallel.** Fan-out for speed.
5. **Review / iteration is expected.** A reviewer profile loops on drafter output.
6. **The audit trail matters.** Board rows persist in SQLite forever.

If *none* of those apply — it's a small one-shot reasoning task — use `delegate_task` instead or answer the user directly.

### Turning Kanban from passive to active

When the user says they want to actively start using Kanban for a workspace, do more than explain the feature:

1. Switch or confirm the intended workspace board as active (`hermes kanban boards switch <slug>`), then verify with an explicit `HERMES_KANBAN_BOARD=<slug> hermes kanban boards current` call if the current session may be env-pinned to another board.
2. Discover valid assignees with `hermes profile list` and `hermes kanban assignees`; summarize only real profile names.
3. Confirm dispatcher readiness (`kanban.dispatch_in_gateway`, gateway status, diagnostics) so ready cards will actually be picked up.
4. Create at least one low-risk intake/triage card for the next likely workflow instead of leaving the board empty. Use `--triage` when the user has not yet approved a concrete worker task.
5. If the workspace is Git-backed, update its Kanban operating note (for example `KANBAN.md`) with the active board slug, assignees, dispatcher behavior, and env-pin caveat, then commit/push that documentation.
6. Tell the user the new operating convention: future multi-step work gets a durable card, simple one-offs stay in chat.

### Consolidating boards back to one default board

When a user decides they do not want multiple boards or demo boards, consolidate deliberately instead of just deleting slugs:

1. Audit first: `hermes kanban boards list`, then list each non-default board with `HERMES_KANBAN_BOARD=<slug> hermes kanban list` so you know what will be preserved or discarded.
2. Create a pre-change backup under the user's project backup area when one exists. Copy `/opt/data/kanban.db` plus the relevant `/opt/data/kanban/boards/<slug>/` directories before destructive changes. If the user explicitly says demo boards are not needed, omit or prune bulky demo workspaces from the retained backup.
3. If the canonical target is `default`, copy the keeper board's SQLite DB into `/opt/data/kanban.db` using SQLite's backup API rather than a blind copy while processes may be active. Also carry over useful `logs/` and `workspaces/` from the keeper board to `/opt/data/kanban/`.
4. Set `/opt/data/kanban/current` and run `hermes kanban boards switch default`; then verify with `HERMES_KANBAN_BOARD=default hermes kanban boards current` and `hermes kanban list`.
5. Remove unwanted boards with `hermes kanban boards rm <slug> --delete` only after backup and verification. Use archive instead of `--delete` when the user did not explicitly ask to remove them.
6. Update any workspace documentation that referenced old board slugs or `HERMES_KANBAN_BOARD=<slug>` overrides. The final docs should show plain `hermes kanban ...` commands when `default` is the only active board.
7. Final verification should show exactly one board in `hermes kanban boards list`, no active diagnostics, and expected task counts on `default`.

## The anti-temptation rules

Your job description says "route, don't execute." The rules that enforce that:

- **Do not execute the work yourself.** Your restricted toolset usually doesn't even include terminal/file/code/web for implementation. If you find yourself "just fixing this quickly" — stop and create a task for the right specialist.
- **For any concrete task, create a Kanban task and assign it.** Every single time.
- **Split multi-lane requests before creating cards.** A user prompt can contain several independent workstreams. Extract those lanes first, then create one card per lane instead of bundling unrelated work into a single implementer card.
- **Run independent lanes in parallel.** If two cards do not need each other's output, leave them unlinked so the dispatcher can fan them out. Link only true data dependencies.
- **If no specialist fits the available profiles, ask the user which profile to create or which existing profile to use.** Do not invent profile names; the dispatcher will silently drop unknown assignees.
- **Decompose, route, and summarize — that's the whole job.**

## Decomposition playbook

### Step 1 — Understand the goal

Ask clarifying questions if the goal is ambiguous. Cheap to ask; expensive to spawn the wrong fleet.

### Step 2 — Sketch the task graph

Before creating anything, draft the graph out loud (in your response to the user). Treat every concrete workstream as a candidate card:

1. Extract the lanes from the request.
2. Map each lane to one of the profiles you discovered in Step 0. If a lane doesn't fit any existing profile, ask the user which to use or create.
3. Decide whether each lane is independent or gated by another lane.
4. Create independent lanes as parallel cards with no parent links.
5. Create synthesis/review/integration cards with parent links to the lanes they depend on.

Examples of prompts that should fan out (using placeholder profile names — substitute whatever exists on the user's setup):

- "Build an app" → one card to a design-oriented profile for product/UI direction, one or two cards to engineering profiles for implementation, plus a later integration/review card if the user has a reviewer profile.
- "Fix blockers and check model variants" → one implementation card for the blocker fixes plus one discovery/research card for config/source verification. A final reviewer card can depend on both.
- "Research docs and implement" → a docs-research card can run in parallel with a codebase-discovery card; implementation waits only if it truly needs those findings.
- "Analyze this screenshot and find the related code" → one card to a vision-capable profile for the visual analysis while another searches the codebase.

Words like "also," "finally," or "and" do not automatically imply a dependency. They often mean "make sure this is covered before reporting back." Only link tasks when one card cannot start until another card's output exists.

Show the graph to the user before creating cards. Let them correct it — including which actual profile name should own each lane.

### Step 3 — Create tasks and link

Use the profile names from Step 0. The example below uses placeholders `<profile-A>`, `<profile-B>`, `<profile-C>` — replace them with what the user actually has.

```python
t1 = kanban_create(
    title="research: Postgres cost vs current",
    assignee="<profile-A>",  # whichever profile handles research on this setup
    body="Compare estimated infrastructure costs, migration costs, and ongoing ops costs over a 3-year window. Sources: AWS/GCP pricing, team time estimates, current Postgres bills from peers.",
    tenant=os.environ.get("HERMES_TENANT"),
)["task_id"]

t2 = kanban_create(
    title="research: Postgres performance vs current",
    assignee="<profile-A>",  # same profile, run in parallel
    body="Compare query latency, throughput, and scaling characteristics at our expected data volume (~500GB, 10k QPS peak). Sources: benchmark papers, public case studies, pgbench results if easy.",
)["task_id"]

t3 = kanban_create(
    title="synthesize migration recommendation",
    assignee="<profile-B>",  # whichever profile does synthesis/analysis
    body="Read the findings from T1 (cost) and T2 (performance). Produce a 1-page recommendation with explicit trade-offs and a go/no-go call.",
    parents=[t1, t2],
)["task_id"]

t4 = kanban_create(
    title="draft decision memo",
    assignee="<profile-C>",  # whichever profile drafts user-facing prose
    body="Turn the analyst's recommendation into a 2-page memo for the CTO. Match the tone of previous decision memos in the team's knowledge base.",
    parents=[t3],
)["task_id"]
```

`parents=[...]` gates promotion — children stay in `todo` until every parent reaches `done`, then auto-promote to `ready`. No manual coordination needed; the dispatcher and dependency engine handle it.

### Step 4 — Complete your own task

If you were spawned as a task yourself (e.g. a planner profile was assigned `T0: "investigate Postgres migration"`), mark it done with a summary of what you created:

```python
kanban_complete(
    summary="decomposed into T1-T4: 2 research lanes in parallel, 1 synthesis on their outputs, 1 prose draft on the recommendation",
    metadata={
        "task_graph": {
            "T1": {"assignee": "<profile-A>", "parents": []},
            "T2": {"assignee": "<profile-A>", "parents": []},
            "T3": {"assignee": "<profile-B>", "parents": ["T1", "T2"]},
            "T4": {"assignee": "<profile-C>", "parents": ["T3"]},
        },
    },
)
```

### Step 5 — Report back to the user

Tell them what you created in plain prose, naming the actual profiles you used:

> I've queued 4 tasks:
> - **T1** (`<profile-A>`): cost comparison
> - **T2** (`<profile-A>`): performance comparison, in parallel with T1
> - **T3** (`<profile-B>`): synthesizes T1 + T2 into a recommendation
> - **T4** (`<profile-C>`): turns T3 into a CTO memo
>
> The dispatcher will pick up T1 and T2 now. T3 starts when both finish. You'll get a gateway ping when T4 completes. Use the dashboard or `hermes kanban tail <id>` to follow along.

## Common patterns

**Fan-out + fan-in (research → synthesize):** N research-style cards with no parents, one synthesis card with all of them as parents.

**Parallel implementation + validation:** one implementer card makes the change while one explorer/researcher card verifies config, docs, or source mapping. A reviewer card can depend on both. Do not make the implementer own unrelated verification just because the user mentioned both in one sentence.

**Pipeline with gates:** `planner → implementer → reviewer`. Each stage's `parents=[previous_task]`. Reviewer blocks or completes; if reviewer blocks, the operator unblocks with feedback and respawns.

**Same-profile queue / bulk seeding:** N tasks can all be assigned to the same profile with no dependencies. On some gateway dispatcher configurations, multiple tasks for the same profile may be claimed at once rather than strictly serialized, so large batches can create many concurrent workers. This is useful when the user wants to see the board fully populated, but add idempotency keys, set realistic `--max-runtime`, and monitor diagnostics/resource pressure for heavy builds.

**Human-in-the-loop:** Any task can `kanban_block()` to wait for input. Dispatcher respawns after `/unblock`. The comment thread carries the full context.

## Pitfalls

**Board selection / env pinning.** A running Hermes session may have `HERMES_KANBAN_BOARD` pinned from startup. That env var takes precedence over the global `kanban/current` file written by `hermes kanban boards switch <slug>`, so shelling out to `hermes kanban boards current` can still show the old board inside the same session. When operating on a project-specific board from a long-lived session, prefix CLI calls with `HERMES_KANBAN_BOARD=<slug>` or start a fresh Hermes session after switching boards.

**Inventing profile names that don't exist.** The dispatcher silently fails to spawn unknown assignees — the card just sits in `ready` forever. Always assign to a profile from your Step 0 discovery; ask the user if you're unsure.

**Force-loading skills workers cannot see.** Worker profiles can have a different available-skill namespace from the parent chat. If a card crashes with `Unknown skill(s): ...`, do not keep retrying unchanged. Remove optional skill preloads from the affected cards, embed the necessary instructions directly in the task body, or create a no-skill recovery controller that continues from the seeded specs. For large portfolio sweeps, make task bodies self-contained so orchestration survives profile/skill drift.

**Bundling independent lanes into one card.** If the user asks for two independent outcomes, create two cards. Example: "fix blockers and check model variants" is not one fixer task; create a fixer/engineer card for the fixes and an explorer/researcher card for the variant check, then optionally gate review on both.

**Over-linking because of wording.** "Finally check X" may still be parallel with implementation if X is static config, docs, or source discovery. Link it after implementation only when the check depends on the implementation result.

**Forgetting dependency links.** If the task graph says `research -> implement -> review`, do not create all tasks as independent ready cards. Use parent links so implement/review cannot run before their inputs exist.

**Reassignment vs. new task.** If a reviewer blocks with "needs changes," create a NEW task linked from the reviewer's task — don't re-run the same task with a stern look. The new task is assigned to the original implementer profile.

**Argument order for links.** `kanban_link(parent_id=..., child_id=...)` — parent first. Mixing them up demotes the wrong task to `todo`.

**Don't pre-create the whole graph if the shape depends on intermediate findings.** If T3's structure depends on what T1 and T2 find, let T3 exist as a "synthesize findings" task whose own first step is to read parent handoffs and plan the rest. Orchestrators can spawn orchestrators.

**Tenant inheritance.** If `HERMES_TENANT` is set in your env, pass `tenant=os.environ.get("HERMES_TENANT")` on every `kanban_create` call so child tasks stay in the same namespace.

## Reconciling stale boards against newer context

When the user asks to "review all Kanban tasks" and says the current chat has newer information than the board, do a reconciliation pass rather than blindly respawning workers:

1. Audit the active board and inspect every non-`done` task's comments/events/runs.
2. Treat explicit newer user direction as authoritative over stale task bodies.
3. Complete `review-required` blocked cards only when their handoffs already contain evidence such as passing tests/builds, clean git status, commits, or pushed remotes.
4. Re-run verification for cards blocked by transient conditions before closing them.
5. Annotate obsolete/rejected ideas so future agents do not recreate them.
6. Remember CLI shape: `hermes kanban complete` can bulk-close multiple task IDs with `--result`, but `--summary` and `--metadata` are per-task only.

See `references/board-reconciliation.md` for the detailed reconciliation checklist and pitfalls.

## Recovering a Kanban DB index integrity error

If `hermes kanban ...` refuses to initialize because SQLite `PRAGMA integrity_check` reports index-only corruption such as `wrong # of entries in index idx_events_run` or `idx_events_task`, do not treat the board as lost. Back up `/opt/data/kanban.db`, run `REINDEX` on the named indexes, verify `PRAGMA integrity_check` returns `ok`, then retry the Kanban command. See `references/kanban-sqlite-index-repair.md` for the exact recovery snippet and guardrails.

## Recovering stuck workers

When a worker profile keeps crashing, hallucinating, or getting blocked by its own mistakes (usually: wrong model, missing skill, broken credential), the kanban dashboard flags the task with a ⚠ badge and opens a **Recovery** section in the drawer. Three primary actions:

1. **Reclaim** (or `hermes kanban reclaim <task_id>`) — abort the running worker immediately and reset the task to `ready`. The existing claim TTL is ~15 min; this is the fast path out.
2. **Reassign** (or `hermes kanban reassign <task_id> <new-profile> --reclaim`) — switch the task to a different profile (one that exists on this setup) and let the dispatcher pick it up with a fresh worker.
3. **Change profile model** — the dashboard prints a copy-paste hint for `hermes -p <profile> model` since profile config lives on disk; edit it in a terminal, then Reclaim to retry with the new model.

Hallucination warnings appear on tasks where a worker's `kanban_complete(created_cards=[...])` claim included card ids that don't exist or weren't created by the worker's profile (the gate blocks the completion), or where the free-form summary references `t_<hex>` ids that don't resolve (advisory prose scan, non-blocking). Both produce audit events that persist even after recovery actions — the trail stays for debugging.
