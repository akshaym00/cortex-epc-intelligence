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
            - Extract persistent project objects. Do not create an event,
              issue, or risk entity for an occurrence that belongs in the
              event timeline (for example, "generator delayed by 7 days").

            Document:

            {document}
            """
        ).strip()

    @staticmethod
    def relationship_extraction(
        document: str,
        entity_names: list[str] | None = None,
    ) -> str:
        entity_names = entity_names or []
        allowed_entities = "\n".join(
            f"- {name}" for name in entity_names
        )

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
            - Source and target must exactly match names from the
              allowed entity list below.
            - Relationship direction must read naturally as:
              "source relationship_type target".
            - For supplies, the source must be a vendor, contractor, or
              supplier and the target must be the supplied equipment or
              material. A delivery, milestone, task, or event never
              supplies equipment.
            - Use depends_on when an activity or milestone cannot proceed
              without another entity.
            - Use references only when the document explicitly refers to
              another entity; do not use it as a generic connection.
            - Do not create a relationship merely because two entity names
              describe the same real-world concept.

            Allowed entities:

            {allowed_entities}

            Document:

            {document}
            """
        ).strip()

    @staticmethod
    def event_extraction(
        document: str,
        entity_names: list[str] | None = None,
    ) -> str:
        entity_names = entity_names or []
        allowed_entities = "\n".join(
            f"- {name}" for name in entity_names
        )

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
            - Return only independent incidents. Do not emit a downstream
              consequence (for example, "commissioning may be affected")
              as a second event when it is caused by an event already listed.
            - affected_entity_name must exactly match one name from the
              allowed entity list below.

            Allowed entities:

            {allowed_entities}

            Document:

            {document}
            """
        ).strip()
