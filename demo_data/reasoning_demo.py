from backend.graph.graph_builder import GraphBuilder
from backend.reasoning.reasoning_engine import ReasoningEngine
from demo_data.sample_project import build_sample_project


project = build_sample_project()

graph = GraphBuilder().build(project)

generator = next(
    entity
    for entity in project.entities
    if entity.name == "Generator G-12"
)

affected = ReasoningEngine().get_downstream_entities(
    graph,
    generator.id,
)

print("Generator G-12 impacts:")

for entity_id in affected:

    print(
        graph.nodes[entity_id]["name"]
    )