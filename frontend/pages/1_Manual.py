from __future__ import annotations

import os

import requests
import streamlit as st

from frontend.ui_shared import THEMES, apply_theme, init_theme_state


API_BASE_URL = os.getenv("AAROHI_API_BASE_URL", "http://localhost:8000")


def fetch_models() -> list[dict]:
    try:
        response = requests.get(f"{API_BASE_URL}/models", timeout=10)
        response.raise_for_status()
        return response.json().get("models", [])
    except requests.RequestException:
        return []


def render_model_table(models: list[dict]) -> None:
    if not models:
        st.info("Model details are unavailable right now because the backend could not be reached.")
        return

    st.table(
        [
            {
                "Model": item["label"],
                "Code": item["id"],
                "Use it when": item["description"],
                "Status": item["status"],
            }
            for item in models
        ]
    )


def main() -> None:
    st.set_page_config(page_title="Aarohi Manual", page_icon="📘", layout="wide")
    init_theme_state()

    with st.sidebar:
        st.markdown("### Manual")
        st.page_link("app.py", label="Back to chat", icon="💬")
        st.selectbox("Theme", list(THEMES.keys()), key="theme_name")
        st.caption(THEMES[st.session_state.theme_name]["tag"])
        st.caption("Use the button above to return to the main chat page.")

    apply_theme(st.session_state.theme_name)

    st.title("Aarohi Manual")
    st.caption("How to use the chat page, choose a model, revisit saved chats, and understand safety behavior.")

    st.markdown("## What Aarohi is for")
    st.markdown(
        """
        Aarohi is designed for emotional support conversations. It works best for:

        - stress and overwhelm
        - anxiety and overthinking
        - low mood and lack of motivation
        - loneliness or relationship pain
        - burnout and mental exhaustion
        - sleep-related emotional distress
        """
    )

    st.markdown("## How to use the chat page")
    st.markdown(
        """
        1. Open the **Chat** page from the sidebar page navigation.
        2. Start a fresh conversation with **New chat** or reopen an older one from **Saved chats**.
        3. Write what feels difficult right now in the message box.
        4. Choose the **Next reply model** in the sidebar.
        5. Send the message and let Aarohi first understand the problem, then offer practical support.
        6. Press **Enter** to send. Use **Shift+Enter** when you want a new line.
        """
    )

    st.markdown("## Saved conversations")
    st.markdown(
        """
        - Every sent conversation is stored in `data/chat_history.json`.
        - Older chats appear in the sidebar under **Saved chats**.
        - Starting a new chat does not delete previous chats.
        - Clicking an older chat loads the full conversation back into the main page.
        """
    )

    st.markdown("## Model guide")
    render_model_table(fetch_models())
    st.markdown(
        """
        Practical recommendation:

        - **Gemini 2.5 Flash Lite**: fastest and usually the best default for everyday support replies
        - **Gemini 2.5 Flash**: balanced when you want a little more depth without too much delay
        - **Gemini 2.5 Pro**: best for layered or nuanced emotional situations when slower replies are acceptable
        """
    )

    st.markdown("## Themes")
    st.markdown(
        """
        The chat page supports multiple visual atmospheres:

        - Forest
        - Lake
        - Waterfall
        - Volcano
        - Dragon
        - Lotus

        Themes only change the visual presentation. They do not change the model or safety behavior.
        """
    )

    st.markdown("## How Aarohi responds")
    st.markdown(
        """
        Aarohi is tuned to:

        - understand the likely emotional problem before suggesting too much
        - ask one clarifying question when the situation is still unclear
        - offer 2 or 3 practical coping options when the situation is clear enough
        - keep the conversation focused on mental health rather than general questions
        """
    )

    st.markdown("## Safety")
    st.markdown(
        """
        If a message includes phrases such as:

        - `suicide`
        - `kill myself`
        - `end my life`

        Aarohi bypasses the normal model reply and returns immediate crisis-support guidance encouraging real human help.
        """
    )

    st.markdown("## Troubleshooting")
    st.markdown(
        """
        - If the chat page cannot load models or saved conversations, make sure the FastAPI backend is running.
        - If replies feel slow, prefer **Gemini 2.5 Flash Lite**.
        - If a previous chat is missing, check that the backend is using the same `data/chat_history.json` file.
        - If the UI looks stale after code changes, restart Streamlit and refresh the browser.
        """
    )


if __name__ == "__main__":
    main()
