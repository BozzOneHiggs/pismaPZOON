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

        # Navigate to Response tab
        page.evaluate("document.getElementById('tabButtonResponse').click();")

        # Check if checkbox exists (it shouldn't yet)
        if page.locator('#odp_odwolanie').count() > 0:
            print("Checkbox already exists (unexpected before changes).")
        else:
            print("Checkbox does not exist yet (expected).")

        browser.close()

if __name__ == '__main__':
    verify()
