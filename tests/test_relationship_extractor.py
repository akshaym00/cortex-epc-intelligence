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


class DifferentlyFormattedEntityNamesLLM:

    def generate(self, prompt: str):
        assert "- Cummins" in prompt
        assert "- Generator G-12" in prompt

        return json.dumps(
            {
                "relationships": [
                    {
                        "source": "  CUMMINS ",
                        "relationship_type": "supplies",
                        "target": "generator g-12",
                    }
                ]
            }
        )


def test_relationship_entity_names_are_matched_robustly():
    extractor = RelationshipExtractor()
    extractor.client = DifferentlyFormattedEntityNamesLLM()

    relationships = extractor.extract(
        "Cummins supplies Generator G-12.",
        {
            "Cummins": "vendor_001",
            "Generator G-12": "equipment_001",
        },
    )

    assert len(relationships) == 1
    assert relationships[0].source_entity_id == "vendor_001"
    assert relationships[0].target_entity_id == "equipment_001"


class InvalidSupplierLLM:
    def generate(self, prompt: str):
        return json.dumps({"relationships": [{
            "source": "Generator Delivery",
            "relationship_type": "supplies",
            "target": "Diesel generator",
        }]})


def test_supplies_relationship_is_repaired_to_vendor_source():
    extractor = RelationshipExtractor()
    extractor.client = InvalidSupplierLLM()

    relationships = extractor.extract(
        "Vendor ABC supplies the diesel generator.",
        {
            "Vendor ABC": "vendor_001",
            "Generator Delivery": "milestone_001",
            "Diesel generator": "equipment_001",
        },
        {
            "vendor_001": "vendor",
            "milestone_001": "milestone",
            "equipment_001": "equipment",
        },
    )

    assert relationships[0].source_entity_id == "vendor_001"
    assert relationships[0].target_entity_id == "equipment_001"
