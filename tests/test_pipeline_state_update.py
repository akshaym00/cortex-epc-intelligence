from backend.models.entity import Entity
from backend.models.enums import EntityType
from backend.models.event import ProjectEvent
from backend.models.project import Project
from backend.project_state.living_project_factory import (
    LivingProjectFactory,
)
from backend.project_state.state_updater import (
    StateUpdater,
)


def test_pipeline_updates_living_project():

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator",
    )

    project = Project(
        name="Demo",
        entities=[generator],
    )

    living = LivingProjectFactory.create(
        project
    )

    updater = StateUpdater()

    event = ProjectEvent(
        title="Delay",
        event_type="VendorDelay",
        description="Delayed",
        affected_entity_name="Generator",
        metadata={
            "delay_days": 7
        },
    )

    living = updater.update(
        living,
        event,
    )

    state = living.state_index[generator.id]

    assert state.status == "delayed"

    assert state.properties["delay_days"] == 7