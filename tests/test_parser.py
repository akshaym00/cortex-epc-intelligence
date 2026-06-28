from backend.extraction.parser import ExtractionParser


def test_parse_entities():

    response = """
    {
        "entities": [
            {
                "entity_type": "equipment",
                "name": "Generator G-12",
                "description": "Diesel Generator"
            }
        ]
    }
    """

    parsed = ExtractionParser.parse_entities(response)

    assert len(parsed.entities) == 1

    assert parsed.entities[0].name == "Generator G-12"

    assert parsed.entities[0].entity_type == "equipment"