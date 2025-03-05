import asyncio
from playwright.async_api import async_playwright
import re
from fake_useragent import UserAgent
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import time

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

        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]  # Hides automation traces
        )  
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


'''
DISCORD EMBED CODE BELOW
'''

TARGET_URLS = [
    "https://www.target.com/p/starburst-easter-original-jellybeans-14oz/-/A-53951890",
    "https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab",
    "https://www.target.com/p/pok-233-mon-trading-card-game-zapdos-ex-deluxe-battle-deck/-/A-91351689#lnk=sametab",
]

TARGET_NAMES = [
    "Starburst Easter Original Jellybeans 14oz",
    "Pokemon Scarlet & Violet S3.5 Booster Bundle Box",
    "Pokemon Trading Card Game: Zapdos-EX Deluxe Battle Deck",
]

def send_embed(url, name, sku):
    webhook_url = "https://discord.com/api/webhooks/1344064369822138419/La7IVFunEqn2iUG9tIcSK-zFQ-QxmlZq2TXUikMK25lYZZAKSOxTw6kVL2vseqzmhXcW"
    webhook = DiscordWebhook(
        url=webhook_url,
        username="Target Monitor",
    )

    embed = DiscordEmbed(title="Target Stock Notification", description=f"[{name}]({url})", color=0x00FF00)
    embed.add_embed_field(name="SKU", value=f"{sku}")
    embed.set_footer(text=f"{datetime.now().strftime('%H:%M:%S')} EST")


    webhook.add_embed(embed)
    response = webhook.execute()

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message. Status code: ", response.status_code)

async def check_all_targets():
    tasks = []
    for i in range(len(TARGET_URLS)):
        tasks.append(check_and_notify(TARGET_URLS[i], TARGET_NAMES[i]))
    
    await asyncio.gather(*tasks)

async def check_and_notify(url, name):
    in_stock = await check_stock(url)
    if in_stock:
        sku = extract_product_id(url)
        send_embed(url, name, sku)

def run_bot():
    while True:
        asyncio.run(check_all_targets())  # Run all checks in parallel
        time.sleep(5)  # Delay before the next round of checks

if __name__ == "__main__":
    run_bot()