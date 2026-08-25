# Security-research source monorepos

Use this workflow when consolidating public malware, phishing, exploit, or dual-use research repositories into one GitHub repository without executing or operationalizing them.

## Safe import sequence

1. Query each upstream repository for default branch, current commit, size, license, archive status, and submodules.
2. Clone into temporary directories without running installers, builds, payloads, or dependency hooks.
3. Record each exact upstream URL, branch, and commit SHA before removing nested `.git` metadata.
4. Copy each project into its own ordinary top-level folder. Preserve upstream README, license, notice, vendored-license, binary, line-ending, file-mode, and whitespace state.
5. Add a root README containing:
   - authorized-research-only warning;
   - folder-to-upstream mapping;
   - pinned commit SHAs;
   - import method;
   - per-folder license status;
   - update procedure.
6. Do not apply a repository-wide license when imported projects use different licenses or an upstream has no license.
7. Run a static pre-publication scan without executing source:
   - private-key PEM markers;
   - `.env` and similar runtime files;
   - credential/token assignments;
   - unsafe symlinks;
   - oversized files and GitHub blob-limit risks.
8. Treat `git diff --check` findings inside byte-preserved imports as provenance observations, not automatic reasons to rewrite upstream source. Validate only newly-authored root files separately if needed.
9. Prefer a private destination when the collection contains deployable malware/phishing code, leaked source, or a no-license project, unless the user explicitly requests public visibility and redistribution rights are clear.
10. Push via temporary `GIT_ASKPASS` when headless HTTPS authentication is needed; do not persist or print the token.
11. Verify both:
    - local HEAD equals `git ls-remote` for the destination branch;
    - GitHub API readback confirms visibility, default branch, and every expected top-level folder.

## Licensing rules

- Public GitHub visibility is not a software license.
- Preserve GPL/MIT and dependency notices inside their original folders.
- For a no-license upstream, state that no rights are granted or claimed and that rights remain with its copyright holders.
- A private archive reduces exposure but does not create redistribution rights; avoid claiming that privacy cures licensing defects.
- If public redistribution is required and a project has no license, use a Git submodule/upstream pointer or obtain permission rather than copying it into a public monorepo.

## Provenance verification

For strongest fidelity, compare each imported folder against a fresh checkout of the pinned SHA after excluding only `.git`. A directory-tree hash or recursive file manifest is preferable to formatting tools because formatters can mutate original evidence.

## Scope boundary

This workflow packages and archives source. It does not include deploying malware, configuring phishing infrastructure, selecting targets, bypassing defenses, or running payloads.