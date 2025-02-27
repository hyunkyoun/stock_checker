import discord
from discord.ext import commands, tasks
import settings
import logging
import targets

# TARGET_URLS = [
#     "https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab",
#     "https://www.target.com/p/pok-233-mon-trading-card-game-zapdos-ex-deluxe-battle-deck/-/A-91351689#lnk=sametab",
# ]

TARGET_URLS = [
    "https://www.target.com/p/pok-233-mon-trading-card-game-zapdos-ex-deluxe-battle-deck/-/A-91351689#lnk=sametab",
]

# Configure logging
logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger("bot")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"User: {bot.user} | ID: {bot.user.id}")
    print("Bot is ready!")
    stock_checker.start()  # Start the stock check loop

@tasks.loop(minutes=5)  # Check stock every 5 minutes
async def stock_checker():
    channel_id = 1343597897819885569  # Replace with your Discord channel ID
    channel = bot.get_channel(channel_id)

    if not channel:
        print("⚠️ Channel not found. Check your channel ID.")
        return

    for url in TARGET_URLS:
        in_stock = targets.check_stock(url)
        if in_stock:
            sku = targets.extract_product_id(url)
            await channel.send(f"@everyone 🚀 The product is IN STOCK! Buy now: {url}")

bot.run(settings.DISCORD_API_SECRET, root_logger=True)