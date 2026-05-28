"""
PsychGuard Telegram Monitor
Monitors your Telegram chats in real time.
When a suspicious message arrives, sends you a warning via bot.
"""

import asyncio
import os
import httpx
from telethon import TelegramClient, events
from dotenv import load_dotenv

from analyzer import PsychGuardAnalyzer

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
API_ID        = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH      = os.getenv("TELEGRAM_API_HASH", "")
BOT_TOKEN     = os.getenv("TELEGRAM_BOT_TOKEN", "")
WARN_USER_ID  = int(os.getenv("TELEGRAM_USER_ID", "0"))

RISK_THRESHOLD = 60   # warn if risk score >= this value
SESSION_NAME   = "psychguard_session"

# ── Globals ───────────────────────────────────────────────────────────────────
analyzer = PsychGuardAnalyzer()


# ── Bot warning sender ────────────────────────────────────────────────────────
async def send_warning(risk_score: float, risk_level: str, tactics: list,
                       overall: str, sender_name: str, message_preview: str,
                       recommendations: list):

    level_emoji = {
        "CRITICAL": "🔴",
        "HIGH":     "🟠",
        "MEDIUM":   "🟡",
        "LOW":      "🟢",
    }.get(risk_level, "⚪")

    level_ru = {
        "CRITICAL": "КРИТИЧЕСКИЙ",
        "HIGH":     "ВЫСОКИЙ",
        "MEDIUM":   "СРЕДНИЙ",
        "LOW":      "НИЗКИЙ",
    }.get(risk_level, risk_level)

    tactic_display = {
        "fear":         "😨 Нагнетание страха",
        "urgency":      "⏰ Давление срочности",
        "authority":    "🏛 Имитация авторитета",
        "scarcity":     "💎 Манипуляция дефицитом",
        "social_proof": "👥 Социальное доказательство",
        "reciprocity":  "🎁 Эксплуатация взаимности",
        "guilt":        "😔 Вина и стыд",
        "intimacy":     "💔 Эксплуатация близости",
    }

    tactics_text = "\n".join(
        f"  {tactic_display.get(t['name'], t['name'])} — {round(t['score'])}/100"
        for t in tactics[:4]
    )

    preview = message_preview[:120] + ("..." if len(message_preview) > 120 else "")
    top_rec = recommendations[0] if recommendations else "Не отвечайте на это сообщение."

    text = (
        f"🛡 *PsychGuard — Предупреждение*\n\n"
        f"{level_emoji} *Риск: {round(risk_score)}/100 — {level_ru}*\n"
        f"👤 От: {sender_name}\n\n"
        f"📩 *Сообщение:*\n_{preview}_\n\n"
        f"🧠 *Обнаруженные тактики:*\n{tactics_text}\n\n"
        f"💬 *Вывод:* {overall}\n\n"
        f"✅ *Что делать:* {top_rec}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id":    WARN_USER_ID,
        "text":       text,
        "parse_mode": "Markdown",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            print(f"[Bot] Failed to send warning: {response.text}")
        else:
            print(f"[Bot] Warning sent for message from {sender_name}")


# ── Message handler ───────────────────────────────────────────────────────────
@events.register(events.NewMessage(incoming=True))
async def handle_message(event):
    message = event.message
    text = message.text or ""

    # Skip short/empty messages
    if len(text.strip()) < 15:
        return

    # Get sender name
    try:
        sender = await event.get_sender()
        if sender is None:
            return
        first = getattr(sender, "first_name", "") or ""
        last  = getattr(sender, "last_name", "")  or ""
        uname = getattr(sender, "username", "")   or ""
        sender_name = f"{first} {last}".strip() or uname or "Неизвестный"
    except Exception:
        sender_name = "Неизвестный"

    print(f"[Monitor] Message from {sender_name}: {text[:60]}...")

    try:
        result = analyzer.analyze(text, channel="telegram")
    except Exception as e:
        print(f"[Monitor] Analysis error: {e}")
        return

    print(f"[Monitor] Risk score: {result.risk_score} ({result.risk_level})")

    if result.risk_score >= RISK_THRESHOLD:
        await send_warning(
            risk_score=result.risk_score,
            risk_level=result.risk_level,
            tactics=[{"name": t.name, "score": t.score} for t in result.tactics],
            overall=result.overall_explanation,
            sender_name=sender_name,
            message_preview=text,
            recommendations=result.recommendations,
        )


# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    if not API_ID or not API_HASH:
        print("❌ Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in .env")
        return
    if not BOT_TOKEN:
        print("❌ Missing TELEGRAM_BOT_TOKEN in .env")
        return
    if not WARN_USER_ID:
        print("❌ Missing TELEGRAM_USER_ID in .env")
        return

    print("🛡 PsychGuard Telegram Monitor starting...")
    print(f"   Threshold: risk >= {RISK_THRESHOLD} triggers warning")

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    client.add_event_handler(handle_message)

    await client.start()
    me = await client.get_me()
    print(f"✅ Monitoring account: {me.first_name} (@{me.username})")
    print("   Waiting for messages...\n")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
