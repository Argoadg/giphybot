import discord
import os
import asyncio
from discord.ext import tasks
from datetime import datetime, timedelta
import random

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

giphy_list = [
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif",
    "https://media.giphy.com/media/3oEduSbSGpGaRX2Vri/giphy.gif"
] * 150  # nur zum Beispiel, auf 365 erweitern
random.shuffle(giphy_list)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot ist online als {client.user}")
    send_giphy.start()

@tasks.loop(hours=24)
async def send_giphy():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        day_of_year = datetime.utcnow().timetuple().tm_yday
        gif = giphy_list[(day_of_year - 1) % len(giphy_list)]
        await channel.send(f"Guten Morgen! ☀️
{gif}")
    else:
        print("❌ Channel nicht gefunden.")

@send_giphy.before_loop
async def before():
    now = datetime.utcnow() + timedelta(hours=2)
    next_run = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if now > next_run:
        next_run += timedelta(days=1)
    await asyncio.sleep((next_run - now).total_seconds())

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot läuft 😎"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

keep_alive()
client.run(TOKEN)
