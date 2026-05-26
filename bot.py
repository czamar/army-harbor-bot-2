import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import os
from dotenv import load_dotenv
import asyncio

# --- LOAD ENV ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# --- CONFIG ---
CHANNEL_ID = 1499696839589629952  # ide a csatorna ID

# Budapest időzóna
timezone = pytz.timezone("Europe/Budapest")

# --- BOT SETUP ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

scheduler = AsyncIOScheduler(timezone=timezone)

# --- SEND MESSAGE FUNCTION ---
async def send_message(message):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print("Channel not found!")

# --- SAFE WRAPPER (IMPORTANT) ---
def job(message):
    asyncio.create_task(send_message(message))

# --- SCHEDULER SETUP ---
def schedule_events():

    # ⚔️ ARMY EVENTS (10 perccel előtte)
    army_hours = [11, 13, 15, 17, 19, 21]
    for hour in army_hours:
        scheduler.add_job(
            job,
            trigger="cron",
            hour=hour,
            minute=50,
            args=["@everyone ⚔️ Army event after 10 minutes!"],
            timezone=timezone
        )

    # 🚢 HARBOR EVENTS (10 perccel előtte)
    harbor_hours = [12, 14, 16, 18, 20, 22]
    for hour in harbor_hours:
        scheduler.add_job(
            job,
            trigger="cron",
            hour=hour,
            minute=50,
            args=["@everyone 🚢 Harbor event after 10 minutes!"],
            timezone=timezone
        )

# --- ON READY ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    schedule_events()
    scheduler.start()

# --- RUN BOT ---
bot.run(TOKEN)