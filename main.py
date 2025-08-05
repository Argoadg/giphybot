import os
import discord
import asyncio
from datetime import datetime, timedelta
import pytz
import random
from dotenv import load_dotenv
import json
from PIL import Image, ImageDraw, ImageFont
import aiohttp
from io import BytesIO

# Giphy URLs (mindestens 150 eindeutige)
default_gifs = [
    # ... (gekürzt für Übersicht – URLs bleiben wie gehabt)
] * 10
random.shuffle(default_gifs)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
BIRTHDAY_FILE = "birthdays.json"
LEVEL_FILE = "levels.json"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

def load_birthdays():
    if not os.path.exists(BIRTHDAY_FILE):
        return {}
    with open(BIRTHDAY_FILE, "r") as f:
        return json.load(f)

def save_birthdays(data):
    with open(BIRTHDAY_FILE, "w") as f:
        json.dump(data, f)

def load_levels():
    if not os.path.exists(LEVEL_FILE):
        return {}
    with open(LEVEL_FILE, "r") as f:
        return json.load(f)

def save_levels(data):
    with open(LEVEL_FILE, "w") as f:
        json.dump(data, f)

async def create_birthday_meme(user: discord.User):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(user.avatar.url) as resp:
                if resp.status != 200:
                    return None
                avatar_bytes = await resp.read()
    except:
        return None

    avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA").resize((256, 256))
    meme = Image.new("RGBA", (512, 300), (255, 255, 255, 255))
    meme.paste(avatar, (128, 20))
    draw = ImageDraw.Draw(meme)
    font = ImageFont.truetype("arial.ttf", 24)
    draw.text((128, 280), f"Happy Birthday, {user.name}! 🎉", fill=(0, 0, 0), font=font)
    buffer = BytesIO()
    meme.save(buffer, format="PNG")
    buffer.seek(0)
    return discord.File(fp=buffer, filename="birthday_meme.png")

async def create_levelup_image(user: discord.User, level: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(user.avatar.url) as resp:
                if resp.status != 200:
                    return None
                avatar_bytes = await resp.read()
    except:
        return None

    avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA").resize((128, 128))
    canvas = Image.new("RGBA", (500, 250), (30, 30, 30, 255))
    canvas.paste(avatar, (20, 60))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("arial.ttf", 28)
    draw.text((170, 100), f"{user.name} ist jetzt Level {level}!", fill=(255, 215, 0), font=font)
    buffer = BytesIO()
    canvas.save(buffer, format="PNG")
    buffer.seek(0)
    return discord.File(fp=buffer, filename="level_up.png")

async def schedule_giphy():
    while True:
        berlin = pytz.timezone("Europe/Berlin")
        now = datetime.now(berlin)
        today_str = now.strftime("%Y-%m-%d")
        today_short = now.strftime("%d.%m.")
        nine_am = now.replace(hour=9, minute=0, second=0, microsecond=0)

        if os.path.exists("last_sent_day.txt"):
            with open("last_sent_day.txt", "r") as f:
                last_sent_day = f.read().strip()
        else:
            last_sent_day = ""

        if now > nine_am and last_sent_day != today_str:
            print("⏰ 9 Uhr verpasst – sende GIF trotzdem nachträglich...")
            channel = client.get_channel(CHANNEL_ID)
            birthdays = load_birthdays()
            for uid, bday in birthdays.items():
                if bday == today_short:
                    user = await client.fetch_user(int(uid))
                    file = await create_birthday_meme(user)
                    if file:
                        await channel.send(file=file, content=f"🎂 Alles Gute zum Geburtstag, {user.mention}!")
                    else:
                        await channel.send(f"🎉 Alles Gute zum Geburtstag, {user.mention}! 🎂")
            gif = random.choice(default_gifs)
            if channel:
                await channel.send(f"Guten Morgen! ☀️\n{gif}")
            with open("last_sent_day.txt", "w") as f:
                f.write(today_str)

        next_run = (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        wait_seconds = (next_run - now).total_seconds()
        print(f"⏳ Wartezeit bis 9 Uhr: {int(wait_seconds)} Sekunden...")
        await asyncio.sleep(wait_seconds)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    levels = load_levels()
    user_data = levels.get(user_id, {"xp": 0, "level": 1})

    user_data["xp"] += random.randint(5, 15)
    xp_needed = user_data["level"] * 1000
    if user_data["xp"] >= xp_needed:
        user_data["xp"] -= xp_needed
        user_data["level"] += 1
        file = await create_levelup_image(message.author, user_data["level"])
        if file:
            await message.channel.send(file=file, content=f"🏆 {message.author.mention} ist jetzt Level {user_data['level']}!")
        else:
            await message.channel.send(f"🏆 {message.author.mention} hat Level {user_data['level']} erreicht!")

    levels[user_id] = user_data
    save_levels(levels)

    if message.content.startswith("!geburtstag"):
        parts = message.content.split()
        if len(parts) == 2 and parts[1].lower() == "löschen":
            birthdays = load_birthdays()
            if str(message.author.id) in birthdays:
                del birthdays[str(message.author.id)]
                save_birthdays(birthdays)
                await message.channel.send("🗑️ Geburtstag gelöscht!")
            else:
                await message.channel.send("⚠️ Du hattest keinen Geburtstag gespeichert.")
        elif len(parts) == 2:
            try:
                datetime.strptime(parts[1], "%d.%m.")
                birthdays = load_birthdays()
                birthdays[str(message.author.id)] = parts[1]
                save_birthdays(birthdays)
                await message.channel.send(f"🎉 Geburtstag gespeichert: {parts[1]}")
            except:
                await message.channel.send("❌ Ungültiges Format. Nutze: !geburtstag TT.MM.")
        else:
            await message.channel.send("❌ Bitte gib dein Geburtsdatum im Format `!geburtstag 30.12.` an oder `!geburtstag löschen`.")

    if message.content.lower().startswith("!testgif"):
        gif = random.choice(default_gifs)
        await message.channel.send(f"Test-GIF 🎯\n{gif}")

    if message.content.lower().startswith("!level"):
        user_data = load_levels().get(user_id, {"xp": 0, "level": 1})
        await message.channel.send(f"📊 {message.author.mention}, du bist Level {user_data['level']} mit {user_data['xp']} XP.")

    if message.content.lower().startswith("!rangliste"):
        levels = load_levels()
        sorted_users = sorted(levels.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)
        lines = []
        for i, (uid, data) in enumerate(sorted_users[:10], start=1):
            member = await client.fetch_user(int(uid))
            lines.append(f"{i}. {member.name}: Level {data['level']} ({data['xp']} XP)")
        await message.channel.send("🏅 **Top 10 Rangliste:**\n" + "\n".join(lines))

@client.event
async def on_member_remove(member):
    birthdays = load_birthdays()
    if str(member.id) in birthdays:
        del birthdays[str(member.id)]
        save_birthdays(birthdays)

@client.event
async def on_member_join(member):
    user_id = str(member.id)
    levels = load_levels()
    user_data = levels.get(user_id, {"xp": 0, "level": 1})
    user_data["xp"] += 5
    levels[user_id] = user_data
    save_levels(levels)

@client.event
async def on_ready():
    print(f"✅ Bot ist online als {client.user}")
    await schedule_giphy()

client.run(TOKEN)
