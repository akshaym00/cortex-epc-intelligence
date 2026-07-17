"""
Project State Engine.
"""

from datetime import datetime, timezone

from backend.models.event import ProjectEvent
from backend.project_state.entity_state import EntityState
from backend.project_state.handlers.vendor_delay_handler import (
    VendorDelayHandler,
)
from backend.project_state.handlers.inspection_failed_handler import (
    InspectionFailedHandler,
)
from backend.project_state.living_project_model import LivingProjectModel


class StateUpdater:
    """
    Updates the Living Project Model.
    """

    def __init__(self):

        self.handlers = {
    "VendorDelay": VendorDelayHandler(),
    "InspectionFailed": InspectionFailedHandler(),
}

    def initialize(
        self,
        living_model: LivingProjectModel,
    ) -> LivingProjectModel:
        """
        Create default states for all project entities.
        """

        for entity in living_model.project.entities:
            living_model.state_index[entity.id] = EntityState(
                entity_id=entity.id
            )

        living_model.updated_at = datetime.now(timezone.utc)

        return living_model

    def update(
        self,
        living_model: LivingProjectModel,
        event: ProjectEvent,
    ) -> LivingProjectModel:
        """
        Apply a ProjectEvent.
        """

        handler = self.handlers.get(event.event_type)

        if handler is None:
            return living_model

        return handler.handle(
            living_model,
            event,
        )