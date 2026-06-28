from pathlib import Path

from backend.ingestion.pdf_loader import PDFLoader
from backend.ingestion.text_loader import TextLoader


class LoaderFactory:

    @staticmethod
    def create(path: str):

        extension = Path(path).suffix.lower()

        if extension == ".pdf":
            return PDFLoader()

        if extension == ".txt":
            return TextLoader()

        raise ValueError(f"Unsupported file type: {extension}")