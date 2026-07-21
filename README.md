# Project Cortex

> **AI-Powered EPC Project Intelligence Platform for Data Centre Delivery**

Transforming fragmented EPC project documents into a **Living Project Model** using **OpenAI GPT-5**, Knowledge Graphs, Retrieval-Augmented Generation (RAG), and deterministic reasoning.

---

# Overview

Project Cortex is an AI-powered project intelligence platform built for Engineering, Procurement and Construction (EPC) projects in the data centre industry.

Large EPC projects generate thousands of documents including:

- Vendor Notifications
- Engineering Specifications
- Vendor Submittals
- RFIs
- Inspection Reports
- Technical Correspondence
- Schedules

Today these documents exist in silos, forcing project managers to manually discover dependencies, assess risks and understand downstream impacts.

Project Cortex converts these unstructured documents into structured project intelligence that executives can immediately act upon.

Instead of acting as another document chatbot, Project Cortex builds a **Living Project Model** capable of reasoning across project entities, dependencies and events to support executive decision-making.

---

# How GPT-5 is Used

OpenAI GPT-5 is used for **structured information extraction**, not decision making.

After a project document is uploaded, GPT-5 extracts:

- Project entities
- Relationships
- Project events
- Engineering attributes
- Metadata
- Context required for reasoning

Example:

Vendor Notification

↓

GPT-5 extracts

- Vendor
- Equipment
- Delay Event
- Delivery Date
- Affected Activity
- Dependencies

↓

Project Cortex constructs the Living Project Model.

From this point onward, **all project reasoning is deterministic.**

The platform performs:

- Dependency reasoning
- Schedule impact analysis
- Critical path assessment
- Specification compliance
- Executive recommendations

without relying on the language model.

This architecture makes every recommendation explainable, repeatable and traceable.

---

# Why This Architecture

Many AI assistants simply summarize documents.

Project Cortex instead separates responsibilities.

### GPT-5

Responsible for:

- Understanding natural language
- Extracting structured information
- Interpreting engineering documents

### Project Cortex Reasoning Engine

Responsible for:

- Dependency propagation
- Impact analysis
- Critical path reasoning
- Compliance evaluation
- Recommendation generation

This hybrid architecture combines the flexibility of LLMs with the reliability of deterministic engineering logic.

---

# Key Features

## Document Intelligence Pipeline

- PDF and text ingestion
- OpenAI GPT-5 extraction
- Entity extraction
- Relationship extraction
- Event extraction
- Structured project representation

---

## Living Project Model

- Dynamic project state
- Dependency graph
- Knowledge Graph
- Event tracking
- Continuous project updates

---

## Executive Intelligence

- Project health monitoring
- Critical path analysis
- Schedule impact prediction
- Executive decision support
- Action prioritization

---

## AI Reasoning

- Dependency reasoning
- Specification compliance
- Impact propagation
- Recommendation engine
- Explainable decisions

---

## Interactive Dashboard

- Executive Command Center
- Executive Project Signal
- Decision Pack
- Dependency Network
- Project Events
- Impact Analysis
- Action Register
- Knowledge Graph Explorer

---

# Architecture

```
Project Documents
        │
        ▼
OpenAI GPT-5
Structured Information Extraction
        │
        ▼
Entities • Relationships • Events
        │
        ▼
Living Project Model
        │
        ▼
Knowledge Graph
        │
        ▼
Deterministic Reasoning Engine
        │
 ┌──────┼──────────┬──────────────┐
 ▼      ▼          ▼              ▼
Impact  Critical   Compliance   Recommendations
Analysis Path
        │
        ▼
Executive Dashboard
```

---

# Technology Stack

## AI

- OpenAI GPT-5 API
- Retrieval-Augmented Generation (RAG)
- Knowledge Graph
- Agentic AI
- Deterministic Reasoning

## Backend

- Python
- FastAPI
- Pydantic

## Frontend

- React
- Vite

## Testing

- Pytest

---

# Repository Structure

```
backend/
frontend/
docs/
demo/
tests/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/akshaym00/cortex-epc-intelligence.git
cd cortex-epc-intelligence
```

Create a virtual environment

```bash
python -m venv .venv
```

Windows

```bash
.\.venv\Scripts\Activate.ps1
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run backend

```bash
uvicorn backend.api.app:app --reload
```

Run tests

```bash
pytest
```

---

# Demo Scenario

The included demonstration showcases a real-world vendor delay scenario.

Project Cortex automatically:

1. Extracts structured information using GPT-5.
2. Builds a Living Project Model.
3. Performs dependency reasoning.
4. Estimates downstream schedule impact.
5. Generates executive recommendations.
6. Produces explainable, citation-backed outputs.

The platform also supports deterministic specification compliance by comparing engineering specifications against vendor submittals.

---

# Project Highlights

- OpenAI GPT-5 powered document intelligence
- Living Project Model
- Knowledge Graph reasoning
- Explainable AI
- Deterministic dependency analysis
- Executive decision support
- Critical path forecasting
- Specification compliance
- Citation-backed recommendations

---

# Future Roadmap

- Multi-project portfolio intelligence
- Primavera integration
- Microsoft Project integration
- BIM integration
- Multi-agent orchestration
- Enterprise deployment
- Real-time procurement monitoring
