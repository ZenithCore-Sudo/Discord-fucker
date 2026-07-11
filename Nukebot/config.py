import os
import json

class Config:
    # ===== BOT SETTINGS =====
    TOKEN = os.getenv('DISCORD_TOKEN', '')
    PREFIX = os.getenv('BOT_PREFIX', '!')
    WHITELIST = json.loads(os.getenv('WHITELIST', '[]')) if os.getenv('WHITELIST') else []

    # ===== MESSAGE SETTINGS =====
    SPAM_MESSAGE = os.getenv('SPAM_MESSAGE', '@everyone')
    SPAM_COUNT = int(os.getenv('SPAM_COUNT', '10'))
    TEXT_TO_SPEECH = os.getenv('TEXT_TO_SPEECH', 'False').lower() == 'true'
    DM_MESSAGE = os.getenv('DM_MESSAGE', 'THE SERVER GOT NUKED')

    # ===== CHANNEL SETTINGS =====
    CHANNEL_NAME = os.getenv('CHANNEL_NAME', 'nuked')
    CHANNELS_COUNT = int(os.getenv('CHANNELS_COUNT', '10'))
    NEW_CHANNEL_NAME = os.getenv('NEW_CHANNEL_NAME', 'nuked')
    VOICE_CHANNELS_COUNT = int(os.getenv('VOICE_CHANNELS_COUNT', '10'))
    VOICE_CHANNEL_NAME = os.getenv('VOICE_CHANNEL_NAME', 'NUKED')
    CATEGORY_NAME = os.getenv('CATEGORY_NAME', 'NUKED')
    CATEGORIES_COUNT = int(os.getenv('CATEGORIES_COUNT', '5'))
    THREAD_COUNT = int(os.getenv('THREAD_COUNT', '5'))
    THREAD_NAME = os.getenv('THREAD_NAME', 'nuked')
    NSFW_CHANNEL_NAME = os.getenv('NSFW_CHANNEL_NAME', 'nuked')
    SLOWMODE_DURATION = int(os.getenv('SLOWMODE_DURATION', '300'))

    # ===== ROLE SETTINGS =====
    ROLE_NAME = os.getenv('ROLE_NAME', 'nuked')
    ROLES_COUNT = int(os.getenv('ROLES_COUNT', '10'))
    NEW_ROLE_NAME = os.getenv('NEW_ROLE_NAME', 'nuked')
    ADMIN_ROLE_NAME = os.getenv('ADMIN_ROLE_NAME', 'ADMIN')

    # ===== SERVER SETTINGS =====
    SERVER_NAME = os.getenv('SERVER_NAME', 'NUKED SERVER')
    SERVER_ICON_URL = os.getenv('SERVER_ICON_URL', 'https://raw.githubusercontent.com/vn4thyt/vnsyt/refs/heads/main/Stuff/Discord%20Nuke%20Bot/server-icon.jpg')
    NICKNAME = os.getenv('NICKNAME', 'NUKED')
    TIMEOUT_DURATION = int(os.getenv('TIMEOUT_DURATION', '28'))

    # ===== WEBHOOK SETTINGS =====
    WEBHOOK_NAME = os.getenv('WEBHOOK_NAME', 'NUKED')
    WEBHOOK_COUNT = int(os.getenv('WEBHOOK_COUNT', '10'))
    WEBHOOK_RENAME = os.getenv('WEBHOOK_RENAME', 'NUKED')

    # ===== INVITE SETTINGS =====
    INVITE_COUNT = int(os.getenv('INVITE_COUNT', '10'))

    # ===== PIN SETTINGS =====
    PIN_SPAM_COUNT = int(os.getenv('PIN_SPAM_COUNT', '5'))

    # ===== VOICE SETTINGS =====
    MOVE_VOICE_CHANNEL_NAME = os.getenv('MOVE_VOICE_CHANNEL_NAME', 'LOSERS')

    # ===== PERMISSION SETTINGS =====
    CHAOS_PERMISSIONS = [True, False, None]
