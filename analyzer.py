import os
import json
from groq import Groq
from dotenv import load_dotenv

from models import AnalysisResult, TacticResult, SpanResult
from taxonomy import SYSTEM_PROMPT, ANALYSIS_TOOL, TACTIC_META, LANGUAGE_INSTRUCTIONS

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


class PsychGuardAnalyzer:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.client = Groq(api_key=api_key)

    def analyze(self, message: str, channel: str = "unknown", language: str = "ru") -> AnalysisResult:
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        raw = self._call_llm(message.strip(), channel, language)
        return self._build_result(raw)

    def _call_llm(self, message: str, channel: str, language: str = "ru") -> dict:
        lang_instruction = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS["ru"])
        system = SYSTEM_PROMPT + "\n\n" + lang_instruction
        user_content = f"CHANNEL: {channel}\n\nMESSAGE:\n---\n{message}\n---"

        groq_tool = {
            "type": "function",
            "function": {
                "name": ANALYSIS_TOOL["name"],
                "description": ANALYSIS_TOOL["description"],
                "parameters": ANALYSIS_TOOL["input_schema"],
            },
        }

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
            tools=[groq_tool],
            tool_choice={"type": "function", "function": {"name": ANALYSIS_TOOL["name"]}},
            max_tokens=4096,
            temperature=0.1,
        )

        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            raise RuntimeError("Model did not return a tool call")

        return json.loads(tool_calls[0].function.arguments)

    def _build_result(self, raw: dict) -> AnalysisResult:
        phishing_prob = float(raw.get("phishing_probability", 0))
        manipulation = float(raw.get("manipulation_intensity", 0))

        tactics = []
        for t in raw.get("tactics", []):
            name = t.get("name", "")
            score = float(t.get("score", 0))
            meta = TACTIC_META.get(name, {"display_name": name, "color": "#6b7280"})

            spans = [
                SpanResult(
                    text=s.get("text", ""),
                    tactic=name,
                    score=float(s.get("score", score)),
                    explanation=s.get("explanation", ""),
                )
                for s in t.get("spans", [])
                if s.get("text")
            ]

            tactics.append(
                TacticResult(
                    name=name,
                    display_name=meta["display_name"],
                    score=score,
                    level=_score_level(score),
                    color=meta["color"],
                    spans=spans,
                    mechanism=t.get("mechanism", ""),
                    scammer_rationale=t.get("scammer_rationale", ""),
                    recommendation=t.get("recommendation", ""),
                )
            )

        tactics.sort(key=lambda x: x.score, reverse=True)

        risk_score = _compute_risk(phishing_prob, manipulation, len(tactics))
        confidence = _compute_confidence(phishing_prob, manipulation, len(tactics))

        return AnalysisResult(
            risk_score=risk_score,
            phishing_probability=phishing_prob,
            manipulation_intensity=manipulation,
            confidence=confidence,
            risk_level=_score_level(risk_score),
            scam_persona=raw.get("scam_persona", "None"),
            scam_persona_description=raw.get("scam_persona_description", ""),
            scam_persona_next_steps=raw.get("scam_persona_next_steps", []),
            tactics=tactics,
            overall_explanation=raw.get("overall_explanation", ""),
            recommendations=raw.get("recommendations", []),
        )


def _score_level(score: float) -> str:
    if score >= 76:
        return "CRITICAL"
    if score >= 51:
        return "HIGH"
    if score >= 26:
        return "MEDIUM"
    return "LOW"


def _compute_risk(phishing_prob: float, manipulation: float, tactic_count: int) -> float:
    base = 0.5 * phishing_prob + 0.5 * manipulation
    combo_bonus = min(10.0, tactic_count * 2.0)
    return min(100.0, round(base + combo_bonus, 1))


def _compute_confidence(phishing_prob: float, manipulation: float, tactic_count: int) -> str:
    if phishing_prob > 80 and manipulation > 70:
        return "VERY HIGH"
    if phishing_prob > 60 or manipulation > 60 or tactic_count >= 3:
        return "HIGH"
    if phishing_prob > 35 or manipulation > 35:
        return "MEDIUM"
    return "LOW"
