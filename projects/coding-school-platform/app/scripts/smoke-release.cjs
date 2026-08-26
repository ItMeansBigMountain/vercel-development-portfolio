const fs = require('fs');
const http = require('http');
const os = require('os');
const path = require('path');
const { chromium } = require('playwright');

const requestedURL = process.env.SMOKE_URL;
const distDir = path.resolve(__dirname, '..', 'dist');

function contentType(filePath) {
  if (filePath.endsWith('.html')) return 'text/html; charset=utf-8';
  if (filePath.endsWith('.js')) return 'application/javascript; charset=utf-8';
  if (filePath.endsWith('.json')) return 'application/json; charset=utf-8';
  if (filePath.endsWith('.ico')) return 'image/x-icon';
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

async function expectVisible(page, text) {
  await page.getByText(text, { exact: false }).first().waitFor({ state: 'visible', timeout: 10000 });
}

(async () => {
  const served = requestedURL ? { server: null, baseURL: requestedURL } : await serveDist();
  const executablePath = process.env.CHROMIUM_PATH || [
    path.join(os.homedir(), '.cache/ms-playwright/chromium-1234/chrome-linux64/chrome'),
    path.join(os.homedir(), '.cache/ms-playwright/chromium-1200/chrome-linux64/chrome'),
  ].find(candidate => fs.existsSync(candidate));
  const browser = await chromium.launch({ headless: true, executablePath });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on('console', message => {
    if (message.type() === 'error') errors.push(message.text());
  });
  page.on('pageerror', error => errors.push(error.message));
  page.on('dialog', dialog => dialog.accept());

  await page.goto(served.baseURL, { waitUntil: 'networkidle' });
  await expectVisible(page, 'Learn by building');
  await expectVisible(page, 'Save evidence for teacher review');
  const sandboxCount = await page.locator('iframe[title="Secure coding sandbox preview"][sandbox=""]').count();
  if (sandboxCount !== 1) throw new Error(`Expected one script-free sandbox iframe, found ${sandboxCount}`);

  await page.getByLabel('Trace-table blank').fill('value');
  await page.getByLabel('Lesson reflection').fill('I traced the loop and will compare index with value next.');
  await page.getByText('Save evidence for teacher review').click();
  await page.getByLabel('Switch to teacher demo view').click();
  await expectVisible(page, 'Teacher review queue');
  await expectVisible(page, 'I traced the loop');
  await page.getByText('Approve mastery').click();
  await expectVisible(page, 'Status: approved');

  await page.getByLabel('Switch to parent demo view').click();
  await expectVisible(page, 'Parent weekly progress');
  await expectVisible(page, 'Learning Journey export');

  await page.getByLabel('Switch to admin demo view').click();
  await expectVisible(page, 'Admin release console');
  await expectVisible(page, 'real student records');
  await expectVisible(page, 'Signed iOS and Android releases require owner Apple/Google credentials');

  await page.setViewportSize({ width: 1280, height: 900 });
  await page.getByLabel('Switch to learner demo view').click();
  await expectVisible(page, '1 teacher-approved');

  await browser.close();
  if (errors.length) throw new Error(`Console/page errors: ${errors.join(' | ')}`);
  if (served.server) served.server.close();
  console.log(JSON.stringify({ ok: true, baseURL: served.baseURL, paths: ['learner', 'teacher', 'parent', 'admin'], viewports: ['390x844', '1280x900'] }));
})().catch(async error => {
  console.error(error);
  process.exit(1);
});
