from backend.prompts.extraction_prompts import ExtractionPrompts


def test_entity_prompt():

    prompt = ExtractionPrompts.entity_extraction(
        "Generator G-12 supplied by Cummins."
    )

    assert "Generator G-12" in prompt
    assert "JSON" in prompt
    assert "entities" in prompt


def test_relationship_prompt():

    prompt = ExtractionPrompts.relationship_extraction(
        "Generator G-12 supplied by Cummins."
    )

    assert "relationships" in prompt
    assert "JSON" in prompt


def test_event_prompt():

    prompt = ExtractionPrompts.event_extraction(
        "Generator delivery delayed by 9 days."
    )

    assert "events" in prompt
    assert "JSON" in prompt