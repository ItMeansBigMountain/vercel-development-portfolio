# Deployment and rollback runbook

## GitHub environments and secrets

The workflows intentionally keep deployment credentials out of repository variables and pull requests.

- `tweet-between-the-lines-development`: environment secrets `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID`. Restrict this environment to `main` and trusted reviewers.
- `tweet-between-the-lines-mobile-preview`: environment secret `EXPO_TOKEN`. Restrict manual dispatch to trusted maintainers. Run `eas init` once from `apps/mobile`, review the generated `expo.extra.eas.projectId`, and commit only that non-secret project ID before dispatching native builds.
- Do not put provider OAuth credentials in GitHub Actions until a deployed backend exists. Use separate least-privilege environment secrets and approved redirect URIs when it does.

CI has read-only repository permissions, no secrets, SHA-pinned third-party actions, concurrency cancellation, a 25-minute timeout, and 14-day web-export retention. Vercel and EAS jobs use read-only repository permissions, environment-scoped secrets, SHA-pinned actions, cancellation, bounded timeouts, and 30-day URL/build metadata retention.

## Development web deployment

`tweetBetweenTheLines Vercel development` runs after relevant `main` changes or by manual dispatch. It pulls the Vercel development environment, builds locally in Actions, deploys the prebuilt output without `--prod`, publishes the immutable HTTPS URL in the GitHub deployment environment and step summary, and retains `deployment-url.txt` for 30 days.

Verify every returned URL externally:

```text
curl -fsSIL <immutable-preview-url>
PLAYWRIGHT_BROWSERS_PATH=/opt/data/.cache/ms-playwright node .hermes-public-web-smoke.cjs <immutable-preview-url>
```

The persistent production alias remains `https://tweetbetweenthelines.vercel.app`. This development workflow never promotes or aliases a deployment to production.

## Mobile preview builds

Dispatch `tweetBetweenTheLines EAS preview` with `ios`, `android`, or `all`. The `preview` EAS profile uses internal distribution; Android emits an APK. EAS owns signing credentials. The workflow queues builds non-interactively and reports build-detail/install URLs in the summary and retained JSON artifact. A missing Expo project binding or credential fails closed; it does not create or guess credentials.

## Rollback

1. Stop the rollout by cancelling the active workflow; concurrency also cancels superseded runs.
2. Revert the faulty commit through a reviewed pull request. Do not edit deployed output or environment variables as an undocumented fix.
3. For development previews, use the prior immutable URL from the GitHub environment history or retained `deployment-url.txt`; redeploy the reverted commit if a fresh URL is required.
4. Production rollback is a separately approved action: promote a previously verified immutable Vercel deployment or deploy the reverted commit with the production workflow. This repository does not automate production promotion.
5. For EAS, keep the previous internal build installed or redistribute its recorded install URL. Increment and rebuild after the fix; native binaries cannot be rolled back in place.
6. Re-run lint, fixture validation, tests, build, HTTP checks, and the mobile Playwright smoke before declaring recovery.

Never print, upload, or copy tokens, downloaded environment files, signing materials, or OAuth credentials into workflow logs or artifacts.