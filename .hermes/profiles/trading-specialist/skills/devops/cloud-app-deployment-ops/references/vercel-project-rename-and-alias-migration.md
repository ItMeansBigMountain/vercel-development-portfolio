# Vercel Project Rename and Alias Migration

Use when an existing GitHub-backed Vercel app must move to a new repository/project identity without losing history, environment variables, or deployment continuity.

## Safe migration sequence

1. Verify the existing local repository is clean and local `HEAD` equals the remote default-branch SHA.
2. Rename the GitHub repository instead of copying into a second repository when history should be preserved.
3. Update the local `origin` URL and verify `git ls-remote origin refs/heads/main` still equals local `HEAD`.
4. Rename the Vercel project with `vercel project rename OLD NEW`. Project IDs and environment variables normally survive a project rename, but verify sensitive variable names/status rather than assuming.
5. Run a fresh production deployment and capture its immutable deployment URL.
6. Do not assume aliases follow a rename. Inspect `vercel alias list` and explicitly attach the desired alias to the verified deployment.
7. If the exact `*.vercel.app` name is unavailable, audit aliases/projects before deleting anything. A globally claimed alias may belong outside the current account and cannot be freed by deleting local projects. Choose a clean available branded alias instead.
8. Compare the immutable URL, generated project alias, legacy production alias, and new branded alias separately.
9. Inspect deployment protection when a new alias redirects to Vercel SSO while an older alias remains public:
   - `vercel project protection PROJECT --json`
   - A setting such as `all_except_custom_domains` protects generated and manually assigned `*.vercel.app` aliases because they are not custom domains.
   - For an intentionally public storefront, disable SSO with `vercel project protection disable PROJECT --sso`; retain unrelated protections such as Git-fork protection.
10. Reattach the alias if needed, then verify homepage, secondary routes, APIs, cookie flags, browser rendering, and mobile E2E checks on the final canonical alias.

## Important distinctions

- **Project rename** does not guarantee **deployment name**, **Git integration label**, or **primary alias** changes immediately.
- A CLI deploy can show the historical deployment name while still deploying to the same renamed project ID.
- `302` to `vercel.com/sso-api` means deployment protection, not an application 404.
- A legacy alias returning 200 while new aliases redirect to SSO indicates protection/alias policy drift, not a failed build.
- Never delete old projects solely because an alias is unavailable. Identify the alias owner and current scope first; if it is globally owned elsewhere, deletion in the current scope cannot solve it.

## Verification checklist

- GitHub repository resolves at the new URL.
- Local `origin` points to the new URL.
- Local and remote SHAs match.
- Vercel project has the intended new name and same project ID.
- Required sensitive environment-variable names remain configured.
- Production deployment is `Ready`.
- Final canonical alias returns 200 without SSO.
- API and responsive browser tests pass on the final alias.
- No unrelated Vercel project was deleted without explicit verification and approval.
