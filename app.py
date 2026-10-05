"""
Context-Based Idiom Meaning Identifier - Streamlit Web Application
Professional dark-mode UI with glassmorphism design.
"""

import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# ──────────────────────────────────────────────
# Path Setup
# ──────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SRC_DIR     = os.path.join(BASE_DIR, "src")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODELS_DIR  = os.path.join(BASE_DIR, "models")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from idiom_dictionary import IDIOM_DICTIONARY, get_all_idioms, get_idiom_info
from predict import analyze_sentence, load_inference_models


# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="IdiomLens · NLP Idiom Identifier",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ──────────────────────────────────────────────
# Global CSS — Dark Glassmorphism Theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root Variables ── */
:root {
    --bg-base:        #080c1a;
    --bg-panel:       rgba(15, 23, 48, 0.85);
    --bg-card:        rgba(20, 30, 65, 0.70);
    --bg-card-hover:  rgba(30, 45, 90, 0.85);
    --border:         rgba(99, 120, 255, 0.18);
    --border-glow:    rgba(99, 120, 255, 0.50);
    --accent:         #6378ff;
    --accent-bright:  #8b9eff;
    --neon-green:     #00e5a0;
    --neon-amber:     #ffb547;
    --neon-red:       #ff6b6b;
    --text-primary:   #e8eeff;
    --text-secondary: #8a9cc8;
    --text-muted:     #4d5c8a;
    --radius-lg:      16px;
    --radius-md:      10px;
    --radius-sm:      6px;
    --shadow:         0 8px 32px rgba(0, 0, 0, 0.45);
    --shadow-glow:    0 0 24px rgba(99, 120, 255, 0.20);
}

/* ── Base App Background ── */
.stApp {
    background: radial-gradient(ellipse at 20% 10%, rgba(63,78,255,0.12) 0%, transparent 55%),
                radial-gradient(ellipse at 80% 90%, rgba(0,229,160,0.07) 0%, transparent 55%),
                linear-gradient(160deg, #080c1a 0%, #0c1228 60%, #080e1e 100%);
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

/* ── Hide Streamlit default chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Remove default padding ── */
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }

/* ════════════════════════════════════
   SIDEBAR
════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10,15,35,0.97) 0%, rgba(12,18,45,0.97) 100%);
    border-right: 1px solid var(--border);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] .stRadio label { color: var(--text-secondary) !important; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] div { border-color: var(--accent) !important; }

/* ════════════════════════════════════
   CUSTOM COMPONENTS
════════════════════════════════════ */

/* ── Hero header ── */
.hero-wrap {
    background: linear-gradient(135deg, rgba(25,35,80,0.70) 0%, rgba(15,22,55,0.80) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow), var(--shadow-glow);
    backdrop-filter: blur(16px);
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -15%;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(99,120,255,0.14) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    background: linear-gradient(120deg, #ffffff 20%, var(--accent-bright) 60%, var(--neon-green) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin: 0 0 0.4rem 0;
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--text-secondary);
    font-weight: 400;
    letter-spacing: 0.01em;
}
.hero-pill {
    display: inline-block;
    background: rgba(99,120,255,0.15);
    border: 1px solid var(--border-glow);
    border-radius: 999px;
    padding: 3px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent-bright);
    margin-right: 8px;
    margin-top: 10px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Glassmorphism card ── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    backdrop-filter: blur(12px);
    transition: border-color 0.25s, box-shadow 0.25s;
}
.glass-card:hover {
    border-color: var(--border-glow);
    box-shadow: var(--shadow), var(--shadow-glow);
}

/* ── Stat metric card ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1rem;
    text-align: center;
    box-shadow: var(--shadow);
    backdrop-filter: blur(12px);
}
.stat-card .stat-value {
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(120deg, var(--accent-bright), var(--neon-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
}
.stat-card .stat-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Usage badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.badge-idiomatic {
    background: rgba(0, 229, 160, 0.12);
    border: 1px solid rgba(0, 229, 160, 0.40);
    color: var(--neon-green);
}
.badge-literal {
    background: rgba(255, 181, 71, 0.12);
    border: 1px solid rgba(255, 181, 71, 0.40);
    color: var(--neon-amber);
}
.badge-none {
    background: rgba(138, 156, 200, 0.10);
    border: 1px solid rgba(138, 156, 200, 0.25);
    color: var(--text-secondary);
}

/* ── Result block ── */
.result-wrap {
    background: linear-gradient(135deg, rgba(18,26,60,0.75) 0%, rgba(12,19,48,0.85) 100%);
    border: 1px solid var(--border-glow);
    border-radius: var(--radius-lg);
    padding: 1.8rem;
    margin-top: 1.2rem;
    box-shadow: var(--shadow), var(--shadow-glow);
    backdrop-filter: blur(14px);
}

/* ── Section heading ── */
.section-heading {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 0.01em;
    margin: 0 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* ── Idiom key display ── */
.idiom-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent-bright);
    background: rgba(99,120,255,0.10);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 4px 12px;
    display: inline-block;
}

/* ── Confidence bar container ── */
.conf-bar-bg {
    background: rgba(255,255,255,0.07);
    border-radius: 999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
    margin-top: 6px;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--neon-green));
    transition: width 0.5s ease;
}

/* ── Meaning quote ── */
.meaning-quote {
    border-left: 3px solid var(--accent);
    padding: 0.6rem 1rem;
    background: rgba(99,120,255,0.06);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-style: italic;
    color: var(--text-primary);
    font-size: 0.95rem;
    margin: 0.5rem 0;
}

/* ── Explanation box ── */
.explanation-box {
    background: rgba(0,229,160,0.05);
    border: 1px solid rgba(0,229,160,0.15);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    color: var(--text-secondary);
    font-size: 0.88rem;
    line-height: 1.6;
    margin-top: 0.6rem;
}

/* ── Keyword tags ── */
.kw-tag {
    display: inline-block;
    background: rgba(99,120,255,0.12);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent-bright);
    margin: 2px 3px 2px 0;
}
.kw-tag-lit {
    background: rgba(255,181,71,0.10);
    border-color: rgba(255,181,71,0.25);
    color: var(--neon-amber);
}

/* ── Idiom explorer card ── */
.idiom-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 2px 12px rgba(0,0,0,0.30);
}
.idiom-card:hover {
    border-color: var(--border-glow);
    transform: translateY(-2px);
    box-shadow: var(--shadow), var(--shadow-glow);
}
.idiom-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 0.02em;
}
.idiom-card-cat {
    font-size: 0.73rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent-bright);
    background: rgba(99,120,255,0.12);
    border-radius: 4px;
    padding: 2px 8px;
    margin-left: 8px;
}
.idiom-card-meaning {
    font-size: 0.88rem;
    color: var(--text-secondary);
    margin-top: 6px;
    line-height: 1.55;
}

/* ── Tabs overrides ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10,15,35,0.60);
    border-radius: var(--radius-md);
    padding: 4px;
    border: 1px solid var(--border);
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: var(--text-secondary) !important;
    font-weight: 500;
    font-size: 0.88rem;
    padding: 8px 18px;
    transition: background 0.2s, color 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), #4f5fcc) !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 12px rgba(99,120,255,0.35);
}

/* ── Input overrides ── */
.stTextArea textarea, .stTextInput input {
    background: rgba(15, 23, 48, 0.80) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,120,255,0.18) !important;
}

/* ── Select box ── */
.stSelectbox > div > div {
    background: rgba(15, 23, 48, 0.80) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}

/* ── Button overrides ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent) 0%, #4a59e8 100%) !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 16px rgba(99,120,255,0.35) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,120,255,0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(99,120,255,0.10) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--accent-bright) !important;
    font-weight: 600 !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Expander override ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Labels ── */
label, .stRadio label, .stSelectbox label { color: var(--text-secondary) !important; font-size: 0.83rem !important; }

/* ── st.info / warning / error ── */
.stAlert { border-radius: var(--radius-md) !important; }

/* ── dataframe ── */
.stDataFrame { border-radius: var(--radius-md) !important; overflow: hidden; }

/* ── sidebar brand ── */
.sidebar-brand {
    background: linear-gradient(135deg, rgba(25,35,80,0.80), rgba(15,22,55,0.90));
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.sidebar-logo {
    font-size: 2.2rem;
    display: block;
    margin-bottom: 4px;
}
.sidebar-name {
    font-size: 1.1rem;
    font-weight: 800;
    background: linear-gradient(120deg, var(--accent-bright), var(--neon-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sidebar-tagline {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Arch box ── */
.arch-box {
    background: rgba(8, 12, 26, 0.90);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.8;
    overflow-x: auto;
    white-space: pre;
}
.arch-node {
    color: var(--accent-bright);
    font-weight: 700;
}
.arch-arrow { color: var(--neon-green); }

/* ── Perf metric row ── */
.perf-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

/* ── Category dot color map ── */
.cat-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# MATPLOTLIB DARK THEME
# ══════════════════════════════════════════════
plt.rcParams.update({
    "figure.facecolor":  "#0c1228",
    "axes.facecolor":    "#0c1228",
    "axes.edgecolor":    "#1e2d5a",
    "axes.labelcolor":   "#8a9cc8",
    "xtick.color":       "#8a9cc8",
    "ytick.color":       "#8a9cc8",
    "text.color":        "#e8eeff",
    "grid.color":        "#1a2448",
    "grid.alpha":        0.5,
    "font.family":       "sans-serif",
    "font.size":         10,
})


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
CATEGORY_COLORS = {
    "Communication & Social":  "#6378ff",
    "Difficulty & Effort":     "#00e5a0",
    "Time & Frequency":        "#ffb547",
    "Accuracy & Truth":        "#ff6b6b",
    "Secrets & Communication": "#c084fc",
    "Health & State":          "#22d3ee",
    "Cost & Value":            "#f472b6",
    "Decision & Courage":      "#fb923c",
    "Rest & Sleep":            "#a78bfa",
}

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-logo">🔭</span>
        <div class="sidebar-name">IdiomLens</div>
        <div class="sidebar-tagline">Context-Based NLP Identifier</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### ⚙️ Model Selection")
    model_choice = st.radio(
        "Active inference pipeline:",
        options=["✦ Contextual  (Sentence Transformer)", "◈ Baseline  (TF-IDF + LogReg)"],
        index=0,
    )
    selected_model_type = "contextual" if "Contextual" in model_choice else "baseline"

    st.markdown("---")
    st.markdown("##### 📊 Dataset Stats")

    cols_s = st.columns(2)
    for label, val, col in [("Samples", "320", cols_s[0]), ("Idioms", "30", cols_s[1])]:
        col.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{val}</span>
            <span class="stat-label">{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    cols_s2 = st.columns(2)
    for label, val, col in [("Train", "80%", cols_s2[0]), ("Test", "20%", cols_s2[1])]:
        col.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{val}</span>
            <span class="stat-label">{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 🎯 Best Accuracy")
    st.markdown("""
    <div style="background:rgba(0,229,160,0.08);border:1px solid rgba(0,229,160,0.25);border-radius:10px;padding:12px 14px;text-align:center;">
        <span style="font-size:1.8rem;font-weight:800;color:#00e5a0;">84.38%</span><br>
        <span style="font-size:0.73rem;color:#8a9cc8;text-transform:uppercase;letter-spacing:.04em;">Sentence Transformer</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(138,156,200,0.06);border:1px solid rgba(138,156,200,0.15);border-radius:10px;padding:10px 14px;text-align:center;margin-top:8px;">
        <span style="font-size:1.4rem;font-weight:700;color:#8a9cc8;">67.19%</span><br>
        <span style="font-size:0.73rem;color:#4d5c8a;text-transform:uppercase;letter-spacing:.04em;">TF-IDF Baseline</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#4d5c8a;text-align:center;line-height:1.7;">
        B.Tech NLP Mini-Project<br>
        <span style="color:#6378ff;font-weight:600;">all-MiniLM-L6-v2</span> · 384d embeddings<br>
        CPU-friendly · &lt;20ms inference
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">🔭 IdiomLens — Context-Based Idiom Identifier</div>
    <div class="hero-sub">Disambiguates figurative vs. literal English expressions using deep bidirectional sentence embeddings</div>
    <div style="margin-top:12px;">
        <span class="hero-pill">NLP</span>
        <span class="hero-pill">Sentence Transformers</span>
        <span class="hero-pill">30 Idioms</span>
        <span class="hero-pill">84.38% Accuracy</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab_analyze, tab_explorer, tab_performance, tab_architecture = st.tabs([
    "🔍  Sentence Analyzer",
    "📚  Idiom Explorer",
    "📈  Model Performance",
    "🏗️  System Architecture",
])


# ════════════════════════════════════════════════════════════════
# TAB 1 — SENTENCE ANALYZER
# ════════════════════════════════════════════════════════════════
with tab_analyze:
    st.markdown("<br>", unsafe_allow_html=True)

    left_col, right_col = st.columns([3, 2], gap="large")

    PRESET_SENTENCES = {
        "— pick an example —": "",
        "🤒  Under the weather (idiomatic)":  "After studying all night, Rahul was feeling under the weather.",
        "🌧️  Under the weather (literal)":    "The child was sitting under the weather shelter.",
        "🌤️  Weather — no idiom":             "The actual weather was cold and rainy.",
        "🔨  Hit the nail on the head (fig.)": "After the presentation, the teacher said I had hit the nail on the head.",
        "🔧  Hit the nail on the head (lit.)": "The carpenter swung the hammer to hit the nail on the head.",
        "🍰  Piece of cake (idiomatic)":       "The mathematics test was a piece of cake.",
        "🌕  Once in a blue moon":             "He visits us once in a blue moon.",
        "📅  Call it a day":                   "We have worked hard, so let's call it a day.",
        "☁️  On cloud nine":                   "After receiving the scholarship, she was on cloud nine.",
        "🏃  Go the extra mile":               "The manager told us to go the extra mile.",
        "🫘  Spilled the beans (literal)":     "The toddler accidentally spilled the beans on the floor.",
    }

    with right_col:
        st.markdown("""<div class="section-heading">⚡ Quick Load Examples</div>""", unsafe_allow_html=True)
        chosen_preset = st.selectbox(
            "Select a preset sentence:",
            list(PRESET_SENTENCES.keys()),
            index=0,
            label_visibility="collapsed"
        )
        default_text = PRESET_SENTENCES.get(chosen_preset) or "After studying all night, Rahul was feeling under the weather."

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding:1rem 1.2rem;">
            <div style="font-size:0.78rem;font-weight:700;color:#6378ff;text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px;">How It Works</div>
            <div style="font-size:0.82rem;color:#8a9cc8;line-height:1.75;">
                <b style="color:#e8eeff;">1.</b> Input or select a sentence<br>
                <b style="color:#e8eeff;">2.</b> Regex + lemmatizer detects idiom<br>
                <b style="color:#e8eeff;">3.</b> MiniLM embeds the full sentence<br>
                <b style="color:#e8eeff;">4.</b> Classifier predicts <span style="color:#00e5a0;">Idiomatic</span> / <span style="color:#ffb547;">Literal</span> / None<br>
                <b style="color:#e8eeff;">5.</b> Meaning + context explanation generated
            </div>
        </div>
        """, unsafe_allow_html=True)

    with left_col:
        st.markdown("""<div class="section-heading">✍️ Enter English Sentence</div>""", unsafe_allow_html=True)
        user_input = st.text_area(
            "Sentence:",
            value=default_text,
            height=130,
            placeholder="Type or paste any English sentence containing a potential idiom...",
            label_visibility="collapsed"
        )

        btn_col, info_col = st.columns([1, 2])
        with btn_col:
            analyze_btn = st.button("🚀  Analyze", type="primary", use_container_width=True)
        with info_col:
            model_label = "Sentence Transformer" if selected_model_type == "contextual" else "TF-IDF Baseline"
            st.markdown(f"""
            <div style="padding:8px 0;font-size:0.8rem;color:#8a9cc8;">
                Using <b style="color:#8b9eff;">{model_label}</b>
            </div>
            """, unsafe_allow_html=True)

    # ── Analysis Result ──
    if analyze_btn and user_input.strip():
        with st.spinner("Running NLP pipeline…"):
            try:
                result = analyze_sentence(user_input, model_type=selected_model_type, models_dir=MODELS_DIR)
            except Exception as e:
                st.error(f"❌ Model inference error: {e}")
                result = None

        if result:
            detected_expr = result.get("detected_expression")
            usage        = result.get("usage", "None")
            meaning      = result.get("meaning", "")
            conf         = result.get("confidence", 0.0)
            context_str  = result.get("context", "")
            explanation  = result.get("explanation", "")
            example      = result.get("example", "N/A")
            category     = result.get("category", "N/A")
            model_used   = result.get("model_used", "")
            probs        = result.get("probabilities", {})

            # ── Determine badge class ──
            if "Idiomatic" in usage:
                badge_html  = '<span class="badge badge-idiomatic">● Idiomatic / Figurative</span>'
                usage_color = "#00e5a0"
            elif "Literal" in usage:
                badge_html  = '<span class="badge badge-literal">● Literal / Non-idiomatic</span>'
                usage_color = "#ffb547"
            else:
                badge_html  = '<span class="badge badge-none">○ No Known Idiom</span>'
                usage_color = "#8a9cc8"

            conf_fill = min(max(conf, 0), 100)

            # ── Top KPI Row ──
            st.markdown("<br>", unsafe_allow_html=True)
            k1, k2, k3 = st.columns(3)

            with k1:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:.05em;color:#4d5c8a;font-weight:600;margin-bottom:8px;">Detected Expression</div>
                    <div class="idiom-key">{detected_expr if detected_expr else "None"}</div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:.05em;color:#4d5c8a;font-weight:600;margin-bottom:12px;">Contextual Usage</div>
                    {badge_html}
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:.05em;color:#4d5c8a;font-weight:600;margin-bottom:4px;">Confidence</div>
                    <div style="font-size:1.9rem;font-weight:800;color:{usage_color};">{conf:.1f}%</div>
                    <div class="conf-bar-bg"><div class="conf-bar-fill" style="width:{conf_fill}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)

            # ── Result Detail ──
            st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
            detail_col, chart_col = st.columns([3, 2], gap="large")

            with detail_col:
                if detected_expr:
                    cat_color = CATEGORY_COLORS.get(category, "#6378ff")
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <span style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;">Category</span><br>
                        <span style="font-size:0.82rem;font-weight:700;color:{cat_color};">
                            <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{cat_color};margin-right:6px;vertical-align:middle;"></span>
                            {category}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-bottom:14px;">
                    <div style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;margin-bottom:4px;">Interpreted Meaning</div>
                    <div class="meaning-quote">{meaning}</div>
                </div>
                """, unsafe_allow_html=True)

                if context_str:
                    st.markdown(f"""
                    <div style="margin-bottom:14px;">
                        <div style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;margin-bottom:4px;">Context Window</div>
                        <code style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:#8b9eff;background:rgba(99,120,255,0.08);padding:4px 8px;border-radius:4px;">{context_str}</code>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-bottom:14px;">
                    <div style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;margin-bottom:4px;">💡 Context Explanation</div>
                    <div class="explanation-box">{explanation}</div>
                </div>
                """, unsafe_allow_html=True)

                if example and example != "N/A":
                    st.markdown(f"""
                    <div>
                        <div style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;margin-bottom:4px;">Canonical Example</div>
                        <div style="font-size:0.87rem;color:#8a9cc8;font-style:italic;">"{example}"</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:16px;padding-top:12px;border-top:1px solid rgba(99,120,255,0.12);">
                    <span style="font-size:0.72rem;color:#4d5c8a;">Inference model: <b style="color:#6378ff;">{model_used}</b></span>
                </div>
                """, unsafe_allow_html=True)

            with chart_col:
                st.markdown('<div style="font-size:0.82rem;font-weight:700;color:#8a9cc8;text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px;">Class Probabilities</div>', unsafe_allow_html=True)

                if probs:
                    # ── Horizontal bar chart ──
                    COLORS_MAP = {
                        "idiomatic": "#00e5a0",
                        "literal":   "#ffb547",
                        "none":      "#4d5c8a"
                    }
                    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

                    for cls_name, cls_val in sorted_probs:
                        bar_color = COLORS_MAP.get(cls_name, "#6378ff")
                        bar_pct   = min(max(cls_val, 0), 100)
                        st.markdown(f"""
                        <div style="margin-bottom:14px;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                                <span style="font-size:0.8rem;font-weight:600;color:#e8eeff;text-transform:capitalize;">{cls_name}</span>
                                <span style="font-size:0.85rem;font-weight:700;color:{bar_color};">{cls_val:.1f}%</span>
                            </div>
                            <div class="conf-bar-bg">
                                <div style="height:100%;width:{bar_pct}%;border-radius:999px;background:{bar_color};transition:width .5s;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    elif analyze_btn and not user_input.strip():
        st.warning("⚠️  Please enter a sentence before analyzing.")


# ════════════════════════════════════════════════════════════════
# TAB 2 — IDIOM EXPLORER
# ════════════════════════════════════════════════════════════════
with tab_explorer:
    st.markdown("<br>", unsafe_allow_html=True)

    search_col, filter_col = st.columns([3, 2], gap="medium")
    with search_col:
        search_query = st.text_input(
            "Search:",
            placeholder="🔍  Search idiom name, meaning, or keyword…",
            label_visibility="collapsed"
        )
    with filter_col:
        all_cats = ["All Categories"] + sorted(set(v["category"] for v in IDIOM_DICTIONARY.values()))
        selected_cat = st.selectbox("Category:", all_cats, label_visibility="collapsed")

    # ── Filter logic ──
    filtered = {}
    for key, info in IDIOM_DICTIONARY.items():
        if selected_cat != "All Categories" and info.get("category") != selected_cat:
            continue
        if search_query:
            q = search_query.lower()
            if not (q in key.lower() or q in info.get("meaning", "").lower()
                    or any(q in kw.lower() for kw in info.get("idiomatic_keywords", []) + info.get("literal_keywords", []))):
                continue
        filtered[key] = info

    st.markdown(f"""
    <div style="font-size:0.82rem;color:#4d5c8a;margin:8px 0 16px 0;">
        Showing <b style="color:#8b9eff;">{len(filtered)}</b> of <b style="color:#8b9eff;">30</b> idioms
    </div>
    """, unsafe_allow_html=True)

    for idx, (idiom_name, info) in enumerate(filtered.items(), 1):
        cat       = info.get("category", "General")
        cat_color = CATEGORY_COLORS.get(cat, "#6378ff")

        with st.expander(f"  {idiom_name.title()}  —  {cat}", expanded=False):
            exp_left, exp_right = st.columns([3, 2], gap="large")

            with exp_left:
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:3px;">Meaning</div>
                    <div style="font-size:0.9rem;color:#e8eeff;line-height:1.6;">{info.get("meaning", "—")}</div>
                </div>
                <div style="margin-bottom:10px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:3px;">Canonical Example</div>
                    <div style="font-size:0.85rem;color:#8a9cc8;font-style:italic;">"{info.get("example", "—")}"</div>
                </div>
                <div>
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:3px;">Historical Origin</div>
                    <div style="font-size:0.82rem;color:#6d7f9e;line-height:1.55;">{info.get("usage_notes", "—")}</div>
                </div>
                """, unsafe_allow_html=True)

            with exp_right:
                idiom_kws   = info.get("idiomatic_keywords", [])[:7]
                literal_kws = info.get("literal_keywords",   [])[:7]

                idiom_tags   = " ".join(f'<span class="kw-tag">{k}</span>' for k in idiom_kws)
                literal_tags = " ".join(f'<span class="kw-tag kw-tag-lit">{k}</span>' for k in literal_kws)

                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#00e5a0;font-weight:600;letter-spacing:.05em;margin-bottom:6px;">Figurative Cues</div>
                    {idiom_tags}
                </div>
                <div>
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#ffb547;font-weight:600;letter-spacing:.05em;margin-bottom:6px;">Literal / Physical Cues</div>
                    {literal_tags}
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 3 — MODEL PERFORMANCE
# ════════════════════════════════════════════════════════════════
with tab_performance:
    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI Row ──
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    for col, val, lbl in [
        (kpi1, "320",      "Dataset Samples"),
        (kpi2, "30",       "Idiom Classes"),
        (kpi3, "84.38%",   "Best Accuracy"),
        (kpi4, "+17.19pp", "Improvement"),
    ]:
        col.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{val}</span>
            <span class="stat-label">{lbl}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    comp_csv_path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    if os.path.exists(comp_csv_path):
        df_comp = pd.read_csv(comp_csv_path)

        # ── Comparison table ──
        st.markdown('<div class="section-heading">📊 Model Comparison</div>', unsafe_allow_html=True)
        st.dataframe(
            df_comp.style
            .format({c: "{:.2%}" for c in df_comp.select_dtypes("float").columns})
            .set_properties(**{"background-color": "#0c1228", "color": "#e8eeff", "border": "1px solid #1e2d5a"})
            .set_table_styles([{"selector": "th", "props": [("background-color", "#0f1730"), ("color", "#8a9cc8"), ("font-size", "0.8rem"), ("text-transform", "uppercase"), ("letter-spacing", "0.04em")]}]),
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Bar chart ──
        st.markdown('<div class="section-heading">📉 Performance Comparison Chart</div>', unsafe_allow_html=True)
        metric_cols = [c for c in df_comp.columns if c != "Model"]
        chart_df = df_comp.melt(id_vars=["Model"], value_vars=metric_cols, var_name="Metric", value_name="Score")

        fig, ax = plt.subplots(figsize=(10, 4.5))
        n_metrics = len(metric_cols)
        x = np.arange(n_metrics)
        width = 0.35

        models = df_comp["Model"].tolist()
        colors = ["#4d5c8a", "#00e5a0"]

        for i, (model_name, color) in enumerate(zip(models, colors)):
            vals = df_comp[df_comp["Model"] == model_name][metric_cols].values.flatten()
            bars = ax.bar(x + (i - 0.5) * width, vals, width, label=model_name, color=color, alpha=0.85, zorder=3)
            for bar, val in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.012,
                        f"{val*100:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold",
                        color=color)

        ax.set_xticks(x)
        ax.set_xticklabels([m.replace(" (Weighted)", "") for m in metric_cols], fontsize=9)
        ax.set_ylim(0, 1.12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y*100:.0f}%"))
        ax.set_ylabel("Score (%)", labelpad=8)
        ax.grid(axis="y", alpha=0.3)
        ax.legend(loc="lower right", framealpha=0.15, labelcolor="white", fontsize=9)
        plt.tight_layout(pad=1.5)
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Run `python src/evaluate.py` to generate evaluation results.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Confusion matrices ──
    st.markdown('<div class="section-heading">🔍 Confusion Matrices</div>', unsafe_allow_html=True)
    cm1, cm2 = st.columns(2, gap="medium")

    cm_base_path = os.path.join(RESULTS_DIR, "confusion_matrix_baseline.png")
    cm_ctx_path  = os.path.join(RESULTS_DIR, "confusion_matrix_contextual.png")

    with cm1:
        st.markdown("""
        <div style="font-size:0.78rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:8px;">
            Baseline — TF-IDF + LogReg
        </div>""", unsafe_allow_html=True)
        if os.path.exists(cm_base_path):
            st.image(cm_base_path, use_container_width=True)
        else:
            st.info("Run `src/evaluate.py` to generate.")

    with cm2:
        st.markdown("""
        <div style="font-size:0.78rem;text-transform:uppercase;color:#00e5a0;font-weight:600;letter-spacing:.05em;margin-bottom:8px;">
            Contextual — Sentence Transformer
        </div>""", unsafe_allow_html=True)
        if os.path.exists(cm_ctx_path):
            st.image(cm_ctx_path, use_container_width=True)
        else:
            st.info("Run `src/evaluate.py` to generate.")

    # ── Classification report ──
    report_path = os.path.join(RESULTS_DIR, "classification_report.txt")
    if os.path.exists(report_path):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📄 Full Classification Report</div>', unsafe_allow_html=True)
        with open(report_path, "r", encoding="utf-8") as f:
            report_text = f.read()
        st.code(report_text, language="text")


# ════════════════════════════════════════════════════════════════
# TAB 4 — SYSTEM ARCHITECTURE
# ════════════════════════════════════════════════════════════════
with tab_architecture:
    st.markdown("<br>", unsafe_allow_html=True)

    arch_left, arch_right = st.columns([3, 2], gap="large")

    with arch_left:
        st.markdown('<div class="section-heading">🏗️ End-to-End NLP Pipeline</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="arch-box">
<span style="color:#6378ff;font-weight:700;">┌─────────────────────────────────────────────────────┐</span>
<span style="color:#6378ff;font-weight:700;">│</span>              User Input Sentence                   <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">└────────────────────────┬────────────────────────────┘</span>
                         <span style="color:#00e5a0;">│</span>
                         <span style="color:#00e5a0;">▼</span>
<span style="color:#4a59e8;font-weight:700;">┌─────────────────────────────────────────────────────┐</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  <span style="color:#e8eeff;">Text Preprocessing</span> (clean · lemmatize · tokenize)  <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">└────────────────────────┬────────────────────────────┘</span>
                         <span style="color:#00e5a0;">│</span>
                         <span style="color:#00e5a0;">▼</span>
<span style="color:#4a59e8;font-weight:700;">┌─────────────────────────────────────────────────────┐</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  <span style="color:#e8eeff;">Candidate Idiom Detection</span>                           <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  Priority 1: Alias regex · word-boundary match       <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  Priority 2: Lemmatized canonical form match         <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">└────────────────────────┬────────────────────────────┘</span>
                         <span style="color:#00e5a0;">│</span>
                         <span style="color:#00e5a0;">▼</span>
<span style="color:#4a59e8;font-weight:700;">┌─────────────────────────────────────────────────────┐</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  <span style="color:#e8eeff;">Context Extraction</span>  C = S ∖ Idiom Span              <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">└────────────────────────┬────────────────────────────┘</span>
                         <span style="color:#00e5a0;">│</span>
                         <span style="color:#00e5a0;">▼</span>
<span style="color:#6378ff;font-weight:700;">┌─────────────────────────────────────────────────────┐</span>
<span style="color:#6378ff;font-weight:700;">│</span>  <span style="color:#8b9eff;font-weight:700;">all-MiniLM-L6-v2</span>  →  384-dim sentence embedding    <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">│</span>  Calibrated Logistic Regression Classifier           <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">└──────┬─────────────────────┬──────────────────┬──────┘</span>
       <span style="color:#00e5a0;">▼</span>                     <span style="color:#ffb547;">▼</span>                  <span style="color:#8a9cc8;">▼</span>
<span style="color:#00e5a0;font-weight:700;">Idiomatic</span>             <span style="color:#ffb547;font-weight:700;">Literal</span>            <span style="color:#8a9cc8;font-weight:700;">None</span>
       <span style="color:#00e5a0;">▼</span>                     <span style="color:#ffb547;">▼</span>                  <span style="color:#8a9cc8;">▼</span>
<span style="color:#00e5a0;">Figurative Meaning</span>  <span style="color:#ffb547;">Physical Note</span>    <span style="color:#8a9cc8;">No Idiom Found</span>
                         <span style="color:#00e5a0;">│</span>
                         <span style="color:#00e5a0;">▼</span>
<span style="color:#6378ff;font-weight:700;">┌─────────────────────────────────────────────────────┐</span>
<span style="color:#6378ff;font-weight:700;">│</span>  Confidence Score + Grounded Context Explanation     <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">└─────────────────────────────────────────────────────┘</span>
        </div>
        """, unsafe_allow_html=True)

    with arch_right:
        st.markdown('<div class="section-heading">📦 Module Map</div>', unsafe_allow_html=True)

        modules = [
            ("preprocessing.py",      "Text clean · tokenize · lemmatize · idiom detection regex",  "#6378ff"),
            ("idiom_dictionary.py",   "30 canonical idioms · aliases · meanings · cue keywords",     "#00e5a0"),
            ("dataset_loader.py",     "CSV loader · stratified 80/20 train-test split",              "#ffb547"),
            ("train_baseline.py",     "TF-IDF (1-3 n-gram) + Logistic Regression training",          "#8a9cc8"),
            ("train_contextual.py",   "MiniLM embeddings + calibrated LR classifier training",       "#c084fc"),
            ("evaluate.py",           "Metrics · confusion matrices · classification report",         "#22d3ee"),
            ("predict.py",            "Inference engine · explanation generator · CLI",               "#f472b6"),
            ("app.py",                "Streamlit web application (this file)",                        "#fb923c"),
        ]

        for fname, desc, color in modules:
            st.markdown(f"""
            <div class="glass-card" style="padding:0.85rem 1rem;margin-bottom:0.6rem;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                    <span style="width:8px;height:8px;border-radius:50%;background:{color};display:inline-block;flex-shrink:0;"></span>
                    <code style="font-family:'JetBrains Mono',monospace;font-size:0.8rem;color:{color};font-weight:600;">{fname}</code>
                </div>
                <div style="font-size:0.78rem;color:#8a9cc8;padding-left:16px;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🎓 Key Design Decisions</div>', unsafe_allow_html=True)
        qa = [
            ("Why not keyword matching alone?",
             "Keyword presence fails for literal usage — 'weather' appears in both 'under the weather shelter' (literal) and 'feeling under the weather' (figurative)."),
            ("Why Sentence Transformers?",
             "Bidirectional self-attention captures semantic dependencies across the entire sentence, not just bag-of-words frequencies."),
            ("Why lightweight MiniLM?",
             "22.7M parameters, &lt;20ms CPU inference, 384-dim embeddings achieve 84.38% test accuracy without any GPU requirement."),
        ]
        for q, a in qa:
            st.markdown(f"""
            <div class="glass-card" style="padding:0.9rem 1rem;margin-bottom:0.7rem;">
                <div style="font-size:0.83rem;font-weight:700;color:#e8eeff;margin-bottom:4px;">Q: {q}</div>
                <div style="font-size:0.8rem;color:#8a9cc8;line-height:1.55;">{a}</div>
            </div>
            """, unsafe_allow_html=True)
