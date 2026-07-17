from backend.models.event import ProjectEvent
from backend.recommendation.recommendation_engine import RecommendationEngine


def test_duplicate_recommendations_are_removed():
    events = [
        ProjectEvent(
            title="Generator delivery delay",
            event_type="delay",
            description="Delivery is late.",
            affected_entity_name="Generator Delivery",
            severity="medium",
        ),
        ProjectEvent(
            title="Commissioning delay risk",
            event_type="risk",
            description="Commissioning may be late.",
            affected_entity_name="Commissioning",
            severity="medium",
        ),
    ]

    recommendations = RecommendationEngine().generate(events, [])
    titles = [recommendation.title for recommendation in recommendations]

    assert len(titles) == len(set(titles))
    assert titles.count("Expedite delayed activity") == 1
    assert titles.count("Review project schedule") == 1
