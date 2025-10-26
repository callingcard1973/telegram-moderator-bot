# moderation.py
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from config import BANNED_KEYWORDS, BANNED_PHRASES, WHITELISTED_USERS, TEMP_BAN_DURATION_SECONDS, NOTIFICATION_DELETE_SECONDS
import logging

logger = logging.getLogger(__name__)

async def check_text_content(text: str) -> tuple[bool, list]:
    if not text:
        return False, []
    text_lower = text.lower()
    violations = []
    for keyword in BANNED_KEYWORDS:
        if keyword in text_lower:
            violations.append(f"keyword: '{keyword}'")
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            violations.append(f"phrase: '{phrase}'")
    return bool(violations), violations

async def handle_violation(update: Update, context: ContextTypes.DEFAULT_TYPE, user, violations):
    chat = update.message.chat
    try:
        await update.message.delete()
        await chat.ban_member(user.id, until_date=datetime.utcnow() + timedelta(seconds=TEMP_BAN_DURATION_SECONDS))
        notification = await context.bot.send_message(
            chat_id=chat.id,
            text=f"🚫 User {user.first_name} (@{user.username or user.id}) temporarily banned.\nReason: {', '.join(violations)}"
        )
        if NOTIFICATION_DELETE_SECONDS > 0:
            async def delete_notification(ctx):
                await notification.delete()
            context.application.job_queue.run_once(delete_notification, NOTIFICATION_DELETE_SECONDS)
    except Exception as e:
        logger.error(f"Error banning user: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or message.chat.type not in ['group', 'supergroup']:
        return
    user = message.from_user
    if user.id in WHITELISTED_USERS:
        return
    text = message.text or message.caption or ""
    is_violation, violations = await check_text_content(text)
    if is_violation:
        await handle_violation(update, context, user, violations)
