import requests
import uuid
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import re
import json
import time
import random
import os
from dotenv import load_dotenv

def generate_visitor_id():
    return uuid.uuid4().hex.upper()

def extract_product_id(url):
    match = re.search(r'/A-(\d+)', url)
    return match.group(1) if match else None

def is_in_stock(tcin: str, location_id: str = "1263", scheduled_store_id: str = "3329"):
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
        "page": "/p/A-" + tcin
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    fulfillment = data["data"]["product"]["fulfillment"]
    
    shipping_status = fulfillment["shipping_options"]["availability_status"]
    pickup_status = fulfillment["store_options"][0]["order_pickup"]["availability_status"]
    scheduled_status = fulfillment["scheduled_delivery"]["availability_status"]

    return {
        "shipping": shipping_status,
        "pickup": pickup_status,
        "scheduled_delivery": scheduled_status
    }

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
        print("Message sent successfully!")
    else:
        print("Failed to send message. Status code: ", response.status_code)

if __name__ == "__main__":
    load_dotenv()

    with open('target_product_pages.json', 'r') as f:
        data = json.load(f)
    
    target_product_pages = data['product_pages']

    while True:
        for product in target_product_pages:
            url = product['url']
            name = product['name']
            sku = extract_product_id(url)

            print(f"Checking {name} ({sku})...")

            in_stock = is_in_stock(sku)

            if in_stock['shipping'] == "IN_STOCK":
                send_embed(url, name, sku, "atc")
                print("item is in stock!")
            elif in_stock['shipping'] == "PRE_ORDER_SELLABLE":
                send_embed(url, name, sku, "pre")
                print("item is available for pre-order!")
            else:
                print("item is out of stock.")

            time.sleep(random.randint(5, 10))  