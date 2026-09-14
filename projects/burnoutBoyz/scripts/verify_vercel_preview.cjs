const { chromium } = require('/tmp/hermes-playwright/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');

const baseUrl = process.argv[2];
if (!baseUrl || !/^https:\/\//.test(baseUrl)) {
  throw new Error('Usage: node scripts/verify_vercel_preview.cjs https://preview-url');
}

const outputDir = path.join(__dirname, '..', 'artifacts', 'vercel-preview');
fs.mkdirSync(outputDir, { recursive: true });

const browserCache = '/opt/data/.cache/ms-playwright';
const cachedChromium = fs.existsSync(browserCache)
  ? fs.readdirSync(browserCache)
      .filter((entry) => entry.startsWith('chromium_headless_shell-'))
      .sort()
      .reverse()
      .map((entry) => path.join(browserCache, entry, 'chrome-headless-shell-linux64', 'chrome-headless-shell'))
      .find((candidate) => fs.existsSync(candidate))
  : undefined;

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: cachedChromium });
  const report = { baseUrl, checkedAt: new Date().toISOString(), checks: [] };
  try {
    for (const viewport of [
      { name: 'desktop', width: 1440, height: 900 },
      { name: 'mobile', width: 390, height: 844 },
    ]) {
      for (const route of ['/', '/explore']) {
        const page = await browser.newPage({ viewport });
        const consoleErrors = [];
        const pageErrors = [];
        const failedResponses = [];
        page.on('console', (message) => {
          if (message.type() === 'error') consoleErrors.push(message.text());
        });
        page.on('pageerror', (error) => pageErrors.push(error.message));
        page.on('response', (response) => {
          if (response.status() >= 400) failedResponses.push({ status: response.status(), url: response.url() });
        });
        const response = await page.goto(`${baseUrl}${route}`, { waitUntil: 'networkidle', timeout: 60_000 });
        const bodyText = await page.locator('body').innerText();
        const dimensions = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
        }));
        const identity = /BURNOUTBOYZ|BurnoutBoyz/i.test(bodyText);
        const navigation = route === '/' ? /Explore/i.test(bodyText) : /Garage|Back/i.test(bodyText);
        const screenshot = path.join(outputDir, `${viewport.name}-${route === '/' ? 'home' : 'explore'}.png`);
        await page.screenshot({ path: screenshot, fullPage: true });
        report.checks.push({
          viewport: viewport.name,
          route,
          status: response && response.status(),
          title: await page.title(),
          identity,
          navigation,
          overflow: dimensions.scrollWidth > dimensions.clientWidth,
          dimensions,
          consoleErrors,
          pageErrors,
          failedResponses,
          screenshot,
        });
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }
  const reportPath = path.join(outputDir, 'report.json');
  fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify(report, null, 2));
  const failed = report.checks.some((check) =>
    check.status !== 200 || !check.identity || !check.navigation || check.overflow ||
    check.consoleErrors.length || check.pageErrors.length || check.failedResponses.length
  );
  if (failed) process.exitCode = 1;
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
