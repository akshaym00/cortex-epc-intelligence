from backend.models.entity import Entity
from backend.models.enums import EntityType
from backend.models.project import Project
from backend.project_state.living_project_model import LivingProjectModel
from backend.project_state.state_updater import StateUpdater


def test_initialize_entity_states():

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator",
    )

    ups = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="UPS",
    )

    project = Project(
        name="Demo Project",
        entities=[generator, ups],
    )

    living_model = LivingProjectModel(
        project=project
    )

    updater = StateUpdater()

    living_model = updater.initialize(living_model)

    assert len(living_model.state_index) == 2

    assert generator.id in living_model.state_index

    assert ups.id in living_model.state_index
from backend.models.event import ProjectEvent


def test_vendor_delay_updates_state():

    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator",
    )

    project = Project(
        name="Demo",
        entities=[generator],
    )

    living_model = LivingProjectModel(
        project=project
    )

    updater = StateUpdater()

    living_model = updater.initialize(living_model)

    event = ProjectEvent(
        title="Generator Delay",
        event_type="VendorDelay",
        description="Shipment delayed",
        affected_entity_name="Generator",
        metadata={
            "delay_days": 9
        }
    )

    living_model = updater.update(
        living_model,
        event,
    )

    state = living_model.state_index[generator.id]

    assert state.status == "delayed"

    assert state.risk_level == "high"

    assert state.properties["delay_days"] == 9

    assert len(living_model.history) == 1