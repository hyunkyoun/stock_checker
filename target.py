import asyncio
from playwright.async_api import async_playwright
import re
import random

def extract_product_id(url: str) -> str:
    match = re.search(r'/A-(\d+)', url)
    return match.group(1) if match else None

def calculate_mb(bytes):
    """Converts bytes to MB."""
    return bytes / (1024 * 1024)

async def fetch_with_proxy(proxy, url):
    """Measures the data usage (MB) when loading a webpage, using a proxy if provided."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(proxy={"server": proxy} if proxy else None, headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        total_bytes = 0

        async def track_request(request):
            nonlocal total_bytes
            length = request.headers.get("content-length")
            if length:
                total_bytes += int(length)

        async def track_response(response):
            nonlocal total_bytes
            length = response.headers.get("content-length")
            if length:
                total_bytes += int(length)

        # Listen for network events
        page.on("request", track_request)
        page.on("response", track_response)

        # Visit the target website
        await page.goto(url, wait_until="load")

        # Close browser
        await browser.close()

        return calculate_mb(total_bytes)

async def check_stock(url, browser):
    """Check stock availability and log data usage."""
    product_sku = extract_product_id(url)

    print(f"Checking stock for URL: {url}")
    print(f"Checking stock for SKU: {product_sku}")

    context = await browser.new_context(
        user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.0.0 Safari/537.36"
    )
    page = await context.new_page()

    try:
        await page.goto(url, wait_until="domcontentloaded")

        # Measure data usage using async function
        page_size_mb = await fetch_with_proxy(None, url)  # No proxy in this case
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