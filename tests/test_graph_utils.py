from backend.graph.graph_builder import GraphBuilder
from backend.graph.graph_utils import GraphUtils
from demo_data.sample_project import build_sample_project


def test_entity_exists():

    project = build_sample_project()

    graph = GraphBuilder().build(project)

    generator = next(
        entity
        for entity in project.entities
        if entity.name == "Generator G-12"
    )

    assert GraphUtils.entity_exists(
        graph,
        generator.id,
    )


def test_find_downstream_entities():

    project = build_sample_project()

    graph = GraphBuilder().build(project)

    generator = next(
        entity
        for entity in project.entities
        if entity.name == "Generator G-12"
    )

    downstream = GraphUtils.find_downstream_entities(
        graph,
        generator.id,
    )

    assert len(downstream) == 3


def test_find_upstream_entities():

    project = build_sample_project()

    graph = GraphBuilder().build(project)

    commissioning = next(
        entity
        for entity in project.entities
        if entity.name == "Commissioning"
    )

    upstream = GraphUtils.find_upstream_entities(
        graph,
        commissioning.id,
    )

    assert len(upstream) == 4


def test_find_shortest_dependency_path():

    project = build_sample_project()

    graph = GraphBuilder().build(project)

    generator = next(
        entity
        for entity in project.entities
        if entity.name == "Generator G-12"
    )

    commissioning = next(
        entity
        for entity in project.entities
        if entity.name == "Commissioning"
    )

    path = GraphUtils.find_shortest_dependency_path(
        graph,
        generator.id,
        commissioning.id,
    )

    assert len(path) == 4