const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({
    width: parseInt(process.env.VIEWPORT_WIDTH || '1440', 10),
    height: parseInt(process.env.VIEWPORT_HEIGHT || '900', 10),
  });

  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));

  const baseUrl = process.env.BASE_URL || 'https://algorithm-academy.vercel.app';
  await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 30000 });

  const title = await page.title();
  const h1 = await page.$eval('h1', el => el.textContent).catch(() => 'no-h1');

  const result = {
    viewport: `${process.env.VIEWPORT_WIDTH || '1440'}x${process.env.VIEWPORT_HEIGHT || '900'}`,
    title,
    h1,
    errors,
    status: (title && title.length > 0) ? 'passed' : 'failed',
  };

  await browser.close();
  const fs = require('fs');
  fs.writeFileSync('desktop-viewport.json', JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result));
  process.exit(result.status === 'passed' ? 0 : 1);
})().catch(err => { console.error(err.message); process.exit(1); });
