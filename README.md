<div align="center">

# ⬡ CityLens
### AI-Driven Urban Resilience & Heat Island Detection

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_AI-2.0_Flash-4285F4?style=flat&logo=google&logoColor=white)
![OpenStreetMap](https://img.shields.io/badge/OpenStreetMap-Nominatim-7EBC6F?style=flat&logo=openstreetmap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

**🏆 2nd Place — SustainAI Hackathon 2026**

*Identify urban heat micro-zones, get AI-generated sustainability interventions, and visualise city-wide climate risk — for any city on Earth.*

</div>

---

## 🌆 What is CityLens?

CityLens is a **decision-support tool for urban planners and sustainability teams**. Type in any city name and within seconds you get:

- 🗺️ An **interactive heat map** showing 6–8 distinct micro-zones within a 5km radius
- 🌡️ **Dynamic heat scores** (1–10) colour-coded by severity
- 🌱 **Specific green interventions** per zone (cool roofs, bioswales, tree canopies, etc.)
- 📊 **City-wide CO₂ savings and water impact estimates**
- 📍 **OSM-verified zone names** — AI coordinates are reverse-geocoded against real OpenStreetMap data to eliminate hallucinations

---

## 🖥️ Demo

| Landing Page | Results Dashboard |
|---|---|
| Centred hero search, Enter-to-submit | 2:1 command-center layout |
| | Map + metrics + blueprint grid |

> Search any city: `Mumbai, India` · `Phoenix, AZ` · `Dubai, UAE` · `Singapore` · `Cairo, Egypt`

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/bhoomiebhasin/cityLens.git
cd cityLens_sustainAI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
```bash
cp .env.example .env
```
Edit `.env` and add your [Google Gemini API key](https://aistudio.google.com/app/apikey):
```
GEMINI_API_KEY=your_key_here
```

### 4. Run the app
```bash
python -m streamlit run app.py
```

Open **http://localhost:8501** — type a city and hit Enter.

---

## 🏗️ Architecture

```
City Name Input
      │
      ▼
 Geocoder (geopy + OpenStreetMap Nominatim)
      │ lat, lon
      ▼
 Gemini AI Engine  ──► Model Fallback Chain
      │               gemini-2.0-flash → 2.5-flash → 1.5-flash
      │ JSON micro-zones
      ▼
 Reverse Geocoder  ──► OSM-verified zone names [OSM ✓]
      │
      ▼
 Folium Map Builder ──► Dynamic colour-coded circles per zone
      │
      ▼
 Streamlit Dashboard ──► 2:1 Command Center UI
```

### Anti-Hallucination Stack

| Layer | Method |
|-------|--------|
| Structured output | `response_mime_type="application/json"` forces pure JSON |
| Large token budget | `max_output_tokens=8192` prevents truncation |
| OSM grounding | AI coordinates → verified real neighbourhood names |
| Retry resilience | Tenacity exponential backoff (3 attempts, 4–10s wait) |
| Model fallback | Auto-switches models on 503 UNAVAILABLE |

---

## 📂 Project Structure

```
cityLens_sustainAI/
├── app.py                      # Streamlit UI — routing, layout, state
├── ai_engine.py                # Gemini integration — prompt, retry, validation
├── geocoder.py                 # Forward + reverse geocoding (Nominatim)
├── map_builder.py              # Folium map — circles, markers, popups
├── styles.py                   # Industrial Tech dark CSS theme
├── HACKATHON_PRESENTATION.md   # Full technical write-up
├── .env.example                # API key template
└── requirements.txt            # Dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (wide mode, CSS injection) |
| AI Engine | Google Gemini via `google-genai` SDK |
| Geocoding | `geopy` + OpenStreetMap Nominatim |
| Maps | Folium + streamlit-folium (Leaflet.js) |
| Resilience | Tenacity (exponential backoff) + model fallback chain |
| Config | `python-dotenv` |

---

## 🌱 Impact Numbers

When all AI-recommended interventions are deployed:

- **~14,000–25,000 tons CO₂/year** reduced per district analysed
- **+30–45% water absorption** via bioswales, tree cover, permeable surfaces  
- **3–5°C peak temperature reduction** in intervention zones
- Based on IPCC-aligned cool-roof and urban greening research

---

## 📄 Full Documentation

See [`HACKATHON_PRESENTATION.md`](./HACKATHON_PRESENTATION.md) for a complete technical breakdown including architecture diagrams, AI prompt design, and judging criteria alignment.

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key — get one free at [aistudio.google.com](https://aistudio.google.com/app/apikey) |

> ⚠️ **Never commit your `.env` file.** It is gitignored by default.

---

## 📜 License

MIT — free to use, modify, and build on.

---

<div align="center">
<sub>Built with ❤️ for the SustainAI Hackathon 2026 · Powered by Google Gemini + OpenStreetMap</sub>
</div>
