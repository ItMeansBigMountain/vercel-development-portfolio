import fs from 'node:fs';
import { chromium } from 'playwright';

const metadataPath = process.env.DEPLOYMENT_METADATA || 'deployment-metadata.json';
const deployment = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
const testUrl = deployment.immutable_url;
if (!testUrl?.startsWith('https://')) throw new Error('Missing public HTTPS deployment URL');

const browser = await chromium.launch({ headless: true });
const results = [];
let failed = false;

for (const viewport of [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }]) {
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();
  const errors = [];
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('pageerror', error => errors.push(error.message));
  page.on('dialog', dialog => dialog.accept());
  let response;
  try {
    response = await page.goto(testUrl, { waitUntil: 'networkidle', timeout: 45000 });
    await page.getByText('Learn by building', { exact: false }).first().waitFor();
    await page.getByLabel('Trace-table blank').fill('value');
    await page.getByLabel('Lesson reflection').fill('I traced the loop and compared index with value.');
    await page.getByText('Save evidence for teacher review').click();
    await page.getByLabel('Switch to teacher demo view').click();
    await page.getByText('Teacher review queue', { exact: false }).first().waitFor();
    await page.getByText('Approve mastery').click();
    await page.getByText('Status: approved', { exact: false }).first().waitFor();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    const title = await page.title();
    const headers = response?.headers() || {};
    const requiredHeaders = ['x-content-type-options', 'referrer-policy'];
    const missingHeaders = requiredHeaders.filter(name => !headers[name]);
    const pass = Boolean(response && response.status() < 400 && title.includes('Algorithm Academy') && !overflow && errors.length === 0 && missingHeaders.length === 0);
    failed ||= !pass;
    results.push({ viewport: viewport.name, dimensions: `${viewport.width}x${viewport.height}`, url: page.url(), status: response?.status(), title, overflow, errors, missing_headers: missingHeaders, classroom_flow: pass, pass });
  } catch (error) {
    failed = true;
    results.push({ viewport: viewport.name, dimensions: `${viewport.width}x${viewport.height}`, url: page.url(), status: response?.status() ?? null, errors, error: error.message, pass: false });
  }
  await context.close();
}
await browser.close();
const output = { generated_at: new Date().toISOString(), deployment, passed: results.filter(result => result.pass).length, count: results.length, results };
fs.writeFileSync('browser-smoke-results.json', `${JSON.stringify(output, null, 2)}\n`);
console.log(JSON.stringify(output));
if (failed) process.exit(1);