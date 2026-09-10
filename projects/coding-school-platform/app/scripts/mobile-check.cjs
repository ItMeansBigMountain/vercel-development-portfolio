// Mobile viewport check via Playwright (375x667)
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({
    width: parseInt(process.env.VIEWPORT_WIDTH || '375', 10),
    height: parseInt(process.env.VIEWPORT_HEIGHT || '667', 10),
  });

  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));

  const baseUrl = process.env.BASE_URL || 'https://algorithm-academy.vercel.app';
  console.error('[mobile-check] Navigating to', baseUrl);
  await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 30000 });

  const title = await page.title();

  // Check for horizontal overflow
  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  const innerWidth = await page.evaluate(() => window.innerWidth);

  const result = {
    viewport: `${process.env.VIEWPORT_WIDTH || '375'}x${process.env.VIEWPORT_HEIGHT || '667'}`,
    title,
    scrollWidth,
    innerWidth,
    horizontalOverflow: scrollWidth > innerWidth,
    errors,
    status: scrollWidth <= innerWidth && errors.length === 0 ? 'passed' : 'failed',
  };

  await browser.close();

  const fs = require('fs');
  fs.writeFileSync('mobile-viewport.json', JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result));
  process.exit(result.status === 'passed' ? 0 : 1);
})().catch((err) => {
  console.error('[mobile-check] ERROR:', err.message);
  console.log(JSON.stringify({ status: 'failed', error: err.message }));
  process.exit(1);
});
