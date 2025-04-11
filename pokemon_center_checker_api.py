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
    match = re.search(r'/product/([\d\-]+)/', url)
    if match:
        return match.group(1)
    return None



def send_embed(url, name, sku, cart_type):
    webhook_url = os.getenv("PC_WEBHOOK")
    webhook = DiscordWebhook(
        url=webhook_url,
        username="Pokemon Center Stock Monitor",
    )

    embed = DiscordEmbed(title="Pokemon Center Stock Notification", description=f"[{name}]({url})", color=0x00FF00)
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

async def run_batches(products, batch_size=3, delay_between_batches=2):
    connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        batches = [products[i:i+batch_size] for i in range(0, len(products), batch_size)]
        
        for batch_index, batch in enumerate(batches):
            print(f"\nStarting Batch {batch_index + 1}")
            # tasks = [check_product(session, p) for p in batch]
            # await asyncio.gather(*tasks)
            if batch_index < len(batches) - 1:
                await asyncio.sleep(delay_between_batches)

async def main_loop():
    with open('./productPages/pokemon_center_product_pages.json', 'r') as f:
        data = json.load(f)

    pokemon_center_product_pages = data['product_pages']

    while True:
        await run_batches(pokemon_center_product_pages, batch_size=3, delay_between_batches=2)
        print("\nWaiting 4-7 seconds before next full check...\n")
        await asyncio.sleep(random.randint(4, 7))

if __name__ == "__main__":
    asyncio.run(main_loop())