import asyncio
from playwright.async_api import async_playwright
import re

def extract_product_id(url: str) -> str:
    match = re.search(r'/A-(\d+)', url)
    return match.group(1) if match else None

async def check_stock(url):
    product_sku = extract_product_id(url)

    print(f"Checking stock for URL: {url}")
    print(f"Checking stock for SKU: {product_sku}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        addtocart_selector = f"button#addToCartButtonOrTextIdFor{product_sku}"
        
        try:
            # page.wait_for_selector(addtocart_selector)
            button = await page.query_selector(addtocart_selector)

            if button:
                is_enabled = await button.is_enabled()
                if is_enabled:
                    print("Product is in stock!")
                    return True
                else:
                    print("Product is out of stock.")
                    return False
        except:
            print("unknown stock status")

        html = await page.content()
        await browser.close()

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    asyncio.run(check_stock("https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab"))