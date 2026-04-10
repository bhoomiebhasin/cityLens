"""
app.py – CityLens: AI-Driven Urban Resilience Engine
Main Streamlit application entry point.
"""

import streamlit as st
from streamlit_folium import st_folium

from geocoder import geocode_city
from ai_engine import analyze_urban_heat
from map_builder import build_map
from styles import inject_css


# ── Cached wrappers ────────────────────────────────────────────────────────────────
# Both functions are memoised for 1 hour.  Same city = zero extra API calls.
# ─────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=3600)
def cached_geocode(query: str):
    """Cache geocoding results – same city name never hits Nominatim twice."""
    return geocode_city(query)


@st.cache_data(show_spinner=False, ttl=3600)
def cached_ai_audit(lat: float, lon: float):
    """Cache AI analysis – same coordinates never hit Gemini twice."""
    return analyze_urban_heat(lat, lon)

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="CityLens – Urban Resilience Engine",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject Industrial Tech Theme ─────────────────────────────────────────────
inject_css()

# ── Hide Streamlit chrome (header, footer, hamburger) ───────────────────────
st.markdown(
    """
    <style>
    #MainMenu, footer, header { visibility: hidden !important; }
    [data-testid="stToolbar"] { display: none !important; }
    .block-container { padding-top: 0rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session State Init ────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "city_prefill" not in st.session_state:
    st.session_state.city_prefill = ""

# ── Trending pill click handler ────────────────────────────────────────────────
def set_prefill(city: str):
    st.session_state.city_prefill = city

# ── Landing vs Results branch ─────────────────────────────────────────────────
if st.session_state.results is None:

    # ── Hero Section ─────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding: 72px 20px 32px;">
            <div style="
                font-family:'Orbitron',sans-serif;
                font-size: clamp(2.4rem, 6vw, 4rem);
                font-weight: 700;
                color: #39ff14;
                text-shadow: 0 0 18px rgba(57,255,20,0.55), 0 0 60px rgba(57,255,20,0.2);
                letter-spacing: 8px;
                margin-bottom: 16px;
            ">⬡ CITYLENS</div>
            <div style="
                font-family:'Space Grotesk',sans-serif;
                font-size: 1.1rem;
                color: #6b8cad;
                letter-spacing: 2px;
                font-weight: 300;
                margin-bottom: 8px;
            ">AI-Driven Urban Resilience &amp; Heat Island Detection</div>
            <div style="
                font-family:'JetBrains Mono',monospace;
                font-size: 0.7rem;
                color: #2a3a4a;
                letter-spacing: 3px;
                margin-bottom: 52px;
            ">GEOCODE · AI ANALYSIS · HEAT MAP · INTERVENTIONS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Centred search form (Enter key submits) ──────────────────────────────
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        with st.form(key="search_form"):
            city_query = st.text_input(
                label="city",
                placeholder="Search a city  e.g. Tokyo, Japan",
                label_visibility="collapsed",
                key="city_input",
                value=st.session_state.city_prefill,
            )
            audit_clicked = st.form_submit_button(
                "🔍  AUDIT CITY",
                use_container_width=True,
            )


else:
    # ─── Compact header when results are shown ────────────────────────────────
    _, hdr_col, _ = st.columns([1, 4, 1])
    with hdr_col:
        st.markdown(
            """
            <div style="
                font-family:'Orbitron',sans-serif;
                font-size:1.3rem; font-weight:700;
                color:#39ff14;
                text-shadow: 0 0 12px rgba(57,255,20,0.4);
                letter-spacing:5px;
                padding: 16px 0 4px;
            ">⬡ CITYLENS</div>
            """,
            unsafe_allow_html=True,
        )

    search_col, btn_col = st.columns([5, 1])
    with search_col:
        city_query = st.text_input(
            label="city",
            placeholder="Search another city…",
            label_visibility="collapsed",
            key="city_input",
        )
    with btn_col:
        audit_clicked = st.button("🔍  AUDIT CITY", key="audit_btn", use_container_width=True)


# ── Audit Workflow ────────────────────────────────────────────────────────────
if audit_clicked:
    query = city_query.strip()

    # Guard: empty input
    if not query:
        st.error("🚫 Please enter a city name before running the audit.")
        st.stop()

    # ── Step 1: Geocode (cached) ──────────────────────────────────────────────
    with st.spinner("📡 Geocoding location via OpenStreetMap Nominatim..."):
        coords = cached_geocode(query)

    if coords is None:
        st.error(
            f"🛑 **Location Not Found:** Could not geocode **\"{query}\"**. "
            "Try adding a country name (e.g., *\"Phoenix, USA\"*) or check the spelling."
        )
        st.stop()

    lat, lon = coords

    # ── Step 2: AI Analysis (cached + retry) ─────────────────────────────────
    with st.spinner("🤖 AI analyzing urban heat patterns — then grounding zone names via OpenStreetMap..."):
        try:
            analysis = cached_ai_audit(lat, lon)
        except ValueError as e:
            st.error(f"🔑 **API Key Error:** {e}")
            st.stop()
        except RuntimeError as e:
            st.error(f"⚠️ **AI Analysis Failed:** {e}")
            st.stop()

    if analysis is None:
        st.error("⚠️ AI returned an unreadable response. Please try again.")
        st.stop()

    # Cache results in session state
    st.session_state.results = {
        "query": query,
        "lat": lat,
        "lon": lon,
        "analysis": analysis,
    }

# ── Results Dashboard ─────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results
    lat = r["lat"]
    lon = r["lon"]
    query = r["query"]
    analysis = r["analysis"]
    micro_zones = analysis.get("micro_zones", [])

    # Aggregate stats from micro-zones
    scores    = [z["heat_score"] for z in micro_zones] if micro_zones else [5]
    avg_score = round(sum(scores) / len(scores), 1)
    max_score = max(scores)
    zone_count = len(micro_zones)

    # Resolved coordinates tag
    st.markdown(
        f'<div class="coord-tag">📍 {query} &nbsp;·&nbsp; '
        f'LAT {lat:.4f}° &nbsp;·&nbsp; LON {lon:.4f}° &nbsp;·&nbsp; '
        f'{zone_count} MICRO-ZONES</div>',
        unsafe_allow_html=True,
    )

    # ── Two-Column Layout ─────────────────────────────────────────────────────
    map_col, data_col = st.columns([2, 1], gap="large")

    # ════════════════════════════════════════════════════════════════════════════
    # LEFT COLUMN – Interactive Map
    # ════════════════════════════════════════════════════════════════════════════
    with map_col:
        st.markdown('<div class="map-label">// MICRO-ZONE HEAT MAP</div>', unsafe_allow_html=True)

        heat_map = build_map(
            lat=lat,
            lon=lon,
            micro_zones=micro_zones,
            city_name=query,
        )

        st_folium(
            heat_map,
            use_container_width=True,
            height=650,
            returned_objects=[],
            key=f"map_{lat}_{lon}",  # Forces re-render on new city
        )

        # Map legend
        st.markdown(
            f"""
            <div style="display:flex; gap:20px; margin-top:10px; flex-wrap:wrap;
                        font-family:'JetBrains Mono',monospace; font-size:0.72rem;">
                <span style="color:#888;">LEGEND:</span>
                <span><span style="color:#FF4B4B;">●</span> CRITICAL (8-10)</span>
                <span><span style="color:#FFA500;">●</span> MODERATE (5-7)</span>
                <span><span style="color:#00FF00;">●</span> LOW RISK (1-4)</span>
                <span><span style="color:#6688ff;">📍</span> INTERVENTION SITES</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ════════════════════════════════════════════════════════════════════════════
    # RIGHT COLUMN – Metrics + AI Strategy Report
    # ════════════════════════════════════════════════════════════════════════════
    with data_col:

        # ── Risk Banner ───────────────────────────────────────────────────────
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-title">⚠ CITY-WIDE RISK ASSESSMENT</div>
                <div class="risk-card-text">{analysis.get('risk_summary', 'Analysis unavailable.')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Metric Cards ──────────────────────────────────────────────────────
        st.markdown('<div class="section-header">// IMPACT METRICS</div>', unsafe_allow_html=True)

        critical_zones = sum(1 for s in scores if s >= 8)
        score_label = f"🔴 {critical_zones} CRITICAL ZONES" if critical_zones else (
            "🟠 MODERATE RISK" if avg_score >= 5 else "🟢 LOW RISK"
        )

        st.metric(
            label="CITY-WIDE HEAT SCORE",
            value=f"{avg_score}/10",
            delta=score_label,
            delta_color="off",
        )
        st.metric(
            label="TOTAL CO₂ SAVED",
            value=analysis.get("co2_savings", "N/A"),
            delta="est. annual",
            delta_color="off",
        )
        st.metric(
            label="WATER IMPACT",
            value=analysis.get("water_impact", "N/A"),
            delta="absorption gain",
            delta_color="off",
        )

        # ── Audit Footer ──────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#3a4a5a; line-height:1.8;">
                AUDIT TARGET &nbsp;·&nbsp; {query.upper()}<br>
                COORDINATES &nbsp;·&nbsp; {lat:.6f}&#176; N, {lon:.6f}&#176; E<br>
                ZONES DETECTED &nbsp;·&nbsp; {zone_count} &nbsp;·&nbsp; PEAK SCORE {max_score}/10<br>
                ENGINE &nbsp;·&nbsp; GEMINI 2.5 FLASH + NOMINATIM<br>
                STATUS &nbsp;·&nbsp; <span style="color:#39ff14;">&#10003; ANALYSIS COMPLETE</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Technical Blueprints Grid (full-width below map + metrics) ────────────────
if st.session_state.results:
    _analysis    = st.session_state.results["analysis"]
    _micro_zones = _analysis.get("micro_zones", [])
    _sorted      = sorted(_micro_zones, key=lambda z: z["heat_score"], reverse=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-header">// TECHNICAL BLUEPRINTS &mdash; MICRO-ZONE INTERVENTIONS</div>',
        unsafe_allow_html=True,
    )

    cards_html = '<div style="display:grid; grid-template-columns: repeat(3,1fr); gap:18px; margin-top:8px;">'
    for zone in _sorted:
        z_score = zone["heat_score"]
        if z_score >= 8:
            badge_color, badge_icon = "#FF4B4B", "&#128308;"
        elif z_score >= 5:
            badge_color, badge_icon = "#FFA500", "&#128992;"
        else:
            badge_color, badge_icon = "#00CC00", "&#128994;"

        cards_html += f"""
        <div style="background:linear-gradient(135deg,rgba(13,18,32,0.95),rgba(20,28,50,0.95));
                    border:1px solid rgba(57,255,20,0.15); border-left:3px solid {badge_color};
                    border-radius:10px; padding:18px 20px;">
            <div style="font-family:'Orbitron',sans-serif; font-size:0.62rem;
                        color:{badge_color}; letter-spacing:2px; margin-bottom:8px;
                        display:flex; justify-content:space-between; align-items:center;">
                <span>{badge_icon} HEAT SCORE {z_score}/10</span>
                <span style="font-family:'JetBrains Mono',monospace; font-size:0.58rem;
                             color:#39ff14; border:1px solid #39ff14;
                             border-radius:4px; padding:1px 6px;">OSM &#10003;</span>
            </div>
            <div style="font-weight:600; font-size:0.95rem; color:#e8f0ff; margin-bottom:8px;">
                {zone["zone_name"]}
            </div>
            <div style="font-size:0.83rem; color:#8a9ab5; line-height:1.6;">
                {zone["intervention"]}
            </div>
        </div>"""
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="citylens-footer">
        ⬡ CITYLENS URBAN RESILIENCE ENGINE &nbsp;·&nbsp;
        Geocoding by <a href="https://nominatim.openstreetmap.org" target="_blank">OpenStreetMap Nominatim</a>
        &nbsp;·&nbsp;
        Map tiles by <a href="https://carto.com/attributions" target="_blank">CARTO</a>
        &nbsp;·&nbsp;
        Map data © <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors
        &nbsp;·&nbsp;
        AI by <a href="https://deepmind.google/technologies/gemini/" target="_blank">Google Gemini</a>
    </div>
    """,
    unsafe_allow_html=True,
)
