from backend.models.entity import Entity
from backend.models.enums import EntityType, RelationshipType
from backend.models.project import Project
from backend.models.relationship import Relationship


def test_project_creation():

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator G-12"
    )

    testing = Entity(
        entity_type=EntityType.TASK,
        name="Electrical Testing"
    )

    relationship = Relationship(
        source_entity_id=generator.id,
        relationship_type=RelationshipType.REQUIRES,
        target_entity_id=testing.id
    )

    project = Project(
        name="Demo Data Center",
        entities=[generator, testing],
        relationships=[relationship]
    )

    assert project.name == "Demo Data Center"

    assert len(project.entities) == 2

    assert len(project.relationships) == 1

    assert project.entities[0].name == "Generator G-12"

    assert project.relationships[0].relationship_type == RelationshipType.REQUIRES