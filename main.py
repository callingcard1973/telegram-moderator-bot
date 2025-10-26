# main.py
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from moderation import handle_message
from commands import cmd_getid, cmd_unban, cmd_appeal, cmd_help

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("getid", cmd_getid))
    app.add_handler(CommandHandler("unban", cmd_unban))
    app.add_handler(CommandHandler("appeal", cmd_appeal))
    app.add_handler(CommandHandler("help", cmd_help))

    app.add_handler(MessageHandler((filters.TEXT | filters.CAPTION) & ~filters.COMMAND, handle_message))

    logger.info("Bot is running...")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        webhook_url="https://your-railway-subdomain.up.railway.app"
    )

if __name__ == "__main__":
    main()
