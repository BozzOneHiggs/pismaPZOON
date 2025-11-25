import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:8000")

        # Pomiń logowanie przez bezpośrednią manipulację DOM
        await page.evaluate("""
            document.getElementById('authContainer').style.display = 'none';
            document.getElementById('appContainer').style.display = 'block';
        """)

        await expect(page.locator("#appContainer")).to_be_visible()

        # 1. Weryfikacja wyglądu - zrzut ekranu strony głównej
        await page.screenshot(path="final_app_view.png")

        # 2. Weryfikacja wizualna automatycznej zmiany na wielkie litery
        dotyczy_input = page.locator("#dotyczy_potwierdzenia")
        uwagi_input = page.locator("#uwagi_potwierdzenia")

        await dotyczy_input.fill("test dotyczy")
        await uwagi_input.fill("test uwagi")

        # Zrób zrzut ekranu samego formularza, aby wizualnie zweryfikować zmianę
        await page.locator("#envelopeForm").screenshot(path="form_screenshot.png")

        # 3. Weryfikacja modala kodów pocztowych
        await page.click("#managePostOfficesButton")
        await expect(page.locator("#postOfficeModal")).to_be_visible()

        # Zrób zrzut ekranu modala
        await page.locator("#postOfficeModal").screenshot(path="modal_screenshot.png")

        await page.locator("#postOfficeKod").fill("00-999")
        await page.locator("#postOfficePoczta").fill("Testowa Poczta")

        print("Kroki weryfikacyjne wykonane. Sprawdź zrzuty ekranu.")

        await browser.close()

asyncio.run(main())
