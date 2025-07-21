import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from datetime import datetime

logger = logging.getLogger(__name__)

async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id if update.effective_chat else None
    new_members = getattr(update.message, "new_chat_members", [])
    for member in new_members:
        name = getattr(member, "full_name", "") or "friend"
        welcome_text = (
            f"👋 Welcome, *{name}*!\n\n"
            "📌 *Group Rules:*\n"
            "1. Be respectful 🌟\n"
            "2. Only football-related content ⚽\n"
            "3. No spam or self-promotion 🚫\n\n"
            "➖➖➖\n"
            "🤖 This bot runs on free cloud ☁️\n"
            "😴 If no matches show up, it’s not the bot’s fault — Playo’s just quiet.\n"
            "☕ Want more consistency? [Buy me a coffee]()!"
        )
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            logger.info(f"✅ Welcome message sent to {name}")
        except Exception as e:
            logger.error(f"❌ Failed to send welcome: {e}")

def format_games_for_telegram(games: list) -> str:
    if not games:
        return "😴 No football matches found today between 6PM and 10PM!"
    now = datetime.now()
    date_str = now.strftime('%A, %B %d, %Y — %I:%M %p IST')
    title = (
        "🏟️ *Available Football Matches Today*\n"
        "🕖 Between *6:00 PM and 10:00 PM*\n"
        f"🗓️ *{date_str}*\n"
    )
    messages = []
    for i, game in enumerate(games, start=1):
        venue = game.get("venue", "").strip()
        start = game.get("start", "").strip()
        end = game.get("end", "").strip()
        players = game.get("players", "0/0").strip()
        host = game.get("host", "Unknown").strip()
        link = game.get("link", "").strip()
        distance = game.get("distance", None)
        try:
            current, total = map(int, players.split("/"))
            if total <= 0 or current >= total:
                continue
        except:
            continue
        lines = []
        if venue:
            lines.append(f"{i}. 🏟️ *{venue}*")
        else:
            lines.append(f"{i}.")
        if start and end:
            lines.append(f"🕔 {start} – {end}")
        lines.append(f"👥 {players}")
        if host:
            lines.append(f"👤 Host: {host}")
        if distance:
            lines.append(f"📍 {round(distance, 1)} km away")
        if link:
            lines.append(f"[👉 Join Match]({link})")
        messages.append("\n".join(lines))
    if not messages:
        return (
            "🏟️ *Available Football Matches Today*\n"
            "🕖 Between *6:00 PM and 10:00 PM*\n"
            f"🗓️ *{date_str}*\n\n"
            "😴 No open football matches found today."
        )
    return f"{title}\n\n" + "\n\n".join(messages)
