"""
Creates a sample Living Project Model for Project Cortex.

This file manually builds a small EPC project.
Later, these objects will be generated automatically
from project documents using AI.
"""

from backend.models.entity import Entity
from backend.models.enums import EntityType, RelationshipType
from backend.models.project import Project
from backend.models.relationship import Relationship


def build_sample_project() -> Project:
    """
    Build a small demo project.
    """

    # -------------------------
    # Entities
    # -------------------------

    vendor = Entity(
        entity_type=EntityType.VENDOR,
        name="Cummins"
    )

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator G-12"
    )

    installation = Entity(
        entity_type=EntityType.TASK,
        name="Generator Installation"
    )

    testing = Entity(
        entity_type=EntityType.TASK,
        name="Electrical Testing"
    )

    commissioning = Entity(
        entity_type=EntityType.MILESTONE,
        name="Commissioning"
    )

    entities = [
        vendor,
        generator,
        installation,
        testing,
        commissioning,
    ]

    # -------------------------
    # Relationships
    # -------------------------

    relationships = [

        Relationship(
            source_entity_id=vendor.id,
            relationship_type=RelationshipType.SUPPLIES,
            target_entity_id=generator.id,
        ),

        Relationship(
            source_entity_id=generator.id,
            relationship_type=RelationshipType.REQUIRES,
            target_entity_id=installation.id,
        ),

        Relationship(
            source_entity_id=installation.id,
            relationship_type=RelationshipType.DEPENDS_ON,
            target_entity_id=testing.id,
        ),

        Relationship(
            source_entity_id=testing.id,
            relationship_type=RelationshipType.PART_OF,
            target_entity_id=commissioning.id,
        ),
    ]

    return Project(
        name="Demo Data Center Project",
        description="Sample EPC project used for Project Cortex development.",
        entities=entities,
        relationships=relationships,
    )


if __name__ == "__main__":

    project = build_sample_project()

    print(f"Project: {project.name}")
    print(f"Entities: {len(project.entities)}")
    print(f"Relationships: {len(project.relationships)}")