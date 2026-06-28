import json

from backend.pipeline.analysis_pipeline import AnalysisPipeline


class FakeLLMClient:

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


def test_analysis_pipeline():

    pipeline = AnalysisPipeline()

    pipeline.entity_extractor.client = FakeLLMClient()

    result = pipeline.analyze(
        "demo_data/sample_document.txt"
    )

    assert len(result.entities) == 2

    assert result.project.name == "Auto Generated Project"

    assert result.project.metadata["graph"].number_of_nodes() == 2