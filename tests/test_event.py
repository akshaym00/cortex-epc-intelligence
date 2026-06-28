from backend.models.event import ProjectEvent


def test_event_creation():

    event = ProjectEvent(
        title="Generator Delay",
        event_type="delay",
        description="Generator delayed by 9 days.",
        affected_entity_name="Generator G-12",
        severity="high",
    )

    assert event.title == "Generator Delay"

    assert event.event_type == "delay"

    assert event.affected_entity_name == "Generator G-12"

    assert event.severity == "high"