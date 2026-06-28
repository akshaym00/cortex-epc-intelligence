"""
Graph utility functions for Project Cortex.

This module centralizes all graph traversal algorithms.
The Reasoning Engine should never call NetworkX directly.
"""

from typing import List

import networkx as nx


class GraphUtils:
    """
    Utility class containing reusable graph algorithms.
    """

    @staticmethod
    def entity_exists(
        graph: nx.DiGraph,
        entity_id: str,
    ) -> bool:
        """
        Check whether an entity exists in the graph.
        """
        return graph.has_node(entity_id)

    @staticmethod
    def find_downstream_entities(
        graph: nx.DiGraph,
        entity_id: str,
    ) -> List[str]:
        """
        Return every entity reachable downstream.
        """
        if not graph.has_node(entity_id):
            return []

        return list(nx.descendants(graph, entity_id))

    @staticmethod
    def find_upstream_entities(
        graph: nx.DiGraph,
        entity_id: str,
    ) -> List[str]:
        """
        Return every entity reachable upstream.
        """
        if not graph.has_node(entity_id):
            return []

        reverse_graph = graph.reverse(copy=False)

        return list(nx.descendants(reverse_graph, entity_id))

    @staticmethod
    def find_shortest_dependency_path(
        graph: nx.DiGraph,
        source_entity_id: str,
        target_entity_id: str,
    ) -> List[str]:
        """
        Return the shortest dependency path between two entities.

        Returns an empty list if no path exists.
        """

        try:
            return nx.shortest_path(
                graph,
                source=source_entity_id,
                target=target_entity_id,
            )

        except nx.NetworkXNoPath:
            return []

        except nx.NodeNotFound:
            return []