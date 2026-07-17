# Project Cortex — 3-minute demo script

## 0:00–0:25 — The problem

“A data-centre project has thousands of schedule lines, hundreds of contractors, and critical facts buried across RFIs, emails, reports, and submittals. A seven-day vendor delay rarely stays a seven-day vendor problem—it propagates into installation, testing, commissioning, and handover.”

## 0:25–0:45 — The distinction

“ChatGPT can summarize this document. Project Cortex converts it into a living project model: typed entities, validated relationships, independent events, and a persistent dependency graph. That structure lets us calculate consequences rather than merely describe them.”

## 0:45–1:10 — Analyze the document

1. Upload `demo/sample_documents/vendor_delay.txt`.
2. Click **Analyze Project**.
3. While it runs, say: “Cortex is extracting entities, resolving aliases, validating relationship direction, separating timeline events from persistent project objects, and building the graph.”

## 1:10–1:35 — Executive view

Point to **Project Health**.

“The project manager immediately sees risk level, entity and relationship counts, independent events, impacted entities, and recommended actions. The event is shown once, enriched with who reported it and which activities are affected.”

## 1:35–2:05 — Quantified schedule impact

Point to **Impact Analysis**.

“The nine-day delay is extracted from the document. Cortex traverses the dependency graph, compares affected activities with the project baseline, and forecasts shifted dates. Severity is calculated from delay duration. This is a nine-day critical-path exposure—not an arbitrary ‘medium’ label.”

Point to the quantified recommendation.

“The action engine proposes a recovery scenario and states the estimated recoverable days, while explicitly asking the scheduler to validate the scenario.”

## 2:05–2:35 — Explainable graph

Point to **Knowledge Graph**, then click an impacted activity.

“The graph is the key difference. Every recommendation is grounded in a path. Clicking Electrical Testing shows the triggering event, the dependency chain, and why the activity is affected. The LLM extracts; graph traversal and date calculations reason.”

## 2:35–2:50 — Scale evidence

“We also tested the reasoning core at the problem-statement scale: 15,200 entities, 29,999 relationships, and a 14,999-node downstream traversal. On our development machine, graph construction completed in 0.096 seconds and traversal in 0.013 seconds.”

## 2:50–3:00 — Close

“Project Cortex turns fragmented construction documents into decision intelligence: what changed, what it affects, when it will move, why, and what to do next.”

## Judge questions

### Why is this better than ChatGPT reading a document?

“ChatGPT summarizes text. Cortex creates a persistent typed graph, validates its semantics, and performs deterministic dependency, critical-path, and impact reasoning across documents. Its output remains queryable and explainable after the chat is over.”

### Is the schedule prediction AI-generated?

“The delay value is extracted from the event. Date shifts and severity are deterministic calculations against the project baseline. AI does not invent the arithmetic.”

### Is the baseline synthetic?

“For this prototype, yes. The interface is designed to accept a real P6/MS Project export next. The demo baseline makes the calculation reproducible without exposing client data.”

### What happens when extraction is wrong?

“We constrain types and names, apply semantic rules after extraction, retain paths and provenance, and would put high-impact changes behind human approval in production.”
