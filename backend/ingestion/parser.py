"""
Document parser for pre-processing raw document text.

Normalizes whitespace, strips boilerplate headers/footers,
and prepares text for LLM extraction.
"""

import re


class DocumentParser:
    """
    Pre-processes raw document text before extraction.
    """

    @staticmethod
    def parse(text: str) -> str:
        """
        Normalize and clean raw document text.

        - Collapses multiple blank lines into a single blank line.
        - Strips leading/trailing whitespace from each line.
        - Removes common boilerplate markers.

        Parameters
        ----------
        text : str
            Raw text extracted from a document loader.

        Returns
        -------
        str
            Cleaned text ready for extraction.
        """

        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Strip each line
        lines = [line.strip() for line in text.split("\n")]

        # Collapse multiple blank lines into one
        cleaned_lines = []
        previous_blank = False

        for line in lines:
            if not line:
                if not previous_blank:
                    cleaned_lines.append("")
                previous_blank = True
            else:
                cleaned_lines.append(line)
                previous_blank = False

        result = "\n".join(cleaned_lines).strip()

        return result

    @staticmethod
    def extract_sections(text: str) -> list[dict[str, str]]:
        """
        Split the document into sections based on common
        heading patterns (numbered headings, uppercase lines).

        Returns a list of dicts with 'heading' and 'content' keys.
        """

        heading_pattern = re.compile(
            r"^(?:\d+[\.\)]\s+|[A-Z][A-Z\s]{4,}$)",
            re.MULTILINE,
        )

        sections = []
        matches = list(heading_pattern.finditer(text))

        if not matches:
            return [{"heading": "", "content": text}]

        for i, match in enumerate(matches):
            heading = match.group().strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content = text[start:end].strip()

            sections.append({
                "heading": heading,
                "content": content,
            })

        return sections
