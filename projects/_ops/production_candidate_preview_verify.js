const { chromium } = require('./vercel-audit-runner/node_modules/playwright-core');
const fs = require('fs');

const urls = [
  { app: 'journal-ai', url: 'https://journal-qmx4djhze-itmeansbigmountains-projects.vercel.app', expected: /Journal AI/i },
  { app: 'coding-school-platform', url: 'https://coding-school-platform-5hh2k4xao-itmeansbigmountains-projects.vercel.app', expected: /Algorithm Academy/i },
  { app: 'tweetbetweenthelines', url: 'https://tweetbetweenthelines-2hr5230u9-itmeansbigmountains-projects.vercel.app', expected: /tweetBetweenTheLines/i },
];
const devices = [
  { name: 'desktop', viewport: { width: 1440, height: 900 } },
  { name: 'mobile', viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
];

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/opt/data/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome' });
  const checks = [];
  for (const item of urls) for (const device of devices) {
    const context = await browser.newContext(device);
    const page = await context.newPage();
    const consoleErrors = [], pageErrors = [], failedResponses = [];
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 500)); });
    page.on('pageerror', e => pageErrors.push(String(e).slice(0, 500)));
    page.on('response', r => { if (r.status() >= 400) failedResponses.push({ status: r.status(), url: r.url().slice(0, 500) }); });
    let response = null, navigationError = null;
    try { response = await page.goto(item.url, { waitUntil: 'networkidle', timeout: 60000 }); } catch (e) { navigationError = String(e).slice(0, 500); }
    const metrics = await page.evaluate(() => ({ title: document.title, body: (document.body?.innerText || '').replace(/\s+/g, ' ').slice(0, 500), scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth })).catch(() => ({ title: '', body: '', scrollWidth: null, clientWidth: null }));
    const identityOk = item.expected.test(`${metrics.title} ${metrics.body}`);
    const overflow = metrics.scrollWidth !== null && metrics.scrollWidth > metrics.clientWidth + 1;
    checks.push({ app: item.app, device: device.name, requested: item.url, final_url: page.url(), status: response?.status() ?? null, title: metrics.title, identity_ok: identityOk, body_sample: metrics.body, horizontal_overflow: overflow, console_errors: consoleErrors, page_errors: pageErrors, failed_responses: failedResponses, navigation_error: navigationError, passed: Boolean(response && response.status() === 200 && !page.url().startsWith('https://vercel.com/login') && identityOk && !overflow && !navigationError && !consoleErrors.length && !pageErrors.length && !failedResponses.length) });
    await context.close();
  }
  await browser.close();
  const out = { generated_at: new Date().toISOString(), checks };
  fs.writeFileSync('/opt/data/HeRmEz/projects/_ops/production-candidate-preview-browser-verification.json', JSON.stringify(out, null, 2) + '\n');
  console.log(JSON.stringify({ checks: checks.length, passed: checks.filter(x => x.passed).length, failed: checks.filter(x => !x.passed).length }));
})();
