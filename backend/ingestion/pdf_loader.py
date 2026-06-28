from pypdf import PdfReader

from backend.ingestion.document_loader import DocumentLoader


class PDFLoader(DocumentLoader):

    def load(self, path: str) -> str:

        reader = PdfReader(path)

        pages = []

        for page in reader.pages:

            pages.append(page.extract_text())

        return "\n".join(pages)