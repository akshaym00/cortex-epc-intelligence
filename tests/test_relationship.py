from backend.models.relationship import Relationship
from backend.models.enums import RelationshipType


def test_relationship_creation():

    relationship = Relationship(
        source_entity_id="generator_001",
        relationship_type=RelationshipType.REQUIRES,
        target_entity_id="testing_001",
    )

    assert relationship.source_entity_id == "generator_001"

    assert relationship.target_entity_id == "testing_001"

    assert relationship.relationship_type == RelationshipType.REQUIRES

    assert relationship.attributes == {}