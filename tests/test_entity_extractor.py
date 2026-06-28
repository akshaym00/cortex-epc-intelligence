import json

from backend.extraction.entity_extractor import EntityExtractor


class FakeLLMClient:

    def generate(self, prompt: str):

        return json.dumps(
            {
                "entities": [
                    {
                        "entity_type": "equipment",
                        "name": "Generator G-12",
                        "description": "Diesel Generator",
                    }
                ]
            }
        )


def test_entity_extraction():

    extractor = EntityExtractor()

    extractor.client = FakeLLMClient()

    entities = extractor.extract(
        "Generator G-12 supplied by Cummins."
    )

    assert len(entities) == 1

    assert entities[0].name == "Generator G-12"