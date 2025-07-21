import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from bot.telegram_helpers import send_welcome_message

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")
RENDER_WEB_URL = os.getenv("RENDER_WEB_URL")
WEBHOOK_PATH = f"/{WEBHOOK_SECRET_TOKEN}"
WEBHOOK_URL = f"{RENDER_WEB_URL}{WEBHOOK_PATH}"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_test(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and working!")

if __name__ == "__main__":
    logger.info("🚀 Booting Telegram bot webhook server...")

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("test", handle_test))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, send_welcome_message))

    logger.info(f"🌐 Starting webhook: {WEBHOOK_URL}")
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=WEBHOOK_SECRET_TOKEN,
        webhook_url=WEBHOOK_URL,
    )
