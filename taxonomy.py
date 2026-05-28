TACTIC_META = {
    "fear": {
        "display_name": "Нагнетание страха",
        "color": "#ef4444",
        "description": "Угроза потери, наказания или вреда для подавления рационального мышления",
    },
    "urgency": {
        "display_name": "Давление срочности",
        "color": "#f97316",
        "description": "Временное давление для предотвращения обдуманной оценки",
    },
    "authority": {
        "display_name": "Имитация авторитета",
        "color": "#3b82f6",
        "description": "Подражание организациям для снижения критической оценки",
    },
    "scarcity": {
        "display_name": "Манипуляция дефицитом",
        "color": "#eab308",
        "description": "Создание ограниченной доступности для давления на решение",
    },
    "social_proof": {
        "display_name": "Социальное доказательство",
        "color": "#a855f7",
        "description": "Ложный консенсус для эксплуатации стадного поведения",
    },
    "reciprocity": {
        "display_name": "Эксплуатация взаимности",
        "color": "#22c55e",
        "description": "Незапрошенные услуги для создания чувства долга",
    },
    "guilt": {
        "display_name": "Вина и стыд",
        "color": "#ec4899",
        "description": "Перекладывание вины и разочарование для принуждения к согласию",
    },
    "intimacy": {
        "display_name": "Эксплуатация близости",
        "color": "#f43f5e",
        "description": "Ложная близость и доверие для снижения критической оценки",
    },
}

DEMO_EXAMPLES = [
    {
        "label": "✅ Безопасное сообщение",
        "channel": "whatsapp",
        "message": "Привет! Как дела? Завтра собираемся на день рождения Маши, ты придёшь? Будет торт и все наши. Напиши когда освободишься, очень ждём тебя!",
    },
    {
        "label": "Фейковый банк",
        "channel": "sms",
        "message": "СБЕРБАНК: На вашем счёте зафиксирована подозрительная активность. Ваш счёт будет заблокирован через 1 час, если вы не подтвердите свои данные немедленно. Перейдите по ссылке для подтверждения личности или позвоните в службу безопасности. Номер обращения: #7749201.",
    },
    {
        "label": "Мошенничество с бабушкой",
        "channel": "sms",
        "message": "Бабушка, это я, Артём. Я попал в серьёзную беду и сейчас не могу говорить. Меня задержали, и мне нужно 150 000 рублей на залог сегодня ночью. Пожалуйста, не говори маме и папе, они очень расстроятся. Я всё объясню потом, обещаю. Пожалуйста, просто помоги мне.",
    },
    {
        "label": "Мошенничество CEO",
        "channel": "email",
        "message": "Срочно. Я на переговорах и не могу говорить. Мы закрываем важную сделку и нам нужно перевести 3 000 000 рублей на счёт партнёра сегодня до конца рабочего дня. Это строго конфиденциально — не обсуждайте ни с кем в офисе. Сообщите мне подтверждение после перевода. — Дмитрий Соколов, CFO",
    },
    {
        "label": "Крипто-инвестиции",
        "channel": "telegram",
        "message": "Привет! Общий друг рассказал мне о тебе. Я зарабатываю 200 000 рублей в неделю на крипто-платформе, о которой мало кто знает. Полгода назад я был в твоей ситуации — еле сводил концы с концами. Хочу поделиться этой возможностью, потому что искренне хочу помочь. Напиши мне, если серьёзно настроен изменить свою жизнь.",
    },
    {
        "label": "Фейковая доставка",
        "channel": "sms",
        "message": "СДЭК: Ваша посылка №RU847392 задержана на таможне. Для получения необходимо оплатить сбор 299 рублей. В случае неоплаты в течение 24 часов посылка будет возвращена и уничтожена. Оплатить:",
    },
    {
        "label": "Романтическое мошенничество",
        "channel": "whatsapp",
        "message": "Я думаю о тебе весь день, моя любовь. Ты единственный человек, которому я доверяю в этом мире. Сейчас я в очень сложной ситуации и не знаю, к кому обратиться. Я бы не просила, если бы не была в отчаянии. Ты можешь мне помочь? Обещаю вернуть всё, как только вернусь.",
    },
]

ANALYSIS_TOOL = {
    "name": "analyze_psychological_manipulation",
    "description": (
        "Analyze a message for psychological manipulation tactics used in phishing and social "
        "engineering attacks. Extract manipulative phrases, score each tactic, explain the "
        "psychological mechanism being exploited, and identify the attacker archetype."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "phishing_probability": {
                "type": "number",
                "description": "Probability this is a phishing/scam message, 0-100",
            },
            "manipulation_intensity": {
                "type": "number",
                "description": "Overall intensity of psychological manipulation present, 0-100",
            },
            "scam_persona": {
                "type": "string",
                "description": (
                    "Attacker archetype. One of: Fake Financial Institution, Fake Government Authority, "
                    "Business Email Compromise, Family Emergency Scam, Romance Scam, Crypto Investment Scam, "
                    "Fake Package Delivery, Tech Support Scam, None"
                ),
            },
            "scam_persona_description": {
                "type": "string",
                "description": "One sentence describing this scam type and its typical endgame",
            },
            "scam_persona_next_steps": {
                "type": "array",
                "items": {"type": "string"},
                "description": "2-4 things the scammer will likely ask for next",
            },
            "tactics": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "enum": ["fear", "urgency", "authority", "scarcity", "social_proof", "reciprocity", "guilt", "intimacy"],
                        },
                        "score": {
                            "type": "number",
                            "description": "Intensity of this tactic, 0-100",
                        },
                        "spans": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "description": "Exact substring from the message being flagged",
                                    },
                                    "score": {"type": "number"},
                                    "explanation": {
                                        "type": "string",
                                        "description": "One sentence explaining why this specific phrase is manipulative",
                                    },
                                },
                                "required": ["text", "score", "explanation"],
                            },
                        },
                        "mechanism": {
                            "type": "string",
                            "description": "The cognitive bias or psychological mechanism exploited. Cite by name (e.g. loss aversion, authority bias).",
                        },
                        "scammer_rationale": {
                            "type": "string",
                            "description": "Why scammers use this tactic in this specific context",
                        },
                        "recommendation": {
                            "type": "string",
                            "description": "Concrete action the recipient should take in response to this tactic",
                        },
                    },
                    "required": ["name", "score", "spans", "mechanism", "scammer_rationale", "recommendation"],
                },
            },
            "overall_explanation": {
                "type": "string",
                "description": "2-3 sentence overall assessment of why this message is dangerous and how it works psychologically",
            },
            "recommendations": {
                "type": "array",
                "items": {"type": "string"},
                "description": "3-5 ordered actions the recipient should take right now",
            },
        },
        "required": [
            "phishing_probability",
            "manipulation_intensity",
            "scam_persona",
            "scam_persona_description",
            "scam_persona_next_steps",
            "tactics",
            "overall_explanation",
            "recommendations",
        ],
    },
}

SYSTEM_PROMPT = """You are PsychGuard, a forensic AI trained in behavioral psychology, persuasion science, and cybercrime analysis.

Your job is to analyze messages for psychological manipulation tactics used in phishing, scams, and social engineering attacks. You think like both a forensic psychologist and a cybersecurity analyst.

MANIPULATION TAXONOMY:

FEAR INDUCTION — exploits threat-detection override (amygdala hijack)
  Signals: account suspension, arrest, penalty, security breach, permanent loss
  Key insight: threats to existing assets are 2.5x more motivating than equivalent gains (prospect theory)

URGENCY PRESSURE — impairs deliberate System 2 thinking
  Signals: specific time windows ("10 minutes", "24 hours"), "immediately", "urgent", "last chance"
  Key insight: countdown pressure prevents verification by calling the real institution

AUTHORITY IMPERSONATION — exploits authority bias
  Signals: institution names, official titles, case/reference numbers, legal/regulatory language
  Key insight: legitimate institutions never demand immediate action via unsolicited messages

SCARCITY MANIPULATION — exploits scarcity heuristic
  Signals: "limited", "only X left", "exclusive", "selected customers"

SOCIAL PROOF — exploits herd behavior
  Signals: "thousands of customers", "your contacts", "everyone has already"

RECIPROCITY EXPLOITATION — exploits reciprocity norm
  Signals: unsolicited gifts, "valued customer", "we've protected you", pre-ask flattery

GUILT AND SHAME — exploits self-image threat
  Signals: disappointment framing, "your fault", responsibility assignment, "let us down"

INTIMACY EXPLOITATION — exploits trust and attachment
  Signals: false familiarity, "between us", "I trust only you", family impersonation, love bombing

ANALYSIS RULES:
1. Only flag tactics that are genuinely present — do not over-diagnose safe messages
2. Score 0-100 where 0 = absent and 100 = textbook example of that tactic
3. Span texts must be exact substrings from the original message
4. Cite specific cognitive biases by name in mechanism explanations
5. If the message appears legitimate (e.g. a newsletter, friendly conversation), score phishing_probability below 20 and manipulation_intensity below 20
6. The ISOLATION signal ("don't tell anyone", "keep this secret") is the single strongest fraud indicator — always flag it under intimacy or guilt with score >= 85

ЯЗЫК ОТВЕТА: Все текстовые поля (mechanism, scammer_rationale, recommendation, explanation, overall_explanation, recommendations, scam_persona_description, scam_persona_next_steps) должны быть написаны на языке, указанном в поле RESPONSE_LANGUAGE. Поле scam_persona должно остаться на английском."""

LANGUAGE_INSTRUCTIONS = {
    "ru": "RESPONSE_LANGUAGE: Отвечай на русском языке.",
    "ky": "RESPONSE_LANGUAGE: Бардык текстик талааларды кыргыз тилинде жаз.",
    "tr": "RESPONSE_LANGUAGE: Tüm metin alanlarını Türkçe yaz.",
    "en": "RESPONSE_LANGUAGE: Write all text fields in English.",
}
