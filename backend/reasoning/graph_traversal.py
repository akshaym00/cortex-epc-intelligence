"""
Graph Traversal helper for the reasoning layer.

Provides higher-level traversal operations built on top of
GraphUtils. The reasoning engine should use this module
instead of calling NetworkX directly.
"""

from typing import List

import networkx as nx

from backend.graph.graph_utils import GraphUtils


class GraphTraversal:
    """
    Higher-level graph traversal operations for reasoning.
    """

    @staticmethod
    def get_all_paths(
        graph: nx.DiGraph,
        source_id: str,
        target_id: str,
    ) -> List[List[str]]:
        """
        Return all simple paths between two entities.

        Returns an empty list if no path exists or
        either node is missing.
        """

        if not GraphUtils.entity_exists(graph, source_id):
            return []

        if not GraphUtils.entity_exists(graph, target_id):
            return []

        try:
            return list(
                nx.all_simple_paths(
                    graph,
                    source=source_id,
                    target=target_id,
                )
            )

        except nx.NetworkXError:
            return []

    @staticmethod
    def get_connected_components(
        graph: nx.DiGraph,
    ) -> List[set[str]]:
        """
        Return the weakly connected components of the graph.

        Each component is a set of entity IDs that are
        reachable from one another (ignoring edge direction).
        """

        return [
            component
            for component in nx.weakly_connected_components(graph)
        ]

    @staticmethod
    def get_impact_subgraph(
        graph: nx.DiGraph,
        entity_id: str,
    ) -> nx.DiGraph:
        """
        Return the subgraph reachable downstream from the
        given entity (including the entity itself).
        """

        if not GraphUtils.entity_exists(graph, entity_id):
            return nx.DiGraph()

        downstream = GraphUtils.find_downstream_entities(
            graph,
            entity_id,
        )

        nodes = {entity_id} | set(downstream)

        return graph.subgraph(nodes).copy()

    @staticmethod
    def get_depth(
        graph: nx.DiGraph,
        entity_id: str,
    ) -> int:
        """
        Return the maximum depth of the downstream
        dependency tree from the given entity.

        Returns 0 if the entity has no downstream dependencies.
        """

        if not GraphUtils.entity_exists(graph, entity_id):
            return 0

        downstream = GraphUtils.find_downstream_entities(
            graph,
            entity_id,
        )

        if not downstream:
            return 0

        max_depth = 0

        for target_id in downstream:
            path = GraphUtils.find_shortest_dependency_path(
                graph,
                entity_id,
                target_id,
            )

            if path:
                max_depth = max(max_depth, len(path) - 1)

        return max_depth
