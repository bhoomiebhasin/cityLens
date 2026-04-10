"""
styles.py – Industrial Tech dark theme CSS injection for CityLens
"""

DARK_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Orbitron:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: #080b10 !important;
    color: #d0d8e8 !important;
}

.stApp {
    background: linear-gradient(135deg, #080b10 0%, #0d1220 50%, #080b10 100%) !important;
    background-attachment: fixed !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── App Header ── */
.citylens-header {
    background: linear-gradient(90deg, rgba(57,255,20,0.08) 0%, rgba(255,119,0,0.06) 100%);
    border: 1px solid rgba(57,255,20,0.2);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.citylens-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #39ff14, #ff7700, #39ff14);
}
.citylens-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #39ff14 0%, #00d4ff 50%, #ff7700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    margin: 0;
}
.citylens-subtitle {
    color: #6b8cad;
    font-size: 0.95rem;
    letter-spacing: 1px;
    margin-top: 4px;
    font-weight: 300;
}
.citylens-badge {
    display: inline-block;
    background: rgba(57,255,20,0.12);
    border: 1px solid rgba(57,255,20,0.4);
    color: #39ff14;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 1px;
    margin-top: 10px;
}

/* ── Search Section ── */
.search-section {
    background: rgba(13,18,32,0.8);
    border: 1px solid rgba(57,255,20,0.12);
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}
.search-label {
    font-family: 'JetBrains Mono', monospace;
    color: #39ff14;
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* ── Input Fields ── */
.stTextInput > div > div > input {
    background: rgba(8,11,16,0.9) !important;
    border: 1px solid rgba(57,255,20,0.25) !important;
    border-radius: 8px !important;
    color: #e0e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    padding: 12px 16px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #39ff14 !important;
    box-shadow: 0 0 0 2px rgba(57,255,20,0.15) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3a4a5a !important;
}

/* ── Audit Button ── */
.stButton > button {
    background: linear-gradient(135deg, #0f2a0a, #1a4a10) !important;
    border: 1px solid #39ff14 !important;
    color: #39ff14 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px !important;
    padding: 14px 32px !important;
    border-radius: 8px !important;
    transition: all 0.25s ease !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    width: 100% !important;
    box-shadow: 0 0 20px rgba(57,255,20,0.1) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1a4a10, #2a6a18) !important;
    box-shadow: 0 0 30px rgba(57,255,20,0.35), 0 0 60px rgba(57,255,20,0.1) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Metric Cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(13,18,32,0.95), rgba(18,25,45,0.95)) !important;
    border: 1px solid rgba(57,255,20,0.2) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #39ff14, transparent);
}
[data-testid="stMetric"]:hover {
    border-color: rgba(57,255,20,0.5) !important;
    box-shadow: 0 4px 20px rgba(57,255,20,0.1) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    color: #6b8cad !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #39ff14 !important;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 3px;
    color: #ff7700;
    text-transform: uppercase;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,119,0,0.25);
    margin-bottom: 16px;
}

/* ── Intervention Cards ── */
.intervention-card {
    background: linear-gradient(135deg, rgba(13,18,32,0.9), rgba(20,28,50,0.9));
    border: 1px solid rgba(57,255,20,0.15);
    border-left: 3px solid #39ff14;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 14px;
    transition: all 0.25s ease;
    position: relative;
}
.intervention-card:hover {
    border-left-color: #ff7700;
    box-shadow: 0 4px 20px rgba(57,255,20,0.08);
    transform: translateX(3px);
}
.intervention-number {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.65rem;
    color: #39ff14;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.intervention-name {
    font-weight: 600;
    font-size: 1rem;
    color: #e8f0ff;
    margin-bottom: 6px;
}
.intervention-desc {
    font-size: 0.87rem;
    color: #8a9ab5;
    line-height: 1.6;
}

/* ── Risk Summary Card ── */
.risk-card {
    background: linear-gradient(135deg, rgba(255,34,0,0.06), rgba(255,119,0,0.04));
    border: 1px solid rgba(255,119,0,0.25);
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 20px;
}
.risk-card-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #ff7700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.risk-card-text {
    font-size: 0.92rem;
    color: #c0cce0;
    line-height: 1.65;
}

/* ── Coordinates Tag ── */
.coord-tag {
    display: inline-block;
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.25);
    color: #00d4ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    padding: 5px 14px;
    border-radius: 20px;
    letter-spacing: 1px;
    margin-bottom: 16px;
}

/* ── Map Container ── */
.map-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #39ff14;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #39ff14 !important;
}

/* ── Error / Warning ── */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid rgba(255,119,0,0.3) !important;
    background: rgba(255,34,0,0.06) !important;
}

/* ── Footer ── */
.citylens-footer {
    margin-top: 40px;
    padding: 16px 24px;
    border-top: 1px solid rgba(57,255,20,0.1);
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #3a4a5a;
    letter-spacing: 1px;
}
.citylens-footer a {
    color: #39ff14;
    text-decoration: none;
}
.citylens-footer a:hover {
    color: #ff7700;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080b10; }
::-webkit-scrollbar-thumb { background: rgba(57,255,20,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(57,255,20,0.6); }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(57,255,20,0.1) !important;
    margin: 24px 0 !important;
}

/* ── Search bar – rounder, Google-style ── */
.stTextInput > div > div > input {
    border-radius: 50px !important;
    padding: 14px 22px !important;
}

/* ── Trending pill buttons (key starts with "pill_") ── */
[data-testid="stButton"] button[kind="secondary"],
div[data-testid^="pill_"] button {
    background: rgba(20,30,50,0.7) !important;
    border: 1px solid rgba(57,255,20,0.18) !important;
    color: #6b8cad !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.5px !important;
    padding: 6px 12px !important;
    border-radius: 50px !important;
    box-shadow: none !important;
    text-transform: none !important;
    width: auto !important;
    transition: all 0.2s ease !important;
}
div[data-testid^="pill_"] button:hover {
    border-color: rgba(57,255,20,0.5) !important;
    color: #39ff14 !important;
    box-shadow: 0 0 12px rgba(57,255,20,0.15) !important;
}
</style>
"""


def inject_css() -> None:
    """Inject the Industrial Tech CSS theme into the Streamlit app."""
    import streamlit as st
    st.markdown(DARK_CSS, unsafe_allow_html=True)
