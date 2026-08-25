import { chromium, devices } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const previewUrl = process.argv[2] || 'http://127.0.0.1:4174/';
const evidenceDir = path.resolve('preview-evidence');
await fs.mkdir(evidenceDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ ...devices['iPhone 14'], colorScheme: 'light' });
const page = await context.newPage();
await page.goto(previewUrl, { waitUntil: 'networkidle' });
await page.evaluate(() => localStorage.setItem('combatatlas.visualTheme', 'real-photography'));
await page.reload({ waitUntil: 'networkidle' });
await page.waitForTimeout(1500);
for (const y of [900, 1800, 3000, 4200, 5400, 0]) {
  await page.evaluate((scrollY) => window.scrollTo(0, scrollY), y);
  await page.waitForTimeout(350);
}
const screenshotPath = path.join(evidenceDir, 'iphone-real-photography-curated.png');
await page.screenshot({ path: screenshotPath, fullPage: true });

const cards = await page.locator('.art-card').evaluateAll((nodes) => nodes.map((card) => {
  const img = card.querySelector('img');
  return {
    name: card.innerText.trim(),
    alt: img?.getAttribute('alt'),
    currentSrc: img?.currentSrc || img?.src,
  };
}));
const dimensions = await page.evaluate(() => ({ width: window.innerWidth, height: document.documentElement.scrollHeight, devicePixelRatio: window.devicePixelRatio }));
await fs.writeFile(path.join(evidenceDir, 'iphone-real-photography-curated.json'), JSON.stringify({ previewUrl, dimensions, cards }, null, 2));
await browser.close();
console.log(JSON.stringify({ screenshotPath, manifestPath: path.join(evidenceDir, 'iphone-real-photography-curated.json'), dimensions, cardCount: cards.length }, null, 2));
