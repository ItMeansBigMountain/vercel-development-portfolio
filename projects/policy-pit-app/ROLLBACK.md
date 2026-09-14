# Rollback — development preview only

Policy Pit is not production. The canonical alias and Vercel project history must be preserved.

1. Find the last verified deployment in Vercel project `policy-pit-app`.
2. Reassign the development alias to that immutable deployment in the Vercel dashboard, or redeploy its exact Git commit through GitHub Actions.
3. Verify the alias returns 200, the expected title, and the desktop/mobile smoke matrix.
4. Record old/new deployment IDs and the reason on the Kanban card.

Do not delete deployments, rename the Vercel project, or promote this scaffold to production.
