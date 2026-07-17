"""
Base class for all Project State handlers.
"""

from abc import ABC, abstractmethod

from backend.models.event import ProjectEvent
from backend.project_state.living_project_model import LivingProjectModel


class BaseStateHandler(ABC):

    @abstractmethod
    def handle(
        self,
        living_model: LivingProjectModel,
        event: ProjectEvent,
    ) -> LivingProjectModel:
        """
        Apply an event to the Living Project Model.
        """
        raise NotImplementedError