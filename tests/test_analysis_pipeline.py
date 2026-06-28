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


def test_analysis_pipeline():

    pipeline = AnalysisPipeline()

    pipeline.entity_extractor.client = FakeEntityLLM()

    pipeline.relationship_extractor.client = FakeRelationshipLLM()

    result = pipeline.analyze(
        "demo_data/sample_document.txt"
    )

    assert len(result.entities) == 2

    assert len(result.relationships) == 1

    assert result.project.metadata["graph"].number_of_nodes() == 2

    assert result.project.metadata["graph"].number_of_edges() == 1