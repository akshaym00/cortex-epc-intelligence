from backend.models.entity import Entity
from backend.models.enums import EntityType
from backend.models.project import Project
from backend.project_state.living_project_factory import (
    LivingProjectFactory,
)


def test_factory_initializes_states():

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator",
    )

    project = Project(
        name="Demo",
        entities=[generator],
    )

    living_model = LivingProjectFactory.create(
        project,
    )

    assert generator.id in living_model.state_index