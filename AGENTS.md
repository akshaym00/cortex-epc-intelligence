# AI Agent Guide for Project Cortex

Project Cortex converts fragmented EPC project documents into a **Living Project Model**—a typed dependency graph that enables deterministic schedule forecasting, quantified impact analysis, and explainable recommendations. This guide helps AI agents understand the codebase structure and development conventions.

## Quick Start Commands

### Backend (Python)
```bash
# Activate environment
.venv\Scripts\Activate.ps1

# Run API server (port 8000)
uvicorn backend.api.app:app --reload

# Run tests
pytest tests/

# Verify setup
python backend/test.py  # Prints "Project Cortex is Ready!"
```

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev      # Port 5173
npm run build
npm run lint     # Oxlint
```

## Architecture Overview

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the complete architecture diagram and rationale.

**Key layers:**
- **Ingestion** (`backend/ingestion/`): PDF/TXT loaders with factory pattern
- **Extraction** (`backend/extraction/`): LLM-based entity, relationship, event extraction
- **Models** (`backend/models/`): Pydantic domain objects (all inherit `CortexBaseModel`)
- **Validation** (`backend/models/enums.py`): 15 entity types, 15 relationship types, severity levels
- **Graph** (`backend/graph/`): NetworkX DiGraph construction and utilities
- **Reasoning** (`backend/reasoning/`): Impact engine, dependency traversal, schedule analysis
- **Pipeline** (`backend/pipeline/`): `AnalysisPipeline` orchestrates extraction → validation → graph → reasoning
- **API** (`backend/api/`): FastAPI routes (POST /analyze), CORS for localhost:5173/5174

## Critical Entry Points

| File | Role |
|------|------|
| `backend/api/app.py` | FastAPI app initialization, CORS setup |
| `backend/api/routes.py` | POST /analyze endpoint |
| `backend/pipeline/analysis_pipeline.py` | Main orchestration: calls extractors → validators → graph builder → reasoning |
| `backend/ai/llm_client.py` | OpenAI client wrapper; mock mode for testing (MOCK_MODE=true/.env) |
| `backend/prompts/extraction_prompts.py` | Centralized LLM prompt templates |
| `backend/models/enums.py` | Authoritative enum definitions (EntityType, RelationshipType, Severity) |

## Project Conventions

### Naming & File Organization
- **Classes**: PascalCase (e.g., `EntityExtractor`)
- **Methods**: snake_case (e.g., `extract_entities()`)
- **Enums**: UPPER_CASE (e.g., `EntityType.PROJECT`)
- **Files**: snake_case (e.g., `entity_extractor.py`)

### Pydantic Models
- All inherit `CortexBaseModel` (auto-generates UUID, timestamps)
- Config: `model_config = {"extra": "forbid"}` (reject unknown fields)
- Collections use `Field(default_factory=dict/list)` to avoid mutable defaults

### Concurrency
- **ThreadPoolExecutor** (max_workers=2) for independent extraction tasks (relationships + events)
- No database transactions—in-memory processing
- See `backend/pipeline/analysis_pipeline.py` for threading context

### Validation Pattern
- **LLM output** (raw JSON) → **Parser** (normalization) → **Typed objects**
- Classes: `ExtractionParser`, `EventParser`, `RelationshipParser`
- Direction rules enforced (e.g., `supplies` originates from vendor/contractor only)

### Deduplication Strategy
- Similarity threshold: 72% for entity name matching
- Event-entity duplicates removed; occurrence nodes merged
- Name normalization: `casefold() + strip()` for comparison

### LLM Integration
- **Mock Mode** (`MOCK_MODE=true` in .env): Returns "MOCK_RESPONSE" for dev/testing
- **Production** (`MOCK_MODE=false`): OpenAI API with gpt-5
- .env loaded explicitly from project root in `backend/ai/llm_client.py`

## Potential Pitfalls

1. **Enum mismatch**: Always check `backend/models/enums.py` before adding new entity/relationship types—validation rules depend on these definitions.
2. **Graph direction**: Relationships are directed; use `graph.nodes()` and `graph.edges()` carefully; validate arc direction in reasoning.
3. **Deduplication timing**: Duplicates are removed *after* extraction, during validation. LLM output may contain duplicates.
4. **CORS headers**: Localhost ports 5173/5174 are whitelisted. Update `backend/api/app.py` if changing frontend port.
5. **ThreadPool cleanup**: Ensure ThreadPoolExecutor is properly closed in pipeline to avoid resource leaks.

## Testing

- **Test directory**: `tests/`
- **Naming**: `test_*.py` files correspond to modules (e.g., `test_entity_extractor.py`)
- **Test base class**: `test_base.py` contains shared fixtures and mocks
- **Mock LLM**: Tests use `MOCK_MODE=true` to avoid API calls

Run: `pytest tests/` (all), `pytest tests/test_graph_builder.py` (specific), `pytest -v` (verbose)

## Key Files to Understand First

1. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Visual flow and design decisions
2. [backend/models/enums.py](backend/models/enums.py) — All valid types; start here for constraint understanding
3. [backend/pipeline/analysis_pipeline.py](backend/pipeline/analysis_pipeline.py) — Orchestration logic
4. [backend/api/routes.py](backend/api/routes.py) — API contract and request/response structure
5. [backend/reasoning/impact_engine.py](backend/reasoning/impact_engine.py) — Dependency traversal and impact propagation

## Scalability Notes

- Tested with 15,200 entities, 29,999 relationships
- Graph construction: ~0.096 seconds
- Traversal (14,999 nodes): ~0.013 seconds

See [docs/SCALABILITY_REPORT.md](docs/SCALABILITY_REPORT.md) for detailed benchmarks.

## Common Development Tasks

### Adding a new entity type
1. Add enum to `backend/models/enums.py` (EntityType)
2. Update extraction prompts in `backend/prompts/extraction_prompts.py`
3. Add validation rules in `backend/extraction/entity_extractor.py` if needed
4. Add test cases to `tests/test_entity_extractor.py`

### Adding a new relationship type
1. Add enum to `backend/models/enums.py` (RelationshipType)
2. Update extraction prompts in `backend/prompts/extraction_prompts.py`
3. Add direction validation rules in `backend/extraction/relationship_extractor.py`
4. Add test cases to `tests/test_relationship_extractor.py`

### Modifying the pipeline
1. Edit `backend/pipeline/analysis_pipeline.py` for orchestration changes
2. Update `backend/api/routes.py` if request/response structure changes
3. Add/update tests in `tests/test_analysis_pipeline.py`

---

**Last Updated**: 2026-07-09  
For detailed architectural rationale, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).
