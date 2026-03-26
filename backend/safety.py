from __future__ import annotations

from dataclasses import dataclass


CRISIS_KEYWORDS = (
    "suicide",
    "kill myself",
    "end my life",
)


@dataclass(frozen=True)
class SafetyResult:
    triggered: bool
    keyword: str | None = None


def detect_crisis_language(text: str) -> SafetyResult:
    normalized = (text or "").lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in normalized:
            return SafetyResult(triggered=True, keyword=keyword)
    return SafetyResult(triggered=False)


def build_crisis_response() -> str:
    return (
        "I'm really glad you shared this with me. What you're carrying sounds very heavy, "
        "and you do not have to handle it alone right now.\n\n"
        "Please reach out to someone you trust immediately, like a friend, family member, "
        "therapist, or local emergency support. If you're in immediate danger or feel you "
        "might act on these thoughts, call emergency services right now.\n\n"
        "If you can, contact a crisis helpline in your area right away. If you're in the "
        "United States or Canada, call or text 988. If you're elsewhere, please contact "
        "your local emergency or suicide crisis service now.\n\n"
        "If you want, you can stay here and tell me one small thing: are you safe in this "
        "moment, and is there someone nearby you can contact right now?"
    )
