from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    message: str
    channel: str = "unknown"
    language: str = "ru"


class SpanResult(BaseModel):
    text: str
    tactic: str
    score: float
    explanation: str


class TacticResult(BaseModel):
    name: str
    display_name: str
    score: float
    level: str
    color: str
    spans: List[SpanResult]
    mechanism: str
    scammer_rationale: str
    recommendation: str


class AnalysisResult(BaseModel):
    risk_score: float
    phishing_probability: float
    manipulation_intensity: float
    confidence: str
    risk_level: str
    scam_persona: str
    scam_persona_description: str
    scam_persona_next_steps: List[str]
    tactics: List[TacticResult]
    overall_explanation: str
    recommendations: List[str]
