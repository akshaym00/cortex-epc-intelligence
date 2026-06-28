from backend.models.enums import RelationshipType


def test_relationship_type():

    assert RelationshipType.SUPPLIES == "supplies"

    assert RelationshipType.DEPENDS_ON == "depends_on"

    assert RelationshipType.PART_OF == "part_of"