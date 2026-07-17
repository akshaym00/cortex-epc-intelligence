"""
Inspection Failed handler.
"""

from datetime import datetime, timezone

from backend.models.event import ProjectEvent
from backend.project_state.entity_resolver import EntityResolver
from backend.project_state.handlers.base_handler import BaseStateHandler
from backend.project_state.living_project_model import LivingProjectModel


class InspectionFailedHandler(BaseStateHandler):
    """
    Handles InspectionFailed events.
    """

    def handle(
        self,
        living_model: LivingProjectModel,
        event: ProjectEvent,
    ) -> LivingProjectModel:

        entity = EntityResolver.by_name(
            living_model.project,
            event.affected_entity_name,
        )

        if entity is None:
            return living_model

        state = living_model.state_index.get(entity.id)

        if state is None:
            return living_model

        state.status = "inspection_failed"
        state.risk_level = "high"

        state.properties["inspection_status"] = "failed"

        state.last_updated = datetime.now(timezone.utc)

        living_model.history.append(event)

        living_model.updated_at = datetime.now(timezone.utc)

        return living_model