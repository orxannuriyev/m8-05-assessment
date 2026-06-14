"""
CodeLens — AI Code Explanation Assistant
Clean ChatGPT/Claude-style UI with multi-turn conversation, chat history,
streaming responses, and safety mitigation.

Run:  streamlit run app.py
"""

import streamlit as st
from llm_service import ChatService

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodeLens — AI Code Explainer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS — clean dark theme, no dashboard clutter
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #0d1117 !important;
    color: #e6edf3 !important;
}
.main .block-container {
    background: transparent !important;
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 1rem 1.5rem 7rem !important;
}

/* ── Hide Streamlit chrome ── */
[data-testid="stHeader"]      { background: transparent !important; border-bottom: none !important; }
[data-testid="stToolbar"]     { display: none !important; }
[data-testid="stStatusWidget"]{ display: none !important; }
footer                        { display: none !important; }
#MainMenu                     { display: none !important; }

/* ── Sidebar toggle button ── */
button[data-testid="stSidebarCollapseButton"],
button[data-testid="stSidebarCollapsedControl"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    width: 2rem !important;
    height: 2rem !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}
button[data-testid="stSidebarCollapseButton"] > *:not(svg),
button[data-testid="stSidebarCollapsedControl"] > *:not(svg) { display: none !important; }
button[data-testid="stSidebarCollapseButton"] svg,
button[data-testid="stSidebarCollapsedControl"] svg {
    fill: #8b949e !important;
    width: 1rem !important;
    height: 1rem !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #30363d !important;
    min-width: 240px !important;
    max-width: 260px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 1rem 0.85rem !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #8b949e !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
}

/* Sidebar selectbox */
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #c9d1d9 !important;
    font-size: 0.82rem !important;
}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div:hover {
    border-color: #58a6ff !important;
}

/* Sidebar slider */
[data-testid="stSlider"] [role="slider"] {
    background: #58a6ff !important;
    border: 2px solid #0d1117 !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.3) !important;
}
[data-testid="stSlider"] [data-testid="stSliderTickBarMin"],
[data-testid="stSlider"] [data-testid="stSliderTickBarMax"] {
    color: #8b949e !important;
    font-size: 0.7rem !important;
}

/* Sidebar New Chat button */
.new-chat-btn > button {
    background: #238636 !important;
    color: #ffffff !important;
    border: 1px solid #2ea043 !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 0.5rem 0.8rem !important;
    transition: background 0.15s !important;
    font-family: 'Inter', sans-serif !important;
    cursor: pointer !important;
}
.new-chat-btn > button:hover {
    background: #2ea043 !important;
}

/* Sidebar history items */
.hist-item > button {
    background: transparent !important;
    color: #8b949e !important;
    border: 1px solid transparent !important;
    border-radius: 6px !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    width: 100% !important;
    padding: 0.35rem 0.6rem !important;
    text-align: left !important;
    transition: all 0.12s !important;
    font-family: 'Inter', sans-serif !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
.hist-item > button:hover {
    background: #21262d !important;
    color: #c9d1d9 !important;
    border-color: #30363d !important;
}
.hist-item-active > button {
    background: #21262d !important;
    color: #58a6ff !important;
    border-color: #30363d !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 8px !important;
    border: 1px solid transparent !important;
}

/* User */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #1c2128 !important;
    border-color: #30363d !important;
}

/* Assistant */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #0d1117 !important;
    border-color: transparent !important;
}

/* Message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #c9d1d9 !important;
    font-size: 0.92rem !important;
    line-height: 1.75 !important;
}
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: #e6edf3 !important;
    font-weight: 600 !important;
    margin: 1rem 0 0.4rem !important;
}
[data-testid="stChatMessage"] strong { color: #e6edf3 !important; font-weight: 600 !important; }

/* Inline code */
[data-testid="stChatMessage"] code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82em !important;
    background: #161b22 !important;
    color: #79c0ff !important;
    border: 1px solid #30363d !important;
    border-radius: 5px !important;
    padding: 2px 6px !important;
}

/* Code blocks */
[data-testid="stChatMessage"] pre {
    background: #161b22 !important;
    border-radius: 10px !important;
    padding: 1rem 1.1rem !important;
    margin: 0.75rem 0 !important;
    border: 1px solid #30363d !important;
}
[data-testid="stChatMessage"] pre code {
    background: transparent !important;
    color: #e6edf3 !important;
    border: none !important;
    padding: 0 !important;
    font-size: 0.84rem !important;
    line-height: 1.6 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    box-shadow: 0 0 0 0 transparent !important;
    transition: border-color 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #58a6ff !important;
}
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] [data-baseweb],
[data-testid="stChatInput"] [class*="InputContainer"],
[data-testid="stChatInput"] [class*="Root"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #c9d1d9 !important;
    -webkit-text-fill-color: #c9d1d9 !important;
    caret-color: #58a6ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #484f58 !important;
    -webkit-text-fill-color: #484f58 !important;
}
[data-testid="stChatInput"] button {
    background: #238636 !important;
    border: none !important;
    border-radius: 8px !important;
    margin: 6px 8px 6px 0 !important;
    min-width: 36px !important;
    height: 36px !important;
    transition: background 0.15s !important;
}
[data-testid="stChatInput"] button:hover { background: #2ea043 !important; }
[data-testid="stChatInput"] button svg { fill: #ffffff !important; }

/* ── Suggestion chips ── */
.chip-btn > button {
    background: #161b22 !important;
    color: #8b949e !important;
    border: 1px solid #30363d !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.9rem !important;
    width: 100% !important;
    transition: all 0.15s !important;
    font-family: 'Inter', sans-serif !important;
}
.chip-btn > button:hover {
    background: #21262d !important;
    color: #c9d1d9 !important;
    border-color: #58a6ff !important;
}

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid #21262d !important; margin: 0.6rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ──────────────────────────────────────────────────────────────────────────────
# chat_sessions: list of {"id": int, "title": str, "messages": list}
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []

# active_session_idx: index into chat_sessions, or None for a blank new chat
if "active_session_idx" not in st.session_state:
    st.session_state.active_session_idx = None

# model / temperature — persist across reruns
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "qwen2.5:0.5b"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.2

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def _active_messages() -> list:
    idx = st.session_state.active_session_idx
    if idx is not None and 0 <= idx < len(st.session_state.chat_sessions):
        return st.session_state.chat_sessions[idx]["messages"]
    return []


def _get_or_create_service() -> "ChatService":
    """Return the ChatService for the current model, creating one if needed."""
    cache_key = f"svc_{st.session_state.model_choice}"
    if cache_key not in st.session_state:
        st.session_state[cache_key] = ChatService(
            model=st.session_state.model_choice,
            temperature=st.session_state.temperature,
        )
    svc: ChatService = st.session_state[cache_key]
    svc.temperature = st.session_state.temperature
    # Sync service history with the current session's displayed messages so
    # multi-turn context is always correct after a rerun.
    idx = st.session_state.active_session_idx
    if idx is not None and 0 <= idx < len(st.session_state.chat_sessions):
        svc.history = list(st.session_state.chat_sessions[idx]["messages"])
    else:
        svc.history = []
    return svc


def _title_from_message(text: str) -> str:
    """Generate a short session title from the first user message."""
    stripped = text.strip().replace("\n", " ")
    return stripped[:48] + "…" if len(stripped) > 48 else stripped


def _start_new_chat() -> None:
    st.session_state.active_session_idx = None


def _load_session(idx: int) -> None:
    st.session_state.active_session_idx = idx


def _save_message(role: str, content: str) -> None:
    """Persist a message into the current (or newly-created) session."""
    idx = st.session_state.active_session_idx
    sessions = st.session_state.chat_sessions

    if idx is None or idx >= len(sessions):
        # First message in a brand-new session — auto-create it
        title = _title_from_message(content) if role == "user" else "New chat"
        sessions.insert(0, {"id": len(sessions), "title": title, "messages": []})
        st.session_state.active_session_idx = 0
        idx = 0

    sessions[idx]["messages"].append({"role": role, "content": content})


def _get_token_counts() -> tuple[int, int]:
    """Return (total_input_tokens, total_output_tokens) for the active model."""
    cache_key = f"svc_{st.session_state.model_choice}"
    if cache_key in st.session_state:
        svc: ChatService = st.session_state[cache_key]
        return svc.total_input_tokens, svc.total_output_tokens
    return 0, 0


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:0 0 0.75rem">
        <div style="width:34px;height:34px;background:linear-gradient(135deg,#1f6feb,#58a6ff);
                    border-radius:10px;display:flex;align-items:center;justify-content:center;
                    font-size:1rem;flex-shrink:0">🔍</div>
        <div>
            <div style="font-weight:700;font-size:1rem;color:#e6edf3;letter-spacing:-0.02em">CodeLens</div>
            <div style="font-size:0.68rem;color:#484f58;margin-top:1px">AI Code Explainer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # New Chat button
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("＋  New Chat", key="new_chat_btn", use_container_width=True):
        _start_new_chat()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Chat history
    sessions = st.session_state.chat_sessions
    if sessions:
        st.markdown('<p style="font-size:0.68rem;font-weight:600;text-transform:uppercase;'
                    'letter-spacing:0.08em;color:#484f58;margin:0 0 6px">History</p>',
                    unsafe_allow_html=True)
        for i, sess in enumerate(sessions):
            is_active = (st.session_state.active_session_idx == i)
            css_class = "hist-item-active" if is_active else "hist-item"
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(sess["title"], key=f"hist_{i}", use_container_width=True):
                _load_session(i)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

    # Model selector
    st.markdown('<p style="font-size:0.68rem;font-weight:600;text-transform:uppercase;'
                'letter-spacing:0.08em;color:#484f58;margin:0 0 5px">Model</p>',
                unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Model",
        ["qwen2.5:0.5b", "phi3:latest"],
        index=0 if st.session_state.model_choice == "qwen2.5:0.5b" else 1,
        label_visibility="collapsed",
        key="model_select",
    )
    st.session_state.model_choice = model_choice

    # Temperature slider
    st.markdown('<p style="font-size:0.68rem;font-weight:600;text-transform:uppercase;'
                'letter-spacing:0.08em;color:#484f58;margin:0.75rem 0 5px">Temperature</p>',
                unsafe_allow_html=True)
    temperature = st.slider("Temp", 0.0, 1.0, st.session_state.temperature, 0.05,
                             label_visibility="collapsed", key="temp_slider")
    st.session_state.temperature = temperature
    _desc = "precise" if temperature < 0.4 else "balanced" if temperature < 0.7 else "creative"
    st.markdown(f'<p style="font-size:0.7rem;color:#484f58;text-align:right;margin-top:-4px">'
                f'{temperature:.2f} · {_desc}</p>', unsafe_allow_html=True)

    # ── Token Usage (Requirement: token usage visible) ────────────────────────
    tok_in, tok_out = _get_token_counts()
    st.markdown("---")
    st.markdown('<p style="font-size:0.68rem;font-weight:600;text-transform:uppercase;'
                'letter-spacing:0.08em;color:#484f58;margin:0 0 6px">Token Usage</p>',
                unsafe_allow_html=True)
    if tok_in + tok_out == 0:
        st.markdown(
            '<p style="font-size:0.75rem;color:#484f58;margin:0">No tokens yet</p>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'<p style="font-size:0.78rem;color:#8b949e;margin:2px 0">'
            f'↑&nbsp;<b style="color:#c9d1d9">{tok_in:,}</b>&nbsp;prompt</p>'
            f'<p style="font-size:0.78rem;color:#8b949e;margin:2px 0">'
            f'↓&nbsp;<b style="color:#c9d1d9">{tok_out:,}</b>&nbsp;completion</p>'
            f'<p style="font-size:0.78rem;color:#8b949e;margin:2px 0">'
            f'Σ&nbsp;<b style="color:#c9d1d9">{tok_in + tok_out:,}</b>&nbsp;total</p>'
            f'<p style="font-size:0.7rem;color:#484f58;margin:4px 0 0">'
            f'local model · $0.00 cost</p>',
            unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# MAIN — header
# ──────────────────────────────────────────────────────────────────────────────
messages = _active_messages()

example_prompt = None  # may be set by a chip click below

if not messages:
    # ── Empty state ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:3rem 0 2rem">
        <div style="font-size:2.5rem;margin-bottom:0.5rem">🔍</div>
        <h1 style="font-size:1.75rem;font-weight:700;color:#e6edf3;
                   letter-spacing:-0.03em;margin:0 0 0.4rem">CodeLens</h1>
        <p style="font-size:1rem;color:#8b949e;margin:0 0 0.25rem;font-weight:500">
            Understand code instantly.
        </p>
        <p style="font-size:0.85rem;color:#484f58;margin:0">
            Paste Python, JavaScript, SQL, Bash, or any code snippet and get a clear explanation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips
    CHIPS = [
        ("💡", "Explain this code"),
        ("🐛", "Find bugs"),
        ("📋", "Explain line by line"),
        ("✨", "Improve this code"),
    ]
    cols = st.columns(len(CHIPS))
    for i, (icon, label) in enumerate(CHIPS):
        with cols[i]:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(f"{icon} {label}", key=f"chip_{i}", use_container_width=True):
                example_prompt = label
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

else:
    # ── Active conversation — show title bar ──────────────────────────────────
    idx = st.session_state.active_session_idx
    if idx is not None and 0 <= idx < len(st.session_state.chat_sessions):
        title = st.session_state.chat_sessions[idx]["title"]
        st.markdown(f'<p style="font-size:0.75rem;color:#484f58;margin:0 0 0.5rem;'
                    f'text-align:center">{title}</p>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# RENDER EXISTING MESSAGES
# ──────────────────────────────────────────────────────────────────────────────
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ──────────────────────────────────────────────────────────────────────────────
# HANDLE INPUT
# ──────────────────────────────────────────────────────────────────────────────
def handle(user_text: str) -> None:
    """Send a user message, stream the reply, and persist both."""
    _save_message("user", user_text)
    with st.chat_message("user"):
        st.markdown(user_text)

    service = _get_or_create_service()
    with st.chat_message("assistant"):
        reply = st.write_stream(service.stream(user_text))

    _save_message("assistant", str(reply))


# Chat input (always visible at bottom)
if prompt := st.chat_input("Paste code or ask a question…"):
    handle(prompt)
    st.rerun()

# Suggestion chip click (only possible on the empty-state screen)
if example_prompt:
    handle(example_prompt)
    st.rerun()
