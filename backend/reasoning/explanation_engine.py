"""
Explanation Engine.

Converts dependency paths into human-readable explanations.
"""

from backend.models.project import Project


class ExplanationEngine:
    """
    Generates human-readable explanations.
    """

    def explain_path(
        self,
        project: Project,
        dependency_path: list[str],
    ) -> str:

        names = []

        for entity_id in dependency_path:

            entity = next(
                (
                    e
                    for e in project.entities
                    if e.id == entity_id
                ),
                None,
            )

            if entity:
                names.append(entity.name)

        if not names:
            return "No dependency path found."

        return " → ".join(names)