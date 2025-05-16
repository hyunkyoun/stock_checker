import asyncio
import aiohttp
import uuid
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import re
import json
import random
import os
from dotenv import load_dotenv
from fake_useragent import UserAgent

load_dotenv()

def generate_visitor_id():
    return uuid.uuid4().hex.upper()

def extract_product_id(url):
    match = re.search(r'/A-(\d+)', url)
    return match.group(1) if match else None

def send_embed(url, name, sku, cart_type):
    webhook_url = os.getenv("TARGET_WEBHOOK")
    webhook = DiscordWebhook(
        url=webhook_url,
        username="Target Stock Monitor",
    )

    embed = DiscordEmbed(title="Target Stock Notification", description=f"[{name}]({url})", color=0x00FF00)
    embed.add_embed_field(name="SKU", value=f"{sku}")

    if cart_type == "atc":
        embed.add_embed_field(name="Product Status", value="Available Now")
    elif cart_type == "pre":
        embed.add_embed_field(name="Product Status", value="Pre-Order")

    embed.set_footer(text=f"{datetime.now().strftime('%H:%M:%S')}")
    webhook.add_embed(embed)

    response = webhook.execute()
    if response.status_code == 200:
        print(f"Notification sent for {name} ({sku})")
    else:
        print(f"Failed to send for {name} - Status Code: {response.status_code}")

async def is_in_stock(session, tcin: str, location_id: str = "1263", scheduled_store_id: str = "3329"):
    
    ua = UserAgent()

    url = "https://redsky.target.com/redsky_aggregations/v1/web/product_fulfillment_and_variation_hierarchy_v1"
    params = {
        "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
        "latitude": "40.862661",
        "longitude": "-73.967577",
        "scheduled_delivery_store_id": scheduled_store_id,
        "state": "NJ",
        "zip": "07024",
        "store_id": location_id,
        "paid_membership": "false",
        "base_membership": "true",
        "card_membership": "false",
        "is_bot": "false",
        "tcin": tcin,
        "visitor_id": generate_visitor_id(),
        "channel": "WEB",
        "page": f"/p/A-{tcin}"
    }

    useragent = ua.random

    headers = {
        "User-Agent": useragent
    }

    print(useragent)

    try:
        async with session.get(url, headers=headers, params=params, timeout=10) as response:
            data = await response.json()
            fulfillment = data["data"]["product"]["fulfillment"]

            return {
                "shipping": fulfillment["shipping_options"]["availability_status"],
                "pickup": fulfillment["store_options"][0]["order_pickup"]["availability_status"],
                "scheduled_delivery": fulfillment["scheduled_delivery"]["availability_status"]
            }
    except Exception as e:
        print(f"Error checking product {tcin}: {e}")
        return None

async def check_product(session, product):
    url = product['url']
    name = product['name']
    sku = extract_product_id(url)
    print(f"Checking {name} ({sku})...")

    stock = await is_in_stock(session, sku)
    if not stock:
        return

    if stock['shipping'] == "IN_STOCK":
        send_embed(url, name, sku, "atc")
        print("In Stock!")
    elif stock['shipping'] == "PRE_ORDER_SELLABLE":
        send_embed(url, name, sku, "pre")
        print("Pre-Order!")
    else:
        print("Out of stock.")

async def run_batches(products, batch_size=3, delay_between_batches=2):
    connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        batches = [products[i:i+batch_size] for i in range(0, len(products), batch_size)]
        
        for batch_index, batch in enumerate(batches):
            print(f"\nStarting Batch {batch_index + 1}")
            tasks = [check_product(session, p) for p in batch]
            await asyncio.gather(*tasks)
            if batch_index < len(batches) - 1:
                await asyncio.sleep(delay_between_batches)

async def main_loop():
    with open('./productPages/target_product_pages.json', 'r') as f:
        data = json.load(f)

    target_product_pages = data['product_pages']

    while True:
        await run_batches(target_product_pages, batch_size=3, delay_between_batches=2)
        print("\nWaiting 4-7 seconds before next full check...\n")
        await asyncio.sleep(random.randint(5, 10))

if __name__ == "__main__":
    asyncio.run(main_loop())