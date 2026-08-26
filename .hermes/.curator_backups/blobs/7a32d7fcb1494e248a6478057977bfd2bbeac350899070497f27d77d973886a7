# Recovering from a malformed historical submodule pointer

Use this when `git pull` fails with:

```text
fatal: remote error: upload-pack: not our ref <sha>
Errors during submodule fetch:
    <submodule-path>
```

and the current parent tip already points to a valid reachable submodule commit.

## Why it happens

A newly fetched *intermediate parent commit* may contain a mistyped or unreachable gitlink. Recursive fetch scans submodule SHAs introduced anywhere in the fetched parent range before the parent fast-forward completes. A later parent commit can correct the gitlink, yet the pull still aborts on the bad historical SHA.

Confirm by comparing pointer transitions across the fetched range:

```bash
git rev-list --reverse <old-parent>..<new-parent> | while read c; do git ls-tree "$c" <submodule-path>; done
```

Also verify the current tip and remote submodule refs:

```bash
git ls-tree <new-parent> <submodule-path>
git -C <submodule-path> ls-remote origin
```

## Safe recovery

Fetch the parent without recursive submodule fetching, fast-forward directly to the corrected tip, then initialize/update only the final tree's submodules:

```bash
git -c fetch.recurseSubmodules=false fetch origin main
git merge --ff-only origin/main
git submodule sync --recursive
git submodule update --init --recursive
```

Windows CMD uses the same four single-line commands.

## Pitfalls

- Do not rewrite parent history merely to remove the bad intermediate commit unless repository owners explicitly approve a force-push.
- Do not assume the current gitlink is bad just because recursive pull names a bad SHA; inspect the current tip first.
- A new empty commit or re-setting an already-correct current gitlink does not prevent clients crossing the broken historical range from fetching the intermediate SHA.
- Avoid `git reset --hard` in a dirty user workspace. Use the non-recursive fetch plus fast-forward merge, which will stop safely if tracked local changes conflict.
