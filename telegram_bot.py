"""
PsychGuard Telegram Bot
Add this bot to any group chat.
It monitors messages and warns when manipulation is detected.
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from analyzer import PsychGuardAnalyzer

load_dotenv()

BOT_TOKEN      = os.getenv("TELEGRAM_BOT_TOKEN", "")
RISK_THRESHOLD = 60

analyzer = PsychGuardAnalyzer()

TACTIC_EMOJI = {
    "fear":         "😨",
    "urgency":      "⏰",
    "authority":    "🏛",
    "scarcity":     "💎",
    "social_proof": "👥",
    "reciprocity":  "🎁",
    "guilt":        "😔",
    "intimacy":     "💔",
}

LEVEL_EMOJI = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MEDIUM":   "🟡",
    "LOW":      "🟢",
}

LEVEL_RU = {
    "CRITICAL": "КРИТИЧЕСКИЙ",
    "HIGH":     "ВЫСОКИЙ",
    "MEDIUM":   "СРЕДНИЙ",
    "LOW":      "НИЗКИЙ",
}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.strip()

    # Skip short messages and bot commands
    if len(text) < 15 or text.startswith("/"):
        return

    # Skip messages from bots
    if message.from_user and message.from_user.is_bot:
        return

    sender = message.from_user
    sender_name = (sender.first_name or "") + (" " + sender.last_name if sender.last_name else "")
    sender_name = sender_name.strip() or "Неизвестный"

    print(f"[Bot] Analyzing message from {sender_name}: {text[:60]}...")

    try:
        result = analyzer.analyze(text, channel="telegram")
    except Exception as e:
        print(f"[Bot] Analysis error: {e}")
        return

    print(f"[Bot] Risk: {result.risk_score} ({result.risk_level})")

    if result.risk_score < RISK_THRESHOLD:
        return

    # Build warning message
    level_emoji = LEVEL_EMOJI.get(result.risk_level, "⚪")
    level_ru    = LEVEL_RU.get(result.risk_level, result.risk_level)

    tactics_lines = "\n".join(
        f"  {TACTIC_EMOJI.get(t.name, '•')} {t.display_name} — {round(t.score)}/100"
        for t in result.tactics[:4]
    )

    preview = text[:100] + ("..." if len(text) > 100 else "")
    top_rec = result.recommendations[0] if result.recommendations else "Не отвечайте на это сообщение."

    warning = (
        f"🛡 *PsychGuard — Предупреждение*\n\n"
        f"{level_emoji} *Риск: {round(result.risk_score)}/100 — {level_ru}*\n\n"
        f"👤 Отправитель: *{sender_name}*\n"
        f"📩 Сообщение: _{preview}_\n\n"
        f"🧠 *Обнаруженные тактики манипуляции:*\n{tactics_lines}\n\n"
        f"💬 *Вывод:* {result.overall_explanation}\n\n"
        f"✅ *Что делать:* {top_rec}"
    )

    try:
        await message.reply_text(warning, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        # Fallback without markdown if formatting fails
        try:
            plain = (
                f"🛡 PsychGuard — Предупреждение\n\n"
                f"{level_emoji} Риск: {round(result.risk_score)}/100 — {level_ru}\n\n"
                f"Отправитель: {sender_name}\n\n"
                f"Тактики: {', '.join(t.display_name for t in result.tactics[:3])}\n\n"
                f"Что делать: {top_rec}"
            )
            await message.reply_text(plain)
        except Exception as e2:
            print(f"[Bot] Failed to send warning: {e2}")


async def handle_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages sent directly to the bot in private chat."""
    message = update.message
    if not message or not message.text:
        return

    text = message.text.strip()

    if text.startswith("/start"):
        await message.reply_text(
            "👋 Привет! Я PsychGuard.\n\n"
            "Добавь меня в групповой чат, и я буду автоматически анализировать сообщения "
            "на психологическую манипуляцию.\n\n"
            "Или отправь мне любое подозрительное сообщение — я его проверю прямо здесь."
        )
        return

    if len(text) < 5:
        return

    await message.reply_text("🔍 Анализирую...")

    try:
        result = analyzer.analyze(text, channel="telegram")
    except Exception as e:
        await message.reply_text(f"Ошибка анализа: {e}")
        return

    level_emoji = LEVEL_EMOJI.get(result.risk_level, "⚪")
    level_ru    = LEVEL_RU.get(result.risk_level, result.risk_level)

    tactics_lines = "\n".join(
        f"  {TACTIC_EMOJI.get(t.name, '•')} {t.display_name} — {round(t.score)}/100"
        for t in result.tactics[:4]
    ) or "  Не обнаружено"

    reply = (
        f"🛡 *Результат анализа PsychGuard*\n\n"
        f"{level_emoji} *Риск: {round(result.risk_score)}/100 — {level_ru}*\n"
        f"Вероятность фишинга: {round(result.phishing_probability)}%\n\n"
        f"🧠 *Тактики манипуляции:*\n{tactics_lines}\n\n"
        f"💬 {result.overall_explanation}\n\n"
        f"✅ *Что делать:*\n" +
        "\n".join(f"  {i+1}. {r}" for i, r in enumerate(result.recommendations[:3]))
    )

    try:
        await message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    except Exception:
        await message.reply_text(
            f"Риск: {round(result.risk_score)}/100 — {level_ru}\n\n"
            f"{result.overall_explanation}"
        )


def main():
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set in .env")
        return

    print("🛡 PsychGuard Bot starting...")
    print(f"   Risk threshold: {RISK_THRESHOLD}/100")
    print("   Add the bot to a group chat to start monitoring\n")

    app = Application.builder().token(BOT_TOKEN).build()

    # Group messages
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS,
        handle_message
    ))

    # Private chat messages
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE,
        handle_private
    ))

    print("✅ Bot is running. Press Ctrl+C to stop.\n")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
