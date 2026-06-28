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

print("\nRelationships\n")

for relationship in result.relationships:

    print(
        relationship.source_entity_id,
        "--",
        relationship.relationship_type.value,
        "-->",
        relationship.target_entity_id,
    )

print()

graph = result.project.metadata["graph"]

print("Graph Nodes :", graph.number_of_nodes())

print("Graph Edges :", graph.number_of_edges())