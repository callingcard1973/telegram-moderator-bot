# commands.py
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def cmd_getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat = update.message.chat
    await update.message.reply_text(
        f"🆔 ID Info:\n\n👤 User ID: `{user.id}`\n💬 Chat ID: `{chat.id}`\n📦 Chat Type: {chat.type}",
        parse_mode='Markdown'
    )

async def cmd_unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat = update.message.chat
    if chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("❌ This command only works in groups.")
        return
    member = await chat.get_member(user.id)
    if member.status not in ['creator', 'administrator']:
        await update.message.reply_text("❌ Only admins can unban users.")
        return
    if not context.args:
        await update.message.reply_text("❌ Usage: /unban <user_id>")
        return
    try:
        user_id = int(context.args[0])
        await chat.unban_member(user_id)
        await update.message.reply_text(f"✅ User {user_id} has been unbanned.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def cmd_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        "📝 Appeal received. An admin will review your case shortly."
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ Moderation Bot Commands:\n\n"
        "/getid - Show your user and chat ID\n"
        "/unban <user_id> - Unban a user (admin only)\n"
        "/appeal - Request review if banned\n"
        "/help - Show this help message"
    )
