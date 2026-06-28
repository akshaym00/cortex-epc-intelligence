from backend.models.enums import ImpactSeverity
from backend.models.impact import Impact


def test_impact_creation():

    impact = Impact(
        affected_entity_id="task_001",
        affected_entity_name="Electrical Testing",
        severity=ImpactSeverity.HIGH,
        dependency_path=[
            "Generator G-12",
            "Generator Installation",
            "Electrical Testing",
        ],
        reason=(
            "Electrical Testing depends on "
            "Generator Installation."
        ),
    )

    assert impact.affected_entity_id == "task_001"

    assert impact.affected_entity_name == "Electrical Testing"

    assert impact.severity == ImpactSeverity.HIGH

    assert len(impact.dependency_path) == 3

    assert impact.confidence == 1.0