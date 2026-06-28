from backend.pipeline.analysis_pipeline import AnalysisPipeline


pipeline = AnalysisPipeline()

result = pipeline.analyze(
    "demo_data/sample_document.txt"
)

print("=" * 60)
print("PROJECT CORTEX")
print("=" * 60)

print("\nEntities\n")

for entity in result.entities:

    print(
        f"{entity.entity_type.value:12} {entity.name}"
    )

print()

print(
    "Graph Nodes:",
    result.project.metadata["graph"].number_of_nodes(),
)

print(
    "Graph Edges:",
    result.project.metadata["graph"].number_of_edges(),
)