#!/opt/data/.venvs/google-oauth-browser/bin/python
from __future__ import annotations
import json, os, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

PROFILE_ENV = {
    "personal-main": ("GOOGLE_PERSONAL_MAIN_EMAIL", "GOOGLE_PERSONAL_MAIN_PASSWORD"),
    "personal-secondary": ("GOOGLE_PERSONAL_SECONDARY_EMAIL", "GOOGLE_PERSONAL_SECONDARY_PASSWORD"),
    "trapiistan": ("GOOGLE_TRAPIISTAN_EMAIL", "GOOGLE_TRAPIISTAN_PASSWORD"),
    "classicalechos": ("GOOGLE_CLASSICALECHOS_EMAIL", "GOOGLE_CLASSICALECHOS_PASSWORD"),
    "burner": ("GOOGLE_BURNER_EMAIL", "GOOGLE_BURNER_PASSWORD"),
}
HELPER = "/opt/data/scripts/google_reauth_workflow.py"
GOOGLE_PYTHON = "/opt/hermes/.venv/bin/python3"
BROWSER_PATH = "/opt/data/cache/ms-playwright"


def run_helper(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([GOOGLE_PYTHON, HELPER, *args], text=True, capture_output=True, timeout=120)


def main() -> int:
    profile = sys.argv[1] if len(sys.argv) > 1 else "personal-main"
    if profile not in PROFILE_ENV:
        print(f"BLOCKED unknown_profile={profile}")
        return 2
    email_key, password_key = PROFILE_ENV[profile]
    email, password = os.getenv(email_key), os.getenv(password_key)
    if not email or not password:
        print(f"BLOCKED profile={profile} reason=missing_environment")
        return 2

    auth = run_helper("workspace-auth-url", profile)
    if auth.returncode:
        print(f"FAILED profile={profile} stage=auth_url")
        return auth.returncode
    try:
        payload = json.loads(auth.stdout)
        auth_url = payload[profile]["auth_url"]
    except Exception:
        print(f"FAILED profile={profile} stage=parse_auth_url")
        return 2

    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = BROWSER_PATH
    callback = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(locale="en-US")
        page = context.new_page()
        try:
            try:
                page.goto(auth_url, wait_until="domcontentloaded", timeout=60000)
            except PlaywrightTimeoutError:
                pass
            if page.locator('input[type="email"]').count():
                email_input = page.locator('input[type="email"]').first
                email_input.fill(email)
                email_input.press("Enter")
                page.wait_for_timeout(1500)
                if page.locator('input[type="email"]').count():
                    page.get_by_role("button", name="Next", exact=True).click(timeout=10000)
                    page.wait_for_timeout(1500)
                page.locator('input[name="Passwd"]:visible, input[type="password"]:visible').first.wait_for(state="visible", timeout=15000)
            password_input = page.locator('input[name="Passwd"]:visible, input[type="password"]:visible').first
            if password_input.count():
                password_input.fill(password, timeout=10000)
                password_input.press("Enter")
                page.wait_for_timeout(2500)
                if page.locator('input[name="Passwd"]:visible, input[type="password"]:visible').count():
                    page.get_by_role("button", name="Next", exact=True).click(timeout=10000)
                    page.wait_for_timeout(2500)

            deadline = time.time() + 90
            while time.time() < deadline:
                if page.url.startswith("http://localhost") and "code=" in page.url:
                    callback = page.url
                    break
                acted = False
                for selector in [
                    'button:has-text("Continue")',
                    'button:has-text("Allow")',
                    'button:has-text("Accept")',
                    'button:has-text("Confirm")',
                ]:
                    loc = page.locator(selector)
                    if loc.count() and loc.first.is_visible():
                        loc.first.click(); acted = True; page.wait_for_timeout(1500); break
                if not acted:
                    page.wait_for_timeout(1000)
            if not callback:
                title = (page.title() or "").replace("\n", " ")[:80]
                snapshot_dir = Path("/opt/data/cache/oauth-debug")
                snapshot_dir.mkdir(parents=True, exist_ok=True)
                snapshot = snapshot_dir / f"{profile}-blocked.png"
                page.screenshot(path=str(snapshot), full_page=True)
                os.chmod(snapshot, 0o600)
                print(f"BLOCKED profile={profile} stage=browser title={title!r} url_host={page.url.split('/')[2] if '://' in page.url else 'unknown'} snapshot={snapshot}")
                return 3
        finally:
            browser.close()

    exchanged = run_helper("workspace-exchange", profile, callback)
    if exchanged.returncode:
        print(f"FAILED profile={profile} stage=exchange")
        return exchanged.returncode
    verified = run_helper("verify", "workspace", profile)
    if verified.returncode:
        print(f"FAILED profile={profile} stage=verify")
        return verified.returncode
    print(f"AUTHENTICATED profile={profile}")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        # Never serialize browser exceptions: Playwright call logs may contain
        # values entered into form fields.
        print("FAILED stage=browser_automation reason=redacted_exception")
        raise SystemExit(1)
