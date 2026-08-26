const fs = require('fs');
const http = require('http');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const requestedURL = process.env.INPUT_GATE_URL || process.env.SMOKE_URL;
const distDir = path.resolve(__dirname, '..', 'dist');
const reportPath = path.resolve(process.env.INPUT_GATE_REPORT || path.join(__dirname, '..', 'input-quality-report.json'));

const viewports = [
  { name: 'phone-portrait', width: 390, height: 844 },
  { name: 'phone-landscape', width: 844, height: 390 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'laptop', width: 1366, height: 768 },
  { name: 'wide-monitor', width: 1920, height: 1080 },
];

function contentType(filePath) {
  if (filePath.endsWith('.html')) return 'text/html; charset=utf-8';
  if (filePath.endsWith('.js')) return 'application/javascript; charset=utf-8';
  if (filePath.endsWith('.json')) return 'application/json; charset=utf-8';
  if (filePath.endsWith('.ico')) return 'image/x-icon';
  if (filePath.endsWith('.png')) return 'image/png';
  return 'application/octet-stream';
}

async function serveDist() {
  const server = http.createServer((request, response) => {
    const url = new URL(request.url || '/', 'http://127.0.0.1');
    const pathname = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname);
    const filePath = path.resolve(distDir, `.${pathname}`);
    if (!filePath.startsWith(distDir)) {
      response.writeHead(403).end('Forbidden');
      return;
    }
    fs.readFile(filePath, (error, data) => {
      if (error) {
        fs.readFile(path.join(distDir, 'index.html'), (fallbackError, fallback) => {
          if (fallbackError) response.writeHead(404).end('Not found');
          else response.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }).end(fallback);
        });
        return;
      }
      response.writeHead(200, { 'content-type': contentType(filePath) }).end(data);
    });
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const address = server.address();
  return { server, baseURL: `http://127.0.0.1:${address.port}/` };
}

function findChromium() {
  return process.env.CHROMIUM_PATH || [
    path.join(os.homedir(), '.cache/ms-playwright/chromium-1234/chrome-linux64/chrome'),
    path.join(os.homedir(), '.cache/ms-playwright/chromium-1200/chrome-linux64/chrome'),
  ].find(candidate => fs.existsSync(candidate));
}

async function expectVisible(page, text) {
  await page.getByText(text, { exact: false }).first().waitFor({ state: 'visible', timeout: 10000 });
}

async function expectValue(page, label, expected) {
  const value = await page.getByLabel(label).inputValue();
  if (!value.includes(expected)) throw new Error(`${label} did not persist expected text: ${expected}`);
}

async function assertNoHorizontalOverflow(page, viewportName) {
  const metrics = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));
  if (metrics.scrollWidth > metrics.clientWidth + 2) {
    throw new Error(`${viewportName} has horizontal overflow: ${metrics.scrollWidth} > ${metrics.clientWidth}`);
  }
}

async function assertVisibleAfterFocus(page, label) {
  const locator = page.getByLabel(label);
  await locator.focus();
  await locator.scrollIntoViewIfNeeded();
  const box = await locator.boundingBox();
  const viewport = page.viewportSize();
  if (!box || !viewport || box.y < 0 || box.y + Math.min(box.height, 80) > viewport.height) {
    throw new Error(`${label} is not visible after focus/scroll`);
  }
}

async function assertButtonNames(page) {
  const unnamed = await page.evaluate(() => Array.from(document.querySelectorAll('[role="button"],button'))
    .map((node, index) => ({
      index,
      label: node.getAttribute('aria-label') || node.textContent || '',
    }))
    .filter(item => !item.label.trim()));
  if (unnamed.length) throw new Error(`Found unnamed button(s): ${JSON.stringify(unnamed)}`);
}

async function runViewport(browser, baseURL, viewport) {
  const context = await browser.newContext({ viewport, permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await context.newPage();
  const errors = [];
  page.on('console', message => {
    if (message.type() === 'error') errors.push(message.text());
  });
  page.on('pageerror', error => errors.push(error.message));
  page.on('dialog', dialog => dialog.accept());

  await page.goto(baseURL, { waitUntil: 'networkidle' });
  await expectVisible(page, 'Learn by building');
  await assertButtonNames(page);
  await assertNoHorizontalOverflow(page, viewport.name);

  await page.keyboard.press('Tab');
  const activeRole = await page.evaluate(() => document.activeElement?.getAttribute('role') || document.activeElement?.tagName || 'none');
  if (activeRole === 'BODY' || activeRole === 'none') throw new Error(`${viewport.name} keyboard tab did not move focus`);

  await page.getByText('Save evidence for teacher review').click();
  await expectVisible(page, 'Complete the trace-table blank');

  await page.getByLabel('Code draft').fill('');
  await page.getByLabel('Code draft').focus();
  await page.evaluate(() => navigator.clipboard.writeText('def linear_search(nums, target):\n    return nums.index(target)\n'));
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+V' : 'Control+V');
  await expectValue(page, 'Code draft', 'linear_search');

  await page.getByLabel('Trace-table blank').fill('value');
  await page.getByLabel('Toggle word bank value').click();
  await page.getByLabel('Toggle word bank index').click();
  await page.getByLabel('Lesson reflection').fill('');
  await page.getByLabel('Lesson reflection').focus();
  await page.evaluate(() => navigator.clipboard.writeText('I pasted a reflection, traced index versus value, and tested a missing target.'));
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+V' : 'Control+V');
  await assertVisibleAfterFocus(page, 'Lesson reflection');

  await page.reload({ waitUntil: 'networkidle' });
  await expectValue(page, 'Code draft', 'linear_search');
  await expectValue(page, 'Trace-table blank', 'value');
  await expectValue(page, 'Lesson reflection', 'pasted a reflection');

  await page.getByText('Save evidence for teacher review').click();
  await page.getByLabel('Switch to teacher demo view').click();
  await expectVisible(page, 'Teacher review queue');
  await expectVisible(page, 'pasted a reflection');
  await page.getByText('Approve mastery').click();
  await expectVisible(page, 'Status: approved');

  await page.getByLabel('Switch to parent demo view').click();
  await expectVisible(page, 'Parent weekly progress');
  await expectVisible(page, 'Learning Journey export');
  await expectVisible(page, 'teacher-approved mastery evidence');
  await expectValue(page, 'Parent-safe weekly note', 'pasted a reflection');

  await page.getByLabel('Switch to admin demo view').click();
  await expectVisible(page, 'Admin release console');
  await expectVisible(page, 'demo roles available');
  await expectVisible(page, 'Parent-safe progress export avoids private profile fields');
  await assertNoHorizontalOverflow(page, viewport.name);
  await assertButtonNames(page);

  await context.close();
  if (errors.length) throw new Error(`${viewport.name} console/page errors: ${errors.join(' | ')}`);
  return {
    viewport: viewport.name,
    size: `${viewport.width}x${viewport.height}`,
    covered: ['keyboard focus', 'textarea editor', 'fill-in-the-blank', 'word bank', 'paste', 'autosave reload', 'submission', 'teacher feedback', 'parent export', 'admin validation', 'focus/scroll', 'accessibility button names', 'horizontal overflow'],
  };
}

(async () => {
  const served = requestedURL ? { server: null, baseURL: requestedURL } : await serveDist();
  const browser = await chromium.launch({ headless: true, executablePath: findChromium() });
  const results = [];
  try {
    for (const viewport of viewports) {
      results.push(await runViewport(browser, served.baseURL, viewport));
    }
  } finally {
    await browser.close();
    if (served.server) served.server.close();
  }
  const report = {
    ok: true,
    baseURL: served.baseURL,
    generatedAt: new Date().toISOString(),
    roles: ['learner', 'teacher', 'parent', 'admin'],
    viewports: results,
  };
  fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify(report));
})().catch(error => {
  console.error(error);
  process.exit(1);
});
