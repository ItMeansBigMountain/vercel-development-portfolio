/**
 * Browser Smoke & Identity Test for Coding School Platform
 * Tests the IMMUTABLE deployment URL (not the canonical alias)
 * to verify the newly deployed artifact is correct before any aliasing.
 */

import fs from 'node:fs';
import { chromium, devices } from 'playwright';

// Load deployment metadata from CI artifacts
const metadataDir = 'deployment-metadata';
const metadataFiles = fs.existsSync(metadataDir)
  ? fs.readdirSync(metadataDir, { recursive: true }).filter(f => f.endsWith('.json'))
  : [];

if (metadataFiles.length === 0) {
  console.error('Missing deployment metadata');
  process.exit(1);
}

const metadataPath = `${metadataDir}/${metadataFiles[0]}`;
const deployment = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));

// Configuration for Coding School Platform
const appConfig = {
  app: 'coding-school-platform',
  identity: 'Algorithm Academy',
  repo_path: 'projects/coding-school-platform/app',
};

const browser = await chromium.launch({ headless: true });
const results = [];
let failed = false;

const testUrl = deployment.immutable_url;
const expectedIdentity = appConfig.identity;

console.log(`Testing immutable URL: ${testUrl}`);
console.log(`Expected identity: ${expectedIdentity}`);

for (const [viewportName, viewportOptions] of Object.entries({
  desktop: { viewport: { width: 1440, height: 900 } },
  mobile: devices['iPhone 13'],
})) {
  const context = await browser.newContext(viewportOptions);
  const page = await context.newPage();

  let response = null;
  let finalUrl = '';
  let title = '';
  let body = '';
  let protectedRedirect = false;
  let identityPass = false;
  let pass = false;
  let error = null;

  try {
    response = await page.goto(testUrl, {
      waitUntil: 'domcontentloaded',
      timeout: 45000,
    });

    finalUrl = page.url();
    title = await page.title();
    body = (await page.locator('body').innerText()).trim();

    // Check for Vercel login redirect (protected deployment)
    protectedRedirect = finalUrl.startsWith('https://vercel.com/login');

    // Identity assertion: title + body must contain expected identity string
    identityPass = expectedIdentity
      ? `${title}\n${body}`.toLowerCase().includes(expectedIdentity.toLowerCase())
      : body.length > 0;

    pass = Boolean(
      response &&
      response.status() < 400 &&
      !protectedRedirect &&
      identityPass
    );

    if (!pass) {
      failed = true;
    }
  } catch (e) {
    error = e.message;
    pass = false;
    failed = true;
  }

  results.push({
    app: appConfig.app,
    viewport: viewportName,
    url: testUrl,
    final_url: finalUrl,
    status: response?.status() ?? null,
    title,
    identity: expectedIdentity,
    pass,
    immutable_url: deployment.immutable_url,
    commit_sha: deployment.commit_sha,
    error,
  });

  console.log(`${viewportName}: ${pass ? 'PASS' : 'FAIL'} - ${finalUrl} (${response?.status() ?? 'N/A'})`);

  await context.close();
}

await browser.close();

// Write results
const output = {
  generated_at: new Date().toISOString(),
  count: results.length,
  passed: results.filter((x) => x.pass).length,
  results,
};

fs.writeFileSync('browser-smoke-results.json', JSON.stringify(output, null, 2) + '\n');
console.log(`Browser smoke: ${output.passed}/${output.count} passed`);

if (failed) {
  process.exit(1);
}