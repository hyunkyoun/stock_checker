import discord
from discord.ext import commands, tasks
import settings
import logging
import target 
from target import TARGET_PRODUCT_URL

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

    in_stock = target.check_stock()
    if in_stock:
        await channel.send(f"🚀 The product is IN STOCK! Buy now: {TARGET_PRODUCT_URL}")

bot.run(settings.DISCORD_API_SECRET, root_logger=True)