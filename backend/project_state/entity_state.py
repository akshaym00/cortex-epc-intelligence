"""
Dynamic state of an entity inside the Living Project Model.
"""

from datetime import datetime, timezone
from typing import Any

from pydantic import Field

from backend.models.base import CortexBaseModel


class EntityState(CortexBaseModel):
    """
    Stores changing information about an entity.
    """

    entity_id: str

    status: str = "active"

    health: str = "normal"

    risk_level: str = "low"

    properties: dict[str, Any] = Field(default_factory=dict)

    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))