from backend.graph.graph_builder import GraphBuilder
from backend.models.entity import Entity
from backend.models.enums import EntityType, RelationshipType
from backend.models.project import Project
from backend.models.relationship import Relationship
from backend.reasoning.dependency_reasoner import DependencyReasoner


def test_get_downstream_entities():

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator",
    )

    installation = Entity(
        entity_type=EntityType.TASK,
        name="Installation",
    )

    relationship = Relationship(
        source_entity_id=generator.id,
        target_entity_id=installation.id,
        relationship_type=RelationshipType.DEPENDS_ON,
    )

    project = Project(
        name="Demo",
        entities=[generator, installation],
        relationships=[relationship],
    )

    graph = GraphBuilder().build(project)

    reasoner = DependencyReasoner()

    downstream = reasoner.get_downstream_entities(
        graph,
        generator.id,
    )

    assert installation.id in downstream