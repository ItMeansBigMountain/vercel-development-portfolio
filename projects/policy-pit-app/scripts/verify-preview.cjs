const { chromium } = require("playwright");
const fs = require("node:fs");
const path = require("node:path");

const url = process.argv[2];
if (!url) throw new Error("Usage: node scripts/verify-preview.cjs <url>");
const output = path.resolve("artifacts/browser-evidence");
fs.mkdirSync(output, { recursive: true });

const devices = [
  { name: "desktop", viewport: { width: 1440, height: 900 } },
  { name: "mobile", viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
];

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: "/opt/data/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome",
  });
  const checks = [];
  for (const device of devices) {
    const context = await browser.newContext(device);
    const page = await context.newPage();
    const consoleErrors = [];
    const pageErrors = [];
    const failedResponses = [];
    page.on("console", (message) => message.type() === "error" && consoleErrors.push(message.text()));
    page.on("pageerror", (error) => pageErrors.push(String(error)));
    page.on("response", (response) => response.status() >= 400 && failedResponses.push({ status: response.status(), url: response.url() }));
    const response = await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
    await page.getByRole("button", { name: "Prefer Blue" }).click();
    await page.getByRole("button", { name: "Neutral / skip" }).click();
    await page.getByRole("button", { name: "Prefer Red" }).click();
    const result = await page.getByRole("heading", { name: "Your local preview result" }).isVisible();
    await page.getByRole("button", { name: "Try again" }).click();
    const restarted = await page.getByText("1 of 3", { exact: true }).isVisible();
    const metrics = await page.evaluate(() => ({
      title: document.title,
      body: document.body.innerText.replace(/\s+/g, " ").slice(0, 500),
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    const screenshot = path.join(output, `${device.name}.png`);
    await page.screenshot({ path: screenshot, fullPage: true });
    const check = {
      device: device.name,
      viewport: device.viewport,
      status: response?.status() ?? null,
      finalUrl: page.url(),
      ...metrics,
      resultVisible: result,
      restartVerified: restarted,
      horizontalOverflow: metrics.scrollWidth > metrics.clientWidth + 1,
      consoleErrors,
      pageErrors,
      failedResponses,
      screenshot,
    };
    check.passed = check.status === 200 && check.title === "Policy Pit — Development Preview" && result && restarted && !check.horizontalOverflow && !consoleErrors.length && !pageErrors.length && !failedResponses.length;
    checks.push(check);
    await context.close();
  }
  await browser.close();
  const evidence = { url, checks, passed: checks.every((check) => check.passed) };
  fs.writeFileSync(path.join(output, "evidence.json"), `${JSON.stringify(evidence, null, 2)}\n`);
  console.log(JSON.stringify(evidence));
  if (!evidence.passed) process.exitCode = 1;
})();
