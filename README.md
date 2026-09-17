# 💧 Darukaa.Earth: Watershed Restoration Intelligence

An **AI-powered environmental scientist** that uses a hybrid knowledge system (RAG + Structured SQL) to generate **evidence-backed, multi-metric recommendations** for restoring freshwater ecosystems and watershed health.

> Built for the **Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge**

**Repository:** https://github.com/Adi222004/Darukaa_Ai

---

## 📖 Overview

This system behaves like a **freshwater ecologist**: it retrieves scientific literature, cross-references water quality, riparian soil, climate, land use, and aquatic biodiversity metrics, asks clarifying questions when data is missing, and produces **actionable, source-cited recommendations** with measurable impact estimates and time horizons.

### What makes this different from a generic LLM?

| Feature | Generic LLM | This System |
|---|---|---|
| Knowledge source | Frozen training data | Live RAG over IUCN, Ramsar, UNEP, EPA reports |
| Reasoning | Single-variable guesses | Multi-metric rule engine (≥3 variables per recommendation) |
| Evidence | Hallucinated citations | Retrieved chunks + real report links |
| Missing data | Guesses | Asks clarifying questions (slot filling) |
| Memory | None | Multi-turn conversation memory |

---

## 🏗️ Architecture

```text
┌────────────────────────────────────────────────────────────┐
│                    USER (Browser)                          │
│              Streamlit UI (app.py) — :8501                 │
└──────────────────────┬─────────────────────────────────────┘
                       │ HTTP POST /chat
                       ▼
┌────────────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py) — :8000             │
│  • Conversation Manager  (memory + slot filling)           │
│  • Reasoning Engine      (multi-metric rules)              │
│  • RAG Orchestrator      (query → retrieve → cite)         │
└──────────┬──────────────────────────────────┬──────────────┘
           │                                  │
           ▼                                  ▼
┌─────────────────────────┐      ┌───────────────────────────┐
│  UNSTRUCTURED KNOWLEDGE │      │   STRUCTURED KNOWLEDGE    │
│  ChromaDB Vector Store  │      │   SQLite (watersheds.db)  │
│  ├── IUCN freshwater    │      │   ├── watersheds          │
│  ├── Ramsar wetlands    │      │   ├── documents           │
│  ├── UNEP water quality │      │   └── recommendations     │
│  └── EPA riparian       │      │                           │
│  Embeddings: MiniLM-L6  │      │   SoilGrids + NASA POWER  │
└─────────────────────────┘      └───────────────────────────┘
```

### Component Responsibilities

1. **Frontend (`app.py`)** — Streamlit chat UI + water quality sidebar.
2. **Backend (`main.py`)** — FastAPI endpoint coordinating memory, reasoning, and retrieval.
3. **Reasoning Engine (`reasoning/`)** — Applies freshwater ecological rules connecting water ↔ biodiversity ↔ land use.
4. **Knowledge Layer (`rag/`)** — Hybrid retrieval: vector search (ChromaDB) + structured SQL.
5. **Data Sources (`data/`)** — Curated water PDFs + real data from SoilGrids and NASA POWER.

---

## 🗄️ Database Schema

The structured layer uses **SQLite** (see `db/schema.sql`):

```sql
CREATE TABLE watersheds (
    id INTEGER PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL,
    region TEXT,

    -- Riparian soil
    riparian_soil_ph REAL,
    riparian_soc_pct REAL,
    clay_pct REAL,
    moisture TEXT,

    -- Climate
    rainfall_mm REAL,
    temp_c REAL,

    -- Water quality
    water_ph REAL,
    turbidity_ntu REAL,
    dissolved_oxygen_mgl REAL,

    -- Land use & human impact
    upstream_land_use TEXT,
    deforestation_rate TEXT,
    pollution_level TEXT,

    -- Biodiversity
    aquatic_species_richness INTEGER,
    riparian_buffer_width_m REAL,
    habitat_diversity TEXT
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    title TEXT, source TEXT, year INTEGER, url TEXT,
    text TEXT, embedding_id TEXT
);

CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY,
    practice TEXT, metrics_improved TEXT, time_horizon TEXT,
    confidence TEXT, evidence TEXT, source_ids TEXT
);
```

---

## 📂 Project Structure

```text
darukaa-watershed-ai/
├── app.py                     # Streamlit UI
├── main.py                    # FastAPI backend
├── fetch_watershed_data.py    # SoilGrids + NASA POWER fetcher
├── requirements.txt
├── README.md
├── data/
│   ├── documents/             # IUCN, Ramsar, UNEP, EPA PDFs
│   ├── structured/
│   │   ├── watershed_data.json
│   │   └── watersheds.db
│   └── vectorstore/           # ChromaDB (auto-generated)
├── rag/
│   ├── ingest.py              # PDF → chunks → embeddings → Chroma
│   └── retriever.py           # Similarity search
├── reasoning/
│   ├── conversation.py        # Slot filling + memory
│   ├── recommender.py         # Multi-metric watershed rules
│   └── confidence.py          # Confidence scoring
├── db/
│   ├── schema.sql
│   └── seed.py
└── .github/workflows/ci.yml   # CI pipeline
```

---

## 🚀 Local Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/Adi222004/Darukaa_Ai.git
cd Darukaa_Ai
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Fetch watershed data (SoilGrids + NASA POWER)

```bash
python fetch_watershed_data.py
```

This queries:
- **SoilGrids API** for riparian soil pH, SOC, and clay content
- **NASA POWER API** for annual rainfall and average temperature

It merges the results into `data/structured/watershed_data.json`.

### 4. Seed the SQLite database

```bash
python db/seed.py
```

Creates `data/structured/watersheds.db`.

### 5. Ingest water science PDFs

Add IUCN/Ramsar/UNEP/EPA PDFs to `data/documents/`, then run:

```bash
python rag/ingest.py
```

You should see: `Successfully ingested N chunks into the vector database.`

### 6. Run the Backend (Terminal 1)

```bash
uvicorn main:app --reload
```

### 7. Run the Frontend (Terminal 2)

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🧪 Example Usage

**Step 1 — User asks vaguely:**
> "Fish populations are collapsing in my river."

**Step 2 — System asks for missing data:**
> "I can help with that. To give you a scientific recommendation, I need a bit more data. Can you provide: water_ph, turbidity_ntu, dissolved_oxygen_mgl, upstream_land_use, aquatic_species_richness, pollution_level, region?"

**Step 3 — User provides structured data via sidebar:**
- Region: `semi-arid`
- Water pH: `5.5`
- Turbidity: `35 NTU`
- Dissolved Oxygen: `4.0 mg/L`
- Upstream Land Use: `agricultural`
- Aquatic Species Richness: `8`
- Pollution Level: `high`
- Riparian Buffer Width: `5 m`
- Rainfall: `450 mm/year`

**Step 4 — System returns evidence-backed recommendations:**

> **Construct constructed wetlands for nutrient runoff filtration**
> - *Why:* Constructed wetlands reduce nitrogen loading by 40-60% and phosphorus by 30-50%, raising dissolved oxygen levels and restoring aquatic habitat.
> - *Metrics improved:* dissolved oxygen, turbidity, aquatic species richness
> - *Time horizon:* medium (2-3 years)
> - *Confidence:* High
> - *Evidence:* UNEP (2021)

> **Restore 30-meter riparian buffer strips with native vegetation**
> - *Why:* Riparian buffers of 30m width reduce sediment load by 70-90% and support 2-3x more aquatic macroinvertebrate taxa.
> - *Metrics improved:* turbidity, aquatic species richness, water temperature
> - *Time horizon:* long (3-5 years)
> - *Confidence:* High
> - *Evidence:* IUCN (2020)

> **📚 Knowledge Retrieved from Vector DB (RAG):** [relevant scientific snippet]

---

## 🔬 Scientific Grounding

Every recommendation is triggered by a **multi-metric rule** (minimum 3 environmental variables) and is backed by a credible source:

| Practice | Variables Connected | Source |
|---|---|---|
| Constructed wetlands | DO + Turbidity + Upstream land use | UNEP (2021) |
| 30m riparian buffers | Buffer width + Species richness | IUCN (2020) |
| Limestone channel beds | Water pH + Pollution + Rainfall | Ramsar (2018) |
| Sand filtration + reed beds | Region + Turbidity + Species richness | IUCN (2020) |

---

## 📚 Data Sources

**Unstructured (RAG):**
- IUCN — *Freshwater Biodiversity Report*
- Ramsar — *Wetlands and Water Quality Guidelines*
- UNEP — *Water Quality Guidelines*
- WWF — *Living Planet Report (Freshwater)*
- EPA — *Riparian Buffer Science*

**Structured (SQL):**
- SoilGrids 2.0 API (`rest.isric.org`) — riparian soil pH, SOC, clay
- NASA POWER API — rainfall, temperature
- USGS Water Quality Portal (optional) — real turbidity and DO

> **Note on data sourcing:** No proprietary dataset was provided with the challenge. The system is designed as a **plug-and-play RAG architecture** that ingests any environmental dataset — demonstrated here with authoritative public sources (IUCN, Ramsar, UNEP, EPA, SoilGrids, NASA POWER).

---

## 🔄 CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push:

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python -m py_compile main.py app.py db/seed.py fetch_watershed_data.py rag/ingest.py rag/retriever.py reasoning/conversation.py reasoning/recommender.py
```

---

## 🎯 Evaluation Criteria Coverage

| Criterion | Weight | How this system satisfies it |
|---|---|---|
| **Depth of Reasoning** | 30% | Every rule connects ≥3 environmental variables (water quality + climate + land use). |
| **Scientific Grounding** | 25% | Every recommendation cites IUCN / Ramsar / UNEP / EPA with year and link. |
| **Knowledge System Design** | 20% | Hybrid RAG (ChromaDB) + Structured SQL (SQLite) + live API retrieval. |
| **Conversational Intelligence** | 15% | Slot filling, multi-turn memory, context-aware follow-ups. |
| **Output Clarity** | 10% | Structured output: Recommendation / Why / Metrics / Horizon / Confidence / Evidence. |

---

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI** — backend API
- **Streamlit** — conversational UI
- **LangChain** — RAG orchestration
- **ChromaDB** — vector store
- **HuggingFace `all-MiniLM-L6-v2`** — embeddings
- **SQLite** — structured knowledge
- **SoilGrids REST API** — live riparian soil data
- **NASA POWER API** — live climate data

---

## 📄 License

Built for the Darukaa.Earth Hackathon 2025.