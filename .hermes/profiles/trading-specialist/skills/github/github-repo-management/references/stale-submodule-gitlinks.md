# Stale submodule gitlinks with missing `.gitmodules` mappings

Use when `git submodule update --init --recursive` fails with:

```text
fatal: No url found for submodule path '<path>' in .gitmodules
fatal: no submodule mapping found in .gitmodules for path '<path>'
```

This means the parent repo still tracks `<path>` as a `160000` gitlink, but `.gitmodules` no longer contains a matching `submodule.*.path` + URL entry.

## Diagnose

Run from the parent repo:

```bash
git ls-files --stage <path> .gitmodules
git config --file .gitmodules --get-regexp 'submodule\..*' || true
git status --short -- <path> .gitmodules
```

A stale gitlink shows as mode `160000` for `<path>` in `git ls-files --stage`, while `.gitmodules` lacks that path.

## Fix when the local folder is intentionally no longer a submodule

1. If the working directory exists and contains local work, inspect it first. Do not delete the directory.
2. Ensure `.gitignore` already ignores the local standalone/nested repo path so its contents will not be staged into the parent after removing the gitlink.
3. Remove only the parent gitlink from the index:

```bash
git rm --cached -f <path>
```

4. Repeat for any next stale path exposed by a full recursive check.
5. Verify:

```bash
git submodule status --recursive
git submodule update --init --recursive
git diff --cached --summary
```

The cached diff should show `delete mode 160000 <path>` for stale local-project gitlinks only.

## Commit/push pattern

Commit only the removed gitlinks and any intentional ignore updates; do not stage unrelated dirty files from the parent workspace.

Example commit message:

```text
chore: remove stale local project gitlinks
```

After pushing, have the user run a one-line Windows command such as:

```cmd
cd C:\path\to\HeRmEz && git pull origin main && git submodule sync --recursive && git submodule update --init --recursive
```

## Pitfalls

- Do not edit `.gitmodules` alone; the failure is caused by an index gitlink without a mapping.
- Do not use `git rm -f <path>` unless the user wants the local working folder deleted from disk. Use `git rm --cached -f <path>` for cleanup while preserving the local folder.
- A full recursive check may reveal stale gitlinks one at a time; fix all stale gitlinks before reporting that `git submodule update --init --recursive` works.
- For this user, return Windows `cmd` commands as one-liners, not multi-line continuations.