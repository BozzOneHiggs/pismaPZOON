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

        # 1. Verify Toggle Button Visibility on Envelopes Tab
        toggle_btn = page.locator('#toggleMailMergeButton')
        if toggle_btn.is_visible():
            print("Toggle button visible on start (Envelopes tab).")
        else:
            print("Error: Toggle button NOT visible on start.")

        # 2. Switch Tab and Verify Hiding
        page.evaluate("document.getElementById('tabButtonSupport').click();")
        if not toggle_btn.is_visible():
            print("Toggle button hidden on Support tab.")
        else:
            print("Error: Toggle button STILL visible on Support tab.")

        # 3. Switch Back
        page.evaluate("document.getElementById('tabButtonEnvelopes').click();")
        if toggle_btn.is_visible():
            print("Toggle button visible again on Envelopes tab.")
        else:
            print("Error: Toggle button NOT visible after return.")

        # 4. Open Sidebar
        toggle_btn.click()
        sidebar = page.locator('#mailMergeSidebar')
        # Wait for transition (using expect or wait_for)
        page.wait_for_timeout(500) # Simple wait for transition

        # Check if translate class removed (meaning visible/active)
        # Note: We check if the sidebar does NOT have '-translate-x-full'
        sidebar_class = sidebar.get_attribute('class')
        if '-translate-x-full' not in sidebar_class:
             print("Sidebar opened (class removed).")
        else:
             print(f"Error: Sidebar did not open. Class: {sidebar_class}")

        # 5. Verify Elements in Sidebar
        if page.locator('#mailMergeSearch').is_visible():
            print("Search input visible.")
        if page.locator('#mailMergePrintEnvelopesButton').is_visible():
            print("Print Envelopes button visible.")

        # 6. Test interaction (Mocking adding list item)
        # Since we can't search without DB data, we simulate adding to the list via JS console
        page.evaluate("""
            const mockItem = { numer_sprawy: 'TEST/123/MOCK', adresat: 'Test Adresat' };
            addToMailMergeList(mockItem);
        """)

        # Verify List Item appears
        list_item = page.locator('#mailMergeList').locator('div', has_text='TEST/123/MOCK')
        if list_item.count() > 0:
            print("Mock item added to list.")
        else:
            print("Error: Mock item NOT added to list.")

        # 7. Close Sidebar
        page.locator('#closeMailMergeButton').click()
        page.wait_for_timeout(500)
        sidebar_class = sidebar.get_attribute('class')
        if '-translate-x-full' in sidebar_class:
             print("Sidebar closed.")
        else:
             print("Error: Sidebar NOT closed.")

        page.screenshot(path='verification/mail_merge_verification.png')
        browser.close()

if __name__ == '__main__':
    verify()
