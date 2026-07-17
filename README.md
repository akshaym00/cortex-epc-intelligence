# CORTEX
### AI-Powered EPC Project Intelligence Platform for Data Centre Delivery

> Transforming fragmented EPC documents into a living project intelligence model using Knowledge Graphs, RAG, and Agentic AI.

---

## Overview

CORTEX is an AI-powered project intelligence platform built for Data Centre EPC projects. It continuously ingests project documents—including specifications, vendor submittals, RFIs, schedules, inspection records, and technical correspondence—and transforms them into a **living knowledge graph** that enables real-time project intelligence.

Instead of acting as a document chatbot, CORTEX reasons over project dependencies to identify schedule risks, compliance issues, downstream impacts, and executive actions before they become costly project delays.

Developed for **ET AI Hackathon 2026 – Problem Statement 4: AI Intelligence Platform for Data Centre EPC Project Delivery.**

---

## Key Features

- Document Intelligence Pipeline
  - PDF and text document ingestion
  - Entity, relationship, and event extraction
  - Structured project knowledge generation

- Living Project Model
  - Dynamic project state management
  - Dependency graph construction
  - Continuous project intelligence updates

- Executive Intelligence
  - Critical path analysis
  - Schedule risk prediction
  - Impact propagation
  - Project health assessment

- AI Reasoning
  - Specification compliance checking
  - Dependency reasoning
  - Recommendation engine
  - Explainable executive decisions

- Interactive Dashboard
  - Executive Command Center
  - Project Risk Dashboard
  - Critical Path visualization
  - Knowledge Graph Explorer
  - Action Register

---

## System Architecture

```text
Project Documents
        │
        ▼
Document Intelligence Pipeline
        │
        ▼
Entity • Relationship • Event Extraction
        │
        ▼
Living Project Knowledge Graph
        │
        ▼
Reasoning Engine
        │
        ▼
Impact Analysis
Critical Path
Schedule Risk
Compliance
Recommendations
        │
        ▼
Executive Dashboard
```

---

## Repository Structure

```text
backend/        FastAPI backend and AI pipeline
frontend/       React + Vite dashboard
docs/           Architecture and documentation
demo/           Demo scripts and sample scenarios
tests/          Unit and integration tests
```

---

## Technology Stack

### Backend

- Python
- FastAPI
- OpenAI API
- Pydantic

### AI

- GPT-5
- RAG
- Knowledge Graph
- Agentic AI
- Dependency Reasoning

### Frontend

- React
- Vite

### Testing

- Pytest

---

## Installation

Clone the repository:

```bash
git clone https://github.com/akshaym00/cortex-epc-intelligence.git
cd cortex-epc-intelligence
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment (Windows):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Backend

```bash
uvicorn backend.api.app:app --reload
```

---

## Running Tests

```bash
pytest
```

---

## Demo

Sample project documents are available under:

```text
demo/sample_documents/
```

Run demo scenarios from:

```text
demo/
```

---

## Project Highlights

- Living Project Intelligence Model
- Knowledge Graph–based reasoning
- Explainable AI recommendations
- Deterministic dependency analysis
- Executive decision support
- Critical path forecasting
- Specification compliance intelligence

---

## Future Roadmap

- Multi-project portfolio intelligence
- Primavera & MS Project integration
- BIM integration
- Real-time procurement monitoring
- Multi-agent orchestration
- Enterprise deployment

---

## License

This project was developed as part of **ET AI Hackathon 2026**.
