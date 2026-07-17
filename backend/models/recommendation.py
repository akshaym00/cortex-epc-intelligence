"""
Recommendation model.
"""

from backend.models.base import CortexBaseModel


class Recommendation(CortexBaseModel):
    """
    Action recommended by Project Cortex.
    """

    title: str

    description: str

    priority: str = "medium"

    related_event: str | None = None