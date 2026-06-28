from backend.graph.graph_builder import GraphBuilder
from backend.reasoning.reasoning_engine import ReasoningEngine
from demo_data.sample_project import build_sample_project


def test_reasoning_engine():

    project = build_sample_project()

    builder = GraphBuilder()

    graph = builder.build(project)

    generator = next(
        entity
        for entity in project.entities
        if entity.name == "Generator G-12"
    )

    engine = ReasoningEngine()

    affected = engine.get_downstream_entities(
        graph,
        generator.id,
    )

    assert len(affected) == 3