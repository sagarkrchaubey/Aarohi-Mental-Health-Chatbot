from __future__ import annotations

import json
from datetime import datetime, timezone

from backend.config import CHAT_HISTORY_FILE, DATA_DIR


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_store_exists() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CHAT_HISTORY_FILE.exists():
        CHAT_HISTORY_FILE.write_text(json.dumps({}, indent=2), encoding="utf-8")


def _default_session() -> dict:
    timestamp = _now_iso()
    return {
        "title": "New conversation",
        "created_at": timestamp,
        "updated_at": timestamp,
        "messages": [],
    }


def _derive_title(messages: list[dict]) -> str:
    for item in messages:
        if item.get("role") == "user" and item.get("content"):
            text = " ".join(item["content"].split())
            return text[:56] + ("..." if len(text) > 56 else "")
    return "New conversation"


def _normalize_store(raw_store: dict) -> dict[str, dict]:
    normalized: dict[str, dict] = {}

    for session_id, value in raw_store.items():
        if isinstance(value, dict) and isinstance(value.get("messages"), list):
            session = {
                "title": value.get("title") or _derive_title(value["messages"]),
                "created_at": value.get("created_at") or (
                    value["messages"][0].get("timestamp") if value["messages"] else _now_iso()
                ),
                "updated_at": value.get("updated_at") or (
                    value["messages"][-1].get("timestamp") if value["messages"] else _now_iso()
                ),
                "messages": value["messages"],
            }
        elif isinstance(value, list):
            session = _default_session()
            session["messages"] = value
            session["title"] = _derive_title(value)
            if value:
                session["created_at"] = value[0].get("timestamp", _now_iso())
                session["updated_at"] = value[-1].get("timestamp", _now_iso())
        else:
            session = _default_session()

        normalized[session_id] = session

    return normalized


def _read_store() -> dict[str, dict]:
    _ensure_store_exists()
    try:
        raw_store = json.loads(CHAT_HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raw_store = {}

    normalized = _normalize_store(raw_store)
    if normalized != raw_store:
        _write_store(normalized)
    return normalized


def _write_store(payload: dict[str, dict]) -> None:
    _ensure_store_exists()
    CHAT_HISTORY_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def create_session(session_id: str, title: str | None = None) -> dict:
    store = _read_store()
    session = store.get(session_id)
    if not session:
        session = _default_session()
        if title:
            session["title"] = title
        store[session_id] = session
        _write_store(store)
    return session


def get_session(session_id: str) -> dict | None:
    store = _read_store()
    return store.get(session_id)


def get_session_history(session_id: str) -> list[dict]:
    session = get_session(session_id)
    return session.get("messages", []) if session else []


def list_sessions() -> list[dict]:
    store = _read_store()
    sessions = []
    for session_id, session in store.items():
        messages = session.get("messages", [])
        last_message = messages[-1] if messages else {}
        sessions.append(
            {
                "session_id": session_id,
                "title": session.get("title") or _derive_title(messages),
                "created_at": session.get("created_at"),
                "updated_at": session.get("updated_at"),
                "message_count": len(messages),
                "preview": last_message.get("content", "")[:100],
            }
        )

    sessions.sort(key=lambda item: item.get("updated_at") or "", reverse=True)
    return sessions


def append_message(
    session_id: str,
    role: str,
    content: str,
    used_model: str | None = None,
    concerns: list[str] | None = None,
) -> None:
    store = _read_store()
    session = store.setdefault(session_id, _default_session())
    timestamp = _now_iso()
    message = {
        "role": role,
        "content": content,
        "timestamp": timestamp,
    }
    if used_model:
        message["used_model"] = used_model
    if concerns:
        message["concerns"] = concerns

    session_history = session.setdefault("messages", [])
    session_history.append(message)

    if session.get("title") in {None, "", "New conversation"} and role == "user":
        session["title"] = _derive_title(session_history)

    session["updated_at"] = timestamp
    if not session.get("created_at"):
        session["created_at"] = timestamp

    store[session_id] = session
    _write_store(store)


def delete_session(session_id: str) -> bool:
    store = _read_store()
    if session_id not in store:
        return False
    del store[session_id]
    _write_store(store)
    return True
