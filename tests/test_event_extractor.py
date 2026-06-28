import json

from backend.extraction.event_extractor import (
    EventExtractor,
)


class FakeLLMClient:

    def generate(self, prompt: str):

        return json.dumps(
            {
                "events": [
                    {
                        "title": "Generator Delay",
                        "event_type": "delay",
                        "description": "Generator G-12 delayed by 9 days.",
                        "affected_entity_name": "Generator G-12",
                        "severity": "high",
                    }
                ]
            }
        )


def test_event_extraction():

    extractor = EventExtractor()

    extractor.client = FakeLLMClient()

    events = extractor.extract(
        "Generator G-12 will be delayed by 9 days."
    )

    assert len(events) == 1

    event = events[0]

    assert event.title == "Generator Delay"

    assert event.event_type == "delay"

    assert (
        event.affected_entity_name
        == "Generator G-12"
    )

    assert event.severity == "high"