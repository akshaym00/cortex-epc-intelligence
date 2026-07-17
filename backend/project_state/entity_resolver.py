"""
Entity Resolver.

Resolves project entities from names or IDs.
"""

from difflib import SequenceMatcher

from backend.models.entity import Entity
from backend.models.project import Project


class EntityResolver:

    @staticmethod
    def by_name(
        project: Project,
        name: str,
    ) -> Entity | None:

        # --------------------------
        # Exact match
        # --------------------------

        for entity in project.entities:

            if entity.name == name:
                return entity

        # --------------------------
        # Case-insensitive match
        # --------------------------

        query = name.strip().lower()

        for entity in project.entities:

            if entity.name.lower() == query:
                return entity

        # Score every candidate instead of returning the first partial
        # match. For example, "diesel generator delivery" should resolve
        # to "Generator Delivery", not whichever entity was extracted first.
        query_tokens = set(query.split())
        candidates = []

        for entity in project.entities:
            candidate = entity.name.strip().lower()
            candidate_tokens = set(candidate.split())
            shared_tokens = query_tokens & candidate_tokens

            token_score = (
                2 * len(shared_tokens)
                / (len(query_tokens) + len(candidate_tokens))
            )
            sequence_score = SequenceMatcher(
                None,
                query,
                candidate,
            ).ratio()

            score = (0.6 * sequence_score) + (0.4 * token_score)
            candidates.append((score, entity))

        if not candidates:
            return None

        score, entity = max(candidates, key=lambda item: item[0])
        return entity if score >= 0.5 else None

    @staticmethod
    def by_id(
        project: Project,
        entity_id: str,
    ) -> Entity | None:

        for entity in project.entities:

            if entity.id == entity_id:
                return entity

        return None
