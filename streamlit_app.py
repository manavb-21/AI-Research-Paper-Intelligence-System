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
                --ink: #172033;
                --muted: #617086;
                --line: #dce3ee;
                --panel: #ffffff;
                --soft: #f5f7fb;
                --accent: #2264d1;
                --accent-dark: #184a9b;
                --success: #0f766e;
            }

            .stApp {
                background:
                    linear-gradient(180deg, #f7f9fd 0%, #eef3f9 45%, #f8fafc 100%);
                color: var(--ink);
            }

            .block-container {
                padding-top: 2.25rem;
                padding-bottom: 1.5rem;
                max-width: 1180px;
            }

            h1, h2, h3 {
                letter-spacing: 0;
                color: var(--ink);
            }

            .app-header {
                border-bottom: 1px solid var(--line);
                padding-bottom: 1.2rem;
                margin-bottom: 1.3rem;
            }

            .app-kicker {
                color: var(--accent);
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-bottom: 0.35rem;
            }

            .app-title {
                color: var(--ink);
                font-size: clamp(2rem, 4vw, 3.5rem);
                font-weight: 800;
                line-height: 1.05;
                margin: 0;
            }

            .app-subtitle {
                color: var(--muted);
                font-size: 1.05rem;
                line-height: 1.65;
                max-width: 780px;
                margin-top: 0.8rem;
            }

            .metric-strip {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.8rem;
                margin: 1.2rem 0 1.5rem;
            }

            .metric-card, .summary-card, .paper-card, .empty-card {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid var(--line);
                border-radius: 8px;
                box-shadow: 0 14px 36px rgba(31, 45, 71, 0.08);
            }

            .metric-card {
                padding: 0.9rem 1rem;
            }

            .metric-label {
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 700;
                text-transform: uppercase;
            }

            .metric-value {
                color: var(--ink);
                font-size: 1.35rem;
                font-weight: 800;
                margin-top: 0.2rem;
            }

            .summary-card {
                padding: 1.25rem 1.35rem;
                margin-top: 1rem;
            }

            .summary-title, .section-title {
                color: var(--ink);
                font-size: 1.05rem;
                font-weight: 800;
                margin-bottom: 0.65rem;
            }

            .summary-body {
                color: #263247;
                line-height: 1.75;
                font-size: 1.02rem;
            }

            .paper-card {
                padding: 1.1rem 1.2rem;
                margin: 0.9rem 0;
            }

            .paper-title {
                color: var(--ink);
                font-size: 1.02rem;
                font-weight: 800;
                line-height: 1.4;
                margin-bottom: 0.4rem;
            }

            .score-pill {
                display: inline-flex;
                align-items: center;
                border: 1px solid rgba(34, 100, 209, 0.24);
                border-radius: 999px;
                color: var(--accent-dark);
                background: rgba(34, 100, 209, 0.08);
                font-size: 0.82rem;
                font-weight: 750;
                padding: 0.2rem 0.6rem;
                margin-bottom: 0.65rem;
            }

            .tag-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.42rem;
                margin-top: 0.45rem;
            }

            .tag {
                border: 1px solid #d8e1ef;
                background: #f7f9fd;
                border-radius: 999px;
                color: #344258;
                font-size: 0.8rem;
                padding: 0.22rem 0.55rem;
            }

            .entity-tag {
                border-color: rgba(15, 118, 110, 0.24);
                background: rgba(15, 118, 110, 0.08);
                color: #0f5f59;
            }

            .empty-card {
                color: var(--muted);
                padding: 1.1rem 1.2rem;
                line-height: 1.65;
            }

            .footer {
                color: var(--muted);
                border-top: 1px solid var(--line);
                font-size: 0.88rem;
                margin-top: 2rem;
                padding-top: 1rem;
                text-align: center;
            }

            section[data-testid="stSidebar"] {
                background: #ffffff;
                border-right: 1px solid var(--line);
            }

            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3 {
                color: var(--ink);
            }

            .stTextInput input {
                border-radius: 8px;
            }

            .stButton > button {
                border-radius: 8px;
                background: var(--accent);
                color: white;
                border: 1px solid var(--accent);
                font-weight: 750;
                min-height: 2.8rem;
            }

            .stButton > button:hover {
                background: var(--accent-dark);
                border-color: var(--accent-dark);
                color: white;
            }

            @media (max-width: 760px) {
                .metric-strip {
                    grid-template-columns: 1fr;
                }

                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
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
            labels.append(f"{name} · {entity_type}" if entity_type else name)
        elif isinstance(item, dict):
            name = item.get("word") or item.get("text") or item.get("entity")
            entity_type = item.get("entity_group") or item.get("type") or item.get("label")
            if name and entity_type:
                labels.append(f"{name} · {entity_type}")
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
        st.title("Research Intelligence")
        st.caption("Semantic discovery for machine learning papers")
        st.markdown(
            """
            This interface connects to your FastAPI backend and runs:

            - SentenceTransformer query embeddings
            - FAISS semantic retrieval
            - KeyBERT keyword extraction
            - BERT named entity recognition
            - BART-Large-CNN summary generation
            """
        )
        st.divider()
        st.subheader("Backend")
        st.code(API_BASE_URL, language="text")
        st.caption("Override with the API_BASE_URL environment variable.")


def render_header() -> None:
    """Render the main application header."""
    st.markdown(
        """
        <div class="app-header">
            <div class="app-kicker">AI Research Paper Intelligence System</div>
            <h1 class="app-title">Explore research papers with semantic search and AI synthesis.</h1>
            <div class="app-subtitle">
                Ask a technical question, retrieve the most relevant ML papers, and review
                a concise generated summary with supporting paper metadata.
            </div>
        </div>
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
                <div class="metric-label">Backend</div>
                <div class="metric-value">FastAPI</div>
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
        <div class="summary-card">
            <div class="summary-title">AI Generated Summary</div>
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

    st.markdown('<div class="section-title">Top Retrieved Papers</div>', unsafe_allow_html=True)

    for paper in top_papers:
        if not isinstance(paper, dict):
            continue

        title = str(paper.get("title", "Untitled paper"))
        score = paper.get("similarity_score", paper.get("score"))
        keywords = normalize_keywords(paper.get("keywords"))
        entities = normalize_entities(paper.get("entities"))

        st.markdown(
            f"""
            <div class="paper-card">
                <div class="paper-title">{escape(title)}</div>
                <div class="score-pill">Similarity score: {format_score(score)}</div>
                <div>
                    <strong>Keywords</strong>
                    <div class="tag-row">{render_tag_row(keywords)}</div>
                </div>
                <div style="margin-top: 0.75rem;">
                    <strong>Named entities</strong>
                    <div class="tag-row">{render_tag_row(entities, "tag entity-tag")}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    """Render the application footer."""
    st.markdown(
        """
        <div class="footer">
            Built for research exploration with FastAPI, FAISS, Sentence Transformers,
            KeyBERT, BERT NER, and BART-Large-CNN.
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
            placeholder="Example: transformer architectures for efficient document summarization",
        )
        col_k, col_button = st.columns([1, 2])
        with col_k:
            k = st.slider("Top K papers", min_value=1, max_value=10, value=3)
        with col_button:
            st.write("")
            submitted = st.form_submit_button("Search Papers", use_container_width=True)

    if submitted:
        if not query.strip():
            st.warning("Enter a research question to start the search.")
        else:
            with st.spinner("Searching papers and generating the synthesis..."):
                try:
                    payload = search_papers(query.strip(), k)
                except RuntimeError as exc:
                    st.error(str(exc))
                else:
                    render_metrics(payload)
                    render_summary(payload)
                    st.divider()
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
