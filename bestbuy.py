import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import re
from fake_useragent import UserAgent
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import time
import random
import json
import itertools
    
HOME_PAGE_URL = "https://www.bestbuy.com/"

def get_next_proxy():
    selected_proxy = next(proxy_cycle)
    return {
        "server": f"http://{selected_proxy['ip']}:{selected_proxy['port']}",
        "username": selected_proxy["username"],
        "password": selected_proxy["password"]
    }

async def check_stock(sku):
    print(f"Checking stock for SKU: {sku}")

    proxy = get_next_proxy()
    print(f"Using proxy: {proxy['server']}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            proxy=proxy,
            headless=False, 
            args=["--disable-blink-features=AutomationControlled"]  # Hides automation traces
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            java_script_enabled=True
        )
        page = await context.new_page()
        
        await stealth_async(page)  # Apply stealth mode

        try:
            await page.goto(HOME_PAGE_URL, wait_until="domcontentloaded")

            try:
                usa_button = await page.wait_for_selector('img[alt="United States"]', timeout=3000)  # Wait 3s max
                if usa_button:
                    print("Country selection detected. Clicking 'United States'...")
                    await usa_button.click()
                    await page.wait_for_timeout(random.randint(2000, 4000))  # Wait for transition
            except:
                print("No country selection popup detected. Continuing...")

            search_input_selector = "input#gh-search-input.search-input.search-input-default"

            # Simulate human-like interaction
            await page.mouse.move(random.randint(100, 300), random.randint(100, 300))
            await page.wait_for_timeout(random.randint(1000, 3000))  # Wait like a human

            # Ensure search bar is available
            search_bar = await page.wait_for_selector(search_input_selector)

            if search_bar:
                print("Search bar found.")

                await page.click(search_input_selector, delay=random.randint(100, 150))  # Mimic a human click
                await page.wait_for_timeout(random.randint(100, 200))  # Short pause
                await page.type(search_input_selector, sku, delay=random.randint(150, 250))  # Slower typing
                await page.press(search_input_selector, "Enter")
                await page.wait_for_load_state("domcontentloaded")

                addtocart_button_selector = "[data-button-state='ADD_TO_CART']"
                oos_button_selector = "[data-button-state='SOLD_OUT']"
                comingsoon_button_selector = "[data-button-state='COMING_SOON']"
                preorder_button_selector = "[data-button-state='PRE_ORDER']"

                await page.mouse.wheel(0, 300)  # Scroll down a bit

                await page.wait_for_timeout(random.randint(200, 400))  # Pause before checking buttons

                if await page.locator(addtocart_button_selector).first.is_visible():
                    print("Add to Cart button found! Clicking it...")
                    return True, page.url, "atc"
                elif await page.locator(preorder_button_selector).first.is_visible():
                    print("Item is available for Pre-Order.")
                    return True, page.url, "pre"
                
                elif await page.locator(oos_button_selector).first.is_visible():
                    print("Item is Sold Out.")
                elif await page.locator(comingsoon_button_selector).first.is_visible():
                    print("Item is Coming Soon.")

                return False, page.url, ""

        except asyncio.TimeoutError:
            print("Timeout: Button not found. Product might be unavailable.")
            return False, page.url, ""
        except Exception as e:
            print(f"Error: {e}")
            return False, page.url, ""
        finally:
            await browser.close()


'''
DISCORD EMBED CODE BELOW
'''


BESTBUY_SKUS = [
    "6621081",
    "6609201",
    "6590379",
]

BESTBUY_NAMES = [
    "Pokémon TCG - Prismatic Evolutions Super-Premium Collection",
    "Pokémon TCG - Blooming Waters Premium Collection",
    "Pokémon TCG - Charizard ex Super-Premium Collection",
]

# def send_embed(url, name, sku, cart_type):
#     webhook_url = ""
#     webhook = DiscordWebhook(
#         url=webhook_url,
#         username="BestBuy Monitor",
#     )

#     embed = DiscordEmbed(title="BestBuy Stock Notification", description=f"[{name}]({url})", color=0x00FF00)
#     embed.add_embed_field(name="SKU", value=f"{sku}")

#     if cart_type == "atc":
#         embed.add_embed_field(name="Product Status", value="Available Now")
#     elif cart_type == "pre":
#         embed.add_embed_field(name="Product Status", value="Pre-Order")

#     embed.set_footer(text=f"{datetime.now().strftime('%H:%M:%S')}")

#     webhook.add_embed(embed)
#     response = webhook.execute()

#     if response.status_code == 200:
#         print("Message sent successfully!")
#     else:
#         print("Failed to send message. Status code: ", response.status_code)

# async def check_all_targets():
#     tasks = []
#     for i in range(len(BESTBUY_SKUS)):
#         tasks.append(check_and_notify(BESTBUY_SKUS[i], BESTBUY_NAMES[i]))
    
#     await asyncio.gather(*tasks)

# async def check_and_notify(sku, name):
#     in_stock, page_url, cart_type = await check_stock(sku)
#     if in_stock:
#         send_embed(page_url, name, sku, cart_type)


# # main function
# def run_bot():
#     while True:
#         asyncio.run(check_all_targets())  # Run all checks in parallel
#         time.sleep(random.randint(5, 10))  # Delay before the next round of checks

if __name__ == "__main__":

    with open("proxies.json", "r") as file:
        proxies = json.load(file)["proxies"]

    proxy_cycle=itertools.cycle(proxies)

    run_bot()