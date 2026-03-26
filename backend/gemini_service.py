from __future__ import annotations

from typing import Any

import requests

from backend.config import (
    DEFAULT_MODEL,
    FALLBACK_MODEL,
    GEMINI_API_KEY,
    GEMINI_API_URL,
    HISTORY_WINDOW_SIZE,
    MAX_OUTPUT_TOKENS,
    REQUEST_MAX_RETRIES,
    REQUEST_TIMEOUT_SECONDS,
    SECONDARY_FALLBACK_MODEL,
)
from backend.guidance_library import build_guidance_context, infer_concerns


BASE_PROMPT = """You are Aarohi, a calm and deeply empathetic mental health support companion.

Your role is to support users emotionally using evidence-based conversational techniques.

Guidelines:

* Be gentle, non-judgmental, and patient
* Focus on understanding before responding
* Reflect emotions before giving suggestions
* Use CBT-inspired questioning when appropriate
* Keep responses simple, human, and warm
* Never diagnose or label disorders
* Never act like a doctor
* If user expresses distress, prioritize emotional support over solutions
* Only respond to mental health, emotions, thoughts, stress, anxiety, or personal struggles
* If user asks unrelated questions, gently redirect to emotional context
* Never answer general knowledge questions

Safety:

* If user mentions self-harm or suicide:
  * Respond with care
  * Encourage reaching out to trusted people or helplines
  * Do NOT ignore

Response style:

* First identify what the user's main difficulty seems to be
* Reflect or validate briefly, then help
* Ask at most one clarifying question when understanding is incomplete
* If the problem is clear enough, give 2 or 3 situation-matched options instead of vague comfort
* Keep replies practical, concise, human, and low-jargon
* Avoid fake empathy, robotic phrasing, or advice dumping
* Prefer suggestions the user can try in the next few minutes when they feel stuck

You exist only to help users feel heard, understood, and supported."""


class GeminiServiceError(RuntimeError):
    """Raised when Gemini interactions fail."""


_session = requests.Session()


def _headers() -> dict[str, str]:
    if not GEMINI_API_KEY:
        raise GeminiServiceError("GEMINI_API_KEY is missing. Add it to your environment.")
    return {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }


def _build_contents(message: str, history: list[dict]) -> list[dict[str, Any]]:
    contents: list[dict[str, Any]] = []

    for item in history[-HISTORY_WINDOW_SIZE:]:
        contents.append(
            {
                "role": "model" if item.get("role") == "assistant" else "user",
                "parts": [{"text": item.get("content", "")}],
            }
        )

    contents.append({"role": "user", "parts": [{"text": message}]})
    return contents


def _build_system_instruction(message: str, history: list[dict]) -> dict[str, Any]:
    guidance_context = build_guidance_context(message, history)
    return {
        "parts": [{"text": f"{BASE_PROMPT}\n\n{guidance_context}"}],
    }


def fetch_available_models() -> list[str]:
    response = _session.get(
        GEMINI_API_URL,
        headers=_headers(),
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()
    model_ids = []
    for item in payload.get("models", []):
        name = item.get("name", "")
        supported_methods = item.get("supportedGenerationMethods", [])
        if name.startswith("models/") and "generateContent" in supported_methods:
            model_ids.append(name.replace("models/", "", 1))
    return model_ids


def generate_support_response(message: str, history: list[dict], model: str) -> tuple[str, str, bool]:
    attempted_models = []
    for candidate in (model, FALLBACK_MODEL, DEFAULT_MODEL, SECONDARY_FALLBACK_MODEL):
        if candidate not in attempted_models:
            attempted_models.append(candidate)

    last_error: Exception | None = None
    for index, candidate_model in enumerate(attempted_models):
        try:
            response_text = _generate_with_retries(message, history, candidate_model)
            return response_text, candidate_model, index > 0
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    raise GeminiServiceError(
        f"Unable to generate a response with '{model}' or fallback '{FALLBACK_MODEL}'."
    ) from last_error


def _generate_with_retries(message: str, history: list[dict], model: str) -> str:
    last_error: Exception | None = None
    endpoint = f"{GEMINI_API_URL}/{model}:generateContent"
    payload = {
        "system_instruction": _build_system_instruction(message, history),
        "contents": _build_contents(message, history),
        "generationConfig": {
            "temperature": 0.55,
            "topP": 0.85,
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
        },
    }

    for _ in range(REQUEST_MAX_RETRIES + 1):
        try:
            response = _session.post(
                endpoint,
                headers=_headers(),
                json=payload,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return _extract_text(response.json())
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    raise GeminiServiceError(f"Gemini request failed for model '{model}'.") from last_error


def _extract_text(payload: dict[str, Any]) -> str:
    candidates = payload.get("candidates", [])
    if not candidates:
        raise GeminiServiceError("Gemini response did not include any candidates.")

    parts = candidates[0].get("content", {}).get("parts", [])
    text_segments = [part.get("text", "") for part in parts if part.get("text")]
    if not text_segments:
        raise GeminiServiceError("Gemini response did not include text content.")
    return "\n".join(text_segments).strip()


def infer_response_concerns(message: str, history: list[dict]) -> list[str]:
    return infer_concerns(message, history)
