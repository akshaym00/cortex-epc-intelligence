from typing import Any

from pydantic import Field

from backend.models.base import CortexBaseModel
from backend.models.enums import EntityType


class Entity(CortexBaseModel):
    """
    Represents any real-world object inside
    the Living Project Model.
    """

    entity_type: EntityType

    name: str

    description: str | None = None

    status: str = "active"

    attributes: dict[str, Any] = Field(
        default_factory=dict
    )