import json

from backend.extraction.relationship_extractor import (
    RelationshipExtractor,
)
from backend.models.enums import RelationshipType


class FakeLLMClient:

    def generate(self, prompt: str):

        return json.dumps(
            {
                "relationships": [
                    {
                        "source": "Cummins",
                        "relationship_type": "supplies",
                        "target": "Generator G-12",
                    }
                ]
            }
        )


def test_relationship_extraction():

    extractor = RelationshipExtractor()

    extractor.client = FakeLLMClient()

    entity_lookup = {
        "Cummins": "vendor_001",
        "Generator G-12": "equipment_001",
    }

    relationships = extractor.extract(
        "Cummins supplies Generator G-12.",
        entity_lookup,
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_entity_id == "vendor_001"

    assert relationship.target_entity_id == "equipment_001"

    assert (
        relationship.relationship_type
        == RelationshipType.SUPPLIES
    )