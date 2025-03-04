from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import time
# import targets
import target
import asyncio

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
    # embed.set_footer(text={datetime.now().strftime("%H:%M:%S")})

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
    in_stock = await target.check_stock(url)
    if in_stock:
        sku = target.extract_product_id(url)
        send_embed(url, name, sku)

def run_bot():
    while True:
        asyncio.run(check_all_targets())  # Run all checks in parallel
        time.sleep(5)  # Delay before the next round of checks

if __name__ == "__main__":
    run_bot()
