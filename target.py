import asyncio
from playwright.async_api import async_playwright
import re
from fake_useragent import UserAgent

ua = UserAgent()

def extract_product_id(url: str) -> str:
    match = re.search(r'/A-(\d+)', url)
    return match.group(1) if match else None

async def check_stock(url):
    product_sku = extract_product_id(url)

    print(f"Checking stock for URL: {url}")
    print(f"Checking stock for SKU: {product_sku}")

    async with async_playwright() as p:
        user_agent = ua.random

        browser = await p.chromium.launch(headless=True)  
        context = await browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1280, "height": 720},  
            java_script_enabled=True 
        )
        page = await context.new_page()

        print(f"Checking with user agent: {user_agent}")

        try:
            await page.goto(url, wait_until="domcontentloaded")

            addtocart_selector = f"button#addToCartButtonOrTextIdFor{product_sku}"
            button = await page.wait_for_selector(addtocart_selector)

            if button:
                is_enabled = await button.is_enabled()
                if is_enabled:
                    print("Product is in stock!")
                    return True
                else:
                    print("Product is out of stock.")
                    return False
        except asyncio.TimeoutError:
            print("Timeout: Button not found. Product might be unavailable.")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check_stock("https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab"))