from backend.graph.graph_builder import GraphBuilder
from demo_data.sample_project import build_sample_project


def test_graph_builder():

    project = build_sample_project()

    builder = GraphBuilder()

    graph = builder.build(project)

    assert graph.number_of_nodes() == 5

    assert graph.number_of_edges() == 4