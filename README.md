# Project Cortex

Project Cortex converts fragmented engineering project documents into a living, typed dependency graph for deterministic schedule forecasting, impact analysis, and explainable recommendations.

## Project Overview

Project Cortex ingests EPC documents and extracts entities, events, and relationships using a mixture of structured parsing and LLM-driven extraction. The resulting graph enables reasoning about project risk, compliance, schedule impact, and recommendations.

## Features

- Document ingestion with configurable loaders
- Entity, relationship, and event extraction
- Typed domain models with validation
- Directed graph construction for dependency analysis
- Impact severity scoring and schedule risk reasoning
- Recommendation engine for project decisions
- API backend with FastAPI
- Frontend-ready architecture for visualization

## Architecture

- `backend/`: core Python services, extraction, graph, reasoning, and API
- `frontend/`: Vite-based UI scaffold
- `docs/`: architecture and project documentation
- `demo/`: demo scripts and sample documents
- `tests/`: unit and integration test coverage

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd project_cortex
```

2. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Usage

### Run the backend API

```powershell
uvicorn backend.api.app:app --reload
```

### Run tests

```powershell
pytest tests/
```

## Tech Stack

- Python 3.14
- FastAPI
- pytest
- Vite + frontend scaffold

## Demo

Use the sample documents in `demo/sample_documents/` and the demo scripts in `demo/` to verify ingestion and graph analysis.

## Notes

- `.env` is excluded by `.gitignore`; configure `OPENAI_API_KEY` before using OpenAI.
- Remove temporary logs such as `backend-server.log` and `frontend-server.log` before committing.

## License

Specify your license here.
