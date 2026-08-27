#!/usr/bin/env python3
"""hCaptcha Accessibility Signup - runs in the google-oauth-browser venv"""
import asyncio
from playwright.async_api import async_playwright

async def signup_hcaptcha():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/opt/data/cache/ms-playwright/chromium-1234/chrome-linux64/chrome",
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        
        try:
            await page.goto("https://dashboard.hcaptcha.com/welcome_accessibility", wait_until="networkidle", timeout=60000)
            # Wait for React app to render - look for the login form
            await page.wait_for_selector('[data-cy="sso-option-standard"], button:has-text("Continue with Email"), input[type="email"]', timeout=30000)
            print("Page title:", await page.title())
            print("URL:", page.url)
            content = await page.content()
            print("Content length:", len(content))
            
            # Save full page for analysis
            with open("/opt/data/cache/hcaptcha_page.html", "w") as f:
                f.write(content)
            
            # Look for signup/login forms
            if "sign" in content.lower() or "register" in content.lower() or "email" in content.lower():
                print("Found signup/login indicators")
                forms = await page.query_selector_all("form")
                print(f"Forms found: {len(forms)}")
                for i, form in enumerate(forms):
                    inputs = await form.query_selector_all("input")
                    print(f"  Form {i}: {len(inputs)} inputs")
                    for inp in inputs:
                        name = await inp.get_attribute("name")
                        type_attr = await inp.get_attribute("type")
                        placeholder = await inp.get_attribute("placeholder")
                        print(f"    input: name={name}, type={type_attr}, placeholder={placeholder}")
            
            # Also look for buttons
            buttons = await page.query_selector_all("button, [role=button]")
            print(f"Buttons found: {len(buttons)}")
            for btn in buttons:
                text = await btn.inner_text()
                data_cy = await btn.get_attribute("data-cy")
                print(f"  Button: text='{text[:50]}', data-cy={data_cy}")
            
            # Click "Sign in with Github"
            github_btn = await page.query_selector('button:has-text("Sign in with Github")')
            if github_btn:
                print("Clicking GitHub sign-in...")
                await github_btn.click()
                await page.wait_for_load_state("networkidle", timeout=30000)
                print("After GitHub click - URL:", page.url)
                print("After GitHub click - Title:", await page.title())
                content = await page.content()
                with open("/opt/data/cache/hcaptcha_github_page.html", "w") as f:
                    f.write(content)
                print("Content length:", len(content))
            else:
                print("GitHub button not found with text selector, trying alternative...")
                # Try clicking by text content
                github_btn = await page.query_selector('text="Sign in with Github"')
                if github_btn:
                    print("Found with text= selector")
                    await github_btn.click()
                    await page.wait_for_load_state("networkidle", timeout=30000)
                    print("After GitHub click - URL:", page.url)
                else:
                    # Try XPath
                    github_btn = await page.query_selector('xpath=//button[contains(text(), "Github")]')
                    if github_btn:
                        print("Found with XPath")
                        await github_btn.click()
                        await page.wait_for_load_state("networkidle", timeout=30000)
                        print("After GitHub click - URL:", page.url)
                    else:
                        print("Could not find GitHub button")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(signup_hcaptcha())