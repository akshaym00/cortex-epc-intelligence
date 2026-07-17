# Scalability Evidence

## Test scope

The repeatable benchmark in `demo/scalability_benchmark.py` models the lower bound of the hackathon brief:

- 200 contractors
- 15,000 schedule activities
- 15,200 total graph nodes
- 29,999 directed relationships
- A worst-case chain traversal reaching 14,999 downstream activities

## Measured result

Measured locally on 8 July 2026:

| Operation | Result |
|---|---:|
| Model generation | 0.443 s |
| Directed graph construction | 0.096 s |
| 14,999-node downstream traversal | 0.013 s |

## Real 20-line RFI extraction test

The production pipeline was also run against `demo/sample_documents/dense_rfi_log.txt`, containing 20 RFIs across vendors, equipment, approvals, testing, commissioning and handover.

| Result | Value |
|---|---:|
| End-to-end extraction time (before parallel-call optimization) | 141.21 s |
| Extracted persistent entities | 37 |
| Validated relationships | 27 |
| Independent events | 8 |
| Propagated impacts | 7 |
| Recommendations | 4 |
| Raw unconnected entities | 2 |

Unconnected entities are retained in the entity inventory but deliberately excluded from the visual knowledge graph, preventing floating nodes from obscuring connected project logic. The run exposed and led to fixes for a Windows console-encoding crash and over-extraction of routine supply statements as events.

## What this proves

It demonstrates that the in-memory graph and dependency-reasoning core can represent and traverse a project at the brief’s stated line-item scale.

## What this does not prove

It does not measure LLM extraction throughput for 15,000 lines, concurrent users, database persistence, or production infrastructure. Those require chunked asynchronous ingestion, caching, a graph database, and load testing. This boundary should be stated plainly during judging.

## Reproduce

From the project root:

```powershell
.\.venv\Scripts\python.exe -m demo.scalability_benchmark
```
