# Vercel + GitHub Actions Workflow Templates for tweetBetweenTheLines

## `.github/workflows/vercel-dev.yml`

```yaml
name: tweetBetweenTheLines Vercel development
on:
  push:
    branches: [main]
    paths:
      - 'apps/mobile/**'
      - 'packages/**'
      - 'package.json'
      - 'package-lock.json'
      - 'tsconfig.base.json'
  workflow_dispatch:

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  deploy-preview:
    name: Deploy Vercel development preview
    runs-on: ubuntu-latest
    environment: tweet-between-the-lines-development
    permissions:
      contents: read
      deployments: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: amondnet/vercel-action@v25
        id: vercel
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prebuilt --token=${{ secrets.VERCEL_TOKEN }}'
      - name: Upload deployment URL
        uses: actions/upload-artifact@v4
        with:
          name: deployment-url
          path: deployment-url.txt
          retention-days: 30
      - name: Summary
        run: |
          echo "## Vercel Development Preview" >> $GITHUB_STEP_SUMMARY
          echo "**URL:** ${{ steps.vercel.outputs.url }}" >> $GITHUB_STEP_SUMMARY
          echo "**Inspect:** ${{ steps.vercel.outputs.inspect-url }}" >> $GITHUB_STEP_SUMMARY
```

## `.github/workflows/eas-preview.yml`

```yaml
name: tweetBetweenTheLines EAS preview
on:
  workflow_dispatch:
    inputs:
      platform:
        type: choice
        description: Target platform
        options: [ios, android, all]
        default: all

jobs:
  build-preview:
    name: EAS preview (${{ github.event.inputs.platform }})
    runs-on: ubuntu-latest
    environment: tweet-between-the-lines-mobile-preview
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          expo-token: ${{ secrets.EXPO_TOKEN }}
          eas-version: 'latest'
      - run: |
          cd apps/mobile
          eas build --platform ${{ github.event.inputs.platform }} --profile preview --non-interactive --json
```