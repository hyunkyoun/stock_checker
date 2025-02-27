import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import re
import random

TARGET_URLS = [
    "https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab",
    "https://www.target.com/p/pok-233-mon-trading-card-game-zapdos-ex-deluxe-battle-deck/-/A-91351689#lnk=sametab",
]

RETRY_TIMING = 5  # Retry interval in seconds

def extract_product_id(url: str) -> str:
    match = re.search(r'/A-(\d+)', url)
    return match.group(1) if match else None

def calculate_mb(bytes):
    """Converts bytes to MB."""
    return bytes / (1024 * 1024)

def fetch_with_proxy(proxy, url):
    """Measures the data usage (MB) when loading a webpage, using a proxy if provided."""
    with sync_playwright() as p:
        browser = p.chromium.launch(proxy={"server": proxy} if proxy else None, headless=True)
        context = browser.new_context()
        page = context.new_page()

        total_bytes = 0

        def track_request(request):
            nonlocal total_bytes
            if request.headers.get("content-length"):
                total_bytes += int(request.headers["content-length"])

        def track_response(response):
            nonlocal total_bytes
            if response.headers.get("content-length"):
                total_bytes += int(response.headers["content-length"])

        # Listen for network events
        page.on("request", track_request)
        page.on("response", track_response)

        # Visit the target website
        page.goto(url, wait_until="load")

        # Close browser
        browser.close()

        return calculate_mb(total_bytes)

async def check_stock(url, browser):
    product_sku = extract_product_id(url)

    print(f"Checking stock for URL: {url}")
    print(f"Checking stock for SKU: {product_sku}")

    context = await browser.new_context(
        user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.0.0 Safari/537.36"
    )
    page = await context.new_page()

    try:
        await page.goto(url, wait_until="domcontentloaded")

        # Measure data usage
        page_size_mb = fetch_with_proxy(None, url)  # No proxy in this case
        print(f"Data usage for {url}: {page_size_mb:.2f} MB")

        addtocart_selector = f"button#addToCartButtonOrTextIdFor{product_sku}"

        try:
            await page.wait_for_selector(addtocart_selector, timeout=2000)
            button = await page.query_selector(addtocart_selector)
            if button and await button.is_enabled():
                print("In stock")
                return True
            else:
                print("Out of stock")
                return False
        except:
            print("Unknown stock status")

    finally:
        await page.close()
        await context.close()

async def check_stock_main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for url in TARGET_URLS:
            await check_stock(url, browser)
        
        await browser.close()

        print(f"Retrying all URLs in {RETRY_TIMING} seconds...\n")
        await asyncio.sleep(RETRY_TIMING)
        await check_stock_main()  # Loop for continuous checking

if __name__ == "__main__":
    asyncio.run(check_stock_main())