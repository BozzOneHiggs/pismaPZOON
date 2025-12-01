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

        # Explicitly switch to envelopes to trigger the toggle button visibility
        # (This mimics what onAuthStateChanged does)
        print("Switching to Envelopes tab...")
        page.evaluate("document.getElementById('tabButtonEnvelopes').click();")

        # 1. Verify Toggle Button Visibility on Envelopes Tab
        toggle_btn = page.locator('#toggleMailMergeButton')
        if toggle_btn.is_visible():
            print("Toggle button visible.")
        else:
            print("Error: Toggle button NOT visible.")

        # 2. Switch Tab and Verify Hiding
        print("Switching to Support tab...")
        page.evaluate("document.getElementById('tabButtonSupport').click();")
        if not toggle_btn.is_visible():
            print("Toggle button hidden on Support tab.")
        else:
            print("Error: Toggle button STILL visible on Support tab.")

        # 3. Switch Back
        print("Switching back to Envelopes tab...")
        page.evaluate("document.getElementById('tabButtonEnvelopes').click();")
        if toggle_btn.is_visible():
            print("Toggle button visible again.")
        else:
            print("Error: Toggle button NOT visible after return.")

        # 4. Open Sidebar
        print("Opening sidebar...")
        toggle_btn.click()
        sidebar = page.locator('#mailMergeSidebar')
        page.wait_for_timeout(500)

        sidebar_class = sidebar.get_attribute('class')
        if '-translate-x-full' not in sidebar_class:
             print("Sidebar opened.")
        else:
             print(f"Error: Sidebar did not open. Class: {sidebar_class}")

        # 5. Verify Elements
        if page.locator('#mailMergeSearch').is_visible():
            print("Search input visible.")
        if page.locator('#mailMergePrintEnvelopesButton').is_visible():
            print("Print Envelopes button visible.")

        # 6. Close Sidebar
        print("Closing sidebar...")
        page.locator('#closeMailMergeButton').click()
        page.wait_for_timeout(500)
        sidebar_class = sidebar.get_attribute('class')
        if '-translate-x-full' in sidebar_class:
             print("Sidebar closed.")
        else:
             print("Error: Sidebar NOT closed.")

        page.screenshot(path='verification/mail_merge_final.png')
        browser.close()

if __name__ == '__main__':
    verify()
