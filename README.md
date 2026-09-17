# 💧 Darukaa.Earth: Watershed Restoration Intelligence

An **AI-powered environmental scientist** that uses a hybrid knowledge system (RAG + Structured SQL) to generate **evidence-backed, multi-metric recommendations** for restoring freshwater ecosystems and watershed health.

> Built for the **Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge**

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