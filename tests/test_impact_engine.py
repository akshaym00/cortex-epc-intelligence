from backend.graph.graph_builder import GraphBuilder
from backend.models.entity import Entity
from backend.models.enums import (
    EntityType,
    RelationshipType,
)
from backend.models.event import ProjectEvent
from backend.models.project import Project
from backend.models.relationship import Relationship
from backend.project_state.living_project_factory import (
    LivingProjectFactory,
)
from backend.reasoning.impact_engine import ImpactEngine


def test_impact_engine():

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

    living_model = LivingProjectFactory.create(project)

    event = ProjectEvent(
        title="Vendor Delay",
        event_type="VendorDelay",
        description="Generator delivery delayed",
        affected_entity_name="Generator",
    )

    engine = ImpactEngine()

    report = engine.analyze(
        living_model,
        graph,
        event,
    )

    assert len(report.impacted_entities) == 1
    assert report.impacted_entities[0].affected_entity_name == "Installation"


def test_event_and_risk_nodes_are_not_reported_as_impacted_activities():
    generator = Entity(entity_type=EntityType.EQUIPMENT, name="Generator")
    risk = Entity(entity_type=EntityType.RISK, name="Delivery Risk")
    installation = Entity(entity_type=EntityType.TASK, name="Installation")
    project = Project(
        name="Demo",
        entities=[generator, risk, installation],
        relationships=[
            Relationship(
                source_entity_id=generator.id,
                target_entity_id=risk.id,
                relationship_type=RelationshipType.AFFECTS,
            ),
            Relationship(
                source_entity_id=risk.id,
                target_entity_id=installation.id,
                relationship_type=RelationshipType.AFFECTS,
            ),
        ],
    )
    event = ProjectEvent(
        title="Generator delay",
        event_type="delay",
        description="Generator is delayed.",
        affected_entity_name="Generator",
    )

    report = ImpactEngine().analyze(
        LivingProjectFactory.create(project),
        GraphBuilder().build(project),
        event,
    )

    assert [impact.affected_entity_name for impact in report.impacted_entities] == [
        "Installation"
    ]
