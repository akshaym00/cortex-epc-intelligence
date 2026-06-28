from abc import ABC, abstractmethod


class DocumentLoader(ABC):
    """
    Base class for all document loaders.
    """

    @abstractmethod
    def load(self, path: str) -> str:
        """
        Return the document text.
        """
        pass