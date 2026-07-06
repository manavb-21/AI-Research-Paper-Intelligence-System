import os
from html import escape
from typing import Any

import requests
import streamlit as st


DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"
API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


st.set_page_config(
    page_title="AI Research Paper Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    """Apply custom CSS for a polished research-focused interface."""
    st.markdown(
        """
        <style>
            :root {
                --bg: #f6f8fc;
                --bg-deep: #e8eef8;
                --surface: rgba(255, 255, 255, 0.92);
                --surface-strong: rgba(255, 255, 255, 0.98);
                --ink: #0f172a;
                --ink-soft: #1f2937;
                --muted: #475569;
                --line: rgba(71, 85, 105, 0.26);
                --line-strong: rgba(51, 65, 85, 0.38);
                --accent: #2563eb;
                --accent-strong: #1d4ed8;
                --accent-soft: rgba(37, 99, 235, 0.12);
                --teal: #0f766e;
                --teal-soft: rgba(15, 118, 110, 0.12);
                --violet: #6d28d9;
                --violet-soft: rgba(109, 40, 217, 0.12);
                --shadow-sm: 0 10px 26px rgba(15, 23, 42, 0.10);
                --shadow-md: 0 18px 48px rgba(15, 23, 42, 0.15);
                --radius: 18px;
            }

            html {
                scroll-behavior: smooth;
            }

            .stApp {
                background:
                    radial-gradient(circle at 16% 4%, rgba(37, 99, 235, 0.13), transparent 30%),
                    radial-gradient(circle at 88% 12%, rgba(15, 118, 110, 0.10), transparent 28%),
                    linear-gradient(180deg, var(--bg) 0%, var(--bg-deep) 48%, #f8fafc 100%);
                color: #0f172a;
            }

            .stApp,
            .stApp [data-testid="stAppViewContainer"],
            .stApp [data-testid="stHeader"],
            .stApp [data-testid="stToolbar"],
            .stApp [data-testid="stDecoration"],
            .stApp [data-testid="block-container"],
            .stApp [data-testid="stVerticalBlock"],
            .stApp [data-testid="stHorizontalBlock"] {
                color: #0f172a;
            }

            .stMarkdown,
            .stMarkdown p,
            .stMarkdown li,
            .stMarkdown span,
            .stMarkdown div,
            div[data-testid="stMarkdownContainer"],
            div[data-testid="stMarkdownContainer"] p,
            div[data-testid="stMarkdownContainer"] li,
            div[data-testid="stMarkdownContainer"] span,
            div[data-testid="stMarkdownContainer"] strong,
            div[data-testid="stMarkdownContainer"] em {
                color: #0f172a;
            }

            div[data-testid="stCaptionContainer"],
            div[data-testid="stCaptionContainer"] p,
            div[data-testid="stCaptionContainer"] span,
            .stCaptionContainer,
            .stCaptionContainer p,
            .stCaptionContainer span {
                color: #475569;
            }

            code,
            pre,
            div[data-testid="stCodeBlock"],
            div[data-testid="stCodeBlock"] * {
                background-color: rgba(248, 250, 252, 0.96);
                color: #0f172a;
            }

            div[data-testid="stAlert"],
            div[data-testid="stAlert"] *,
            div[data-testid="stException"],
            div[data-testid="stException"] * {
                color: #0f172a;
            }

            .block-container {
                max-width: 1180px;
                padding: 2.2rem 2rem 1.6rem;
            }

            h1, h2, h3, p {
                letter-spacing: 0;
                color: #0f172a;
            }

            h1, h2, h3 {
                color: #0f172a;
            }

            div[data-testid="stForm"] {
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: var(--radius);
                box-shadow: var(--shadow-sm);
                backdrop-filter: blur(18px);
                padding: 1.1rem 1.15rem 1.2rem;
                transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
                color: #0f172a;
            }

            div[data-testid="stForm"]:hover {
                border-color: rgba(37, 99, 235, 0.25);
                box-shadow: var(--shadow-md);
            }

            div[data-testid="stTextInput"] label,
            div[data-testid="stTextInput"] label *,
            div[data-testid="stSlider"] label,
            div[data-testid="stSlider"] label *,
            label[data-testid="stWidgetLabel"],
            label[data-testid="stWidgetLabel"] *,
            div[data-testid="stWidgetLabel"],
            div[data-testid="stWidgetLabel"] * {
                color: #1f2937;
                font-size: 0.88rem;
                font-weight: 760;
            }

            div[data-testid="stTextInput"] input {
                min-height: 3.15rem;
                border: 1px solid var(--line-strong);
                border-radius: 14px;
                background: rgba(255, 255, 255, 0.98);
                color: #0f172a;
                font-size: 1rem;
                padding: 0.85rem 1rem;
                box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04);
                transition: border-color 180ms ease, box-shadow 180ms ease, background 180ms ease;
                caret-color: #1d4ed8;
                -webkit-text-fill-color: #0f172a;
            }

            div[data-testid="stTextInput"] input::placeholder {
                color: #64748b;
                opacity: 1;
                -webkit-text-fill-color: #64748b;
            }

            div[data-testid="stTextInput"] input:focus {
                border-color: rgba(37, 99, 235, 0.72);
                box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.11);
                background: #ffffff;
                color: #0f172a;
                -webkit-text-fill-color: #0f172a;
            }

            div[data-testid="stSlider"] {
                padding-top: 0.1rem;
                color: #0f172a;
            }

            div[data-testid="stSlider"] [data-baseweb="slider"],
            div[data-testid="stSlider"] [data-baseweb="slider"] * {
                color: #1d4ed8;
            }

            div[data-testid="stSlider"] [role="slider"] {
                background-color: #ffffff;
                border: 2px solid #1d4ed8;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.28);
            }

            div[data-testid="stSlider"] div[data-testid="stTickBar"],
            div[data-testid="stSlider"] div[data-testid="stTickBar"] * {
                color: #475569;
            }

                    /* ================= BUTTON ================= */

            div.stButton > button,
            .stButton > button,
            button[kind="primary"],
            button[kind="secondary"],
            button[data-testid="stBaseButton-primary"],
            button[data-testid="stBaseButton-secondary"],
            button[data-testid="stBaseButton-secondaryFormSubmit"],
            button[data-testid="baseButton-primary"],
            button[data-testid="baseButton-secondary"],
            button[data-testid="baseButton-secondaryFormSubmit"],
            div[data-testid="stFormSubmitButton"] button,
            div[data-testid="stFormSubmitButton"] button[kind],
            div[data-testid="stFormSubmitButton"] button[data-testid] {

                width: 100%;
                min-height: 3.3rem;

                border: none !important;
                border-radius: 14px;

                background: linear-gradient(135deg,#2563eb,#1d4ed8) !important;
                background-color: #2563eb !important;

                color: white !important;
                -webkit-text-fill-color: white !important;

                font-size: 1rem;
                font-weight: 700;

                cursor:pointer;

                transition: all .25s ease;

                box-shadow:
                    0 8px 20px rgba(37,99,235,.25);

            }

            div.stButton > button:hover,
            .stButton > button:hover,
            button[kind="primary"]:hover,
            button[kind="secondary"]:hover,
            button[data-testid="stBaseButton-primary"]:hover,
            button[data-testid="stBaseButton-secondary"]:hover,
            button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
            button[data-testid="baseButton-primary"]:hover,
            button[data-testid="baseButton-secondary"]:hover,
            button[data-testid="baseButton-secondaryFormSubmit"]:hover,
            div[data-testid="stFormSubmitButton"] button:hover {

                transform:translateY(-2px);

                background:
                linear-gradient(135deg,#1d4ed8,#1e40af) !important;
                background-color: #1d4ed8 !important;

                color:white !important;
                -webkit-text-fill-color:white !important;

            }

            div.stButton > button *,
            .stButton > button *,
            button[kind="primary"],
            button[kind="primary"] *,
            button[kind="secondary"],
            button[kind="secondary"] *,
            button[data-testid="stBaseButton-primary"],
            button[data-testid="stBaseButton-primary"] *,
            button[data-testid="stBaseButton-secondary"],
            button[data-testid="stBaseButton-secondary"] *,
            button[data-testid="stBaseButton-secondaryFormSubmit"],
            button[data-testid="stBaseButton-secondaryFormSubmit"] *,
            button[data-testid="baseButton-primary"],
            button[data-testid="baseButton-primary"] *,
            button[data-testid="baseButton-secondary"],
            button[data-testid="baseButton-secondary"] *,
            button[data-testid="baseButton-secondaryFormSubmit"],
            button[data-testid="baseButton-secondaryFormSubmit"] *,
            div[data-testid="stFormSubmitButton"] button,
            div[data-testid="stFormSubmitButton"] button *,
            div[data-testid="stFormSubmitButton"] p,
            div[data-testid="stFormSubmitButton"] span {

                color:white !important;

                fill:white !important;

                -webkit-text-fill-color:white !important;

            }

            section[data-testid="stSidebar"] {
                background:
                    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.98));
                border-right: 1px solid var(--line);
                color: #0f172a;
            }

            section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
                padding-top: 1.6rem;
            }

            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] li,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] div,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
            section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
                color: #0f172a;
            }

            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
            section[data-testid="stSidebar"] .sidebar-copy,
            section[data-testid="stSidebar"] .pipeline-arrow {
                color: #475569;
            }

            section[data-testid="stSidebar"] code,
            section[data-testid="stSidebar"] pre,
            section[data-testid="stSidebar"] div[data-testid="stCodeBlock"],
            section[data-testid="stSidebar"] div[data-testid="stCodeBlock"] * {
                background-color: #f8fafc;
                color: #0f172a;
            }

            .hero {
                position: relative;
                overflow: hidden;
                background:
                    linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.82)),
                    linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(15, 118, 110, 0.08));
                border: 1px solid var(--line);
                border-radius: 26px;
                box-shadow: var(--shadow-md);
                backdrop-filter: blur(20px);
                padding: clamp(1.35rem, 3vw, 2.25rem);
                margin-bottom: 1.2rem;
            }

            .hero::after {
                content: "";
                position: absolute;
                width: 220px;
                height: 220px;
                right: -90px;
                top: -90px;
                background: radial-gradient(circle, rgba(37, 99, 235, 0.18), transparent 70%);
                pointer-events: none;
            }

            .eyebrow {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                border: 1px solid rgba(37, 99, 235, 0.18);
                border-radius: 999px;
                background: rgba(37, 99, 235, 0.08);
                color: #1d4ed8;
                font-size: 0.78rem;
                font-weight: 820;
                letter-spacing: 0.06em;
                line-height: 1;
                padding: 0.48rem 0.72rem;
                text-transform: uppercase;
            }

            .hero-title {
                color: #0f172a;
                font-size: clamp(2.2rem, 5vw, 4.25rem);
                font-weight: 880;
                line-height: 1.02;
                margin: 1rem 0 0.75rem;
                max-width: 920px;
            }

            .hero-subtitle {
                color: #1f2937;
                font-size: clamp(1rem, 1.6vw, 1.18rem);
                font-weight: 640;
                line-height: 1.65;
                max-width: 790px;
                margin-bottom: 1.1rem;
            }

            .hero-meta {
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
            }

            .hero-chip {
                border: 1px solid var(--line);
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.88);
                color: #1f2937;
                font-size: 0.84rem;
                font-weight: 720;
                padding: 0.42rem 0.7rem;
            }

            .section-heading {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                margin: 1.35rem 0 0.65rem;
            }

            .section-title {
                color: #0f172a;
                font-size: 1.18rem;
                font-weight: 840;
                margin: 0;
            }

            .section-note {
                color: #475569;
                font-size: 0.88rem;
                font-weight: 650;
            }

            .metric-strip {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.9rem;
                margin: 1.15rem 0 1.35rem;
            }

            .metric-card,
            .summary-card,
            .paper-card,
            .empty-card,
            .status-card {
                background: var(--surface-strong);
                border: 1px solid var(--line);
                border-radius: var(--radius);
                box-shadow: var(--shadow-sm);
                backdrop-filter: blur(18px);
                color: #0f172a;
            }

            .metric-card,
            .summary-card,
            .paper-card,
            .empty-card {
                transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
            }

            .metric-card:hover,
            .summary-card:hover,
            .paper-card:hover {
                border-color: rgba(37, 99, 235, 0.22);
                box-shadow: var(--shadow-md);
                transform: translateY(-2px);
            }

            .metric-card {
                padding: 1rem 1.05rem;
            }

            .metric-label {
                color: #475569;
                font-size: 0.74rem;
                font-weight: 820;
                letter-spacing: 0.055em;
                text-transform: uppercase;
            }

            .metric-value {
                color: #0f172a;
                font-size: 1.55rem;
                font-weight: 880;
                line-height: 1.1;
                margin-top: 0.34rem;
            }

            .summary-card {
                padding: clamp(1.15rem, 2.5vw, 1.65rem);
                margin-top: 0.75rem;
            }

            .summary-title {
                color: #0f172a;
                font-size: 1.12rem;
                font-weight: 860;
                margin-bottom: 0.7rem;
            }

            .summary-body {
                color: #1f2937;
                font-size: 1.03rem;
                line-height: 1.78;
            }

            .paper-card {
                padding: clamp(1.05rem, 2.4vw, 1.35rem);
                margin: 0.92rem 0;
            }

            .paper-topline {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 0.8rem;
            }

            .paper-title {
                color: #0f172a;
                font-size: 1.04rem;
                font-weight: 820;
                line-height: 1.45;
                margin: 0;
            }

            .score-badge {
                flex: 0 0 auto;
                display: inline-flex;
                align-items: center;
                border: 1px solid rgba(37, 99, 235, 0.22);
                border-radius: 999px;
                background: var(--accent-soft);
                color: #1d4ed8;
                font-size: 0.82rem;
                font-weight: 820;
                line-height: 1;
                padding: 0.46rem 0.68rem;
                white-space: nowrap;
            }

            .paper-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.9rem;
            }

            .chip-group-title {
                color: #1f2937;
                font-size: 0.78rem;
                font-weight: 840;
                letter-spacing: 0.045em;
                text-transform: uppercase;
                margin-bottom: 0.45rem;
            }

            .tag-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.46rem;
            }

            .tag {
                display: inline-flex;
                align-items: center;
                border: 1px solid rgba(37, 99, 235, 0.15);
                border-radius: 999px;
                background: rgba(37, 99, 235, 0.07);
                color: #1e3a8a;
                font-size: 0.8rem;
                font-weight: 720;
                line-height: 1;
                padding: 0.42rem 0.62rem;
            }

            .entity-tag {
                border-color: rgba(15, 118, 110, 0.18);
                background: var(--teal-soft);
                color: #115e59;
            }

            .empty-card {
                color: #334155;
                font-size: 0.98rem;
                line-height: 1.7;
                padding: 1.15rem 1.25rem;
            }

            .status-card {
                padding: 1rem 1.1rem;
                margin-top: 1rem;
                color: #0f172a;
            }

            div[data-testid="stStatusWidget"],
            div[data-testid="stStatus"],
            details[data-testid="stStatusWidget"],
            details[data-testid="stStatus"],
            div[data-testid="stStatusWidget"] details,
            div[data-testid="stStatus"] details {
                background: rgba(255, 255, 255, 0.96) !important;
                background-color: rgba(255, 255, 255, 0.96) !important;
                color: #0f172a !important;
                border-color: rgba(71, 85, 105, 0.26) !important;
                border-radius: 14px !important;
                box-shadow: 0 10px 26px rgba(15, 23, 42, 0.10);
            }

            div[data-testid="stStatusWidget"] *,
            div[data-testid="stStatus"] *,
            details[data-testid="stStatusWidget"] *,
            details[data-testid="stStatus"] * {
                color: #0f172a !important;
                -webkit-text-fill-color: #0f172a !important;
            }

            div[data-testid="stStatusWidget"] summary,
            div[data-testid="stStatusWidget"] summary *,
            div[data-testid="stStatus"] summary,
            div[data-testid="stStatus"] summary *,
            div[data-testid="stStatusWidget"] [data-testid="stStatusLabel"],
            div[data-testid="stStatusWidget"] [data-testid="stStatusLabel"] *,
            div[data-testid="stStatus"] [data-testid="stStatusLabel"],
            div[data-testid="stStatus"] [data-testid="stStatusLabel"] * {
                background: transparent !important;
                color: #0f172a !important;
                font-weight: 760;
                -webkit-text-fill-color: #0f172a !important;
            }

            div[data-testid="stStatusWidget"] [data-testid="stStatusContent"],
            div[data-testid="stStatus"] [data-testid="stStatusContent"],
            div[data-testid="stStatusWidget"] [data-testid="stStatusContent"] *,
            div[data-testid="stStatus"] [data-testid="stStatusContent"] * {
                background: transparent !important;
                color: #0f172a !important;
                -webkit-text-fill-color: #0f172a !important;
            }

            .sidebar-brand {
                border: 1px solid var(--line);
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.94);
                box-shadow: var(--shadow-sm);
                padding: 1rem;
                margin-bottom: 1rem;
            }

            .sidebar-title {
                color: #0f172a;
                font-size: 1.22rem;
                font-weight: 880;
                line-height: 1.2;
                margin-bottom: 0.4rem;
            }

            .sidebar-copy {
                color: #475569;
                font-size: 0.9rem;
                line-height: 1.55;
            }

            .sidebar-section {
                color: #0f172a;
                font-size: 0.8rem;
                font-weight: 840;
                letter-spacing: 0.06em;
                margin: 1.1rem 0 0.55rem;
                text-transform: uppercase;
            }

            .pipeline {
                border: 1px solid var(--line);
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.86);
                padding: 0.78rem;
            }

            .pipeline-step {
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid rgba(37, 99, 235, 0.14);
                border-radius: 12px;
                background: rgba(37, 99, 235, 0.055);
                color: #1f2937;
                font-size: 0.86rem;
                font-weight: 760;
                min-height: 2.25rem;
                padding: 0.45rem 0.65rem;
                text-align: center;
            }

            .pipeline-arrow {
                color: #475569;
                font-size: 1rem;
                font-weight: 800;
                line-height: 1;
                padding: 0.26rem 0;
                text-align: center;
            }

            .stack-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 0.42rem;
            }

            .stack-chip {
                border: 1px solid var(--line);
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.9);
                color: #1f2937;
                font-size: 0.78rem;
                font-weight: 720;
                padding: 0.35rem 0.56rem;
            }

            .footer {
                border-top: 1px solid var(--line);
                color: #475569;
                font-size: 0.9rem;
                font-weight: 620;
                margin-top: 2rem;
                padding: 1.15rem 0 0.2rem;
                text-align: center;
            }

            @media (max-width: 900px) {
                .block-container {
                    padding-left: 1.1rem;
                    padding-right: 1.1rem;
                }

                .metric-strip,
                .paper-grid {
                    grid-template-columns: 1fr;
                }

                .paper-topline {
                    align-items: flex-start;
                    flex-direction: column;
                }
            }

            @media (max-width: 640px) {
                .hero {
                    border-radius: 20px;
                    padding: 1.1rem;
                }

                .hero-title {
                    font-size: 2.05rem;
                }

                .hero-meta {
                    gap: 0.4rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def search_papers(query: str, k: int) -> dict[str, Any]:
    """Call the FastAPI backend search endpoint and return its JSON response."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/search",
            params={"query": query, "k": k},
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("The backend request timed out. Try a smaller k value or retry shortly.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            f"Could not reach the backend at {API_BASE_URL}. Make sure FastAPI is running."
        ) from exc
    except requests.exceptions.HTTPError as exc:
        detail = _extract_error_detail(exc.response)
        raise RuntimeError(detail) from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError("The backend request failed unexpectedly.") from exc
    except ValueError as exc:
        raise RuntimeError("The backend returned a response that was not valid JSON.") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("The backend returned an unexpected response format.")

    return payload


def _extract_error_detail(response: requests.Response | None) -> str:
    """Extract a readable error message from a failed backend response."""
    if response is None:
        return "The backend returned an error."

    try:
        payload = response.json()
    except ValueError:
        return f"The backend returned HTTP {response.status_code}."

    detail = payload.get("detail") if isinstance(payload, dict) else None
    if isinstance(detail, str):
        return detail

    return f"The backend returned HTTP {response.status_code}."


def normalize_keywords(raw_keywords: Any) -> list[str]:
    """Convert backend keyword payloads into display-ready labels."""
    if not isinstance(raw_keywords, list):
        return []

    labels: list[str] = []
    for item in raw_keywords:
        if isinstance(item, str):
            labels.append(item)
        elif isinstance(item, (list, tuple)) and item:
            labels.append(str(item[0]))
        elif isinstance(item, dict):
            value = item.get("keyword") or item.get("word") or item.get("text")
            if value:
                labels.append(str(value))

    return labels


def normalize_entities(raw_entities: Any) -> list[str]:
    """Convert backend entity payloads into compact display labels."""
    if not isinstance(raw_entities, list):
        return []

    labels: list[str] = []
    for item in raw_entities:
        if isinstance(item, str):
            labels.append(item)
        elif isinstance(item, (list, tuple)) and item:
            name = str(item[0])
            entity_type = str(item[1]) if len(item) > 1 else ""
            labels.append(f"{name} - {entity_type}" if entity_type else name)
        elif isinstance(item, dict):
            name = item.get("word") or item.get("text") or item.get("entity")
            entity_type = item.get("entity_group") or item.get("type") or item.get("label")
            if name and entity_type:
                labels.append(f"{name} - {entity_type}")
            elif name:
                labels.append(str(name))

    return labels


def format_score(score: Any) -> str:
    """Format a similarity score from the backend for display."""
    try:
        return f"{float(score):.3f}"
    except (TypeError, ValueError):
        return "N/A"


def render_sidebar() -> None:
    """Render the project overview and runtime settings in the sidebar."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-title">AI Research Paper Intelligence</div>
                <div class="sidebar-copy">
                    A semantic research assistant for discovering, enriching, and
                    synthesizing machine learning papers.
                </div>
            </div>
            <div class="sidebar-section">Pipeline</div>
            <div class="pipeline">
                <div class="pipeline-step">Sentence Transformer</div>
                <div class="pipeline-arrow">↓</div>
                <div class="pipeline-step">FAISS</div>
                <div class="pipeline-arrow">↓</div>
                <div class="pipeline-step">KeyBERT</div>
                <div class="pipeline-arrow">↓</div>
                <div class="pipeline-step">NER</div>
                <div class="pipeline-arrow">↓</div>
                <div class="pipeline-step">BART</div>
                <div class="pipeline-arrow">↓</div>
                <div class="pipeline-step">Summary</div>
            </div>
            <div class="sidebar-section">Tech Stack</div>
            <div class="stack-grid">
                <span class="stack-chip">FastAPI</span>
                <span class="stack-chip">PyTorch</span>
                <span class="stack-chip">Transformers</span>
                <span class="stack-chip">FAISS</span>
                <span class="stack-chip">KeyBERT</span>
                <span class="stack-chip">BERT</span>
                <span class="stack-chip">Streamlit</span>
            </div>
            <div class="sidebar-section">Backend</div>
            """,
            unsafe_allow_html=True,
        )
        st.code(API_BASE_URL, language="text")
        st.caption("Set API_BASE_URL to point this UI at another backend.")


def render_header() -> None:
    """Render the main application header."""
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Modern AI Research Platform</div>
            <h1 class="hero-title">AI Research Paper Intelligence System</h1>
            <div class="hero-subtitle">
                Semantic Search • Named Entity Recognition • Generative AI
                <br>
                Ask a research question and receive a synthesized answer backed by
                retrieved machine learning papers, keywords, and entities.
            </div>
            <div class="hero-meta">
                <span class="hero-chip">Semantic retrieval</span>
                <span class="hero-chip">Paper intelligence</span>
                <span class="hero-chip">AI synthesis</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(payload: dict[str, Any]) -> None:
    """Render high-level response metrics."""
    top_papers = payload.get("top_papers", [])
    paper_count = len(top_papers) if isinstance(top_papers, list) else 0
    summary = str(payload.get("generative_summary", ""))
    word_count = len(summary.split())

    st.markdown(
        f"""
        <div class="metric-strip">
            <div class="metric-card">
                <div class="metric-label">Retrieved Papers</div>
                <div class="metric-value">{paper_count}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Summary Words</div>
                <div class="metric-value">{word_count}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Pipeline</div>
                <div class="metric-value">AI Search</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary(payload: dict[str, Any]) -> None:
    """Render the generated summary card."""
    summary = payload.get("generative_summary") or payload.get("summary") or ""
    if not summary:
        st.markdown(
            '<div class="empty-card">No generated summary was returned by the backend.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="section-heading">
            <h2 class="section-title">AI Generated Summary</h2>
            <div class="section-note">Synthesized from retrieved papers</div>
        </div>
        <div class="summary-card">
            <div class="summary-body">{escape(str(summary))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tag_row(labels: list[str], css_class: str = "tag") -> str:
    """Render labels as inline HTML tags."""
    if not labels:
        return '<span class="tag">None returned</span>'

    return "".join(f'<span class="{css_class}">{escape(label)}</span>' for label in labels)


def render_top_papers(payload: dict[str, Any]) -> None:
    """Render top retrieved papers when the backend includes them."""
    top_papers = payload.get("top_papers")
    if not isinstance(top_papers, list) or not top_papers:
        st.markdown(
            """
            <div class="empty-card">
                Top retrieved papers will appear here when the backend includes them.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        """
        <div class="section-heading">
            <h2 class="section-title">Top Retrieved Papers</h2>
            <div class="section-note">Ranked by semantic similarity</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for paper in top_papers:
        if not isinstance(paper, dict):
            continue

        title = str(paper.get("title", "Untitled paper"))
        score = paper.get("similarity_score", paper.get("score"))
        keywords = normalize_keywords(paper.get("keywords"))
        entities = normalize_entities(paper.get("entities"))

        st.markdown(
            f"""
            <article class="paper-card">
                <div class="paper-topline">
                    <h3 class="paper-title">{escape(title)}</h3>
                    <span class="score-badge">Similarity {format_score(score)}</span>
                </div>
                <div class="paper-grid">
                    <div>
                        <div class="chip-group-title">Keywords</div>
                        <div class="tag-row">{render_tag_row(keywords)}</div>
                    </div>
                    <div>
                        <div class="chip-group-title">Named Entities</div>
                        <div class="tag-row">{render_tag_row(entities, "tag entity-tag")}</div>
                    </div>
                </div>
            </article>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    """Render the application footer."""
    st.markdown(
        """
        <div class="footer">
            Built using FastAPI • FAISS • Sentence Transformers • KeyBERT • BERT NER • BART-Large-CNN
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Run the Streamlit frontend."""
    inject_styles()
    render_sidebar()
    render_header()

    with st.form("search_form"):
        query = st.text_input(
            "Research question",
            placeholder="Search for topics like efficient transformers, graph neural networks, or RAG evaluation",
        )
        col_k, col_button = st.columns([0.85, 2.15])
        with col_k:
            k = st.slider("Top K papers", min_value=1, max_value=10, value=3)
        with col_button:
            st.write("")
            submitted = st.form_submit_button("Search Papers", use_container_width=True)

    if submitted:
        if not query.strip():
            st.warning("Enter a research question to start the search.")
        else:
            status = st.status("Searching papers...", expanded=True)
            status.write("Generating embeddings...")
            status.write("Running semantic search...")
            status.write("Extracting keywords and named entities...")
            status.write("Generating AI summary...")

            try:
                payload = search_papers(query.strip(), k)
            except RuntimeError as exc:
                status.update(label="Search failed", state="error", expanded=False)
                st.error(str(exc))
            else:
                status.update(label="Research synthesis complete", state="complete", expanded=False)
                render_metrics(payload)
                render_summary(payload)
                render_top_papers(payload)
    else:
        st.markdown(
            """
            <div class="empty-card">
                Enter a research question above to retrieve relevant papers and generate
                an evidence-aware summary.
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_footer()


if __name__ == "__main__":
    main()
