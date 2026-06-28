from backend.models.entity import Entity
from backend.models.enums import EntityType


def test_entity_creation():
    generator = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Generator G-12",
        attributes={
            "capacity": "1500 KVA",
            "vendor": "Cummins"
        }
    )

    assert generator.entity_type == EntityType.EQUIPMENT
    assert generator.name == "Generator G-12"
    assert generator.attributes["capacity"] == "1500 KVA"
    assert generator.status == "active"