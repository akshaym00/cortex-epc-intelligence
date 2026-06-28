from backend.ingestion.document_loader import DocumentLoader


class TextLoader(DocumentLoader):

    def load(self, path: str) -> str:

        with open(path, "r", encoding="utf-8") as file:

            return file.read()