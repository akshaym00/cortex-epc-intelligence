import pytest

from backend.extraction.relationship_parser import RelationshipParser


def test_parse_relationships():

    response = """
    {
        "relationships": [
            {
                "source": "Cummins",
                "relationship_type": "supplies",
                "target": "Generator G-12"
            }
        ]
    }
    """

    parsed = RelationshipParser.parse(response)

    assert len(parsed.relationships) == 1

    assert parsed.relationships[0].source == "Cummins"

    assert parsed.relationships[0].relationship_type == "supplies"

    assert parsed.relationships[0].target == "Generator G-12"


def test_invalid_json():

    response = "INVALID JSON"

    with pytest.raises(Exception):
        RelationshipParser.parse(response)