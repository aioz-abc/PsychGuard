# 🛡 PsychGuard — AI detector of psychological phishing

Scam messages rarely rely on technical tricks. They work on people: fear, urgency, fake authority,
false intimacy. **PsychGuard reads a message and shows which manipulation tactics it uses, how
likely it is to be phishing, and which exact phrases give it away.** Built at a hackathon.

## What it does

- **Message analysis:** paste a text and get a risk score (0–100), a phishing probability, and the
  manipulation tactics found, with the suspicious phrases highlighted.
- **Screenshot analysis:** upload a screenshot of a chat or SMS and a vision model extracts the text first.
- **8 manipulation tactics:** fear, urgency, fake authority, scarcity, social proof, reciprocity,
  guilt and shame, exploiting intimacy.
- **4 languages:** Russian, English, Turkish, Kyrgyz.
- **Telegram bot:** add it to a group and it warns members when a risky message appears.
- **Personal Telegram monitor:** watches your own chats (Telethon) and privately alerts you about suspicious messages.

## How it works

```
message / screenshot ──▶ FastAPI ──▶ LLM on Groq (Llama 3.3 70B, structured tool call)
                                          │
                                          ▼
                     tactics + highlighted phrases + phishing probability
                                          │
                                          ▼
                 risk score & confidence ──▶ web UI · Telegram bot · Telegram monitor
```

The LLM answers through a strict JSON schema (function calling), so results are always structured.
The risk score combines phishing probability, manipulation intensity and the number of tactics found.

## Run locally

```bash
git clone https://github.com/aioz-abc/PsychGuard.git
cd PsychGuard
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then fill in GROQ_API_KEY (and Telegram keys for the bots)

python main.py            # web app at http://localhost:8000
python telegram_bot.py    # optional: group bot
python telegram_monitor.py  # optional: personal chat monitor
```

Or run `./start.sh` to start the web app and the bot together and open the demo presentation.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/analyze` | analyze a message (`message`, `channel`, `language`) |
| POST | `/api/extract-text` | extract text from a screenshot (up to 10 MB) |
| GET | `/api/examples` | demo messages |
| GET | `/api/health` | health check |

Interactive docs: http://localhost:8000/docs

## Project structure

```
app.py               FastAPI app and endpoints
analyzer.py          LLM call, risk score and confidence
taxonomy.py          tactic definitions, system prompt, output schema, demo examples
models.py            Pydantic request/response models
telegram_bot.py      group bot
telegram_monitor.py  personal chat monitor (Telethon)
frontend/index.html  web interface
presentation.html    hackathon pitch
```

## Tech stack

Python · FastAPI · Pydantic · Groq (Llama 3.3 70B, Llama 4 Scout for images) · python-telegram-bot · Telethon · HTML/JS
