import json

from backend.pipeline.analysis_pipeline import AnalysisPipeline


class FakeEntityLLM:

    def generate(self, prompt: str):

        return json.dumps(
            {
                "entities": [
                    {
                        "entity_type": "vendor",
                        "name": "Cummins",
                        "description": "Generator supplier",
                    },
                    {
                        "entity_type": "equipment",
                        "name": "Generator G-12",
                        "description": "Diesel Generator",
                    },
                ]
            }
        )


class FakeRelationshipLLM:

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


class FakeEventLLM:

    def generate(self, prompt: str):

        return json.dumps(
            {
                "events": [
                    {
                        "title": "Generator Delay",
                        "event_type": "delay",
                        "description": "Generator delayed by 9 days.",
                        "affected_entity_name": "Generator G-12",
                        "severity": "high",
                    }
                ]
            }
        )


def test_analysis_pipeline():

    pipeline = AnalysisPipeline()

    pipeline.entity_extractor.client = FakeEntityLLM()

    pipeline.relationship_extractor.client = (
        FakeRelationshipLLM()
    )

    pipeline.event_extractor.client = FakeEventLLM()

    result = pipeline.analyze(
        "demo_data/sample_document.txt"
    )

    assert len(result.entities) == 2

    assert len(result.relationships) == 1

    assert len(result.events) == 1

    assert (
        result.events[0].title
        == "Generator Delay"
    )

    graph = result.project.metadata["graph"]

    assert graph.number_of_nodes() == 2

    assert graph.number_of_edges() == 1

    assert (
        len(result.project.metadata["events"])
        == 1
    )