"""
Factory for creating a LivingProjectModel.
"""

from backend.models.project import Project
from backend.project_state.living_project_model import (
    LivingProjectModel,
)
from backend.project_state.state_updater import StateUpdater


class LivingProjectFactory:
    """
    Creates initialized LivingProjectModels.
    """

    @staticmethod
    def create(
        project: Project,
    ) -> LivingProjectModel:

        living_model = LivingProjectModel(
            project=project,
        )

        updater = StateUpdater()

        return updater.initialize(
            living_model,
        )