from __future__ import annotations

from datetime import datetime

import streamlit as st


THEMES = {
    "Forest": {
        "tag": "Grounded and restorative",
        "background": "radial-gradient(circle at top left, rgba(163, 214, 154, 0.20), transparent 24%), linear-gradient(135deg, #0F1712 0%, #18281E 44%, #264133 100%)",
        "sidebar": "linear-gradient(180deg, rgba(12, 21, 16, 0.96), rgba(30, 52, 39, 0.92))",
        "panel": "rgba(18, 30, 23, 0.72)",
        "panel_alt": "rgba(30, 50, 40, 0.68)",
        "text": "#EEF6EF",
        "muted": "#C3D6C8",
        "accent": "#95E39B",
        "accent_soft": "rgba(149, 227, 155, 0.16)",
        "line": "rgba(255, 255, 255, 0.10)",
    },
    "Lake": {
        "tag": "Cool and spacious",
        "background": "radial-gradient(circle at top right, rgba(159, 217, 248, 0.18), transparent 26%), linear-gradient(135deg, #0A1320 0%, #0F2741 44%, #174E6A 100%)",
        "sidebar": "linear-gradient(180deg, rgba(10, 19, 32, 0.96), rgba(20, 58, 82, 0.92))",
        "panel": "rgba(16, 31, 48, 0.74)",
        "panel_alt": "rgba(26, 55, 74, 0.70)",
        "text": "#F2F9FF",
        "muted": "#C8DCEA",
        "accent": "#7BD8FF",
        "accent_soft": "rgba(123, 216, 255, 0.16)",
        "line": "rgba(255, 255, 255, 0.10)",
    },
    "Waterfall": {
        "tag": "Bright and clarifying",
        "background": "radial-gradient(circle at top center, rgba(221, 244, 255, 0.18), transparent 22%), linear-gradient(135deg, #0A2230 0%, #12415A 44%, #4890B5 100%)",
        "sidebar": "linear-gradient(180deg, rgba(9, 28, 39, 0.96), rgba(19, 74, 99, 0.92))",
        "panel": "rgba(12, 34, 46, 0.72)",
        "panel_alt": "rgba(28, 79, 104, 0.68)",
        "text": "#F7FCFF",
        "muted": "#D1E7F1",
        "accent": "#A3EAFF",
        "accent_soft": "rgba(163, 234, 255, 0.16)",
        "line": "rgba(255, 255, 255, 0.10)",
    },
    "Volcano": {
        "tag": "Strong and intense",
        "background": "radial-gradient(circle at top left, rgba(255, 170, 110, 0.16), transparent 24%), linear-gradient(135deg, #170B08 0%, #311811 44%, #6E2F1D 100%)",
        "sidebar": "linear-gradient(180deg, rgba(23, 11, 8, 0.96), rgba(73, 30, 18, 0.92))",
        "panel": "rgba(27, 14, 10, 0.74)",
        "panel_alt": "rgba(62, 28, 17, 0.68)",
        "text": "#FFF5F0",
        "muted": "#EBC9BD",
        "accent": "#FFA56B",
        "accent_soft": "rgba(255, 165, 107, 0.15)",
        "line": "rgba(255, 255, 255, 0.10)",
    },
    "Dragon": {
        "tag": "Mythic but gentle",
        "background": "radial-gradient(circle at top right, rgba(236, 202, 126, 0.15), transparent 22%), linear-gradient(135deg, #101012 0%, #24312E 42%, #4D6752 100%)",
        "sidebar": "linear-gradient(180deg, rgba(16, 16, 18, 0.96), rgba(43, 55, 47, 0.92))",
        "panel": "rgba(20, 20, 24, 0.74)",
        "panel_alt": "rgba(41, 52, 44, 0.68)",
        "text": "#FAF5EC",
        "muted": "#D8CEBF",
        "accent": "#E0B971",
        "accent_soft": "rgba(224, 185, 113, 0.14)",
        "line": "rgba(255, 255, 255, 0.10)",
    },
    "Lotus": {
        "tag": "Soft and reassuring",
        "background": "radial-gradient(circle at top left, rgba(255, 221, 231, 0.18), transparent 26%), linear-gradient(135deg, #24141C 0%, #492A38 44%, #8F6071 100%)",
        "sidebar": "linear-gradient(180deg, rgba(36, 20, 28, 0.96), rgba(84, 48, 67, 0.92))",
        "panel": "rgba(38, 22, 31, 0.74)",
        "panel_alt": "rgba(72, 42, 58, 0.68)",
        "text": "#FFF7FA",
        "muted": "#EED6DF",
        "accent": "#FFC5D8",
        "accent_soft": "rgba(255, 197, 216, 0.15)",
        "line": "rgba(255, 255, 255, 0.10)",
    },
}


def init_theme_state() -> None:
    if "theme_name" not in st.session_state:
        st.session_state.theme_name = "Forest"


def apply_theme(theme_name: str) -> None:
    theme = THEMES[theme_name]
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;700&family=Manrope:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: "Manrope", sans-serif;
        }}

        .stApp {{
            background: {theme["background"]};
            color: {theme["text"]};
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        [data-testid="stSidebar"] {{
            background: {theme["sidebar"]};
            border-right: 1px solid {theme["line"]};
        }}

        [data-testid="stSidebar"] * {{
            color: {theme["text"]};
        }}

        .block-container {{
            max-width: 1200px;
            padding-top: 1.15rem;
            padding-bottom: 4.8rem;
        }}

        .aarohi-shell {{
            border: 1px solid {theme["line"]};
            background: linear-gradient(180deg, {theme["panel"]} 0%, {theme["panel_alt"]} 100%);
            border-radius: 24px;
            padding: 1rem 1.1rem;
            box-shadow: 0 20px 48px rgba(0, 0, 0, 0.16);
        }}

        .aarohi-topbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
            padding-bottom: 0.7rem;
            border-bottom: 1px solid {theme["line"]};
        }}

        .aarohi-title {{
            font-family: "Fraunces", serif;
            font-size: 2rem;
            margin: 0;
            color: {theme["text"]};
        }}

        .aarohi-subtitle {{
            margin: 0.2rem 0 0 0;
            color: {theme["muted"]};
            font-size: 0.95rem;
        }}

        .aarohi-chip {{
            display: inline-flex;
            align-items: center;
            padding: 0.28rem 0.62rem;
            border-radius: 999px;
            background: {theme["accent_soft"]};
            color: {theme["accent"]};
            font-size: 0.77rem;
            font-weight: 700;
            margin-right: 0.45rem;
            margin-top: 0.35rem;
        }}

        .aarohi-summary {{
            margin: 0;
            color: {theme["muted"]};
            line-height: 1.5;
            font-size: 0.94rem;
        }}

        .aarohi-empty {{
            border: 1px dashed {theme["line"]};
            background: rgba(255, 255, 255, 0.04);
            border-radius: 24px;
            padding: 1.2rem;
            color: {theme["muted"]};
        }}

        [data-testid="stSidebar"] .stButton > button {{
            min-height: 2.05rem;
            padding: 0.3rem 0.55rem;
            justify-content: flex-start;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 0.87rem;
        }}

        [data-testid="stSidebar"] .stTextInput input {{
            background: rgba(255, 255, 255, 0.06) !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["line"]} !important;
            border-radius: 14px !important;
        }}

        div[data-baseweb="select"] > div {{
            background: rgba(255, 255, 255, 0.06) !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["line"]} !important;
            border-radius: 14px !important;
        }}

        [data-testid="stBottomBlockContainer"] {{
            background: linear-gradient(180deg, rgba(0, 0, 0, 0.0), {theme["panel_alt"]}) !important;
            padding-bottom: 0 !important;
            padding-top: 0 !important;
            border-top: none !important;
        }}

        [data-testid="stBottomBlockContainer"] > div {{
            background: transparent !important;
            padding: 0 !important;
            max-width: 982px !important;
            margin: 0 auto !important;
            border-top: none !important;
        }}

        [data-testid="stBottom"] {{
            background: linear-gradient(180deg, rgba(0, 0, 0, 0.0), {theme["panel_alt"]}) !important;
        }}

        [data-testid="stChatInput"] {{
            bottom: 0 !important;
            background: transparent !important;
            padding-bottom: 0 !important;
            margin-bottom: 0 !important;
            width: 982px !important;
            max-width: calc(100vw - 2rem) !important;
        }}

        [data-testid="stChatInput"] > div {{
            width: 982px !important;
            max-width: calc(100vw - 2rem) !important;
            margin: 0 auto;
            border-radius: 0 !important;
            border: none !important;
            background: transparent !important;
            backdrop-filter: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }}

        [data-testid="stChatInput"] > div:focus-within {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}

        [data-testid="stChatInput"] textarea {{
            min-height: 38px !important;
            max-height: 96px !important;
            padding-top: 0.52rem !important;
            padding-bottom: 0.48rem !important;
            padding-left: 0.9rem !important;
            padding-right: 2.8rem !important;
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid {theme["line"]} !important;
            border-radius: 999px !important;
            box-shadow: none !important;
            overflow-y: auto !important;
        }}

        [data-testid="stChatInput"] textarea:focus {{
            border-color: {theme["accent"]} !important;
            box-shadow: 0 0 0 1px {theme["accent_soft"]} !important;
        }}

        [data-testid="stChatInput"] button {{
            min-height: 2rem !important;
            height: 2rem !important;
            width: 2rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            align-self: center !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding: 0 !important;
        }}

        [data-testid="stChatInput"] button svg,
        [data-testid="stChatInputSubmitButton"] button svg,
        [data-testid="stChatInputSubmitButton"] svg {{
            display: block !important;
            margin: auto !important;
            transform: translateY(-1px);
        }}

        .stButton > button, .stFormSubmitButton > button {{
            border-radius: 15px;
            border: 1px solid {theme["line"]};
            background: linear-gradient(135deg, {theme["accent"]}, rgba(255, 255, 255, 0.12));
            color: #101317;
            font-weight: 800;
        }}

        .stButton > button:hover, .stFormSubmitButton > button:hover {{
            border-color: rgba(255, 255, 255, 0.22);
        }}

        .stCaption, label, .stMarkdown, .stSelectbox label, .stTextArea label {{
            color: {theme["muted"]};
        }}

        .jump-latest {{
            position: fixed;
            right: 1.4rem;
            bottom: 3.8rem;
            z-index: 40;
            padding: 0.6rem 0.9rem;
            border-radius: 999px;
            background: {theme["accent"]};
            color: #0E1117 !important;
            font-weight: 800;
            text-decoration: none !important;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.18);
        }}

        @media (max-width: 960px) {{
            .block-container {{
                padding-top: 0.9rem;
                padding-bottom: 4.6rem;
            }}

            .aarohi-topbar {{
                flex-direction: column;
                align-items: flex-start;
            }}

            .aarohi-title {{
                font-size: 1.75rem;
            }}

            [data-testid="stChatInput"],
            [data-testid="stChatInput"] > div,
            [data-testid="stBottomBlockContainer"] > div {{
                width: calc(100vw - 1rem) !important;
                max-width: calc(100vw - 1rem) !important;
            }}

            .jump-latest {{
                right: 0.8rem;
                bottom: 3.5rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_timestamp(value: str | None) -> str:
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%d %b, %H:%M")
    except ValueError:
        return value


def format_sidebar_timestamp(value: str | None) -> str:
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        if dt.date() == now.date():
            return dt.strftime("%H:%M")
        return dt.strftime("%d %b")
    except ValueError:
        return value
