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

        # 1. Check if new fields exist
        checkbox = page.locator('#odp_odwolanie')
        data_odwolania = page.locator('#odp_data_odwolania')
        data_wyslania = page.locator('#odp_data_wyslania_odwolania')
        data_prawomocnosci = page.locator('#odp_data_prawomocnosci')

        if checkbox.count() > 0 and data_odwolania.count() > 0 and data_wyslania.count() > 0:
            print("New fields found.")
        else:
            print("Error: New fields NOT found.")
            browser.close()
            return

        # 2. Test interaction
        print("Testing interaction...")
        # Initial state: checkbox unchecked, prawomocnosc enabled
        if not checkbox.is_checked() and data_prawomocnosci.is_enabled():
            print("Initial state correct.")
        else:
            print("Error: Initial state incorrect.")

        # Check the box
        checkbox.check()

        # Verify prawomocnosc is disabled and cleared (if it had value)
        # First fill it to test clearing
        checkbox.uncheck()
        data_prawomocnosci.fill('2023-01-01')
        checkbox.check()

        if not data_prawomocnosci.is_enabled():
            print("Data prawomocnosci disabled when checked.")
        else:
            print("Error: Data prawomocnosci NOT disabled.")

        val = data_prawomocnosci.input_value()
        if val == '':
            print("Data prawomocnosci cleared.")
        else:
            print(f"Error: Data prawomocnosci NOT cleared. Value: '{val}'")

        # Take screenshot
        page.screenshot(path='verification/appeal_verification.png')
        print("Screenshot saved.")

        browser.close()

if __name__ == '__main__':
    verify()
