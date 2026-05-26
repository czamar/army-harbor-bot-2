import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1499696839589629952  # IDE A CHANNEL ID

timezone = pytz.timezone("Europe/Budapest")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
scheduler = AsyncIOScheduler(timezone=timezone)

async def send_message(message):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)

def schedule_events():

    # Army event (10 perccel előtte)
    for hour in [11, 13, 15, 17, 19, 21]:
        scheduler.add_job(
            lambda: bot.loop.create_task(
                send_message("@everyone ⚔️ Army event after 10 minutes!")
            ),
            trigger="cron",
            hour=hour,
            minute=50
        )

    # Harbor event (10 perccel előtte)
    for hour in [12, 14, 16, 18, 20, 22]:
        scheduler.add_job(
            lambda: bot.loop.create_task(
                send_message("@everyone 🚢 Harbor event after 10 minutes!")
            ),
            trigger="cron",
            hour=hour,
            minute=50
        )

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    schedule_events()
    scheduler.start()

bot.run(TOKEN)