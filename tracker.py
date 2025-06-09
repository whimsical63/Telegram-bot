from playwright.sync_api import sync_playwright

def get_shopee_price(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)

        try:
            title = page.locator(".vR6K3w").inner_text()
            price_text = page.locator(".IZPeQz B67UQ0").inner_text()
        except:
            browser.close()
            return None, None

        browser.close()
        try:
            price = float(price_text.replace("₱", "").replace(",", "").strip())
        except:
            price = price_text  # fallback if conversion fails

        return title, price
