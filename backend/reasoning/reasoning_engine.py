"""
Reasoning Engine for Project Cortex.

Uses graph traversal to identify downstream impacts
of changes within a project.
"""

import networkx as nx


class ReasoningEngine:
    """
    Performs reasoning over the Living Project Graph.
    """

    def get_downstream_entities(
        self,
        graph: nx.DiGraph,
        entity_id: str,
    ) -> list[str]:
        """
        Return all downstream entities affected by
        the supplied entity.
        """

        return list(nx.descendants(graph, entity_id))