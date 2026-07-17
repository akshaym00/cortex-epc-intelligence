import json

from backend.extraction.event_extractor import EventExtractor


class DuplicateEventLLM:
    def generate(self, prompt: str):
        return json.dumps({"events": [
            {
                "title": "Generator delivery delayed by 7 days",
                "event_type": "delay",
                "description": "Vendor ABC reported a 7 day generator delay.",
                "affected_entity_name": "Generator Delivery",
                "severity": "medium"
            },
            {
                "title": "Potential impact on commissioning",
                "event_type": "risk",
                "description": "Commissioning may be affected by the generator delay.",
                "affected_entity_name": "Commissioning",
                "severity": "medium"
            }
        ]})


def test_downstream_consequence_is_not_a_duplicate_event():
    extractor = EventExtractor()
    extractor.client = DuplicateEventLLM()

    events = extractor.extract("Vendor ABC reported a generator delay.")

    assert len(events) == 1
    assert events[0].title == "Generator delivery delayed by 7 days"
