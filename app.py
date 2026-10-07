"""
Context-Based Multilingual Idiom Meaning Identifier - Streamlit Web Application
Supports: English (en), Hindi (hi), and Marathi (mr)
Professional dark-mode UI with glassmorphism design.
"""

import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
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

from idiom_dictionary import IDIOM_DICTIONARY, get_all_idioms, get_idiom_info, get_idioms_by_language
from predict import analyze_sentence, load_inference_models
from multilingual_preprocessing import infer_language, clean_unicode


# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="IdiomLens · Multilingual Idiom Identifier",
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');

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
    font-family: 'Inter', 'Noto Sans Devanagari', sans-serif;
    color: var(--text-primary);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10,15,35,0.97) 0%, rgba(12,18,45,0.97) 100%);
    border-right: 1px solid var(--border);
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] .stRadio label { color: var(--text-secondary) !important; }

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
    padding: 1.1rem 0.8rem;
    text-align: center;
    box-shadow: var(--shadow);
    backdrop-filter: blur(12px);
}
.stat-card .stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(120deg, var(--accent-bright), var(--neon-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
}
.stat-card .stat-label {
    font-size: 0.74rem;
    color: var(--text-secondary);
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Badges ── */
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
.lang-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.lang-en { background: rgba(99,120,255,0.20); color: #8b9eff; border: 1px solid #6378ff; }
.lang-hi { background: rgba(255,181,71,0.20); color: #ffb547; border: 1px solid #ffb547; }
.lang-mr { background: rgba(255,107,107,0.20); color: #ff6b6b; border: 1px solid #ff6b6b; }

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

.section-heading {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 0.01em;
    margin: 0 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.meaning-quote {
    font-size: 1.02rem;
    font-weight: 600;
    color: #e8eeff;
    line-height: 1.6;
    border-left: 3px solid var(--accent);
    padding-left: 12px;
    margin: 8px 0;
}

.explanation-box {
    background: rgba(99, 120, 255, 0.08);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    color: var(--text-primary);
    line-height: 1.65;
}

.conf-bar-bg {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin-top: 6px;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--neon-green));
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.kw-tag {
    display: inline-block;
    background: rgba(0, 229, 160, 0.10);
    border: 1px solid rgba(0, 229, 160, 0.30);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.75rem;
    color: var(--neon-green);
    margin: 2px 3px;
    font-family: 'JetBrains Mono', monospace;
}
.kw-tag-lit {
    background: rgba(255, 181, 71, 0.10);
    border: 1px solid rgba(255, 181, 71, 0.30);
    color: var(--neon-amber);
}

.sidebar-brand {
    background: linear-gradient(135deg, rgba(25,35,80,0.80), rgba(15,22,55,0.90));
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.sidebar-logo { font-size: 2.2rem; display: block; margin-bottom: 4px; }
.sidebar-name {
    font-size: 1.15rem;
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
    "Affection & Family":      "#f43f5e",
    "Emotion & Fear":          "#e11d48",
    "Support & Commitment":    "#0ea5e9",
    "Communication & Refusal": "#f97316",
    "Suspicion & Mystery":     "#8b5cf6",
    "Speed & Motion":          "#10b981",
    "Deception & Betrayal":    "#ef4444",
    "Challenge & Grit":        "#f59e0b",
    "Effort & Work":           "#14b8a6",
    "Victory & Defeat":        "#ec4899",
    "Wisdom & Experience":     "#3b82f6",
    "Emotion & Happiness":     "#84cc16",
}


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-logo">🔭</span>
        <div class="sidebar-name">IdiomLens Multilingual</div>
        <div class="sidebar-tagline">English · Hindi · Marathi NLP</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 🌐 Language Selector")
    language_choice = st.selectbox(
        "Target Analysis Language:",
        options=["English", "Hindi", "Marathi"],
        index=0,
        help="Select language for candidate detection, preprocessing, and explanation."
    )
    lang_code_map = {"English": "en", "Hindi": "hi", "Marathi": "mr"}
    selected_lang = lang_code_map[language_choice]

    st.markdown("---")
    st.markdown("##### ⚙️ Model Selection")
    model_choice = st.radio(
        "Active inference pipeline:",
        options=["✦ Contextual (Multilingual MiniLM)", "◈ Baseline (Multilingual TF-IDF)"],
        index=0,
    )
    selected_model_type = "contextual" if "Contextual" in model_choice else "baseline"

    st.markdown("---")
    st.markdown("##### 📊 Benchmark Dataset Stats")

    cols_s = st.columns(2)
    for label, val, col in [("Samples", "5,400", cols_s[0]), ("Idioms", "108", cols_s[1])]:
        col.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{val}</span>
            <span class="stat-label">{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    cols_s2 = st.columns(3)
    for label, val, col in [("EN", "1,800", cols_s2[0]), ("HI", "1,800", cols_s2[1]), ("MR", "1,800", cols_s2[2])]:
        col.markdown(f"""
        <div class="stat-card" style="padding:0.7rem 0.4rem;">
            <span class="stat-value" style="font-size:1.3rem;">{val}</span>
            <span class="stat-label" style="font-size:0.65rem;">{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    cols_s3 = st.columns(3)
    for label, val, col in [("Train 70%", "3,780", cols_s3[0]), ("Val 15%", "810", cols_s3[1]), ("Test 15%", "810", cols_s3[2])]:
        col.markdown(f"""
        <div class="stat-card" style="padding:0.7rem 0.4rem;">
            <span class="stat-value" style="font-size:1.15rem;">{val}</span>
            <span class="stat-label" style="font-size:0.62rem;">{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 🎯 Test Performance")
    st.markdown("""
    <div style="background:rgba(0,229,160,0.08);border:1px solid rgba(0,229,160,0.25);border-radius:10px;padding:10px 12px;text-align:center;">
        <span style="font-size:1.7rem;font-weight:800;color:#00e5a0;">99.75%</span><br>
        <span style="font-size:0.72rem;color:#8a9cc8;text-transform:uppercase;letter-spacing:.04em;">Contextual MiniLM F1: 0.9975</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(138,156,200,0.06);border:1px solid rgba(138,156,200,0.15);border-radius:10px;padding:8px 12px;text-align:center;margin-top:8px;">
        <span style="font-size:1.3rem;font-weight:700;color:#8a9cc8;">100.0%</span><br>
        <span style="font-size:0.70rem;color:#4d5c8a;text-transform:uppercase;letter-spacing:.04em;">TF-IDF Baseline F1: 1.0000</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#4d5c8a;text-align:center;line-height:1.7;">
        B.Tech NLP Multilingual Upgrade<br>
        <span style="color:#6378ff;font-weight:600;">paraphrase-multilingual-MiniLM-L12-v2</span><br>
        384d Dense Embeddings · CPU-Friendly
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">🔭 IdiomLens — Multilingual Idiom Identifier</div>
    <div class="hero-sub">Robust Context-Based Idiom Classification & Sense Disambiguation for English, Hindi, and Marathi</div>
    <div style="margin-top:12px;">
        <span class="hero-pill">Multilingual NLP</span>
        <span class="hero-pill">English + Hindi + Marathi</span>
        <span class="hero-pill">5,400 Benchmark Samples</span>
        <span class="hero-pill">108 Canonical Idioms</span>
        <span class="hero-pill">99.75% Test F1</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab_analyze, tab_explorer, tab_performance, tab_architecture = st.tabs([
    "🔍  Sentence Analyzer",
    "📚  Idiom Explorer (108)",
    "📈  Evaluation & Benchmark",
    "🏗️  System Architecture",
])


# ════════════════════════════════════════════════════════════════
# TAB 1 — SENTENCE ANALYZER
# ════════════════════════════════════════════════════════════════
with tab_analyze:
    st.markdown("<br>", unsafe_allow_html=True)

    # Multilingual Preset Samples
    PRESET_SAMPLES = {
        "en": {
            "— Select an English example —": "",
            "🤒  under the weather (Idiomatic)": "After studying all night, Rahul was feeling under the weather.",
            "🌧️  under the weather (Literal)": "The school children stood huddled under the weather shelter during the heavy rainstorm.",
            "🌤️  general weather report (None)": "The actual weather was cold and rainy yesterday in the valley.",
            "🍰  piece of cake (Idiomatic)": "The final calculus examination was an absolute piece of cake for the prepared student.",
            "🍰  piece of cake (Literal)": "The server carefully placed a generous piece of cake onto the porcelain saucer.",
            "🔨  hit the nail on the head (Idiomatic)": "Her perceptive analysis of the software bug hit the nail on the head.",
            "🔨  hit the nail on the head (Literal)": "The carpenter swung the steel hammer to hit the nail on the head into the oak beam.",
            "🌕  once in a blue moon (Idiomatic)": "He visits his ancestral village once in a blue moon.",
            "📅  call it a day (Idiomatic)": "We have worked hard all morning, so let's call it a day now.",
            "☁️  on cloud nine (Idiomatic)": "After receiving the scholarship, she was on cloud nine.",
        },
        "hi": {
            "— हिंदी उदाहरण चुनें —": "",
            "🌟  आँखों का तारा (Idiomatic)": "रोहन अपने माता-पिता की आँखों का तारा है और सबकी प्रशंसा पाता है।",
            "🐱  भीगी बिल्ली बनना (Idiomatic)": "अध्यापक के कक्षा में आते ही शरारती छात्र भीगी बिल्ली बन गया।",
            "🌧️  भीगी बिल्ली (Literal)": "भारी मानसूनी वर्षा में भीगी बिल्ली बरामदे की सीढ़ियों पर ठंड से कांप रही थी।",
            "🍲  दाल में काला (Literal)": "रसोईघर में दाल बीनते समय थाली में दाल में काला कंकड़ अलग दिखाई दे रहा था।",
            "🧐  दाल में काला (Idiomatic)": "व्यापारिक सौदे में अधिकारियों की चुप्पी से लगा कि दाल में कुछ काला है।",
            "📚  दिन-रात एक करना (Idiomatic)": "सिविल सेवा परीक्षा में सफल होने के लिए उसने दिन-रात एक कर दिया।",
            "🏃  नौ दो ग्यारह होना (Idiomatic)": "पुलिस की गाड़ी देखते ही जेबकतरे नौ दो ग्यारह हो गए।",
            "⛅  सामान्य मौसम समाचार (None)": "मौसम विभाग के अनुसार आगामी चौबीस घंटों में उत्तर भारत में हल्की धूप खिली रहेगी।",
        },
        "mr": {
            "— मराठी उदाहरण निवडा —": "",
            "👀  डोळ्यात धूळ फेकणे (Idiomatic)": "चोर पोलिसांच्या डोळ्यात धूळ फेकून अंधारात पसार झाला.",
            "🌪️  डोळ्यात धूळ (Literal)": "वादळाच्या वाऱ्यामुळे डोळ्यात धूळ उडून डोळे लाल झाले.",
            "💪  कंबर कसणे (Idiomatic)": "दुष्काळावर मात करण्यासाठी ग्रामस्थांनी एकदिलाने कंबर कसली.",
            "🌾  रक्ताचे पाणी करणे (Idiomatic)": "शेतकऱ्याने रक्ताचे पाणी करून शेतात सोन्यासारखे पीक पिकवले.",
            "🤝  हात देणे (Literal)": "डोंगरावर चढणाऱ्या सहकाऱ्याला वर खेचण्यासाठी त्याने पुढे हात दिला.",
            "🤝  हात देणे (Idiomatic)": "संकटकाळात शेजाऱ्यांनी पुढे येऊन गरीब कुटुंबाला हात दिला.",
            "📖  सामान्य ग्रंथालय नोंद (None)": "ग्रंथालयाने वाचकांसाठी आधुनिक मराठी साहित्य आणि ज्ञानकोश उपलब्ध करून दिले आहेत.",
        }
    }

    PLACEHOLDERS = {
        "en": "Type or paste an English sentence containing a potential idiom...",
        "hi": "हिंदी वाक्य दर्ज करें (उदा. 'रोहन अपने माता-पिता की आँखों का तारा है।')...",
        "mr": "मराठी वाक्य प्रविष्ट करा (उदा. 'चोर पोलिसांच्या डोळ्यात धूळ फेकून अंधारात पसार झाला.')..."
    }

    left_col, right_col = st.columns([3, 2], gap="large")

    with right_col:
        st.markdown(f"""<div class="section-heading">⚡ Preset Examples ({language_choice})</div>""", unsafe_allow_html=True)
        active_presets = PRESET_SAMPLES[selected_lang]
        chosen_preset = st.selectbox(
            "Select preset:",
            list(active_presets.keys()),
            index=0,
            label_visibility="collapsed"
        )
        default_sentence = active_presets.get(chosen_preset) or ""

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card" style="padding:1rem 1.2rem;">
            <div style="font-size:0.78rem;font-weight:700;color:#6378ff;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;">Pipeline Execution Steps</div>
            <div style="font-size:0.82rem;color:#8a9cc8;line-height:1.75;">
                <b style="color:#e8eeff;">1. Language & Script:</b> Normalizes NFC Unicode & infers script/grammar<br>
                <b style="color:#e8eeff;">2. Boundary Scanner:</b> Matches aliases with script-aware Devanagari regex<br>
                <b style="color:#e8eeff;">3. Context Extraction:</b> Excises target phrase to isolate context window<br>
                <b style="color:#e8eeff;">4. Multilingual Transformer:</b> MiniLM-L12 generates 384d sentence vector<br>
                <b style="color:#e8eeff;">5. Sense Disambiguation:</b> Distinguishes <span style="color:#00e5a0;">Idiomatic</span> vs <span style="color:#ffb547;">Literal</span> vs None<br>
                <b style="color:#e8eeff;">6. Grounded Explanation:</b> Outputs transparent reasoning in native language
            </div>
        </div>
        """, unsafe_allow_html=True)

    with left_col:
        lang_flag = {"en": "🇬🇧 English", "hi": "🇮🇳 Hindi", "mr": "🚩 Marathi"}[selected_lang]
        st.markdown(f"""<div class="section-heading">✍️ Input Sentence <span class="lang-badge lang-{selected_lang}" style="margin-left:8px;">{lang_flag}</span></div>""", unsafe_allow_html=True)

        user_input = st.text_area(
            "Sentence input:",
            value=default_sentence,
            height=130,
            placeholder=PLACEHOLDERS[selected_lang],
            label_visibility="collapsed"
        )

        btn_col, info_col = st.columns([1, 2])
        with btn_col:
            analyze_btn = st.button("🚀  Analyze", type="primary", use_container_width=True)
        with info_col:
            model_label = "Contextual (Multilingual MiniLM)" if selected_model_type == "contextual" else "Multilingual TF-IDF Baseline"
            st.markdown(f"""
            <div style="padding:8px 0;font-size:0.8rem;color:#8a9cc8;">
                Pipeline: <b style="color:#8b9eff;">{model_label}</b> · Lang: <b style="color:#00e5a0;">{selected_lang.upper()}</b>
            </div>
            """, unsafe_allow_html=True)

    # ── Analysis Result ──
    if analyze_btn and user_input.strip():
        with st.spinner("Executing multilingual NLP analysis…"):
            try:
                result = analyze_sentence(
                    user_input,
                    model_type=selected_model_type,
                    language=selected_lang,
                    models_dir=MODELS_DIR
                )
            except Exception as e:
                st.error(f"❌ Pipeline Execution Error: {e}")
                result = None

        if result:
            detected_expr = result.get("detected_expression")
            usage        = result.get("usage", "None")
            meaning      = result.get("meaning", "")
            conf         = result.get("confidence", 0.0)
            context_str  = result.get("context", "")
            explanation  = result.get("explanation", "")
            example      = result.get("example", "N/A")
            category     = result.get("category", "General")
            model_used   = result.get("model_used", "")
            probs        = result.get("probabilities", {})
            res_lang     = result.get("language", selected_lang)
            warning_msg  = result.get("warning")

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

            # Top KPI Row
            st.markdown("<br>", unsafe_allow_html=True)
            k0, k1, k2, k3 = st.columns(4)

            lang_display_name = {"en": "English", "hi": "Hindi", "mr": "Marathi"}.get(res_lang, res_lang)
            with k0:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:.05em;color:#4d5c8a;font-weight:600;margin-bottom:8px;">Language</div>
                    <span class="lang-badge lang-{res_lang}" style="font-size:0.95rem;padding:4px 12px;">{res_lang.upper()} ({lang_display_name})</span>
                </div>
                """, unsafe_allow_html=True)

            with k1:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:.05em;color:#4d5c8a;font-weight:600;margin-bottom:8px;">Detected Expression</div>
                    <div style="font-size:1.05rem;font-weight:700;color:#e8eeff;">{detected_expr if detected_expr else "None"}</div>
                </div>
                """, unsafe_allow_html=True)

            with k2:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:.05em;color:#4d5c8a;font-weight:600;margin-bottom:8px;">Contextual Usage</div>
                    {badge_html}
                </div>
                """, unsafe_allow_html=True)

            with k3:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <div style="font-size:0.73rem;text-transform:uppercase;letter-spacing:.05em;color:#4d5c8a;font-weight:600;margin-bottom:4px;">Confidence</div>
                    <div style="font-size:1.8rem;font-weight:800;color:{usage_color};">{conf:.1f}%</div>
                    <div class="conf-bar-bg"><div class="conf-bar-fill" style="width:{conf_fill}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)

            # Warning if unsupported idiom
            if warning_msg:
                st.warning(f"⚠️ {warning_msg}")

            # Result Detail Block
            st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
            detail_col, chart_col = st.columns([3, 2], gap="large")

            with detail_col:
                if detected_expr:
                    cat_color = CATEGORY_COLORS.get(category, "#6378ff")
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <span style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;">Category</span><br>
                        <span style="font-size:0.85rem;font-weight:700;color:{cat_color};">
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
                        <div style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;margin-bottom:4px;">Context Window (Target Excised)</div>
                        <code style="font-family:'JetBrains Mono','Noto Sans Devanagari',monospace;font-size:0.84rem;color:#8b9eff;background:rgba(99,120,255,0.08);padding:4px 8px;border-radius:4px;">{context_str}</code>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-bottom:14px;">
                    <div style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;margin-bottom:4px;">💡 Grounded Context Explanation</div>
                    <div class="explanation-box">{explanation}</div>
                </div>
                """, unsafe_allow_html=True)

                if example and example != "Not applicable" and example != "N/A":
                    st.markdown(f"""
                    <div>
                        <div style="font-size:0.73rem;text-transform:uppercase;color:#4d5c8a;letter-spacing:.05em;font-weight:600;margin-bottom:4px;">Canonical Knowledge Base Example</div>
                        <div style="font-size:0.88rem;color:#8a9cc8;font-style:italic;">"{example}"</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:16px;padding-top:12px;border-top:1px solid rgba(99,120,255,0.12);">
                    <span style="font-size:0.72rem;color:#4d5c8a;">Model: <b style="color:#6378ff;">{model_used}</b></span>
                </div>
                """, unsafe_allow_html=True)

            with chart_col:
                st.markdown('<div style="font-size:0.82rem;font-weight:700;color:#8a9cc8;text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px;">Calibrated Class Probabilities</div>', unsafe_allow_html=True)

                if probs:
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
        st.warning("⚠️ Please enter a sentence before clicking Analyze.")


# ════════════════════════════════════════════════════════════════
# TAB 2 — IDIOM EXPLORER (108 MULTILINGUAL IDIOMS)
# ════════════════════════════════════════════════════════════════
with tab_explorer:
    st.markdown("<br>", unsafe_allow_html=True)

    c_lang, c_cat, c_search = st.columns([1.5, 1.5, 2], gap="medium")

    with c_lang:
        exp_lang = st.selectbox(
            "Filter Language:",
            ["All Languages (108)", "English (36)", "Hindi (36)", "Marathi (36)"],
            index=0
        )
    lang_filter_code = None
    if "English" in exp_lang:
        lang_filter_code = "en"
    elif "Hindi" in exp_lang:
        lang_filter_code = "hi"
    elif "Marathi" in exp_lang:
        lang_filter_code = "mr"

    with c_cat:
        all_categories = ["All Categories"] + sorted(list(set(v["category"] for v in IDIOM_DICTIONARY.values())))
        exp_cat = st.selectbox("Filter Category:", all_categories, index=0)

    with c_search:
        exp_query = st.text_input(
            "Search Expression:",
            placeholder="Search idiom, alias, or meaning..."
        )

    # Filter Idiom Dictionary
    filtered_idioms = {}
    for key, info in IDIOM_DICTIONARY.items():
        if lang_filter_code and info.get("language") != lang_filter_code:
            continue
        if exp_cat != "All Categories" and info.get("category") != exp_cat:
            continue
        if exp_query:
            q = exp_query.lower()
            aliases_str = " ".join(info.get("aliases", [])).lower()
            text_pool = f"{key} {info.get('meaning', '')} {info.get('canonical_concept', '')} {aliases_str}".lower()
            if q not in text_pool:
                continue
        filtered_idioms[key] = info

    st.markdown(f"""
    <div style="font-size:0.84rem;color:#8a9cc8;margin:8px 0 16px 0;">
        Showing <b style="color:#00e5a0;">{len(filtered_idioms)}</b> of <b style="color:#8b9eff;">108</b> canonical idioms across English, Hindi, and Marathi
    </div>
    """, unsafe_allow_html=True)

    for idiom_name, info in filtered_idioms.items():
        cat = info.get("category", "General")
        lang = info.get("language", "en")
        concept = info.get("canonical_concept", "")

        header_label = f"[{lang.upper()}]  {idiom_name}  ·  {cat}"
        with st.expander(header_label, expanded=False):
            exp_l, exp_r = st.columns([3, 2], gap="large")

            with exp_l:
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:3px;">Canonical Concept</div>
                    <code style="color:#8b9eff;background:rgba(99,120,255,0.1);padding:3px 8px;border-radius:4px;font-size:0.8rem;">{concept}</code>
                </div>
                <div style="margin-bottom:10px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:3px;">Figurative Meaning</div>
                    <div style="font-size:0.92rem;color:#e8eeff;line-height:1.6;">{info.get('meaning', '—')}</div>
                </div>
                <div style="margin-bottom:10px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:3px;">Natural Example</div>
                    <div style="font-size:0.86rem;color:#8a9cc8;font-style:italic;">"{info.get('example', '—')}"</div>
                </div>
                <div>
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#4d5c8a;font-weight:600;letter-spacing:.05em;margin-bottom:3px;">Usage & Cultural Context</div>
                    <div style="font-size:0.82rem;color:#6d7f9e;line-height:1.55;">{info.get('usage_notes', '—')}</div>
                </div>
                """, unsafe_allow_html=True)

            with exp_r:
                aliases_list = info.get("aliases", [])
                aliases_tags = " ".join(f'<span class="kw-tag" style="color:#8b9eff;border-color:rgba(99,120,255,0.3);background:rgba(99,120,255,0.08);">{a}</span>' for a in aliases_list[:6])

                idiom_kws = info.get("idiomatic_keywords", [])[:6]
                lit_kws = info.get("literal_keywords", [])[:6]
                idiom_tags = " ".join(f'<span class="kw-tag">{k}</span>' for k in idiom_kws)
                lit_tags = " ".join(f'<span class="kw-tag kw-tag-lit">{k}</span>' for k in lit_kws)

                st.markdown(f"""
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#8b9eff;font-weight:600;letter-spacing:.05em;margin-bottom:4px;">Aliases & Inflections</div>
                    {aliases_tags}
                </div>
                <div style="margin-bottom:12px;">
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#00e5a0;font-weight:600;letter-spacing:.05em;margin-bottom:4px;">Figurative Cues</div>
                    {idiom_tags}
                </div>
                <div>
                    <div style="font-size:0.72rem;text-transform:uppercase;color:#ffb547;font-weight:600;letter-spacing:.05em;margin-bottom:4px;">Literal / Concrete Cues</div>
                    {lit_tags}
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 3 — MODEL PERFORMANCE & BENCHMARK EVALUATION
# ════════════════════════════════════════════════════════════════
with tab_performance:
    st.markdown("<br>", unsafe_allow_html=True)

    # 4 KPI Stat Cards
    kp1, kp2, kp3, kp4 = st.columns(4)
    for col, val, lbl in [
        (kp1, "5,400", "Dataset Samples"),
        (kp2, "108", "Idioms Across 3 Langs"),
        (kp3, "99.75%", "Contextual MiniLM Acc"),
        (kp4, "100.0%", "Baseline TF-IDF Acc")
    ]:
        col.markdown(f"""
        <div class="stat-card">
            <span class="stat-value">{val}</span>
            <span class="stat-label">{lbl}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Model Comparison Table
    st.markdown('<div class="section-heading">📊 Overall Model Comparison (Test Set: N=810)</div>', unsafe_allow_html=True)
    comp_csv_path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    if os.path.exists(comp_csv_path):
        df_comp = pd.read_csv(comp_csv_path)
        st.dataframe(
            df_comp.style
            .format({c: "{:.2%}" for c in df_comp.select_dtypes("float").columns})
            .set_properties(**{"background-color": "#0c1228", "color": "#e8eeff", "border": "1px solid #1e2d5a"})
            .set_table_styles([{"selector": "th", "props": [("background-color", "#0f1730"), ("color", "#8a9cc8"), ("font-size", "0.8rem"), ("text-transform", "uppercase"), ("letter-spacing", "0.04em")]}]),
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Per-Language Comparison Table
    st.markdown('<div class="section-heading">🌐 Per-Language Performance Breakdown (English · Hindi · Marathi)</div>', unsafe_allow_html=True)
    lang_comp_path = os.path.join(RESULTS_DIR, "per_language_comparison.csv")
    if os.path.exists(lang_comp_path):
        df_lang = pd.read_csv(lang_comp_path)
        st.dataframe(
            df_lang.style
            .format({c: "{:.2%}" for c in df_lang.select_dtypes("float").columns})
            .set_properties(**{"background-color": "#0c1228", "color": "#e8eeff", "border": "1px solid #1e2d5a"})
            .set_table_styles([{"selector": "th", "props": [("background-color", "#0f1730"), ("color", "#8a9cc8"), ("font-size", "0.8rem"), ("text-transform", "uppercase"), ("letter-spacing", "0.04em")]}]),
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Per-Language Confusion Matrix Image
    st.markdown('<div class="section-heading">🔍 Multilingual Confusion Matrices (3-Panel Per-Language Breakdown)</div>', unsafe_allow_html=True)
    cm_lang_path = os.path.join(RESULTS_DIR, "confusion_matrix_per_language.png")
    if os.path.exists(cm_lang_path):
        st.image(cm_lang_path, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cm1, cm2 = st.columns(2, gap="medium")
    cm_base_path = os.path.join(RESULTS_DIR, "confusion_matrix_baseline.png")
    cm_ctx_path  = os.path.join(RESULTS_DIR, "confusion_matrix_contextual.png")

    with cm1:
        st.markdown('<div style="font-size:0.78rem;text-transform:uppercase;color:#8a9cc8;font-weight:600;letter-spacing:.05em;margin-bottom:8px;">Baseline (TF-IDF + LogReg)</div>', unsafe_allow_html=True)
        if os.path.exists(cm_base_path):
            st.image(cm_base_path, use_container_width=True)

    with cm2:
        st.markdown('<div style="font-size:0.78rem;text-transform:uppercase;color:#00e5a0;font-weight:600;letter-spacing:.05em;margin-bottom:8px;">Contextual (Multilingual MiniLM)</div>', unsafe_allow_html=True)
        if os.path.exists(cm_ctx_path):
            st.image(cm_ctx_path, use_container_width=True)

    # Full Classification Report
    report_path = os.path.join(RESULTS_DIR, "classification_report.txt")
    if os.path.exists(report_path):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📄 Complete Empirical Classification Report</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="section-heading">🏗️ Multilingual NLP Architecture Flow</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="arch-box">
<span style="color:#6378ff;font-weight:700;">┌────────────────────────────────────────────────────────────────────────┐</span>
<span style="color:#6378ff;font-weight:700;">│</span>       Input Sentence (English · Hindi [हिंदी] · Marathi [मराठी])       <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">└───────────────────────────────────┬────────────────────────────────────┘</span>
                                    <span style="color:#00e5a0;">│</span>
                                    <span style="color:#00e5a0;">▼</span>
<span style="color:#4a59e8;font-weight:700;">┌────────────────────────────────────────────────────────────────────────┐</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  <span style="color:#e8eeff;">Unicode Normalization & Script Detection</span>                               <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  - NFC Unicode Canonicalization & Zero-width sanitization              <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  - Script Identification: Latin vs. Devanagari                         <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  - Grammar Disambiguation: Hindi vs. Marathi marker heuristics         <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">└───────────────────────────────────┬────────────────────────────────────┘</span>
                                    <span style="color:#00e5a0;">│</span>
                                    <span style="color:#00e5a0;">▼</span>
<span style="color:#4a59e8;font-weight:700;">┌────────────────────────────────────────────────────────────────────────┐</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  <span style="color:#e8eeff;">Multilingual Candidate Idiom Scanner</span>                                 <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  - Latin Word-Boundary matching (\\b...\\b)                             <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  - Devanagari Word Boundary [?&lt;!dev_char]...[?!dev_char]               <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">│</span>    (Supports Dandas ।, Double Dandas ॥, Inflections & Surface Aliases) <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">└───────────────────────────────────┬────────────────────────────────────┘</span>
                                    <span style="color:#00e5a0;">│</span>
                                    <span style="color:#00e5a0;">▼</span>
<span style="color:#4a59e8;font-weight:700;">┌────────────────────────────────────────────────────────────────────────┐</span>
<span style="color:#4a59e8;font-weight:700;">│</span>  <span style="color:#e8eeff;">Context Isolation Window</span>   C = S ∖ Target Idiom Expression            <span style="color:#4a59e8;font-weight:700;">│</span>
<span style="color:#4a59e8;font-weight:700;">└───────────────────────────────────┬────────────────────────────────────┘</span>
                                    <span style="color:#00e5a0;">│</span>
            ┌───────────────────────┴───────────────────────┐
            <span style="color:#8a9cc8;">▼</span>                                               <span style="color:#00e5a0;">▼</span>
<span style="color:#8a9cc8;font-weight:700;">┌───────────────────────────────┐</span>   <span style="color:#00e5a0;font-weight:700;">┌───────────────────────────────────┐</span>
<span style="color:#8a9cc8;font-weight:700;">│</span>  <span style="color:#e8eeff;">Baseline Pipeline</span>            <span style="color:#8a9cc8;font-weight:700;">│</span>   <span style="color:#00e5a0;font-weight:700;">│</span>  <span style="color:#e8eeff;">Contextual Model</span>                 <span style="color:#00e5a0;font-weight:700;">│</span>
<span style="color:#8a9cc8;font-weight:700;">│</span>  Multilingual TF-IDF (1-3)    <span style="color:#8a9cc8;font-weight:700;">│</span>   <span style="color:#00e5a0;font-weight:700;">│</span>  paraphrase-multilingual-         <span style="color:#00e5a0;font-weight:700;">│</span>
<span style="color:#8a9cc8;font-weight:700;">│</span>  (10,591 Multilingual N-grams)<span style="color:#8a9cc8;font-weight:700;">│</span>   <span style="color:#00e5a0;font-weight:700;">│</span>  MiniLM-L12-v2 (384-dim dense)    <span style="color:#00e5a0;font-weight:700;">│</span>
<span style="color:#8a9cc8;font-weight:700;">│</span>  Logistic Regression          <span style="color:#8a9cc8;font-weight:700;">│</span>   <span style="color:#00e5a0;font-weight:700;">│</span>  Logistic Regression Classifier   <span style="color:#00e5a0;font-weight:700;">│</span>
<span style="color:#8a9cc8;font-weight:700;">└───────────────┬───────────────┘</span>   <span style="color:#00e5a0;font-weight:700;">└─────────────────┬─────────────────┘</span>
                │                                     │
                └───────────────────┬─────────────────┘
                                    <span style="color:#00e5a0;">│</span>
                                    <span style="color:#00e5a0;">▼</span>
<span style="color:#6378ff;font-weight:700;">┌────────────────────────────────────────────────────────────────────────┐</span>
<span style="color:#6378ff;font-weight:700;">│</span>  <span style="color:#e8eeff;">Grounded Context Disambiguation & Bayesian Cue Regularization</span>         <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">│</span>  Integrates domain context keywords from 108-idiom Knowledge Base      <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">└───────────────────────────────────┬────────────────────────────────────┘</span>
                                    <span style="color:#00e5a0;">│</span>
        ┌───────────────────────────┼───────────────────────────┐
        <span style="color:#00e5a0;">▼</span>                           <span style="color:#ffb547;">▼</span>                           <span style="color:#8a9cc8;">▼</span>
<span style="color:#00e5a0;font-weight:700;">Idiomatic / Figurative</span>      <span style="color:#ffb547;font-weight:700;">Literal / Concrete</span>          <span style="color:#8a9cc8;font-weight:700;">None / Negative</span>
        <span style="color:#00e5a0;">▼</span>                           <span style="color:#ffb547;">▼</span>                           <span style="color:#8a9cc8;">▼</span>
<span style="color:#00e5a0;">Native Fig. Meaning</span>         <span style="color:#ffb547;">Concrete Context Note</span>       <span style="color:#8a9cc8;">Unsupported / Non-Idiom</span>
        <span style="color:#00e5a0;">│</span>                           <span style="color:#ffb547;">│</span>                           <span style="color:#8a9cc8;">│</span>
        └───────────────────────────┼───────────────────────────┘
                                    <span style="color:#00e5a0;">│</span>
                                    <span style="color:#00e5a0;">▼</span>
<span style="color:#6378ff;font-weight:700;">┌────────────────────────────────────────────────────────────────────────┐</span>
<span style="color:#6378ff;font-weight:700;">│</span>  Calibrated Probabilities + Native Context Explanation (EN / HI / MR) <span style="color:#6378ff;font-weight:700;">│</span>
<span style="color:#6378ff;font-weight:700;">└────────────────────────────────────────────────────────────────────────┘</span>
        </div>
        """, unsafe_allow_html=True)

    with arch_right:
        st.markdown('<div class="section-heading">📦 Multilingual Module Registry</div>', unsafe_allow_html=True)

        modules_list = [
            ("multilingual_preprocessing.py", "NFC Unicode clean · script inference · Devanagari boundary regex", "#6378ff"),
            ("idiom_dictionary.py",           "108 idioms (36 EN, 36 HI, 36 MR) · cross-lingual canonical concepts", "#00e5a0"),
            ("dataset_validator.py",          "Validation suite: duplicate checks · NFC verify · distribution tests", "#ffb547"),
            ("build_multilingual_dataset.py", "Master builder: 5,400 balanced records across Lang × Idiom × Class", "#8a9cc8"),
            ("dataset_loader.py",             "Leak-free stratified 70/15/15 train/val/test splitter", "#c084fc"),
            ("train_baseline.py",             "Multilingual TF-IDF (10,591 n-grams) + Logistic Regression", "#22d3ee"),
            ("train_contextual.py",           "MiniLM-L12 384d sentence embeddings + Logistic Regression", "#f472b6"),
            ("evaluate.py",                   "Benchmark evaluation: overall & per-language matrices and reports", "#fb923c"),
            ("predict.py",                    "Multilingual inference engine & context explanation generator", "#a78bfa"),
            ("app.py",                        "Interactive multilingual Streamlit web UI", "#4ade80"),
        ]

        for fname, desc, color in modules_list:
            st.markdown(f"""
            <div class="glass-card" style="padding:0.75rem 0.9rem;margin-bottom:0.5rem;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:2px;">
                    <span style="width:8px;height:8px;border-radius:50%;background:{color};display:inline-block;flex-shrink:0;"></span>
                    <code style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:{color};font-weight:600;">{fname}</code>
                </div>
                <div style="font-size:0.76rem;color:#8a9cc8;padding-left:16px;line-height:1.45;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🎓 Core Architectural Decisions</div>', unsafe_allow_html=True)
        qa_multilingual = [
            ("Why replace all-MiniLM-L6-v2?",
             "all-MiniLM-L6-v2 was trained exclusively on English monolingual corpora. paraphrase-multilingual-MiniLM-L12-v2 was pretrained on 50+ languages with native support for English, Hindi, and Marathi in a shared semantic vector space."),
            ("How are Devanagari word boundaries handled?",
             "Standard Python \\b fails on Devanagari syllables. We engineered boundary lookarounds excluding combining signs while correctly handling dandas (।), double dandas (॥), and punctuation."),
            ("How was data leakage prevented?",
             "We enforced a leak-free stratified 70/15/15 split on (Language × Class) with fixed random seed 42. No sentence or near-duplicate template is shared between splits."),
        ]
        for q, a in qa_multilingual:
            st.markdown(f"""
            <div class="glass-card" style="padding:0.85rem 1rem;margin-bottom:0.6rem;">
                <div style="font-size:0.81rem;font-weight:700;color:#e8eeff;margin-bottom:3px;">Q: {q}</div>
                <div style="font-size:0.78rem;color:#8a9cc8;line-height:1.5;">{a}</div>
            </div>
            """, unsafe_allow_html=True)
