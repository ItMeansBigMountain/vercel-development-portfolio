// Mobile interaction check via Playwright (375x667)
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({
    width: parseInt(process.env.VIEWPORT_WIDTH || '375', 10),
    height: parseInt(process.env.VIEWPORT_HEIGHT || '667', 10),
  });

  const baseUrl = process.env.BASE_URL || 'https://algorithm-academy.vercel.app';
  console.error('[mobile-interaction] Navigating to', baseUrl);
  await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 30000 });

  // Try to find a link and click it
  const links = await page.$$('a, button, [role="button"]');
  if (links.length === 0) {
    const result = { status: 'failed', reason: 'no-interactive-elements', url: page.url() };
    const fs = require('fs');
    fs.writeFileSync('mobile-interaction.json', JSON.stringify(result, null, 2));
    console.log(JSON.stringify(result));
    await browser.close();
    process.exit(1);
  }

  const initialUrl = page.url();
  await links[0].click();
  await page.waitForLoadState('networkidle', { timeout: 10000 });
  const finalUrl = page.url();

  const result = {
    viewport: `${process.env.VIEWPORT_WIDTH || '375'}x${process.env.VIEWPORT_HEIGHT || '667'}`,
    linksFound: links.length,
    navigated: finalUrl !== initialUrl,
    initialUrl,
    finalUrl,
    status: 'passed',
  };

  await browser.close();

  const fs = require('fs');
  fs.writeFileSync('mobile-interaction.json', JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result));
  process.exit(0);
})().catch((err) => {
  console.error('[mobile-interaction] ERROR:', err.message);
  console.log(JSON.stringify({ status: 'failed', error: err.message }));
  process.exit(1);
});
