from backend.models.enums import EntityType


def test_entity_type_values():
    assert EntityType.EQUIPMENT == "equipment"
    assert EntityType.VENDOR == "vendor"
    assert EntityType.RISK == "risk"