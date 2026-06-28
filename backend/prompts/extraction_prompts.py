"""
Prompt templates for Project Cortex.

All prompts used by the AI system should be defined here.
"""

from textwrap import dedent


class ExtractionPrompts:
    """
    Centralized prompt library.
    """

    @staticmethod
    def entity_extraction(document: str) -> str:
        return dedent(
            f"""
            You are an EPC project knowledge extraction assistant.

            Extract every project entity from the document.

            Valid entity types:

            - project
            - equipment
            - system
            - task
            - milestone
            - vendor
            - contractor
            - team
            - person
            - document
            - risk
            - event
            - issue
            - approval
            - location

            Return ONLY valid JSON.

            Format:

            {{
                "entities": [
                    {{
                        "entity_type": "...",
                        "name": "...",
                        "description": "..."
                    }}
                ]
            }}

            Document:

            {document}
            """
        ).strip()

    @staticmethod
    def relationship_extraction(document: str) -> str:
        return dedent(
            f"""
            You are an EPC project knowledge extraction assistant.

            Extract every relationship that exists between project entities.

            Valid relationship types:

            - depends_on
            - requires
            - supplies
            - installed_by
            - owned_by
            - modifies
            - references
            - generates
            - mitigates
            - affects
            - located_in
            - approved_by
            - triggers
            - part_of
            - caused_by

            Return ONLY valid JSON.

            Format:

            {{
                "relationships": [
                    {{
                        "source": "...",
                        "relationship_type": "...",
                        "target": "..."
                    }}
                ]
            }}

            Document:

            {document}
            """
        ).strip()

    @staticmethod
    def event_extraction(document: str) -> str:
        return dedent(
            f"""
            You are an EPC project event extraction assistant.

            Extract every project event.

            Return ONLY valid JSON.

            Format:

            {{
                "events": [
                    {{
                        "title": "...",
                        "description": "...",
                        "severity": "..."
                    }}
                ]
            }}

            Document:

            {document}
            """
        ).strip()