# Project Cortex

> **AI-Powered EPC Project Intelligence Platform for Data Centre Delivery**

Transforming fragmented EPC project documents into a **Living Project Model** using **OpenAI GPT-5**, Knowledge Graphs, Retrieval-Augmented Generation (RAG), and deterministic reasoning.

---

## Overview

Project Cortex is an AI-powered project intelligence platform built for Engineering, Procurement and Construction (EPC) projects in the data centre industry.

Large EPC projects generate thousands of documents including:

- Vendor Notifications
- Engineering Specifications
- Vendor Submittals
- RFIs
- Inspection Reports
- Technical Correspondence
- Project Schedules

These documents typically exist in disconnected silos, making it difficult for project managers to identify dependencies, assess risks, understand downstream impacts, and make timely decisions.

Project Cortex transforms these unstructured documents into structured project intelligence that enables real-time executive decision support.

Unlike traditional document chatbots, Project Cortex builds a **Living Project Model** capable of reasoning across project entities, dependencies, and events to proactively identify schedule risks, compliance issues, downstream impacts, and recommended actions.

---

# How OpenAI GPT-5 is Used

OpenAI GPT-5 powers the document intelligence pipeline.

After a project document is uploaded, GPT-5 extracts structured project information including:

- Project entities
- Relationships
- Project events
- Engineering attributes
- Metadata
- Context required for downstream reasoning

Example workflow:

```
Vendor Notification
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
        ▼
Executive Dashboard
```

GPT-5 is responsible for understanding natural language documents.

All business-critical reasoning—including dependency analysis, schedule impact assessment, specification compliance, and recommendation generation—is performed deterministically by Project Cortex.

This architecture produces explainable, repeatable, and citation-backed decisions.

---

# Model Flexibility

Project Cortex is model-agnostic.

The document intelligence pipeline is designed around a pluggable LLM interface, allowing different OpenAI models to be used without changes to the downstream reasoning engine.

This implementation uses **OpenAI GPT-5**, which provides an excellent balance of extraction quality, latency, and API cost for large-scale EPC document processing.

The architecture can easily be configured to use newer OpenAI models (such as GPT-5.6 or future releases) depending on deployment requirements.

---

# Development Workflow

Project Cortex was developed using both **OpenAI ChatGPT** and **OpenAI Codex**.

OpenAI Codex accelerated software development by assisting with:

- FastAPI backend implementation
- React frontend development
- API integration
- Code refactoring
- Debugging
- Unit testing
- Documentation improvements

ChatGPT was used extensively for system architecture discussions, technical design decisions, feature planning, and overall project development.

---

# Key Features

## Document Intelligence

- PDF and text document ingestion
- GPT-5 powered extraction
- Entity extraction
- Relationship extraction
- Event extraction

---

## Living Project Model

- Dynamic project state management
- Knowledge Graph construction
- Dependency graph generation
- Continuous project intelligence

---

## Executive Intelligence

- Critical path analysis
- Schedule risk prediction
- Impact propagation
- Project health monitoring
- Executive decision support

---

## AI Reasoning

- Dependency reasoning
- Specification compliance
- Recommendation engine
- Explainable AI
- Citation-backed outputs

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

# System Architecture

```
Project Documents
        │
        ▼
OpenAI GPT-5
        │
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
 ┌────────┼───────────┬──────────────┐
 ▼        ▼           ▼              ▼
Impact   Critical   Compliance   Recommendations
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

```powershell
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

# Demo

The included demonstration showcases a vendor delay scenario.

Project Cortex automatically:

1. Uses GPT-5 to extract structured project information.
2. Builds a Living Project Model.
3. Performs dependency reasoning.
4. Estimates downstream schedule impact.
5. Generates executive recommendations.
6. Produces explainable, citation-backed outputs.

The platform also supports automated specification compliance by comparing engineering specifications with vendor submittals to identify technical deviations.

---

# Highlights

- OpenAI GPT-5 powered document intelligence
- Living Project Model
- Knowledge Graph reasoning
- Deterministic reasoning engine
- Executive decision support
- Explainable AI
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
