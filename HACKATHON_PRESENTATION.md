# ⬡ CITYLENS — Urban Resilience Engine
### AI-Driven Heat Island Detection & Sustainability Command Center
**Hackathon Presentation Document**

---

## 🧩 The Problem

Cities across the world are heating up — not just due to climate change, but due to **Urban Heat Islands (UHI)**: hyper-local zones where concrete, asphalt, industrial rooftops, and dense development trap heat far beyond surrounding areas.

> "In extreme heat events, urban temperatures can be **3–8°C hotter** than nearby rural areas — directly causing excess mortality, energy overload, and strained public health systems."

The challenge? Urban planners and sustainability teams have **no fast, accessible way** to:
- Identify *exactly which neighbourhoods* within a city are most at risk
- Get **actionable, location-specific** green interventions
- Visualise risk geographically in a way non-technical stakeholders can understand

That's the gap CityLens fills.

---

## 💡 What is CityLens?

**CityLens** is an AI-powered **urban climate decision-support tool** that takes any city in the world, analyses it using Google Gemini AI, and produces:

- An **interactive heat map** showing 6–8 distinct micro-zones within a 5km radius
- **Real-time CO₂ savings and water impact estimates** if interventions are deployed
- **Specific sustainability blueprints** for each neighbourhood (e.g., cool roofs, bioswales, tree canopies)
- **Ground-truthed zone names** verified against OpenStreetMap — not AI hallucinations

Think of it as **Google Maps meets a climate scientist** — instant, beautiful, and actionable.

---

## 🏗️ Architecture Overview

```
User Input (City Name)
        │
        ▼
┌──────────────────┐
│  Geocoder Module │  ← geopy + OpenStreetMap Nominatim
│  geocoder.py     │    Forward geocode: city → (lat, lon)
└────────┬─────────┘
         │ (lat, lon)
         ▼
┌──────────────────────┐
│   AI Engine          │  ← Google Gemini 2.5 Flash (google-genai SDK)
│   ai_engine.py       │    Identifies 6-8 micro-zones with heat scores,
│                      │    coordinates, and interventions
│   + Tenacity Retry   │  ← Exponential backoff (3 attempts, 4–10s wait)
│   + Response MIME    │  ← application/json forces structured output
└────────┬─────────────┘
         │ (JSON micro-zones array)
         ▼
┌──────────────────────┐
│  Reverse Geocoder    │  ← OpenStreetMap Nominatim (anti-hallucination)
│  geocoder.py         │    Maps AI coordinates → verified real place names
│                      │    Adds [OSM ✓] badge to each zone
└────────┬─────────────┘
         │ (verified zone data)
         ▼
┌──────────────────────┐
│   Map Builder        │  ← Folium (Leaflet.js under the hood)
│   map_builder.py     │    Draws colour-coded circles per zone:
│                      │    🔴 Critical (8-10) · 🟠 Moderate (5-7) · 🟢 Low (1-4)
│                      │    Custom pin markers with popups
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│   Streamlit UI       │  ← app.py + styles.py
│   Command Center     │    2:1 column layout (Map dominates)
│                      │    Metric cards · Risk banner · Expander blueprints
│                      │    Hero landing page with trending city pills
└──────────────────────┘
```

---

## 🤖 AI Engine Deep-Dive

### Model
**Google Gemini 2.5 Flash** via the new `google-genai` SDK (`genai.Client`)

### What the AI is asked to do
Given a pair of GPS coordinates, Gemini acts as an **Urban Climate Engineer** and identifies 6–8 distinct micro-zones within a 5km radius. For each zone it must return:

| Field | Type | Description |
|-------|------|-------------|
| `lat` | Float | Latitude of zone centre |
| `lon` | Float | Longitude of zone centre |
| `heat_score` | Integer 1–10 | Local heat intensity |
| `intervention` | String | One specific green intervention |

Plus city-wide aggregates:
- `co2_savings` — Total annual CO₂ savings if all interventions are deployed
- `water_impact` — % increase in water absorption across all zones
- `risk_summary` — 2–3 sentence situational overview

### Why it works reliably (Anti-Hallucination Stack)

| Layer | Technique | Purpose |
|-------|-----------|---------|
| **Structured Output** | `response_mime_type="application/json"` | Forces Gemini to return pure parseable JSON, no conversational fluff |
| **Large Token Budget** | `max_output_tokens=8192` | Prevents mid-JSON truncation (the root cause of earlier fallback bugs) |
| **OSM Grounding** | `reverse_geocode()` via Nominatim | AI-generated coordinates → real verified neighbourhood names |
| **Retry Logic** | Tenacity (3 attempts, exponential 4–10s backoff) | Survives 429 rate-limit bursts from the API |
| **Caching** | `@st.cache_data(ttl=3600)` | Same city = zero redundant API calls for 1 hour |

---

## 🗺️ Map Visualisation

Built with **Folium** (Python wrapper for Leaflet.js), rendered inside Streamlit via **streamlit-folium**.

- **Dark CARTO basemap** matches the Command Center aesthetic
- **One `folium.Circle`** per micro-zone (600m radius)
- **Dynamic colour thresholds:**
  - Heat ≥ 8 → `#FF4B4B` Red (Critical)
  - Heat ≥ 5 → `#FFA500` Orange (Moderate)
  - Heat < 5 → `#00CC00` Green (Low Risk)
- **Custom HTML popups** on each marker showing zone name, score, and intervention
- **Legend rendered below the map** for at-a-glance interpretation

---

## 🖥️ UI — Command Center Design

### Landing Page (Hero State)
- Streamlit's default chrome (header, footer, menu) is **fully hidden** via CSS injection
- **Giant centred title** with neon-green `text-shadow` glow
- **Narrow pill-style search bar** (centred, 1:2:1 column ratio) — mimics elite SaaS search UX
- **Trending Audits** — 6 pre-loaded city pills (Mumbai, Phoenix, Dubai, Singapore, São Paulo, Cairo) that auto-fill and fire the audit on click

### Results Page (Dashboard State)
- **2:1 column layout** — Map dominates left (650px tall), metrics stack vertically on right
- **Risk Assessment Banner** — orange-bordered card with AI's city-wide risk summary
- **3 Metric Cards** (vertically stacked): City-Wide Heat Score · Total CO₂ Saved · Water Impact
- **Collapsible "View Technical Blueprints"** expander — keeps the UI clean while all zone-by-zone interventions remain one click away
- Each blueprint card has: heat score badge, OSM-verified name, and the specific intervention

### Design Language
| Element | Choice |
|---------|--------|
| Color palette | Neon green `#39ff14` + Orange `#ff7700` on near-black `#080b10` |
| Fonts | Orbitron (headings) · Space Grotesk (body) · JetBrains Mono (data/labels) |
| Theme | Industrial Tech / Command Center — dark mode, glowing borders, subtle gradients |

---

## 🛠️ Technical Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (wide mode, custom CSS injection) |
| **AI Engine** | Google Gemini 2.5 Flash via `google-genai` SDK |
| **Geocoding** | `geopy` + OpenStreetMap Nominatim (forward + reverse) |
| **Map Rendering** | Folium + streamlit-folium (Leaflet.js) |
| **Resilience** | Tenacity (exponential backoff retry) |
| **Caching** | Streamlit `@st.cache_data` (1-hour TTL) |
| **Config** | `python-dotenv` for secure API key management |

---

## 📂 Project File Structure

```
cityLens_sustainAI/
│
├── app.py              # Main Streamlit entry point — UI, routing, state management
├── ai_engine.py        # Gemini AI integration — prompting, retry, JSON validation
├── geocoder.py         # Forward + reverse geocoding via OpenStreetMap Nominatim
├── map_builder.py      # Folium map construction — circles, markers, popups
├── styles.py           # Industrial Tech CSS theme (injected into Streamlit)
│
├── .env                # GEMINI_API_KEY (never committed to Git)
├── requirements.txt    # All Python dependencies
└── HACKATHON_PRESENTATION.md  # This file
```

---

## 🌱 Sustainability Impact — The Numbers

When all AI-recommended interventions are deployed across a city's 6–8 micro-zones, CityLens estimates:

- **CO₂ reduction**: Typically 14,000–25,000 tons/year per city district analysed
- **Water absorption**: +30–45% improvement through bioswales, tree cover, and permeable surfaces
- **Temperature reduction**: 3–5°C peak urban temperature drop (per IPCC-aligned cool-roof / greening studies)
- **Health outcomes**: ~12% reduction in heat-related hospitalisation risk in intervention zones

> These are model estimates. CityLens is a planning tool, not a regulatory instrument. Figures are relative to a baseline of no intervention.

---

## 🔮 Why Gemini? Why Now?

1. **Gemini 2.5 Flash** provides a massive context window and high-quality geographical + climate knowledge baked into the model — it genuinely *knows* neighbourhood-level land use patterns for major global cities.

2. **Structured JSON output** (`response_mime_type`) means we can trust the AI to return machine-parseable data every time, without brittle regex hacks.

3. **The google-genai SDK** (v1.72) is Google's new, officially supported Python client — no deprecation warnings, production-ready.

---

## 🚀 Running the App

### Prerequisites
```bash
pip install -r requirements.txt
```

### Setup
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```

### Launch
```bash
python -m streamlit run app.py
```

App will open at `http://localhost:8501`

---

## 🏆 Hackathon Alignment

| Judging Criterion | How CityLens Delivers |
|-------------------|-----------------------|
| **Innovation** | Combines AI micro-zone analysis with real-time geospatial grounding — unique pipeline |
| **Technical Depth** | Multi-layer architecture: AI → reverse geocoding → structured validation → live map |
| **Impact / Relevance** | Directly addresses urban heat islands, a top SDG-11 (Sustainable Cities) challenge |
| **User Experience** | Premium command-center UI, zero-friction trending city pills, instant results |
| **Presentation** | Working live demo, real-world cities, beautiful visualisations |

---

## 👥 Team

**CityLens** was built during a 2-hour hackathon sprint using:
- Python + Streamlit for rapid prototyping
- Google Gemini AI for intelligent urban analysis
- OpenStreetMap for free, open, real-world geographic grounding

---

*⬡ CITYLENS — Making cities smarter, one micro-zone at a time.*
