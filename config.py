# config.py
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

WHITELISTED_USERS = {547047851}

BANNED_KEYWORDS = [
    'porn', 'xxx', 'nsfw', 'nude', 'sex', 'adult content',
    'dick', 'pussy', 'fuck', 'cock', 'boobs', 'ass',
    'naked', 'tits', 'penis', 'vagina', 'sexy',
]

BANNED_PHRASES = [
    'only fans', 'onlyfans', 'send nudes', 'hot girls',
    'cam girl', 'adult dating',
]

NOTIFICATION_DELETE_SECONDS = 10
TEMP_BAN_DURATION_SECONDS = 3600  # 1 hour
