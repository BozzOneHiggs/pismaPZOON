from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:8000')
        page.wait_for_load_state('domcontentloaded')

        # Bypass login
        page.evaluate("document.getElementById('authContainer').style.display = 'none';")
        page.evaluate("document.getElementById('appContainer').style.display = 'block';")
        page.evaluate("document.getElementById('appContainer').classList.remove('hidden');")

        # Test 1: Uppercase input
        dotyczy = page.locator('#dotyczy_potwierdzenia')
        uwagi = page.locator('#uwagi_potwierdzenia')

        dotyczy.fill('test dotyczy')
        uwagi.fill('test uwagi')

        # Switch tab to response
        page.evaluate("document.getElementById('tabButtonResponse').click();")

        # Take screenshot
        page.screenshot(path='verification/verification.png')

        browser.close()

if __name__ == '__main__':
    verify()
