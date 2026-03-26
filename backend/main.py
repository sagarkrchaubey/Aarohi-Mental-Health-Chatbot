from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import DEFAULT_MODEL, FALLBACK_MODEL
from backend.gemini_service import (
    GeminiServiceError,
    fetch_available_models,
    generate_support_response,
    infer_response_concerns,
)
from backend.history_store import (
    append_message,
    create_session,
    delete_session,
    get_session,
    get_session_history,
    list_sessions,
)
from backend.model_manager import (
    cache_model_ids,
    get_cached_model_ids,
    get_static_model_options,
    merge_model_options,
    validate_model_selection,
)
from backend.safety import build_crisis_response, detect_crisis_language
from backend.schemas import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ModelListResponse,
    ModelResponse,
    SessionDetailResponse,
    SessionListResponse,
    SessionSummaryResponse,
)


app = FastAPI(
    title="Aarohi Mental Health Support API",
    version="1.0.0",
    description="Backend service for the Aarohi mental health support companion.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/models", response_model=ModelListResponse)
def get_models() -> ModelListResponse:
    try:
        dynamic_models = fetch_available_models()
        cache_model_ids(dynamic_models)
        model_options = merge_model_options(dynamic_models)
    except Exception:  # noqa: BLE001
        model_options = get_static_model_options()

    return ModelListResponse(
        default_model=DEFAULT_MODEL,
        fallback_model=FALLBACK_MODEL,
        models=[ModelResponse(**option.__dict__) for option in model_options],
    )


@app.get("/sessions", response_model=SessionListResponse)
def get_sessions() -> SessionListResponse:
    return SessionListResponse(
        sessions=[SessionSummaryResponse(**item) for item in list_sessions()]
    )


@app.get("/sessions/{session_id}", response_model=SessionDetailResponse)
def get_session_detail(session_id: str) -> SessionDetailResponse:
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    messages = [ChatMessage(**message) for message in session.get("messages", [])]
    return SessionDetailResponse(
        session_id=session_id,
        title=session.get("title", "New conversation"),
        created_at=session.get("created_at"),
        updated_at=session.get("updated_at"),
        messages=messages,
    )


@app.delete("/sessions/{session_id}")
def remove_session(session_id: str) -> dict[str, bool]:
    deleted = delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return {"deleted": True}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or "default"
    create_session(session_id)
    safety_result = detect_crisis_language(request.message)

    if safety_result.triggered:
        response_text = build_crisis_response()
        append_message(session_id, "user", request.message, used_model=request.model or DEFAULT_MODEL)
        append_message(
            session_id,
            "assistant",
            response_text,
            used_model="safety_override",
            concerns=["crisis_support"],
        )
        return ChatResponse(
            response=response_text,
            used_model="safety_override",
            session_id=session_id,
            safety_triggered=True,
            fallback_used=False,
            inferred_concerns=["crisis_support"],
        )

    try:
        cached_model_ids = get_cached_model_ids()
        if not cached_model_ids:
            try:
                cached_model_ids = fetch_available_models()
                cache_model_ids(cached_model_ids)
            except Exception:  # noqa: BLE001
                cached_model_ids = []

        available_models = [item.id for item in get_static_model_options()]
        available_models.extend(model_id for model_id in cached_model_ids if model_id not in available_models)
        selected_model = validate_model_selection(
            request.model or DEFAULT_MODEL,
            available_models,
        )
        history = get_session_history(session_id)
        inferred_concerns = infer_response_concerns(request.message, history)
        response_text, used_model, fallback_used = generate_support_response(
            message=request.message,
            history=history,
            model=selected_model,
        )
    except GeminiServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the message.",
        ) from exc

    append_message(session_id, "user", request.message, used_model=selected_model)
    append_message(
        session_id,
        "assistant",
        response_text,
        used_model=used_model,
        concerns=inferred_concerns,
    )

    return ChatResponse(
        response=response_text,
        used_model=used_model,
        session_id=session_id,
        safety_triggered=False,
        fallback_used=fallback_used,
        inferred_concerns=inferred_concerns,
    )
