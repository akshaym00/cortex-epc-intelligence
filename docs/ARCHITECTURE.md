# Project Cortex Architecture

Project Cortex converts fragmented EPC project documents into a persistent, explainable project model. Unlike a document chatbot, the output is not only prose: it is a typed graph that supports deterministic dependency traversal and schedule forecasting.

```mermaid
flowchart LR
    A["Project documents<br/>PDF · TXT · RFI · Logs"] --> B["Ingestion layer<br/>Format-aware loaders"]
    B --> C["AI extraction<br/>Entities · Relationships · Events"]
    C --> D["Semantic validation<br/>Deduplication · Direction rules"]
    D --> E["Living Project Model<br/>Persistent typed entities"]
    E --> F["Knowledge Graph<br/>Directed dependencies"]
    F --> G["Reasoning Engine<br/>Traversal · Impact propagation"]
    G --> H["Schedule Intelligence<br/>Baseline vs forecast dates"]
    H --> I["Action Engine<br/>Quantified recommendations"]
    I --> J["Decision Dashboard<br/>Health · Graph · Explanations"]

    K["Project baseline schedule"] --> H
    L["Future: specs and standards"] -.-> C
```

## Why this is not ordinary RAG

A RAG assistant retrieves passages and composes an answer. Cortex creates durable typed objects and edges, then runs graph algorithms and schedule calculations over them. The LLM performs extraction; deterministic services perform validation, traversal, date arithmetic, severity assignment, and recommendation formatting.

## Trust boundaries

- AI-generated entities and edges are constrained to enumerated types and known names.
- Relationship semantics are validated after extraction (`supplies` must originate from a vendor or contractor).
- Duplicate consequence events and duplicate occurrence-nodes are removed.
- Schedule forecasts disclose their methodology and compare baseline dates with calculated forecast dates.
- Every impact retains its dependency path for explainability.

## Scale strategy

The extraction layer can process documents in chunks and merge entities by normalized identity. The graph and reasoning layers have been exercised with 15,200 entities and 29,999 relationships. Production deployment would add a graph database, background extraction workers, document-level provenance, and human approval for high-impact changes.
