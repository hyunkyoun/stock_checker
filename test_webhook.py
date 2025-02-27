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
    embed.set_footer(text=f"{datetime.now().strftime("%H:%M:%S")} EST")

    webhook.add_embed(embed)
    response = webhook.execute()

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message. Status code: ", response.status_code)

def run_bot():
    while True:
        for i in range(len(TARGET_URLS)):
            in_stock = asyncio.run(target.check_stock(TARGET_URLS[i]))
            if in_stock:
                sku = target.extract_product_id(TARGET_URLS[i])
                send_embed(TARGET_URLS[i], TARGET_NAMES[i], sku)
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
