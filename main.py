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
    "https://media.giphy.com/media/gif_001/giphy.gif",
    "https://media.giphy.com/media/gif_002/giphy.gif",
    "https://media.giphy.com/media/gif_003/giphy.gif",
    "https://media.giphy.com/media/gif_004/giphy.gif",
    "https://media.giphy.com/media/gif_005/giphy.gif",
    "https://media.giphy.com/media/gif_006/giphy.gif",
    "https://media.giphy.com/media/gif_007/giphy.gif",
    "https://media.giphy.com/media/gif_008/giphy.gif",
    "https://media.giphy.com/media/gif_009/giphy.gif",
    "https://media.giphy.com/media/gif_010/giphy.gif",
    "https://media.giphy.com/media/gif_011/giphy.gif",
    "https://media.giphy.com/media/gif_012/giphy.gif",
    "https://media.giphy.com/media/gif_013/giphy.gif",
    "https://media.giphy.com/media/gif_014/giphy.gif",
    "https://media.giphy.com/media/gif_015/giphy.gif",
    "https://media.giphy.com/media/gif_016/giphy.gif",
    "https://media.giphy.com/media/gif_017/giphy.gif",
    "https://media.giphy.com/media/gif_018/giphy.gif",
    "https://media.giphy.com/media/gif_019/giphy.gif",
    "https://media.giphy.com/media/gif_020/giphy.gif",
    "https://media.giphy.com/media/gif_021/giphy.gif",
    "https://media.giphy.com/media/gif_022/giphy.gif",
    "https://media.giphy.com/media/gif_023/giphy.gif",
    "https://media.giphy.com/media/gif_024/giphy.gif",
    "https://media.giphy.com/media/gif_025/giphy.gif",
    "https://media.giphy.com/media/gif_026/giphy.gif",
    "https://media.giphy.com/media/gif_027/giphy.gif",
    "https://media.giphy.com/media/gif_028/giphy.gif",
    "https://media.giphy.com/media/gif_029/giphy.gif",
    "https://media.giphy.com/media/gif_030/giphy.gif",
    "https://media.giphy.com/media/gif_031/giphy.gif",
    "https://media.giphy.com/media/gif_032/giphy.gif",
    "https://media.giphy.com/media/gif_033/giphy.gif",
    "https://media.giphy.com/media/gif_034/giphy.gif",
    "https://media.giphy.com/media/gif_035/giphy.gif",
    "https://media.giphy.com/media/gif_036/giphy.gif",
    "https://media.giphy.com/media/gif_037/giphy.gif",
    "https://media.giphy.com/media/gif_038/giphy.gif",
    "https://media.giphy.com/media/gif_039/giphy.gif",
    "https://media.giphy.com/media/gif_040/giphy.gif",
    "https://media.giphy.com/media/gif_041/giphy.gif",
    "https://media.giphy.com/media/gif_042/giphy.gif",
    "https://media.giphy.com/media/gif_043/giphy.gif",
    "https://media.giphy.com/media/gif_044/giphy.gif",
    "https://media.giphy.com/media/gif_045/giphy.gif",
    "https://media.giphy.com/media/gif_046/giphy.gif",
    "https://media.giphy.com/media/gif_047/giphy.gif",
    "https://media.giphy.com/media/gif_048/giphy.gif",
    "https://media.giphy.com/media/gif_049/giphy.gif",
    "https://media.giphy.com/media/gif_050/giphy.gif",
    "https://media.giphy.com/media/gif_051/giphy.gif",
    "https://media.giphy.com/media/gif_052/giphy.gif",
    "https://media.giphy.com/media/gif_053/giphy.gif",
    "https://media.giphy.com/media/gif_054/giphy.gif",
    "https://media.giphy.com/media/gif_055/giphy.gif",
    "https://media.giphy.com/media/gif_056/giphy.gif",
    "https://media.giphy.com/media/gif_057/giphy.gif",
    "https://media.giphy.com/media/gif_058/giphy.gif",
    "https://media.giphy.com/media/gif_059/giphy.gif",
    "https://media.giphy.com/media/gif_060/giphy.gif",
    "https://media.giphy.com/media/gif_061/giphy.gif",
    "https://media.giphy.com/media/gif_062/giphy.gif",
    "https://media.giphy.com/media/gif_063/giphy.gif",
    "https://media.giphy.com/media/gif_064/giphy.gif",
    "https://media.giphy.com/media/gif_065/giphy.gif",
    "https://media.giphy.com/media/gif_066/giphy.gif",
    "https://media.giphy.com/media/gif_067/giphy.gif",
    "https://media.giphy.com/media/gif_068/giphy.gif",
    "https://media.giphy.com/media/gif_069/giphy.gif",
    "https://media.giphy.com/media/gif_070/giphy.gif",
    "https://media.giphy.com/media/gif_071/giphy.gif",
    "https://media.giphy.com/media/gif_072/giphy.gif",
    "https://media.giphy.com/media/gif_073/giphy.gif",
    "https://media.giphy.com/media/gif_074/giphy.gif",
    "https://media.giphy.com/media/gif_075/giphy.gif",
    "https://media.giphy.com/media/gif_076/giphy.gif",
    "https://media.giphy.com/media/gif_077/giphy.gif",
    "https://media.giphy.com/media/gif_078/giphy.gif",
    "https://media.giphy.com/media/gif_079/giphy.gif",
    "https://media.giphy.com/media/gif_080/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/xT9IgDEI1iZyb2wqo8/giphy.gif",
    "https://media.giphy.com/media/3o7TKzNqT4FJxZJt7e/giphy.gif",
    "https://media.giphy.com/media/l0HlNQ03J5JxX6lva/giphy.gif",
    "https://media.giphy.com/media/26gsspf0C0p2zhD1i/giphy.gif",
    "https://media.giphy.com/media/3ohs4BSacFKI7A717y/giphy.gif",
    "https://media.giphy.com/media/26FPnsRww5pYB2hGk/giphy.gif",
    "https://media.giphy.com/media/l1J3preURPiwjRPvG/giphy.gif",
    "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif",
    "https://media.giphy.com/media/xT0GqzJ2A2QlYCTlJ6/giphy.gif",
    "https://media.giphy.com/media/3ohs7KViF3gq8DQnUY/giphy.gif",
    "https://media.giphy.com/media/xUOwGce1AX5A5G5MZa/giphy.gif",
    "https://media.giphy.com/media/3oKIPa2TdahY8mZgUg/giphy.gif",
    "https://media.giphy.com/media/3ohzdIuqJoo8QdKlnW/giphy.gif",
    "https://media.giphy.com/media/3oz8xIsloV7zOmt81G/giphy.gif",
    "https://media.giphy.com/media/xT0BKqhdlKCxCNsVTq/giphy.gif",
    "https://media.giphy.com/media/3ov9jExd1a7e7Qhsys/giphy.gif",
    "https://media.giphy.com/media/3ohs84z9t2TgD4ey3O/giphy.gif",
    "https://media.giphy.com/media/3o6ZsY8UbVSVk6H0yI/giphy.gif",
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",
    "https://media.giphy.com/media/26Ff5M0cTC1C8kPJC/giphy.gif",
    "https://media.giphy.com/media/xT0xezQGU5xCDJuCPe/giphy.gif",
    "https://media.giphy.com/media/xUPGcdhiQH8oQxjU5G/giphy.gif",
    "https://media.giphy.com/media/l1J3G5lf06vi58EIE/giphy.gif",
    "https://media.giphy.com/media/3o7TKq6BvP6bQq5vUI/giphy.gif",
    "https://media.giphy.com/media/xT9IgIc0lryrxvqVGM/giphy.gif",
    "https://media.giphy.com/media/xUPGcxpCV81ebKh1Vu/giphy.gif",
    "https://media.giphy.com/media/l0ExsgrTuACbtP1mQ/giphy.gif",
    "https://media.giphy.com/media/3oz8xLDv4w4Rz3GFtu/giphy.gif",
    "https://media.giphy.com/media/xT0Gqgzkc7lZ9ONhCk/giphy.gif",
    "https://media.giphy.com/media/3o6ZsSPk7d6asFSgXK/giphy.gif",
    "https://media.giphy.com/media/xT9Igl1FWV3yYLRcyI/giphy.gif",
    "https://media.giphy.com/media/xT0BKlB8QOlt6yt5DW/giphy.gif",
    "https://media.giphy.com/media/3oKIPsx2VAYAgEHC12/giphy.gif",
    "https://media.giphy.com/media/3o7btU7ACsGWvpCgdy/giphy.gif",
    "https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif",
    "https://media.giphy.com/media/xT9IgpPjvW7fY9GkDC/giphy.gif",
    "https://media.giphy.com/media/3ohzdYJK1wAdPWVk88/giphy.gif",
    "https://media.giphy.com/media/3oEduSbSGpGaRX2Vri/giphy.gif",
    "https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
    "https://media.giphy.com/media/l0HlUJYHYVnZ9IMwQ/giphy.gif",
    "https://media.giphy.com/media/xT9IgKJb5LXY2cprEk/giphy.gif",
    "https://media.giphy.com/media/xT9Igz37eGpYFuS5pW/giphy.gif",
    "https://media.giphy.com/media/3oz8xEeVgdYgV3clQ4/giphy.gif",
    "https://media.giphy.com/media/3o7TKsQZEq2gsY7s76/giphy.gif",
    "https://media.giphy.com/media/l0HlUQ0zGzN8oyCKQ/giphy.gif",
    "https://media.giphy.com/media/l0MYGb1LuZ3n7dRnO/giphy.gif",
    "https://media.giphy.com/media/3o7aD6s5lFq1Jopb9i/giphy.gif",
    "https://media.giphy.com/media/xT9IgM9y3G6du6W8Xu/giphy.gif",
    "https://media.giphy.com/media/xT9IgKZzUDrmE7K0jO/giphy.gif",
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
    "https://media.giphy.com/media/3oz8xLd9DJq2l2VFtu/giphy.gif",
    "https://media.giphy.com/media/l0HlQ7LRal6vrhZvy/giphy.gif",
    "https://media.giphy.com/media/3o6ZsZKnWGfCJJd5wA/giphy.gif",
    "https://media.giphy.com/media/l3q2QHYp6G7W8ZJoY/giphy.gif"
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
