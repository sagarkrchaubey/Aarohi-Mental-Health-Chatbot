from __future__ import annotations

import html
import os
import uuid

import requests
import streamlit as st
from streamlit.components.v1 import html as components_html

from frontend.ui_shared import (
    THEMES,
    apply_theme,
    format_sidebar_timestamp,
    format_timestamp,
    init_theme_state,
)


API_BASE_URL = os.getenv("AAROHI_API_BASE_URL", "http://localhost:8000")

QUICK_STARTERS = [
    "I feel overwhelmed and do not know where to start.",
    "My thoughts keep racing and I cannot calm down.",
    "I feel low and unmotivated lately.",
    "I am carrying too much stress right now.",
]


@st.cache_data(ttl=600, show_spinner=False)
def fetch_models_cached() -> dict:
    response = requests.get(f"{API_BASE_URL}/models", timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_models() -> dict:
    try:
        return fetch_models_cached()
    except requests.RequestException:
        return {
            "default_model": "gemini-2.5-flash",
            "fallback_model": "gemini-2.5-flash-lite",
            "models": [
                {
                    "id": "gemini-2.5-flash-lite",
                    "label": "Gemini 2.5 Flash Lite",
                    "description": "Fastest and best for most emotional support turns",
                    "status": "stable",
                },
                {
                    "id": "gemini-2.5-flash",
                    "label": "Gemini 2.5 Flash",
                    "description": "Balanced speed and quality",
                    "status": "stable",
                },
                {
                    "id": "gemini-2.5-pro",
                    "label": "Gemini 2.5 Pro",
                    "description": "Deeper reasoning, slower",
                    "status": "stable",
                },
            ],
        }


def fetch_sessions() -> list[dict]:
    try:
        response = requests.get(f"{API_BASE_URL}/sessions", timeout=10)
        response.raise_for_status()
        return response.json().get("sessions", [])
    except requests.RequestException:
        return []


def fetch_session_detail(session_id: str) -> dict | None:
    try:
        response = requests.get(f"{API_BASE_URL}/sessions/{session_id}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def send_message(message: str, model: str, session_id: str) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/chat",
        json={"message": message, "model": model, "session_id": session_id},
        timeout=25,
    )
    response.raise_for_status()
    return response.json()


def delete_chat(session_id: str) -> None:
    response = requests.delete(f"{API_BASE_URL}/sessions/{session_id}", timeout=10)
    response.raise_for_status()


def initialize_state() -> None:
    init_theme_state()
    if "model_payload" not in st.session_state:
        st.session_state.model_payload = fetch_models()
    if "sessions" not in st.session_state:
        st.session_state.sessions = []
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None
    if "loaded_session_id" not in st.session_state:
        st.session_state.loaded_session_id = None
    if "active_session_title" not in st.session_state:
        st.session_state.active_session_title = "New conversation"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "prefill_message" not in st.session_state:
        st.session_state.prefill_message = None
    if "chat_prompt" not in st.session_state:
        st.session_state.chat_prompt = ""
    if "session_filter" not in st.session_state:
        st.session_state.session_filter = ""
    if "composer_model" not in st.session_state:
        st.session_state.composer_model = st.session_state.model_payload.get(
            "fallback_model",
            "gemini-2.5-flash-lite",
        )
    if "scroll_to_latest" not in st.session_state:
        st.session_state.scroll_to_latest = False


def refresh_sessions() -> None:
    st.session_state.sessions = fetch_sessions()


def ensure_active_session() -> None:
    if st.session_state.active_session_id:
        return

    if st.session_state.sessions:
        st.session_state.active_session_id = st.session_state.sessions[0]["session_id"]
        load_active_session(force=True)
        return

    start_new_chat()


def start_new_chat() -> None:
    st.session_state.active_session_id = str(uuid.uuid4())
    st.session_state.loaded_session_id = None
    st.session_state.active_session_title = "New conversation"
    st.session_state.messages = []
    st.session_state.chat_prompt = ""


def load_active_session(force: bool = False) -> None:
    session_id = st.session_state.active_session_id
    if not session_id:
        return

    if not force and st.session_state.loaded_session_id == session_id:
        return

    detail = fetch_session_detail(session_id)
    if not detail:
        st.session_state.loaded_session_id = session_id
        st.session_state.active_session_title = "New conversation"
        st.session_state.messages = []
        return

    st.session_state.loaded_session_id = session_id
    st.session_state.active_session_title = detail.get("title", "Conversation")
    st.session_state.messages = detail.get("messages", [])


def sync_selected_model() -> None:
    options = [item["id"] for item in st.session_state.model_payload.get("models", [])]
    if not options:
        return
    if st.session_state.composer_model not in options:
        fallback_model = st.session_state.model_payload.get("fallback_model")
        st.session_state.composer_model = fallback_model if fallback_model in options else options[0]


def prepare_draft_state() -> None:
    if st.session_state.prefill_message:
        st.session_state.chat_prompt = st.session_state.prefill_message
        st.session_state.prefill_message = None


def select_session(session_id: str) -> None:
    st.session_state.active_session_id = session_id
    load_active_session(force=True)


def remove_session_from_sidebar(session_id: str) -> None:
    delete_chat(session_id)
    was_active = session_id == st.session_state.active_session_id
    refresh_sessions()

    if was_active:
        st.session_state.active_session_id = None
        st.session_state.loaded_session_id = None
        st.session_state.messages = []
        st.session_state.active_session_title = "New conversation"
        ensure_active_session()


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### Aarohi")
        st.caption("A focused mental-health support workspace")
        st.page_link("pages/1_Manual.py", label="Open manual", icon="📘")

        if st.button("New chat", use_container_width=True):
            start_new_chat()
            st.rerun()

        st.selectbox("Theme", list(THEMES.keys()), key="theme_name")
        st.caption(THEMES[st.session_state.theme_name]["tag"])

        model_options = st.session_state.model_payload.get("models", [])
        model_ids = [item["id"] for item in model_options]
        model_labels = {
            item["id"]: item["label"]
            for item in model_options
        }
        if model_ids:
            st.selectbox(
                "Next reply model",
                model_ids,
                key="composer_model",
                format_func=lambda model_id: model_labels.get(model_id, model_id),
            )
            st.caption("Set the model before sending the next message.")

        st.markdown("### Saved chats")
        st.text_input(
            "Find a chat",
            key="session_filter",
            placeholder="Search by title or preview",
            label_visibility="collapsed",
        )
        if not st.session_state.sessions:
            st.caption("No saved chats yet. Start a conversation and it will appear here.")

        filter_value = st.session_state.session_filter.strip().lower()
        visible_sessions = []
        for session in st.session_state.sessions:
            haystack = " ".join(
                [
                    session.get("title", ""),
                    session.get("preview", ""),
                ]
            ).lower()
            if filter_value and filter_value not in haystack:
                continue
            visible_sessions.append(session)

        if filter_value and not visible_sessions:
            st.caption("No saved chats match that search.")

        for session in visible_sessions:
            session_id = session["session_id"]
            title = session.get("title") or "Conversation"
            updated_at = format_sidebar_timestamp(session.get("updated_at"))
            selected = session_id == st.session_state.active_session_id
            compact_title = title[:20] + ("..." if len(title) > 20 else "")
            label = f"{compact_title} · {updated_at}" if updated_at else compact_title
            row_left, row_right = st.columns([0.82, 0.18])
            if row_left.button(
                ("• " if selected else "") + label,
                key=f"session_{session_id}",
                use_container_width=True,
                help=title,
            ):
                select_session(session_id)
                st.rerun()
            if row_right.button("✕", key=f"delete_{session_id}", use_container_width=True):
                try:
                    remove_session_from_sidebar(session_id)
                except requests.RequestException:
                    st.error("Could not delete that chat right now.")
                    return
                st.rerun()


def render_topbar() -> None:
    message_count = len(st.session_state.messages)
    safe_title = html.escape(st.session_state.active_session_title)
    model_label = next(
        (
            item["label"]
            for item in st.session_state.model_payload.get("models", [])
            if item["id"] == st.session_state.composer_model
        ),
        st.session_state.composer_model,
    )
    session_count = len(st.session_state.sessions)
    st.markdown(
        f"""
        <div class="aarohi-shell">
            <div class="aarohi-topbar">
                <div>
                    <h1 class="aarohi-title">Aarohi</h1>
                    <p class="aarohi-subtitle">{safe_title}</p>
                </div>
                <div>
                    <span class="aarohi-chip">{message_count} messages</span>
                    <span class="aarohi-chip">{session_count} chats saved</span>
                    <span class="aarohi-chip">{html.escape(model_label)}</span>
                    <span class="aarohi-chip">{st.session_state.theme_name}</span>
                </div>
            </div>
            <p class="aarohi-summary">
                Aarohi listens for the emotional problem first, then responds with focused and practical support.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    st.markdown(
        """
        <div class="aarohi-empty">
            Share what feels heavy right now. Aarohi works best with anxiety, stress, burnout,
            overthinking, low mood, loneliness, sleep difficulty, and emotionally difficult situations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    starter_cols = st.columns(2)
    for index, prompt in enumerate(QUICK_STARTERS):
        target_col = starter_cols[index % 2]
        if target_col.button(prompt, key=f"starter_{index}", use_container_width=True):
            st.session_state.prefill_message = prompt
            st.rerun()


def render_messages() -> None:
    if not st.session_state.messages:
        render_empty_state()
        return

    for message in st.session_state.messages:
        role = message.get("role", "assistant")
        name = "Aarohi" if role == "assistant" else "You"
        with st.chat_message(role, avatar="🌿" if role == "assistant" else "🫶"):
            st.markdown(message.get("content", ""))
            meta_parts = []
            if message.get("used_model"):
                meta_parts.append(message["used_model"])
            for concern in message.get("concerns", []):
                meta_parts.append(concern.replace("_", " "))
            if message.get("timestamp"):
                meta_parts.append(format_timestamp(message["timestamp"]))
            meta_line = " · ".join(meta_parts)
            if meta_line:
                st.caption(f"{name} · {meta_line}")


def render_chat_input() -> str | None:
    return st.chat_input(
        "Type a message. Enter sends. Shift+Enter adds a new line.",
        key="chat_prompt",
        max_chars=2500,
    )


def render_scroll_script() -> None:
    components_html(
        """
        <script>
        const scrollToLatest = () => {
          const parentDoc = window.parent.document;
          const anchor = parentDoc.getElementById("reply-anchor");
          if (anchor) {
            anchor.scrollIntoView({ behavior: "smooth", block: "end" });
          } else {
            window.parent.scrollTo({
              top: parentDoc.body.scrollHeight,
              behavior: "smooth"
            });
          }
        };
        setTimeout(scrollToLatest, 60);
        setTimeout(scrollToLatest, 220);
        </script>
        """,
        height=0,
        width=0,
    )


def handle_submission(user_text: str, selected_model: str) -> None:
    with st.spinner("Aarohi is preparing a reply..."):
        send_message(
            message=user_text,
            model=selected_model,
            session_id=st.session_state.active_session_id,
        )
    refresh_sessions()
    load_active_session(force=True)
    st.session_state.scroll_to_latest = True


def main() -> None:
    st.set_page_config(page_title="Aarohi", page_icon="🌿", layout="wide")
    initialize_state()
    st.session_state.model_payload = fetch_models()
    sync_selected_model()
    refresh_sessions()
    ensure_active_session()
    load_active_session()
    render_sidebar()
    apply_theme(st.session_state.theme_name)
    prepare_draft_state()
    render_topbar()
    st.markdown('<a class="jump-latest" href="#reply-anchor">Jump to latest</a>', unsafe_allow_html=True)
    render_messages()
    st.markdown('<div id="reply-anchor"></div>', unsafe_allow_html=True)
    if st.session_state.scroll_to_latest:
        render_scroll_script()
        st.session_state.scroll_to_latest = False
    prompt = render_chat_input()

    if not prompt or not prompt.strip():
        return

    try:
        handle_submission(prompt.strip(), st.session_state.composer_model)
    except requests.HTTPError as exc:
        detail = "The backend could not process that message right now."
        try:
            detail = exc.response.json().get("detail", detail)
        except Exception:  # noqa: BLE001
            pass
        st.error(detail)
        return
    except requests.RequestException:
        st.error("Aarohi could not reach the backend service. Please confirm the FastAPI server is running.")
        return

    st.rerun()


if __name__ == "__main__":
    main()
