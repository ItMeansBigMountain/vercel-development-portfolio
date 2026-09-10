const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1440, height: 900 });

  const baseUrl = process.env.BASE_URL || 'https://algorithm-academy.vercel.app';
  await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 30000 });

  const navLinks = await page.$$('nav a, header a, [role="navigation"] a');
  if (navLinks.length === 0) {
    const result = { status: 'failed', reason: 'no-nav-links', url: page.url() };
    const fs = require('fs');
    fs.writeFileSync('desktop-functionality.json', JSON.stringify(result, null, 2));
    console.log(JSON.stringify(result));
    await browser.close();
    process.exit(1);
  }
  await navLinks[0].click();
  await page.waitForLoadState('networkidle', { timeout: 15000 });
  const result = { navLinks: navLinks.length, finalUrl: page.url(), status: 'passed' };
  await browser.close();
  const fs = require('fs');
  fs.writeFileSync('desktop-functionality.json', JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result));
  process.exit(0);
})().catch(err => { console.error(err.message); process.exit(1); });
