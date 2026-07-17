from backend.models.entity import Entity
from backend.models.enums import EntityType
from backend.models.project import Project
from backend.project_state.entity_resolver import EntityResolver


def test_resolver_scores_all_partial_matches():
    equipment = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Diesel generator",
    )
    milestone = Entity(
        entity_type=EntityType.MILESTONE,
        name="Generator Delivery",
    )
    project = Project(
        name="Data Centre Build",
        entities=[equipment, milestone],
    )

    resolved = EntityResolver.by_name(
        project,
        "Diesel generator delivery",
    )

    assert resolved == milestone
