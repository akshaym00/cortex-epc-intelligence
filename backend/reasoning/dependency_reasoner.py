"""
Dependency Reasoner.

Provides dependency reasoning over the project graph.
"""

from networkx import DiGraph

from backend.graph.graph_utils import GraphUtils


class DependencyReasoner:
    """
    Responsible only for dependency traversal.
    """

    def get_downstream_entities(
        self,
        graph: DiGraph,
        entity_id: str,
    ) -> list[str]:
        """
        Return all downstream entity IDs.
        """

        return GraphUtils.find_downstream_entities(
            graph,
            entity_id,
        )

    def get_upstream_entities(
        self,
        graph: DiGraph,
        entity_id: str,
    ) -> list[str]:
        """
        Return all upstream entity IDs.
        """

        return GraphUtils.find_upstream_entities(
            graph,
            entity_id,
        )

    def get_dependency_path(
        self,
        graph: DiGraph,
        source_entity_id: str,
        target_entity_id: str,
    ) -> list[str]:
        """
        Return the dependency path.
        """

        return GraphUtils.find_shortest_dependency_path(
            graph,
            source_entity_id,
            target_entity_id,
        )