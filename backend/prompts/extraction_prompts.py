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

            Rules:

            - Return ONLY JSON.
            - Do not include markdown.
            - Do not explain your answer.
            - Do not invent entities.

            Document:

            {document}
            """
        ).strip()

    @staticmethod
    def relationship_extraction(document: str) -> str:
        return dedent(
            f"""
            You are an EPC project knowledge extraction assistant.

            Extract every relationship between the entities found in the document.

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

            Rules:

            - Return ONLY JSON.
            - Do not include markdown.
            - Do not explain your answer.
            - Use only relationship types listed above.
            - Do not invent relationships.

            Document:

            {document}
            """
        ).strip()

    @staticmethod
    def event_extraction(document: str) -> str:
        return dedent(
            f"""
            You are an EPC project event extraction assistant.

            Detect every project event described in the document.

            Typical event types include:

            - delay
            - risk
            - issue
            - approval
            - completion
            - inspection
            - delivery
            - installation
            - failure
            - change

            Return ONLY valid JSON.

            Format:

            {{
                "events": [
                    {{
                        "title": "...",
                        "event_type": "...",
                        "description": "...",
                        "affected_entity_name": "...",
                        "severity": "low|medium|high|critical"
                    }}
                ]
            }}

            Rules:

            - Return ONLY JSON.
            - Do not include markdown.
            - Do not explain your answer.
            - Do not invent events.
            - Severity must be one of:
              low, medium, high, critical.

            Document:

            {document}
            """
        ).strip()