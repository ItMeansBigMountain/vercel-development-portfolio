const { test, expect } = require('playwright/test');

const url = process.env.JOURNAL_AI_URL || 'https://journal-bshzaek8o-itmeansbigmountains-projects.vercel.app';
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;

test.use({ launchOptions: executablePath ? { executablePath } : {} });

for (const viewport of [{ name: 'mobile', width: 390, height: 844 }, { name: 'desktop', width: 1440, height: 900 }]) {
test(`Journal AI preview core flow (${viewport.name})`, async ({ page }) => {
  await page.setViewportSize(viewport);
  const fixture = `browser-smoke-${viewport.name}-${Date.now()}`;
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('pageerror', error => pageErrors.push(error.message));

  const response = await page.goto(url, { waitUntil: 'networkidle' });
  expect(response?.status()).toBe(200);
  await expect(page.getByText('Journal AI')).toBeVisible();
  await expect(page.getByText('PRIVATE BY DEFAULT')).toBeVisible();
  await page.screenshot({ path: `journal-ai-smoke-${viewport.name}-initial.png`, fullPage: true });

  await page.getByLabel('Private journal entry').fill(fixture);
  await page.getByText('good', { exact: true }).click();
  await page.getByText('Save privately', { exact: true }).click();
  await expect(page.getByText(fixture, { exact: true })).toBeVisible();
  await expect(page.getByText(/1 local changes/)).toBeVisible();

  await page.getByText('settings', { exact: true }).click();
  await expect(page.getByText('Privacy & portability')).toBeVisible();
  await expect(page.getByText(fixture, { exact: false })).toBeVisible();
  await page.screenshot({ path: `journal-ai-smoke-${viewport.name}-settings.png`, fullPage: true });

  await page.reload({ waitUntil: 'networkidle' });
  await page.getByText('journal', { exact: true }).click();
  await expect(page.getByText(fixture, { exact: true })).toBeVisible();
  await page.getByText('Remove from this device', { exact: true }).click();
  await expect(page.getByText(fixture, { exact: true })).toHaveCount(0);

  await page.getByText('settings', { exact: true }).click();
  await expect(page.getByText(fixture, { exact: false })).toHaveCount(0);
  await page.screenshot({ path: `journal-ai-smoke-${viewport.name}-final.png`, fullPage: true });

  const hasOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(hasOverflow).toBe(false);

  expect(pageErrors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  console.log(JSON.stringify({ url, viewport, fixture, httpStatus: response?.status(), hasOverflow, pageErrors, consoleErrors }));
});
}
